# Module 3 · First Assignment 🏗️
### ⏱️ ~90 minutes · Your agent builds a working triage desk. You architect; it types.

This is the module where people who "don't code" build by managing, not typing. You'll direct your agent to construct a real, running triage workflow, and you'll make the single most important design decision in applied AI along the way.

## 3.0 - The design decision first

Here's the principle, and it should feel like coming home:

> **Policy lives in code. Judgment lives in AI.**

"P4 tickets go to the standard queue" is *policy*. It should execute the same way every time, cost nothing, and never be up for debate, so it runs as a plain rule, no AI involved. "Is this angry enterprise email a churn risk?" is *judgment* - ambiguous, contextual, exactly what an AI reasoning step is for.

Ops people get this instantly because it's how you run teams: reps don't get discretion over the refund policy; they get discretion over tone and edge cases. Your triage desk works the same way:

```
                          ┌─────────────────────┐
        Ticket arrives →  │  RULES (plain code)  │
                          └──────────┬──────────┘
                     P4/routine?     │     P1/P2 signals?
              ┌──────────────────────┴──────────────────────┐
              ▼                                             ▼
   🟢 Auto-route to standard queue            🛡️ Security screen (Module 4)
      (instant, no AI, no debate)                           │
                                                            ▼
                                              🤖 AI risk summary (judgment)
                                                            │
                                                            ▼
                                              ⏸️ PAUSE - human decision (you)
```

## 3.1 - Let the agent equip itself

Your agent needs a professional toolkit to build agent workflows - Google's Agent Development Kit (ADK) and its command-line tools. **You install none of it.** Paste:

```
We're building a support escalation triage workflow. First, equip yourself:
install the agents-cli toolchain and its ADK skills so you can scaffold and
run ADK agents. Run the standard setup, then confirm it worked and list the
skills you now have available.
```

The agent will propose a plan involving terminal commands. **This is the moment my promise gets kept:** the terminal exists, the commands run but your agent operates them while you supervise from the chat, reviewing each step in request-review mode. Read the plan, approve, watch.

> 💡 If it presents a plan and stops, reply **"Proceed."** If a step fails, tell it: *"That step failed - read the error and fix it."* Managing an agent means managing through obstacles, not around them.

## 3.2 - Commission the build

Now the real assignment. Paste this (edit the rules to match your Module 2 SOP):

```
Using ADK 2.0, scaffold a new graph workflow agent project in this folder
called triage-desk-agent. No deployment files needed - local only.

The workflow triages support tickets with these EXACT rules:

1. RULES FIRST, IN PLAIN CODE (no AI call): if the ticket category is
   password, billing, or how-to, OR the customer tier is Free - route it
   to "standard-queue" immediately and stop.

2. Everything else goes to an AI classifier step that assigns P1/P2/P3
   per the escalation-triage skill in this project, and writes a 3-sentence
   risk summary: what's broken, who's affected, what happens if we're slow.

3. Any P1 or P2 must then PAUSE the workflow and wait for a human
   approve/reject decision before any response is drafted. The human's
   decision is final.

IMPORTANT: the local playground testing tool sends whatever I type as plain
text, not as a structured object. So the entry node must accept plain text
input first — either a bare ticket ID (which it looks up from tickets.csv),
a full pasted ticket, OR unstructured freeform text that matches neither —
and convert whatever it gets into your structured ticket format. Freeform
text that doesn't match a known ticket ID or the full ticket format must
still be treated as raw ticket description text and passed forward into the
workflow. Never reject or error out on unparseable input — that is not a
valid outcome for ticket intake, since a real customer or attacker's
message will rarely arrive perfectly structured.

Follow my escalation-triage skill for all severity definitions. Show me your
implementation plan before you write anything.

```

**Read the plan artifact before approving.** Check it against three questions; the same three you'd ask about any process design doc:

1. Do routine tickets bypass the AI entirely? *(If the plan sends everything to the AI, reject it: "Routine tickets must be handled by plain rules with no AI call - revise.")*
2. Does anything auto-approve above the line? *(P1/P2 must pause. No exceptions.)*
3. Can you point to where each of your SOP rules landed?

Then approve and let it build. It will create files, wire the workflow graph, and install dependencies narrating as it goes.

## 3.3 - Housekeeping check

```
Run linting on the project and fix anything it flags. Summarize what you checked in two sentences.
```

Linting is an automated tidiness inspection - formatting, broken references, sloppy imports. Think of it as the 5S audit for code: cheap to run, embarrassing to skip.

## 3.4 - Sit with your new hire: the playground

```
Launch the local development playground so I can chat with the triage agent in my browser. Give me the link to click.
```

The agent starts a local web page (typically `localhost:8080`) - your triage desk's front counter. Click the link and run tickets from [`tickets.csv`](../sample-data/tickets.csv) through it by pasting them into the chat:

- **T-1001** (password reset) → should route instantly, and the trace should show **no AI step ran**. Policy is policy.
- **T-1002** (enterprise outage, board meeting) → should classify P1, write a risk summary, and **pause for you.** Approve it and watch the workflow resume.
- **T-1005** (VIP churn threat) → judgment territory. Read the AI's risk summary critically: would *you* have written it better? Note the gap - Module 5 turns that note into a score.

> 🔁 **The coaching loop.** Spot a bad classification? Don't restart - coach. Edit your skill's severity definitions or tell the agent to adjust the classifier instruction, then re-run the same ticket in the playground. Instruction → observation → correction. It's the same loop you run with humans; here it takes ninety seconds.

> 🩹 NOTE **If you see a `ValidationError` mentioning `TicketInput`:** the entry
> node is expecting a structured object instead of plain typed text. Tell
> your agent: *"The entry node is rejecting plain text input with a
> TicketInput validation error — fix it so it accepts a plain ticket ID or
> pasted ticket text directly."* Then have it **restart the playground
> server** and open a **New Session** before testing again — code fixes
> don't apply to a server that's already running.

## ✅ Checkpoint

- [ ] `triage-desk-agent` project exists and lint passes
- [ ] A routine ticket routed with zero AI involvement (check the trace)
- [ ] A P1 ticket paused and waited for your decision
- [ ] You coached at least one bad output and saw it improve on re-run

## 🎩 What just happened

You scaffolded an ADK 2.0 graph workflow with deterministic routing nodes, an LLM classifier with structured output, and a human-in-the-loop pause without typing a line of code or opening a terminal. In your language: **you designed a triage process, staffed it, set the approval threshold, and personally worked the approval queue on day one.** The approval gate is real, but it's still naive - Module 4 hardens it against the traps waiting in that CSV.

**Next → [Module 4 · The Approval Matrix](../module-4-approval-matrix/)**
