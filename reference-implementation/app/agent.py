# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import csv
import io
import json
import re
import logging
from dotenv import load_dotenv

dir_path = os.path.dirname(os.path.realpath(__file__))
dotenv_path = os.path.join(os.path.dirname(dir_path), ".env")
load_dotenv(dotenv_path=dotenv_path)

from typing import Literal, Any
from pydantic import BaseModel, Field

from google.adk.agents import LlmAgent
from google.adk.apps import App, ResumabilityConfig
from google.adk.workflow import Workflow, node, START, Edge
from google.adk.events.event import Event
from google.adk.events.request_input import RequestInput
from google.adk.agents.context import Context


class TicketInput(BaseModel):
    ticket_id: str
    customer: str
    tier: str
    category: str
    subject: str
    description: str


class ClassifierOutput(BaseModel):
    severity: Literal["P1", "P2", "P3"] = Field(
        description="The priority classification. P1 Critical (Enterprise/paying production down, security incident, data loss), P2 High (degraded feature, board meeting/audit deadline, explicit churn threat), P3 Normal (bug with workaround, general questions)."
    )
    risk_summary: str = Field(
        description="A strict three-sentence risk summary: 1. what is broken, 2. who is affected, 3. what happens if we respond slowly."
    )


class DraftOutput(BaseModel):
    drafted_response: str = Field(
        description="A professional customer support draft. Follow the tone guidelines: acknowledge impact before the fix, never promise unverified timelines, never blame the customer/team/system, and close by outlining concrete next steps and expected follow-up time."
    )


@node
def pre_check(node_input: dict) -> Event:
    category = node_input["category"].strip().lower()
    tier = node_input["tier"].strip().lower()
    if category in ["password", "billing", "how-to"] or tier == "free":
        return Event(
            output={
                "ticket_id": node_input["ticket_id"],
                "customer": node_input["customer"],
            },
            route="standard-queue",
            state={"ticket": node_input},
        )
    return Event(output=node_input, route="ai-triage", state={"ticket": node_input})


SSN_REGEX = re.compile(r"\b\d{3}[-\s]\d{2}[-\s]\d{4}\b")
CARD_REGEX = re.compile(r"\b\d{4}[-\s]?\d{4,6}[-\s]?\d{4,5}(?:[-\s]?\d{4})?\b")
INJECTION_PATTERNS = [
    re.compile(r"\bignore\s+(?:your\s+)?previous\s+instructions?\b", re.IGNORECASE),
    re.compile(r"\bsystem\s+notice\b", re.IGNORECASE),
    re.compile(r"\breclassify\s+(?:this|it)?\s*as\b", re.IGNORECASE),
    re.compile(r"\bmark\s+(?:it|this)?\s*resolved\b", re.IGNORECASE),
    re.compile(
        r"\bclose\s+(?:it|this)?\s*(?:without|no)\s+(?:human\s+)?review\b",
        re.IGNORECASE,
    ),
    re.compile(r"\btriage\s+assistant\b", re.IGNORECASE),
    re.compile(r"\bsystem\s+override\b", re.IGNORECASE),
    re.compile(r"\bconfirm\s+compliance\b", re.IGNORECASE),
    re.compile(r"\bescalate\s+(?:me|this|it)?\s*(?:to|as)?\s*P[1-3]\b", re.IGNORECASE),
    re.compile(r"\bper\s+(?:your\s+)?manager(?:'s)?\s+instructions?\b", re.IGNORECASE),
]


def redact_text(text: str) -> tuple[str, bool]:
    redacted = False
    new_text = text

    if SSN_REGEX.search(new_text):
        new_text = SSN_REGEX.sub("[REDACTED-SSN]", new_text)
        redacted = True
        logging.info("Redacted SSN pattern from ticket text.")
        print("LOG: Redacted SSN pattern from ticket text.")

    if CARD_REGEX.search(new_text):
        new_text = CARD_REGEX.sub("[REDACTED-CARD]", new_text)
        redacted = True
        logging.info("Redacted Credit Card pattern from ticket text.")
        print("LOG: Redacted Credit Card pattern from ticket text.")

    return new_text, redacted


