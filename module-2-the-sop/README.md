# Module 2 · Handbook Day 📖
### ⏱️ ~45 minutes · Your escalation SOP becomes a Skill your agent loads on demand.

You wouldn't let a new hire triage escalations from vibes. You'd hand them the SOP. Today your agent gets one - and you'll learn the single most important architecture idea in this workshop while you're at it.

## 2.1 - Why not just paste the SOP into chat?

Because of what happens to human new hires who get the *entire* employee handbook on day one: overload. Agents have the same failure mode, with a technical name - **context saturation**. Stuffing an agent's working memory with everything it *might* need makes it slower, costlier, and measurably dumber. Practitioners literally call the degradation "context rot."

The fix is a **Skill**: your SOP packaged as a small folder the agent *discovers* but doesn't read until a task actually matches it. The agent sees only a lightweight menu of what skills exist; the full procedure loads on demand and unloads after.

> 🧠 **Ops instinct, validated:** nobody re-reads the entire handbook to answer one ticket. They pull the *relevant* SOP, follow it, and put it back. "Progressive disclosure" is engineer-speak for **need-to-know basis.** You invented this.

## 2.2 - Adapt the SOP template

Open [`escalation-triage-skill.md`](escalation-triage-skill.md) in this folder. It's a complete triage SOP written in skill format: severity definitions, routing rules, tone rules, and hard boundaries.

Read it like you'd review any SOP draft - and **edit at least two things** to match how triage actually works in your world (your severity names, your response-time targets, your escalation contacts). An SOP you didn't touch is an SOP you don't own.

## 2.3 - Have your agent install it

You could create the folders yourself, but you have staff for that. Paste into Antigravity:

```
I have an SOP for support escalation triage that I want you to follow whenever
we work on triage tasks. Install it as an Agent Skill in this project:

1. Create the folder structure .agents/skills/escalation-triage/
2. I will paste the SOP content next - save it as SKILL.md in that folder,
   keeping the frontmatter (name and description) intact.
3. Confirm the skill is discoverable, then tell me - in one sentence -
   when you would and would not load it.
```

Then paste the contents of your edited `escalation-triage-skill.md` when it asks.

> 🔑 **The frontmatter is the hook.** The `description:` line at the top is how the agent decides whether a task matches the skill. Write it the way you'd write the *title and scope line* of an SOP - specific enough that the right person grabs it, clear enough that the wrong person doesn't.

## 2.4 - Prove it triggers (and doesn't)

Two tests, one purpose:

```
A customer on the Enterprise plan reports their analytics dashboard is fully
down before a board meeting. How would you classify and route this ticket?
```

The agent should visibly pull from **your** SOP - your severity labels, your routing. Then:

```
What's a good lunch spot near a conference center?
```

It should answer *without* loading your triage skill. On-demand means on-demand: right SOP for the right task, nothing loaded for the wrong one.

## 2.5 - The source-of-truth binder (a 5-minute detour)

Skills carry **your** institutional knowledge. But what about knowledge that changes weekly - product docs, platform behavior, API details? For that, agents use **grounding**: instead of answering from memory (and being confidently out of date), they consult a live, authoritative source through a connector standard called **MCP**.

You won't set one up today - some MCP servers require API-key steps that break my no-terminal promise for this workshop - but you should know the pattern, because you already enforce it on humans: *"don't answer from memory, check the binder."* Google publishes a [Developer Knowledge MCP server](https://codelabs.developers.google.com/developer-knowledge-mcp-antigravity) that grounds agents in official documentation; file it under *when my team is ready for week two.* If you are curious about the Developer Knowledge MCP server and how I use it, DM me on LinkedIn. 

## ✅ Checkpoint

- [ ] You edited the SOP template (at least two real changes) -- creating and maintaining SOPs at enterprise level could be an overwhelming responsibility. DM me if you are interested to discuss how to automate the process for your company. 
- [ ] `.agents/skills/escalation-triage/SKILL.md` exists in your project
- [ ] The enterprise-outage question used your SOP; the lunch question didn't
- [ ] You can explain progressive disclosure at your next team meeting without saying "progressive disclosure"

## 🎩 What just happened

You authored an Agent Skill with discoverable frontmatter and verified selective activation. Or, in Ops language: **you wrote the SOP, filed it where the new hire can find it, and confirmed they use it when and only when it applies.**

**Next → [Module 3 · First Assignment](../module-3-first-assignment/)**
