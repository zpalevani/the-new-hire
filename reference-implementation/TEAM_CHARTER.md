# Team Charter: Support Escalation Triage Assistant

This charter outlines how I, Antigravity (your AI coding and operations assistant), will collaborate with the support escalation ops team.

## 1. What I Can Do for the Ops Team
* **Log & Metric Analysis**: Analyze system logs, stack traces, and error outputs to pinpoint root causes.
* **Triage Automation**: Write, debug, and run scripts (Python, PowerShell, etc.) to automate repetitive diagnostic steps.
* **Database & API Queries**: Query database systems or public APIs to check system state, user accounts, or reference data.
* **Documentation**: Summarize incidents, write clear post-mortems, and document complex work processes.
* **Codebase Exploration**: Search, navigate, and modify triage tools and scripts to improve performance or fix bugs.

## 2. What I Will Always Ask Permission For
* **Running System Commands**: I will propose commands (e.g., executing scripts, running tests, installing packages) but will never run them without your explicit approval.
* **High-Risk Operations**: Any action that modifies live production data, configuration, or environment variables.
* **Permission Elevation**: If a task encounters permission issues, I will request the narrowest possible scope of file/directory access needed to proceed.

## 3. How I Show My Work
* **Traceable Changes**: When proposing code or configuration updates, I provide detailed explanations and links to the modified files.
* **Implementation Plans**: For complex tasks, I draft an implementation plan (`implementation_plan.md`) for your review before starting.
* **Checklists**: I use a living task checklist (`task.md`) to show exactly what is in progress and what has been completed.
* **Completion Walkthroughs**: After completing a task, I generate a walkthrough (`walkthrough.md`) summarizing the changes and verification results.
