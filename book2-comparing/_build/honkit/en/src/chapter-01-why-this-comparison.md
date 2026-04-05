# Chapter 1: Why we compare Claude Code and Codex

## 1.1 Because both distrust the model

Calling Claude Code and Codex “models that write code” misses the point. The interesting comparison is not “who has more buttons,” it is how each harness admits a fact marketing often disguises: the model cannot be trusted to operate unbounded shell, files, network, or state. It hallucinates, forgets context, and imagines confidence beyond correctness. Once that model touches a terminal, a filesystem, or a multi-round session, the issue is no longer “was the answer right?” but “who cleans up the mess?”

Claude Code looks like a system born from incident reviews. Read `query.ts`, `toolOrchestration.ts`, `compact.ts`, and the surrounding prompts—you see a system that imagines failure, fatigue, and rollback. Codex is equally honest, but it expresses distrust through explicit modules: threads, rollouts, fragment instructions, exec policies, sandboxing, and tool schemas. Each declares its responsibilities instead of leaving them to the model’s intuition.

So this comparison is about how each harness domesticates unreliability—not about who can hit more commands.

## 1.2 Claude Code: runtime-first harnessing

Claude Code’s strengths cluster around the main loop because it starts from one question: “The model is already cycling. How do we make sure one round doesn’t sabotage the next?” The system is less interested in “pretty prompts” and more interested in prompt layering, compacting, permission gating, interrupts, tool orchestration, and forked agent life cycles. The work happens at runtime: managing message inflation, tool output rerouting, context trimming, child-agent isolation, and independent verification phases. This harness grows out of real shifts—so it solves “dirty work” through control flow, not just through elegant interfaces.

## 1.3 Codex: structured control from the start

Codex takes a different path. Its design treats instructions as typed, bounded fragments. `AGENTS.md`, `skills`, and user fragments appear in the prompts as marked sections with start and end tokens. Tools are schema-first objects. Exec policy is a distinct crate with policies, rules, evaluations, and parsers. The emphasis is on making order explicit, composable, and explainable.

This yields two immediate outcomes: the control plane is easier to explain (you can trace why a fragment is present), and it is easier to programmatically evolve (add new visibility, merge, or precedence rules without rewriting the runtime).

## 1.4 Same question, different starting points

Both systems try to keep an unreliable model from doing unacceptable things. Claude Code begins by asking how a running loop can stay coherent; Codex begins by asking how control information can be turned into explicit, composable structures. Claude Code gravitates toward runtime discipline; Codex gravitates toward typed infrastructure.

## 1.5 Why the difference matters

The direction a team takes often determines how its culture evolves. Emphasize runtime continuity, and you will obsess over recovery, interruption, state pollution, tool choreography, and long-session reliability. Emphasize explicit control, and you will obsess over instruction boundaries, config hierarchies, tool schemas, policy languages, and persistent thread state.

Both paths are valid. The mistake is mixing them without clarity and losing both runtime discipline and institutional order.

## 1.6 The take-away

Claude Code and Codex are harness design philosophies, not feature checklists. They converge on the acceptance that models are untrustworthy; they diverge in what they build around that admission. This book unpacks that divergence.
