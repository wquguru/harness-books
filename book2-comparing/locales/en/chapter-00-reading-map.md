# Reading Map: How to Read Book One and This Comparative Book Together

If you treat both directories as "books about AI coding agents," the easiest misread is to assume they are duplicate documents. They are not. Their division of labor is clear.

Book One is single-system dissection. It uses Claude Code as a specimen to explain why a controllable agent must grow organs such as a control plane, query loop, tool permissions, context governance, recovery paths, multi-agent verification, and team institutions. Its central question is: what internal skeleton does a harness need in order to work continuously in real engineering environments?

This comparison book is comparative dissection. It no longer asks only why Claude Code is designed this way, but puts Claude Code and Codex side by side to compare how each admits model unreliability and places order at different layers. Its central question is: when both systems are building a harness, which choices are consensus and which are just different engineering routes?

There is now one more use for that comparison: once you carry these judgments into third-party harnesses, it becomes easier to spot a common failure mode. Many systems also advertise memory, skills, compaction, and multi-agent support, yet their context-governance axis still amounts to pushing more text into prompt first and truncating or rescuing later. That route looks like "more information," but in practice it often burns more tokens while weakening working semantics.

In other words, you can read them as two sequential steps in one research program:

- Step 1: extract general principles of Harness Engineering in Book One.
- Step 2: observe how those principles land differently across two concrete systems in this comparison book.

## Start with Book One: Nine Structural Judgments from Claude Code

Book One compresses to nine: a harness first stops the model from damaging engineering environments; prompt is part of the control plane; the query loop is the agent's heartbeat; tools are execution interfaces constrained by approval, orchestration, and interrupt semantics; more context is not always better, memory / `CLAUDE.md` / compact are budget-governance mechanisms; errors belong on the main path, recovery is first-class; multi-agent value is role partitioning plus independent verification; team rollout must crystallize rules into reusable institutions; together these become a stable Harness Engineering principle checklist.

Reading only Book One leaves one strong impression: Claude Code's character is runtime governance — it cares first about how the session keeps running, how tools avoid trouble, how recovery avoids dead loops, and how verification avoids ritualism.

## Then Read This Comparison Book: Same Problem, Different Starting Points

Based on that foundation, this book splits comparison into explicit layers.

### Control Plane

Claude Code behaves more like dynamic prompt assembly. A lot of order is packed into runtime prompt composition, session state, and context governance.

Codex behaves more like explicit control-layer engineering. It modularizes and types instruction fragments, approval policies, tool schema, thread, rollout, and hooks as much as possible.

### Continuity

Claude Code places continuity in the main loop and emphasizes query-loop heartbeat discipline.

Codex distributes continuity across thread, rollout, and state bridge, emphasizing structured state ownership and recovery.

### Tools and Permissions

Claude Code leans toward runtime constraints: approval at call time, interrupts, and preventing risky actions from landing directly.

Codex leans toward policy language and tool contracts: schema, approval policy, sandbox, and exec policy as explicit organs.

### Local Governance

Claude Code tends to absorb local experience into field memory: `CLAUDE.md`, memory, skills, and workflow constraints.

Codex tends to mount local institutions onto structured injection and event systems: instructions, skills, hooks, and explicit tool boundaries.

### Multi-Agent and Verification

Claude Code emphasizes multi-agent role partitioning at runtime, and insists verification must be independent from implementation.

Codex emphasizes explicit delegation, persistent state, and tool-mediated collaboration so verification becomes a trackable capability, rather than remaining a polite final gesture.

## What Becomes Clear When You Read Them Together

Putting Book One and this comparative volume together yields three fuller conclusions.

### First, the comparison is centered mainly on the harness

Both books point to the same fact: the core challenge of AI coding systems is to keep models from losing control in terminals, filesystems, permission boundaries, and team institutions. Gains in eloquence matter, but they sit downstream of that problem.

### Second, the main difference between Claude Code and Codex is where order is placed

Claude Code is closer to a system grown from runtime incident pressure, prioritizing continuity, recovery, and field governance.

Codex is closer to a system grown from explicit structural design, prioritizing control-layer naming, policy expression, boundary clarity, and composability.

### Third, followers usually gain more by identifying their own dominant uncertainty

If your biggest pain is long-session instability, brittle recovery, and skipped verification, start with the runtime discipline emphasized in Book One.

If your biggest pain is scattered rules, fuzzy permission boundaries, unstable tool contracts, and non-reproducible team behavior, start with the explicit-control-layer lessons this comparison extracts from Codex.

And if you encounter a system whose continuity depends mainly on stacking bootstrap text, identity files, skill catalogs, and workspace prose into prompt, do not be too impressed by the apparent fullness of context. In many cases, that points to an intermediate state that has not yet truly governed context, rather than a mature third road.

## Recommended Reading Order

If you are new to this material set, use this order:

1. Read the [Preface](preface.md) first to confirm that this material is comparing where order is located, not merely listing features.
2. Read [Chapter 1 Why Put Claude Code and Codex Side by Side](chapter-01-why-this-comparison.md) to establish problem framing.
3. Then read Chapters 2 through 6 in sequence across five axes: control plane, continuity, tool governance, local institutions, and multi-agent verification.
4. If you only want a quick synthesis, jump to [Chapter 7 Converging Destinations, Diverging Branches](chapter-07-convergence-and-divergence.md).
5. If your goal is to build systems yourself, finish with [Chapter 8 If You Build One Yourself: Who to Learn from, and What to Learn First](chapter-08-how-to-choose-or-build.md). That chapter now also includes a three-path diagram showing why some harnesses still feel expensive and disorderly even when their context looks full.

## One-Sentence Summary

Book One explains why a controllable agent must grow this way.

This comparative book explains why two serious harness systems still grow differently.
