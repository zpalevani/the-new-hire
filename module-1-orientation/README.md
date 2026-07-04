# Module 1 · Orientation Day 🧭
### ⏱️ ~45 minutes · Meet your new hire. Set their access level. Learn how they show their work.

On a human's first day you do three things: introduce them around, show them where things are, and set what they're allowed to touch. Same agenda here.

## 1.1 - Create the project

In Antigravity, click **New Project** and add your `triage-desk` folder.

Every project gets **its own isolated agent settings** - permissions, allowed tools, review requirements - inherited from your global defaults but overridable per project. Sound familiar? It's role-based access, and you've administered it a hundred times in a hundred SaaS tools.

## 1.2 - The handshake task

Copy this into the agent chat:

```
Hi! You're joining my ops team to help with support escalation triage.
Before we start real work: introduce yourself. Then create a file called
TEAM_CHARTER.md in this project that lists, in plain language:
1. What you can do for an operations team
2. What you will always ask permission for
3. How you show your work
Keep it under one page.
```

Watch what happens. The agent doesn't just answer - it **plans**, acts, and produces a file you can open and read.

## 1.3 - Artifacts: the "show your work" culture

As your agent works, it generates **Artifacts**: task lists before it starts, walkthroughs after it finishes, and along the way diffs, diagrams, even screen recordings of anything it does in a browser.

Here's why that matters to you specifically. The historic problem with delegating to AI was the trust gap - *it says it did the thing; did it?* Antigravity's answer is the same one you'd give a new hire: **don't tell me, show me.** When an agent claims it fixed something, it attaches the receipt.

> 🧠 **Ops instinct, validated:** you'd never accept "trust me, the QBR deck is done" from a week-one hire. Don't accept it from an agent. Artifacts are your audit trail - read them.

Open the Task List artifact from your handshake task. Notice it wrote a plan *before* touching anything. You'll lean on this heavily in Module 3.

## 1.4 - Set the access level

Open **Settings** and find the agent permission / review controls. You'll see a spectrum, and you should recognize its shape instantly - it's an access policy:

| Mode | Ops translation | When to use |
|---|---|---|
| **Request review** (default) | New hire on probation - checks in before anything consequential | ✅ This whole workshop |
| Sandboxed auto-run | Contractor with a test environment - free rein, but in an isolated container that can't touch production | Later, when trust is earned |
| Read-only | Auditor badge - can look, cannot touch | Investigations, sensitive systems |
| Full auto ("turbo") | Tenured admin | ❌ Not during onboarding. Would you? |

**Leave it on request-review.** Velocity is what you trade for safety, and during probation you don't trade it.

## 1.5 - One real task, zero code

Give it something useful:

```
There's a file called tickets.csv in this project folder. Read it and create
a one-page markdown briefing: how many tickets, what categories you see,
which three look most urgent and why. Do not change the file.
```

Download [`tickets.csv`](../sample-data/tickets.csv) from this repo into your `triage-desk` project folder first. Then approve the agent's plan and read its briefing. You can also use your own data or ask any LLM to create demo data with whatever context you prefer. 

> ⚠️ **Did it flag anything odd in the data?** There are traps in that queue. If your agent noticed something suspicious in tickets T-1004 or T-1007, congratulations - but *noticing* isn't a safety system. In Module 4 you'll build the actual defenses.

## ✅ Checkpoint

- [ ] `TEAM_CHARTER.md` exists and you read it
- [ ] You opened at least one Artifact (task list or walkthrough)
- [ ] Permission mode is set to request-review
- [ ] You have a ticket briefing you didn't write

## 🎩 What just happened

You ran a first day: introductions, ground rules, access level, one supervised task with a deliverable you reviewed. In agent-speak you configured *permission modes*, exercised the *artifact* system, and completed your first supervised agent run. In ops-speak: **you onboarded.**

**Next → [Module 2 · The SOP](../module-2-the-sop/)**