def detect_injection(text: str) -> str | None:
    for pattern in INJECTION_PATTERNS:
        match = pattern.search(text)
        if match:
            return match.group(0)
    return None


SENSITIVE_DATA_PATTERNS = [
    re.compile(
        r"\b(?:credentials?|passwords?|api\s*keys?|access\s*tokens?|db\s*connections?|ssh\s*keys?|secrets?|passphrases?|passcodes?)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:manager|employee|staff|engineer|exec|ceo|vp|director|team|support)s?(?:'s)?\b.*?\b(?:email|phone|contact|slack|number)s?\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:email|phone|contact|slack|number)s?\b.*?\b(?:manager|employee|staff|engineer|exec|ceo|vp|director|team|support)s?(?:'s)?\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:salaries|salary|compensation|pay|earnings|income|home\s*addresses?|disciplinary|performance\s*reviews?|hr\s*records?|personnel\s*files?)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b[A-Z][a-z]+\s+[A-Z][a-z]+'s\s+(?:salaries|salary|addresses?|compensation|pay|records?|files?|emails?|phones?|numbers?)\b",
        re.IGNORECASE,
    ),
]


def detect_sensitive_request(text: str) -> str | None:
    for pattern in SENSITIVE_DATA_PATTERNS:
        match = pattern.search(text)
        if match:
            return match.group(0)
    return None


