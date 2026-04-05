# Chapter 6 Errors and Recovery: An Agent System That Keeps Working After Failure

## 6.1 The least trustworthy sentence in engineering is "under normal conditions"

In many system design docs, the most common shortcut is describing only the "normal path," as if beautiful happy-path flow makes errors secondary by default. Once agent systems enter real runtime, this collapses quickly. In reality, everything breaks:

- models get truncated
- requests get too long
- hooks create loops
- tools get interrupted
- fallback paths trigger
- recovery logic itself fails

So maturity cannot be judged by how human-like the system sounds in smooth scenarios. It must be judged by whether failures look like system behavior. The former can be cosmetically improved with prompt tricks; the latter requires runtime discipline.

Claude Code's strength here is not pretending errors are rare. Source repeatedly reflects a calm assumption: errors are part of the main path, and recovery must be predesigned runtime mechanism.

## 6.2 `prompt too long` is seasonal, not exceptional

For long-session agents, `prompt too long` is not an edge case. It is a season that eventually arrives. Treating it as rare exception is an invitation to be corrected by production.

Claude Code `query.ts` does not treat it as accidental. It can temporarily withhold such errors instead of surfacing immediately. During streaming, withheld logic identifies recoverable classes including:

- prompt too long
- media size error
- max output tokens

Meaning: some errors should be handed to recovery first, then surfaced only if recovery fails. Users usually care less about raw error type than whether work can continue.

For prompt-too-long specifically, Claude Code first tries cheaper, less destructive recovery. If context collapse is enabled, it first calls `recoverFromOverflow()` to flush staged collapse; only if insufficient does it call `reactiveCompact.tryReactiveCompact()`. Recovery is layered: clear known backlog first, then do heavier full compaction.

This sequence is highly practical. Good recovery does not hit every error with one giant hammer. It tries to preserve fine-grained context first and escalates only when required.

## 6.3 Reactive compact: recovery must not become dead-loop machinery

A common mistake in recovery systems is both naive and costly: once an error is "recoverable," keep retrying until recoverable turns into resource disaster.

Claude Code is explicitly defensive against this. Two places in `query.ts` show it.

First is `hasAttemptedReactiveCompact`. Once reactive compact has already been attempted, same-class failures are not blindly retried. If compact did not help, repeating compact often just replays the same failure in different posture.

Second is stop-hook dead-loop guards. Source comments are direct: if stop hooks run after unrecoverable prompt-too-long states, death spirals become possible:

error -> hook blocking -> retry -> error -> hook blocking

This is not literary writing; it is brutally honest engineering. The most dangerous errors are often branches where failure and recovery start reproducing each other.

So when prompt-too-long cannot recover, Claude Code surfaces the error directly and skips stop hooks. Continuing formal process there only ritualizes failure.

## 6.4 `max_output_tokens`: recovery should prioritize continuation

Many model products handle truncation with polite waste: "Sorry, I was cut off, let me summarize." It sounds nice and helps little.

Claude Code behavior after `src/query.ts:1185` is far more engineering-aligned. It first tries lower-cost recovery: if current cap is conservative, raise `maxOutputTokensOverride` and rerun the same request. No meta message, no courtesy preface, just one more chance to finish the task.

If higher cap still fails, it escalates to second layer: append a concise meta user message that says, in effect:

continue directly; no apology; no recap; if cut mid-sentence, continue from that half sentence; split remaining work into smaller chunks.

This instruction is highly instructive. Claude Code treats recovery as preserving task continuity, not preserving social polish. In long tasks this difference is huge. Each truncation recap burns additional budget and increases semantic drift. Eventually system spends turns recapping itself instead of doing the task.

For `max_output_tokens`, good recovery is usually continuation-first. Claude Code explicitly optimizes for that.

## 6.5 Auto-compact circuit breaker: recovery systems need governance too

Previous sections are about "how to recover one failure." `src/services/compact/autoCompact.ts` tackles another layer: what if recovery mechanism itself keeps failing?

Source answer is simple and correct: stop retrying forever.

`AutoCompactTrackingState` tracks `consecutiveFailures`. Once failure count exceeds threshold, even if `shouldAutoCompact` says compact is due, system skips compact directly. Source comments reference historical waste: sessions once burned large amounts of API calls on repeated autocompact failure, so circuit breaker was required.

