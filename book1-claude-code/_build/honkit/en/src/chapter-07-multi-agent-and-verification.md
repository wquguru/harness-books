# Chapter 7 Multi-Agent Work and Verification: Managing Instability Through Division of Labor

## 7.1 Past a certain point, the question is not "can one agent do it" but "how should work be split"

If one agent only answers in one thread, many contradictions can still be hidden by patience. If it is slow, users wait. If reasoning is messy, users ask follow-ups. If context turns muddy, compact may patch it. But once tasks get larger, single-agent designs hit a harder problem: research, implementation, and verification are squeezed into one context chain, competing for budget, attention, and narrative center.

At that point multi-agent seems like an obvious answer: spin up more workers. But this is not cheap. Multi-agent does not produce order by default. Often it just parallelizes single-agent disorder. The real difficulty is isolating instability per agent and then reassembling outputs coherently.

Claude Code source is clear-eyed here. It does not treat subagents as "another chat window." It treats them as managed execution processes with explicit cache boundaries, state boundaries, verification duties, and cleanup responsibilities.

## 7.2 The first principle of forked agents is cache safety

At the top of `src/utils/forkedAgent.ts`, a comment precisely states forked-agent utility duties:

1. share cache-critical params with parent to ensure prompt-cache hits
2. track usage across the whole query loop
3. record metrics
4. isolate mutable state to avoid disturbing parent loop

Among these, cache-critical sharing appears first. That is not accidental. It means fork is runtime-controlled branching. If it is branching, parameters that must remain parent-consistent are crucial; otherwise prompt-cache reuse fails and both cost and latency degrade.

`CacheSafeParams` explicitly includes:

- `systemPrompt`
- `userContext`
- `systemContext`
- `toolUseContext`
- `forkContextMessages`

Source also warns against casually changing `maxOutputTokens`, because thinking configuration may change and thinking config is part of cache keys.

This shows multi-agent is first a runtime economics problem. If each child agent re-burns parent context from scratch, what looks like parallel acceleration is parallel waste. Claude Code's first concern in fork paths is preserving cache discipline.

## 7.3 State isolation: reduce contamination before sharing anything

The second key appears in `createSubagentContext()`. Source writes this plainly: by default, all mutable state is isolated to avoid parent interference.

Default behavior includes:

- cloning `readFileState`
- creating child abort controllers instead of sharing parent controllers directly
- wrapping `getAppState` so child avoids permission prompts
- making `setAppState` a no-op by default
- recreating sets like `nestedMemoryAttachmentTriggers` and `loadedNestedMemoryPaths`

Only explicit opt-in options enable sharing for selected callbacks, such as `shareSetAppState`, `shareSetResponseLength`, and `shareAbortController`.

This is important because many multi-agent implementations miss a hard fact: the main value of child agents is containing local chaos away from main thread. Research misreads, temporary file observations, exploratory reasoning branches, and in-flight tool decisions should not be blindly written back to main context. If they are, you only accelerate contamination.

Claude Code's stance is: sharing requires explicit consent; isolation is default ethics. This is closer to transactional database design than to chat toys.

## 7.4 Coordinator mode: synthesis is the scarce capability

In `src/coordinator/coordinatorMode.ts`, coordinator expectations are disciplined:

- help users reach goals
- direct workers for research, implementation, and verification
- synthesize findings and communicate with users
- answer directly when delegation is unnecessary

The most important line in section 5 of the prompt is: **Always synthesize**. When workers return findings, coordinator must digest and convert them into concrete prompts; it must not forward raw findings and outsource understanding again.

This is the throat of multi-agent design. The scarce capability is not parallel output generation. It is recompressing distributed local knowledge into actionable and verifiable next steps. Without this layer, multi-agent quickly degrades into polite task forwarding.

Claude Code gets this at prompt level: research and synthesis are separated, and coordinator owns interpretation. Follow-up prompts must mention concrete files, concrete locations, and concrete changes, not abstract references like "based on above findings." This is orthodox engineering division of labor: research can be distributed; understanding must reconverge.

## 7.5 Verification must be independent, or implementation completion will impersonate problem solved

`coordinatorMode.ts` also contains a section worth copying verbatim in spirit. It separates common task flow into:

- Research
- Synthesis
- Implementation
- Verification

And explicitly states verification proves effectiveness, not merely code existence:

- run tests with the feature enabled
- investigate errors instead of dismissing them as unrelated
- stay skeptical
- test independently, do not rubber-stamp

This shows Claude Code does not treat verification as a side effect of implementation worker output. It is second-layer quality gate. Prompt even encodes two-layer checks: implementation worker self-check plus independent verification worker.

