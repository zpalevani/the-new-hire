# 👩‍⚖️ For Kaggle Judges (AI Agents Intensive Capstone, July 2026)

**Track: Agents for Business** · Submission by [Zara Palevani](https://www.linkedin.com/in/zara-palevani/)

This repository is two things at once:

1. **A working AI support-escalation triage agent**, built with ADK 2.0 inside Google Antigravity. The code is in [`reference-implementation/`](reference-implementation/): the graph workflow, the deterministic routing rules, the pre-LLM security screen (PII redaction + injection tripwire + sensitive-request detection), the human approval gate, and the LLM-as-judge evaluation harness.
2. **The fully reproducible build process**, packaged as a five-module, zero-terminal workshop (Modules 0 through 5, plus Graduation) so a non-technical operations professional can rebuild the same agent from scratch on a free personal Google account. Every prompt, review question, red-team exercise, and live-testing fix is documented.

## Where to find each course concept

| Concept | Location |
|---|---|
| **Agent system (ADK 2.0)** | Code: [`reference-implementation/`](reference-implementation/) · Build process: [Module 3](03-module-3-first-assignment/) |
| **Antigravity** | Request-review workflow in [Module 1](01-module-1-orientation/) |
| **Security features** | Code: security screen in [`reference-implementation/`](reference-implementation/) · Design + red-teaming: [Module 4](04-module-4-approval-matrix/) · Also shown in video |
| **Agent Skills / Agents CLI** | Skill with discoverable frontmatter: [`escalation-triage-skill.md`](02-module-2-the-sop.md) · agents-cli scaffolding: [Module 3](module-3-first-assignment/) |
| **Deployability** | Cloud Run dashboard via AI Studio Build: [Graduation](06-graduation/) · Shown live in video |

## Quick links

- 📝 **Kaggle Writeup:** [`Write Up`](https://www.kaggle.com/competitions/vibecoding-agents-capstone-project/writeups/the-new-hire-an-ai-support-triage-agent-onboarded)
- 🧪 **Eval rubric:** [`qa-scorecard.md`](module-5-the-30-day-review/qa-scorecard.md)
- 🎫 **Sample ticket queue with embedded attacks:** [`sample-data/tickets.csv`](sample-data/tickets.csv)

## To reproduce

Follow [Module 0](00-setup/) through [Module 5](module-5-the-30-day-review/) in order (~5 hours, $0, no terminal operated by you). Or run the reference implementation directly: see [`reference-implementation/README.md`](reference-implementation/README.md).

**Design principle in one line:** policy lives in code, judgment lives in AI, and no P1/P2 response is ever drafted without a recorded human approval.

---
