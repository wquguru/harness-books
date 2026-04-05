# Preface: Two harnesses, not one accessory pack

Comparing two AI coding harnesses is easy to get wrong if you only line up feature checkboxes. Both Claude Code and Codex have skills, sandboxes, and sub-agents. But seeing shared terminology does not mean their skeletons are the same. It is like noting both cities have bridges—the real question is which river they are trying to cross.

This book aims to compare the bones, not the labels.

Both systems admit something that marketing often sweeps under the rug: a model cannot be trusted to execute without constraints. Shells, filesystems, permissions, tool calls, teams, long sessions, and recovery paths are messy realities. A harness is that messy reality; it is the apparatus that keeps an unreliable model from burning the environment down. When that harness exists, you no longer measure success by how eloquently the model speaks—you measure it by where and how the system places guardrails.

In the first volume I treated Claude Code as a specimen and extracted the general principles of Harness Engineering. That was single-system anatomy. Here the goal is to place Claude Code beside another serious harness with a different lineage. Only in comparison do many design choices reveal themselves as one engineering path among many.

Codex is worth comparing precisely because it is not a clone. A glance at its `core/src/lib.rs` shows a deliberate program: threads, rollouts, state bridges, instructions, skills, hooks, sandboxing, exec policy, tools—each one composed into an explicit module. The ambition is to make the control layer composable, serializable, and policy-aware instead of hiding it inside a bowl of runtime intuition.

Claude Code, by contrast, feels like something grown under the pressure of its runtime loop. Look at `src/query.ts` and the surrounding compacting, tool orchestration, permission handling, interrupts, and recovery logic. Most of its magic answers the question “how does this round hand off safely to the next round?” The harness is first about staying alive; once continuity is stable, then one can polish the rules between phases.

Both systems agree that models are unreliable. That shared conviction matters. Once you admit the model cannot be left inhabiting shell, files, permissions, and long conversations on its own, a harness must grow—prompt stacking, state persistence, approval, context governance, recovery flows, verification, and local conventions. Only the placement of those organs differs.

This book does not reproduce Claude Code or Codex source, and it does not transcribe long implementation excerpts. That boundary is not mysterious: respect for proprietary code, as well as a desire to keep the argument in the engineering analysis. What follows is a comparison of how these systems think about themselves, not a copy-paste of their implementations.

If I had to summarize in one sentence:

> Claude Code and Codex are aligned not because they both call tools, but because neither is willing to treat the model as a free-moving executor.

As for their differences, they are more interesting.

Claude Code approaches harnessing through runtime discipline. It worries about session rupture, tool chaining, compact behavior, user interjections, and what happens if a forked agent dies mid-conversation. It has the feel of someone who has cleaned up after messy shifts in a real operations center—preferring to solve “smart” problems through craftsmanship in control and recovery flows.

Codex approaches it through structured control. Instruction fragments, threads, approval policies, tool schemas, hook events, and exec policies are all spelled out. It values naming, explicit boundaries, and configuration. Codex does not rely on tacit understanding; it prefers to declare marker types and inject them deterministically.

Both routes are valid. They are just valid in different ways.

This is not an article about winners and losers. Valuable engineering comparison helps identify path dependencies, not rank execution speed. The way you choose to constrain an unreliable model determines what your harness becomes. Where your team places control is where the system will grow its flesh. Instead of asking “what is the best practice?,” ask “what uncertainty am I countering, and where am I willing to anchor order?”

The next seven chapters start from that question.

@wquguru  
2026.04.01  
Claude Code fools-day source leak

P.S. Read the online version at [harness-books.agentway.dev/book2-comparing](https://harness-books.agentway.dev/book2-comparing/) for a richer experience.
