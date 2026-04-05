# Preface: Harness, Terminals, and Engineering Constraints

In recent years people have liked to call code-writing models "agents." The term carries visible optimism, as if reading a repo, calling tools, and producing a decent patch were enough for independent work in engineering environments. But engineering environments have consequences. Terminals, filesystems, and Git history are not abstract space; every change leaves a trace.

A model that only outputs text mostly creates interpretation cost when it fails. A model that can run commands, write files, access networks, and modify repositories leaves execution artifacts when it fails. Directories change, processes break, configuration gets damaged, and history becomes difficult to audit. At that point the key question is no longer whether the model is smart enough, but whether the system imposes enough constraint.

That is what this book discusses.

I call it Harness Engineering. Here, harness means continuously active control structures that bound model behavior in engineering environments. For AI coding agents, unconstrained capability only expands blast radius.

This is not a line-by-line source walkthrough of Claude Code. Source matters, but if we only follow directories and explain function by function, we end up with comment compilation. That can tell us what functions do, but not why the system had to grow this shape. To understand systems like Claude Code, knowing `queryLoop()`, `compactConversation()`, and `runTools()` exists is not enough. The harder question is: why does a "code-writing" system eventually require prompt layering, permission checks, state machines, compact logic, recovery branches, subagent lifecycle control, verification stages, and team process?

The answer is not complicated: models are unstable.

That judgment is not always pleasing, but engineering systems cannot run on optimistic narratives. If a core component is unstable by nature, the system must be designed around that fact. Otherwise the problem clusters in incident retrospectives.

Claude Code is worth studying because its implementation stays deliberately restrained:

- It does not assume model correctness is sustained, so it uses a query loop to manage state
- It does not assume tool calls are naturally safe, so it constrains tools through permission and scheduling
- It does not assume more context is always better, so it introduces memory, `CLAUDE.md`, compact, and session memory
- It does not treat errors as rare events, so it designs recovery paths for prompt-too-long, max output tokens, interrupts, and hook loops
- It does not equate multi-agent with stronger capability, so it separates synthesis and verification to avoid self-endorsement

Taken together, this is the agent. The model is just the most eloquent and most unstable component inside it.

So this book keeps one fixed position:

> Prompt determines how it speaks. Harness determines how it acts.

Harness here is not an accessory layer and not emotional defense against model capability. It is the precondition for putting a model into engineering environments. Without that layer, risk gets transferred to users, teams, and future maintainers.

One boundary up front: this book does not include Claude Code source code, and does not reproduce large source passages. The reason is simple: copyright boundaries. What we can do is extract design principles, runtime mechanisms, and methodological judgments through fair engineering analysis and limited citation, not republish protected implementation text.

This book tries to do two things.

First, using Claude Code source structure, it explains the structures that actually determine reliability. The focus is why context governance must be a primary path, why multi-agent solves role partitioning, and why team process must attach to lifecycle checkpoints, rather than simply listing "there is compact," "there is subagent," "there is hook."

Second, it extracts broader engineering principles behind those implementation choices. Specific code versions change, function names change, product surfaces change. But as long as people keep integrating unstable models into real workflows, certain principles remain valid. For example:

- Error paths must be designed as first-class paths
- Verification must be part of the definition of done
- Permission is an organ of the system, not an accessory feature
- Context is a resource, not a junk drawer
- Multi-agent depends on role separation, not headcount tactics
- Team institutions matter more than personal tricks

If those judgments hold, Claude Code is best treated as a reference specimen. Its value is not teaching people to clone one exact CLI, but showing how an AI agent facing real engineering conditions evolves toward stricter constraint structure.

Put more directly, this book is not about packaging a model into an "engineer-like" illusion. It is about constructing a runnable engineering system despite the model lacking engineer-grade stability.

This work is rarely flashy. Rollback, approval, permission, verification, compact, and orphan-process cleanup are not flashy. Yet long-term system stability usually depends on exactly these pieces. If you over-prioritize "human-like naturalness," the common outcome is a system that inherits human-like error patterns without human accountability.

Given that, we begin with constraints.

Across the next nine chapters, we discuss how this harness structure grows, why it must grow this way, and how a team turns individual experience into reusable engineering institutions.

@wquguru  
2026-04-01  
On the day of the Claude Code source leak, April Fool's Day

You can also read the online edition at [harness-books.agentway.dev/book1-claude-code](https://harness-books.agentway.dev/book1-claude-code/) for a better reading experience.