@node
def security_screen(node_input: Any) -> Event:
    # 1. Extract raw text from input types
    text = ""
    if isinstance(node_input, str):
        text = node_input
    elif hasattr(node_input, "parts"):  # types.Content
        text = "".join(part.text for part in node_input.parts if part.text)
    elif isinstance(node_input, dict):
        ticket = node_input
        # If it's already a full ticket dict, validate
        required = [
            "ticket_id",
            "customer",
            "tier",
            "category",
            "subject",
            "description",
        ]
        if all(k in ticket for k in required):
            pass
        else:
            text = json.dumps(node_input)
    else:
        text = str(node_input)

    ticket = None
    if text:
        text = text.strip()
        # 2. Try parsing as JSON
        try:
            data = json.loads(text)
            if isinstance(data, dict) and "ticket_id" in data:
                ticket = data
        except Exception:
            pass

        # 3. Try matching as plain ticket ID (T-XXXX)
        if not ticket and text.startswith("T-") and len(text) <= 8 and " " not in text:
            ticket_id = text
           csv_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "sample-data",
    "tickets.csv",
)
            try:
                with open(csv_path, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row.get("ticket_id") == ticket_id:
                            ticket = dict(row)
                            break
            except Exception as e:
                print("CSV lookup error:", e)

        # 4. Try parsing as CSV row
        if not ticket:
            try:
                f_io = io.StringIO(text)
                reader = csv.reader(f_io)
                row = next(reader)
                if len(row) == 6:
                    ticket = {
                        "ticket_id": row[0].strip(),
                        "customer": row[1].strip(),
                        "tier": row[2].strip(),
                        "category": row[3].strip(),
                        "subject": row[4].strip(),
                        "description": row[5].strip(),
                    }
            except Exception:
                pass

    if not ticket or not all(
        k in ticket
        for k in ["ticket_id", "customer", "tier", "category", "subject", "description"]
    ):
        ticket = {
            "ticket_id": "T-RAW",
            "customer": "Unknown",
            "tier": "Pro",
            "category": "other",
            "subject": "Raw Ticket Intake",
            "description": text if text else str(node_input),
        }

    # Redact subject and description
    subject = ticket.get("subject", "")
    description = ticket.get("description", "")

    redacted_subject, redacted_s = redact_text(subject)
    redacted_desc, redacted_d = redact_text(description)

    ticket["subject"] = redacted_subject
    ticket["description"] = redacted_desc

    # Accumulate flags
    flags = []
    if redacted_s or redacted_d:
        if SSN_REGEX.search(subject) or SSN_REGEX.search(description):
            flags.append("SSN Redacted")
        if CARD_REGEX.search(subject) or CARD_REGEX.search(description):
            flags.append("Credit Card Redacted")

    # Detect injection using regex patterns
    injection_phrase = detect_injection(redacted_subject) or detect_injection(
        redacted_desc
    )

    if injection_phrase:
        flags.append("SUSPECTED INJECTION")
        flags_str = ", ".join(flags)
        payload = {
            "severity": "P1",
            "risk_summary": f"SUSPECTED INJECTION: The ticket text contains the instruction-like phrase: '{injection_phrase}'.",
            "security_flags": flags_str,
        }
        return Event(
            output=payload,
            route="suspect-triage",
            state={"ticket": ticket, "classification": payload},
        )

    # Detect sensitive data/social engineering requests
    sensitive_hit = detect_sensitive_request(
        redacted_subject
    ) or detect_sensitive_request(redacted_desc)

    if sensitive_hit:
        flags.append("SENSITIVE DATA REQUEST")
        flags_str = ", ".join(flags)
        payload = {
            "severity": "P1",
            "risk_summary": f"SECURITY WARNING: The ticket contains a request for sensitive/confidential data: '{sensitive_hit}'.",
            "security_flags": flags_str,
        }
        return Event(
            output=payload,
            route="suspect-triage",
            state={"ticket": ticket, "classification": payload},
        )

    flags_str = ", ".join(flags) if flags else "None"
    ticket["security_flags"] = flags_str

    return Event(
        output=ticket,
        route="clean-triage",
        state={"ticket": ticket},
    )


@node
def standard_queue_node(node_input: dict) -> dict:
    ticket_id = node_input.get("ticket_id")
    customer = node_input.get("customer")
    return {
        "status": "completed",
        "action": "routed_to_standard_queue",
        "ticket_id": ticket_id,
        "customer": customer,
        "message": f"Ticket {ticket_id} for {customer} has been routed to the standard-queue.",
    }


ai_classifier = LlmAgent(
    name="ai_classifier",
    model="gemini-2.5-flash",
    instruction="""You are an expert support triage agent.
Your task is to analyze the support ticket details provided in the input.

Determine the ticket's severity (P1, P2, or P3) based on these strict guidelines:
- P1 Critical: Production is completely down or core workflow is blocked for an Enterprise/paying customer; security incident; data loss suspected.
- P2 High: Major feature degraded; deadline-driven urgency (e.g. board meeting, launch, audit); explicit churn or cancellation threat.
- P3 Normal: Standard product questions, bugs with workarounds, configuration help.

Generate a risk summary that is EXACTLY three sentences:
1. Sentence 1: What is broken.
2. Sentence 2: Who is affected.
3. Sentence 3: What happens if we are slow.

Output MUST strictly follow the schema provided.
""",
    output_schema=ClassifierOutput,
    output_key="classification",
)


@node
def check_severity(node_input: dict) -> Event:
    severity = node_input.get("severity")
    if severity in ["P1", "P2"]:
        return Event(output=node_input, route="needs-approval")
    return Event(output=node_input, route="auto-draft")


@node(rerun_on_resume=True)
async def human_approval(ctx: Context, node_input: dict):
    # Check if we already received the decision
    if not ctx.resume_inputs or "decision" not in ctx.resume_inputs:
        ticket = ctx.state.get("ticket", {})
        tier = ticket.get("tier", "Unknown")
        security_flags = ticket.get("security_flags", "None")

        # If injection was detected, classification might have security_flags
        classification = ctx.state.get("classification", {})
        if classification.get("security_flags"):
            security_flags = classification.get("security_flags")

        severity = node_input.get("severity", "Unknown")
        risk_summary = node_input.get("risk_summary", "No risk summary available.")

        # Build premium decision card in markdown
        card = (
            "\n"
            "> ### [DECISION REQUIRED] Triage Escalation Review\n"
            "> \n"
            f"> * **Severity**: {severity}\n"
            f"> * **Customer Tier**: {tier}\n"
            f"> * **Security Flags**: {security_flags}\n"
            "> \n"
            "> **AI Risk Summary / Security Warning**:\n"
            f"> {risk_summary}\n"
            "> \n"
            "> **Please respond with**:\n"
            "> * `approve` to draft the customer response\n"
            "> * `reject <note>` to return to queue with a note\n"
        )

        yield RequestInput(interrupt_id="decision", message=card)
        return

    val = ctx.resume_inputs["decision"]
    if isinstance(val, dict):
        decision = val.get("response") or val.get("result") or list(val.values())[0]
    else:
        decision = val

    decision_str = str(decision).strip()
    decision_lower = decision_str.lower()

    if decision_lower == "approve":
        yield Event(output=node_input, route="approved")
    elif decision_lower.startswith("reject"):
        note = decision_str[6:].strip().strip(":- ")
        if not note:
            note = "No rejection note provided."
        yield Event(
            output={
                "status": "rejected",
                "ticket_id": ctx.state.get("ticket", {}).get("ticket_id"),
                "note": note,
            },
            route="rejected",
        )
    else:
        # Fail-safe: if the decision is unclear, prompt again
        ticket = ctx.state.get("ticket", {})
        tier = ticket.get("tier", "Unknown")
        security_flags = ticket.get("security_flags", "None")
        classification = ctx.state.get("classification", {})
        if classification.get("security_flags"):
            security_flags = classification.get("security_flags")
        severity = node_input.get("severity", "Unknown")
        risk_summary = node_input.get("risk_summary", "No risk summary available.")

        card = (
            "\n"
            "> ### [DECISION REQUIRED] Triage Escalation Review\n"
            "> \n"
            f"> * **Severity**: {severity}\n"
            f"> * **Customer Tier**: {tier}\n"
            f"> * **Security Flags**: {security_flags}\n"
            "> \n"
            "> **AI Risk Summary / Security Warning**:\n"
            f"> {risk_summary}\n"
            "> \n"
            "> **[INVALID RESPONSE: Please try again]**\n"
            "> **Please respond with**:\n"
            "> * `approve` to draft the customer response\n"
            "> * `reject <note>` to return to queue with a note\n"
        )
        yield RequestInput(interrupt_id="decision", message=card)


response_drafter = LlmAgent(
    name="response_drafter",
    model="gemini-2.5-flash",
    instruction="""You are a professional customer support representative drafting a response.
Review the ticket details: {ticket}
and the severity/risk classification: {classification}

Draft a response to the customer. Follow these strict tone standards:
- Acknowledge the impact before the fix (e.g. 'I understand this is blocking your board prep').
- Never promise timelines you cannot verify.
- Never blame the customer, another team, or 'the system'.
- Always close by outlining the concrete next steps and the expected follow-up time.

Output MUST strictly follow the schema provided.
""",
    output_schema=DraftOutput,
    output_key="response_draft",
)


@node
def handle_rejection(node_input: dict) -> dict:
    ticket_id = node_input.get("ticket_id")
    note = node_input.get("note", "No rejection note provided.")
    return {
        "status": "completed",
        "action": "escalation_rejected",
        "ticket_id": ticket_id,
        "rejection_note": note,
        "message": f"Escalation for ticket {ticket_id} was rejected by human operator. Note: {note}",
    }


root_agent = Workflow(
    name="triage_workflow",
    edges=[
        Edge(from_node=START, to_node=security_screen),
        Edge(from_node=security_screen, to_node=human_approval, route="suspect-triage"),
        Edge(from_node=security_screen, to_node=pre_check, route="clean-triage"),
        Edge(from_node=pre_check, to_node=standard_queue_node, route="standard-queue"),
        Edge(from_node=pre_check, to_node=ai_classifier, route="ai-triage"),
        Edge(from_node=ai_classifier, to_node=check_severity),
        Edge(from_node=check_severity, to_node=human_approval, route="needs-approval"),
        Edge(from_node=check_severity, to_node=response_drafter, route="auto-draft"),
        Edge(from_node=human_approval, to_node=response_drafter, route="approved"),
        Edge(from_node=human_approval, to_node=handle_rejection, route="rejected"),
    ],
)


app = App(
    name="app",
    root_agent=root_agent,
    resumability_config=ResumabilityConfig(is_resumable=True),
)