Why this matters: in agent systems, "I changed code" and "the change is correct" are separated by a wide river. Models are especially good at building paper bridges over that river. They can provide changes, explanations, and even plausible test-like output. None of that guarantees correctness in real runtime.

Independent verification prevents "can modify code" from impersonating "can deliver outcomes." In multi-agent Harness Engineering, this role separation is central.

## 7.6 Hooks and task lifecycle: spawning a subagent is only the beginning

In multi-agent systems, a commonly ignored fact is that spawn is start, not end.

`src/utils/hooks/hooksConfigManager.ts` defines `SubagentStart` and `SubagentStop` hooks. Start events include `agent_id` and `agent_type`. Stop events include `agent_transcript_path`, and even allow exit code 2 so stderr can be fed back and let subagent continue.

This means subagents are explicit lifecycle objects in Claude Code. Start can be observed, pre-stop can be intercepted, transcript paths are traceable. "Subagent end" is itself a managed event.

At another layer, `registerAsyncAgent()` in `src/tasks/LocalAgentTask/LocalAgentTask.tsx` shows each async agent has cleanup handlers. Parent aborts propagate to child abort controllers. On task completion, outputs can be evicted, state updated, and cleanup callbacks unregistered.

This resembles operating-system lifecycle control, not chat tabs:

- is the agent still running
- should child terminate when parent terminates
- should output artifacts be retained
- were cleanup handlers leaked

![Claude Code Multi-Agent Runtime Lifecycle](diagrams/diag-ch07-01-multi-agent-lifecycle.png)

Many multi-agent demos stop at "I can start another agent." Claude Code takes one more crucial step: it treats agents as runtime entities that can leak resources, leave state residue, and become orphans after parent death.

## 7.7 Verification applies to memory and recommendations, not only code

Multi-agent verification is not only post-code-change activity. Claude Code embeds this discipline in memory systems too.

`src/memdir/memoryTypes.ts` explicitly warns that memory records can become stale. Before giving recommendations based on memory, verify current state. If memory conflicts with present reality, trust current observed state and update or delete stale memory.

Placed in this chapter, it shows a broader fact: verification is the system's baseline habit against temporal drift and context drift. If a system verifies newly written code but does not verify old memory, assumptions, or indexes, history will still steer it wrong.

So verification is both a skill and an institutional discipline. You can delegate work, persist information, and let other agents run ahead, but before users act on outputs, someone must return to current reality and revalidate.

## 7.8 Multi-agent really solves uncertainty partitioning

Put these source pieces together and Claude Code's multi-agent design reveals a simple target: partition uncertainty.

Research workers can explore in local contexts without polluting main thread with every tentative branch. Implementation workers can focus on edits without carrying full communication burden. Verification workers can specialize in skepticism without defending their own edits. Coordinator sits in the middle to converge and communicate.

This partitioning gives the main benefit: clear responsibilities. Once responsibilities are clear, failures are easier to locate:

- did research miss a key signal
- did synthesis fail to digest findings
- did implementation introduce defects
- did verification undercheck

If all of this is delegated to one agent "in one go," you get one thick soup. Maybe flavorful, hard to debug.

So multi-agent value is less about speed and more about placing different uncertainties in different containers and then recombining them through coordinator synthesis.

## 7.9 The seventh principle extractable from source

This chapter can be compressed into one sentence:

> Multi-agent systems depend on clear division of labor: research, implementation, verification, and synthesis must run under different constraint containers, then be stitched back into deliverable outcomes by a coordinator.

Claude Code source supports this jointly:

- `forkedAgent.ts` prioritizes cache-safe params, usage tracking, and state isolation, making fork a runtime-control problem first
- `createSubagentContext()` isolates mutable state by default and only shares via explicit opt-in
- `coordinatorMode.ts` requires synthesis instead of forwarding, so understanding cannot be outsourced
- verification is explicitly separated from implementation and must independently prove effectiveness
- `hooksConfigManager.ts` provides `SubagentStart` and `SubagentStop`, making subagents observable lifecycle objects
- `LocalAgentTask.tsx` handles parent abort propagation, cleanup, and output eviction

Portable principles:

- optimize fork for cache and state boundaries before "persona specialization"
- isolate child agents by default; share only by explicit declaration
- research can be delegated; synthesis cannot
- verification must be role-separated from implementation
- agent lifecycle must be observable, interruptible, and reclaimable
- true parallel value is clearer responsibilities, not raw speed

Next chapter moves from runtime design to organization design: how `CLAUDE.md`, skills, approvals, hooks, and memory become reusable team institutions instead of private expert tricks.
