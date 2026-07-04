# The New Hire
### Onboard an AI agent the way an ops pro onboards a person.

> **You will never touch a terminal. Your agent has one.**

This is a self-paced workshop for **operations people**, customer success, support ops, sales ops, biz ops. No coding. No command line. No computer science degree.

You're going to do the one thing you already do better than any engineer: **onboard a new team member.**

Except this new hire is an AI agent. And by the end of five modules, it will be running **support escalation triage** for you with an SOP it actually follows, an approval matrix it can't bypass, and a QA scorecard that proves it. Consider this your Proof of Concept (POC) to start the conversations with your team to proceed with an MVP and evntually production version. 

---

## 💡 The idea

Everyone tells ops people to "learn prompting." That's backwards.

**Prompting is not the skill. Guardrails, context, and validation are the skill.** And ops people have been doing guardrails, context, and validation their entire careers, they just call them *approval matrices, SOPs, and QA reviews.*

This workshop doesn't teach you a new discipline. It shows you that AI agents run on **your** discipline.

| You already know how to... | In agent-land, that's called... |
|---|---|
| Write an SOP | A **Skill** |
| Set an approval matrix | **Human-in-the-loop** |
| Run QA scorecards | **Evals** |
| Manage access & permissions | **Guardrails / permission modes** |
| Demand an audit trail | **Artifacts** |
| Keep a source-of-truth binder | **Grounding (MCP)** |
B
*(Full translation table in [GLOSSARY.md](GLOSSARY.md) ookmark it, it's your Rosetta Stone.)*

---

## 🗺️ The onboarding plan

Treat your agent like a promising junior hire. Same playbook you'd use for a human:

| Module | Onboarding stage | You will... | Time |
|---|---|---|---|
| [**0 · Setup**](00-setup/) | Paperwork | Install Antigravity, sign in, zero terminal | 20 min |
| [**1 · Orientation**](module-1-orientation/) | Day one tour | Meet your agent, learn how it shows its work, set its access level | 45 min |
| [**2 · The SOP**](module-2-the-sop/) | Handbook day | Turn your real escalation SOP into a Skill the agent loads on demand | 45 min |
| [**3 · First Assignment**](module-3-first-assignment/) | Real work begins | Direct the agent to build a triage desk — rules in code, judgment in AI | 90 min |
| [**4 · The Approval Matrix**](module-4-approval-matrix/) | Setting limits | Add PII redaction, an injection tripwire, and a human approval gate | 60 min |
| [**5 · The 30-Day Review**](module-5-the-30-day-review/) | Performance review | Grade your agent with a QA scorecard. Keep it, coach it, or fire it | 60 min |
| [🎓 **Graduation**](graduation/) | Stretch goal | Publish a live triage dashboard from your browser,  still no terminal | 30 min |

**Total: ~5 hours, self-paced.** Do a module per lunch break. Everything runs on a free personal Google account; no billing, no credit card, until the optional graduation stretch.

---

## 🎫 The scenario

Your support queue is drowning. Routine tickets bury the real emergencies. So you're onboarding an agent to run **escalation triage**:

- 🟢 **Routine tickets** (password resets, billing questions) → auto-routed instantly by *rules, not AI*. Policy is policy, it shouldn't cost an AI call, and it shouldn't be up for negotiation.
- 🔴 **High-stakes tickets** (enterprise outages, churn threats) → screened for sensitive data, risk-summarized by AI, then **paused for a human decision.** Yours.

The [sample ticket queue](sample-data/tickets.csv) contains a few traps — a customer who pastes their SSN, a "ticket" that tries to talk your agent into misbehaving, and a VIP threatening to walk. Your onboarding plan handles all three. That's the point.

---

## 📏 Ground rules

1. **You are the manager, not the typist.** Every module gives you plain-English prompts to copy into Antigravity. The agent writes the code, runs the commands, opens the web pages. You review, approve, and decide.
2. **Never approve what you haven't read.** Your agent produces plans and artifacts before acting. Read them. Approving blind is how bad hires slip through probation, same rule here.
3. **If the agent stalls, prompt it forward.** Agents sometimes present a plan and wait. Reply "Proceed." You'd nudge a hesitant new hire too.
4. **Results vary — that's normal.** Agents are not photocopiers. Your file names and outputs may differ slightly from the screenshots. Judge outcomes, not keystrokes. (You'll formalize this instinct in Module 5.)

---

## 🙏 Grounded in

This workshop adapts and reframes Google's official Antigravity conent and codelabs for an operations audience. Unlike those labs that are written for developers, this workshop is the same architecture, translated into the language ops people already speak.

---

## ▶️ Start here

**[Module 0 · Setup →](00-setup/)**

*Hats off optional, but expected.* 🎩 :-) 

---

Created by **[Zara Palevani](https://www.linkedin.com/in/zara-palevani/)** — an operations leader who believes the real discipline in AI was never prompting. It's guardrails, context, and validation, and ops people have been the professionals of that discipline all along. 

MIT licensed — adapt it for your team.
