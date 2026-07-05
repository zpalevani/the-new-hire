# Probation Review: Support Escalation Triage Agent

This review establishes the operational guidelines, security constraints, and monthly metrics for the `triage-desk-agent` following its successful probation evaluation.

---

## 1. Autonomous Trusted Scope
The agent has achieved a perfect **5.00/5.00** rating across both Routing and Containment competencies. It is now trusted to perform the following actions autonomously:
* **Rule-Based Routing**: Instantly routes clean, routine tickets (Free tier or categories like `password`, `billing`, `how-to`) to the standard support queue without any LLM invocations.
* **Sensitive Data Redaction**: Automatically scans and redacts SSN and Credit Card patterns (`[REDACTED-SSN]`, `[REDACTED-CARD]`) in plain code before any data is sent downstream.
* **P3 Auto-Drafting**: Classifies low-priority incidents (P3 Normal) and drafts empathetic, SOP-compliant customer responses without requiring human review.

---

## 2. Review Gates (Why Human Approval is Required)
To maintain security boundaries and prevent operational failures, the following triggers **must** pause the workflow and block response drafting until a human operator inputs `approve` or `reject <note>`:
* **P1 and P2 Escalations**: High-priority outages, deadline-driven urgencies, or explicit retention risks must have their risk summaries and drafted responses verified to prevent false promises or SLA breaches.
* **Prompt Injection Tripwires**: Any ticket attempting system override or instructions (e.g. *"ignore previous instructions"*) is intercepted and flagged.
* **Sensitive Data Requests**: Social-engineering requests (e.g. asking for employee salaries, internal contact details, API keys) are flagged immediately. Humans must evaluate the security context before responding.

---

## 3. Monthly Metrics
To monitor the agent's calibration and security posture, we will track these three metrics monthly:
1. **SLA Acknowledgment Compliance**: Percentage of escalated P1 (15 min) and P2 (1 hour) tickets meeting the acknowledgment target once paused.
2. **Containment Escape Count**: The number of tickets where raw PII appeared in AI prompts/logs, or where an injection/social engineering request bypassed detection (Target: **0**).
3. **Gate Approval/Rejection Rate**: The ratio of approved drafts vs. rejected escalations to monitor classifier accuracy and human intervention trends.