Circuit breaking means admitting current recovery method is ineffective in current state. Mature systems must not only record success metrics; they must know when to back off under repeated failure. Recovery systems without brakes are like vehicles without brakes.

Harness Engineering principle here is hard and clear: any automated recovery must be countable, rate-limited, and breakable.

## 6.6 Compact itself can fail, so recovery action needs its own recovery

`compactConversation()` contains a very realistic moment: compact requests themselves can hit `prompt too long`.

There is black humor here. System sends summary requests to reduce context, then summary requests fail because context is too large. Many designs hide this scenario because it is embarrassing. Engineering systems prioritize survival over elegance.

Claude Code handles this with `truncateHeadForPTLRetry()` in `compact.ts`. When compact input is too large, it strips older API rounds in chunks from the head and retries compact, preventing users from being stuck in "cannot compact compact."

Trade-off is explicit: this fallback is lossy and may drop history, but it prioritizes not deadlocking users. Source comments describe it as last-resort escape hatch.

Value of this choice: it does not deny hard limits. When the system is choking, first priority is restoring breathing, then preserving high-fidelity history.

![Claude Code Recovery Decision Paths](diagrams/diag-ch06-01-recovery-decision-paths.png)

![Claude Code Compact Fallbacks](diagrams/diag-ch06-02-compact-fallbacks.png)

## 6.7 Abort semantics: interrupts are part of recovery

Many teams classify abort under UX only and avoid putting it in recovery discussion. Runtime-wise, interrupts are failure states requiring semantic closure.

Claude Code handles this seriously at two layers.

First in `query.ts`: during streaming user interrupt, runtime consumes `StreamingToolExecutor.getRemainingResults()` and synthesizes tool results for issued-but-unfinished tool calls, preventing dangling commitments.

Second in `compact.ts`: source passes compact abort controller into forked agent and handles `APIUserAbortError`, preventing "compact canceled by user Esc" from being counted as successful summary.

Together, these show interruption is not merely "user stopped reading." It is state transition requiring correct closure. Error recovery that handles exceptions but ignores interruption eventually leaves semantically half-broken execution traces.

## 6.8 Error handling protects narrative consistency of execution

Taken together, Claude Code's recovery philosophy has one core but often overlooked goal: preserve narrative consistency of execution.

Execution narrative means whether the system can still explain:

- what it attempted
- why it failed
- which recovery path was used
- whether it is now continuing, stopping, or rerouting

Fields like `transition.reason`, `maxOutputTokensRecoveryCount`, `hasAttemptedReactiveCompact`, compact boundaries, and synthetic error messages in `query.ts` all exist to keep this narrative unbroken. They are anti-amnesia mechanisms for runtime.

Without narrative consistency, systems may continue outputting text while internally decomposing:

- today users see extra filler
- tomorrow ops sees hook-retry and compact-retry loops with unclear causality
- later teams cannot explain what the system actually went through

So recovery fixes not only errors but system self-explainability. Once explainability breaks, engineering object degrades into opaque magic.

## 6.9 The sixth principle extractable from source

This chapter can be compressed into one sentence:

> The dignity of an agent system is shown by maintaining explainable, bounded, and continuable execution order after failure.

Claude Code source supports this across key points:

- `query.ts` withholds recoverable errors for branch-level transformation before surfacing
- Prompt-too-long recovery layers collapse drain before reactive compact, ordered by cost and destructiveness
- `hasAttemptedReactiveCompact` and stop-hook guards prevent recovery self-loops
- `max_output_tokens` handling escalates cap first and prefers direct continuation over polite recap
- `autoCompact.ts` tracks consecutive failures and enforces circuit breaking
- `compact.ts` includes fallback for compaction's own prompt-too-long failure

Portable principles from this:

- Layer recovery paths; avoid one heavy hammer for all failures
- Recovery logic itself must be loop-safe
- Automated recovery needs counters and circuit breakers
- After truncation, continuation is usually better than summary
- Interruptions are semantic failure states requiring closure
- Reliability is proven by whether the system can still explain itself after errors

Next chapter turns to a harder class of problems: multi-agent and verification. When systems move from "one agent recovers itself" to "one agent delegates and another verifies," error and recovery stop being purely single-thread concerns and become organizational design.
