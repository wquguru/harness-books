# Chapter 3 Where the Heartbeat Lives: Query Loop Versus Thread, Rollout, and State

![Continuity Comparison](diagrams/diag-02-continuity-comparison.png)

## 3.1 The core of an agent system is continuity

Treating an agent system as "multi-turn chat" is like treating a database as "a patient notebook" — it hides the real architectural problem. Continuity is the hard thing: how this turn picks up from the last, how tool results get merged, how interruption gets closed out, how overgrown context is reorganized, whether failure triggers retry, compaction, or faithful reporting. These answers decide whether a system is really an agent rather than a question-answering interface that happens to support tool calls. Claude Code and Codex diverge here more tellingly than any feature table.

## 3.2 Claude Code: continuity compressed into the main loop

The axis sits around `query()` and `queryLoop()`, which push many crucial issues into loop state: current message sequence, tool-use context, compact tracking, output-token recovery counters, pending summaries, turn counts, transitions. The answer to "how does an agent stay alive" is runtime-flavored — continuity is maintained mainly by the loop, and the skeleton feels like a self-correcting conversation engine rather than a system driven first by an external state model. The strength is concrete: tool-return ordering, output truncation, prompt-too-long events, history snips, microcompact, and user interjections all happen inside the loop, and Claude Code treats them as legitimate loop states rather than avoiding them. The design has rough engineering texture — not always elegant, but often more robust.

## 3.3 Codex: continuity split across thread, rollout, and state bridges

Codex looks more ledger-like. From `core/src/lib.rs` onward continuity is distributed across `codex_thread`, `thread_manager`, `rollout`, `state_db_bridge`, `state`, and `message_history`.

![Codex thread-turn-state detail](diagrams/diag-06-codex-thread-state-detail.png)

In `sdk/typescript/src/thread.ts`, `Thread` is already a first-class concept for outside developers: it owns `id`, runs via `runStreamed()` or `run()`, and `thread.started` reports the thread ID back. Turn-level execution conditions — approval policy, working directory, sandbox mode, network access, additional directories — are all explicit parameters tightly coupled to thread execution. Thread sovereignty is literal: `runStreamedInternal()` calls `normalizeInput()` to separate text from images, `createOutputSchemaFile()` to prepare a schema file, then passes `threadId`, `approvalPolicy`, `sandboxMode`, `workingDirectory`, `networkAccessEnabled`, and `additionalDirectories` into `_exec.run()`. When the stream emits `thread.started`, the object updates its `_id`. Thread is not outer packaging — it is the layer turn semantics actually pass through. Continuity is no longer "the loop is still going" but "a thread is being recorded and constrained by an explicit state structure." Rollout, especially, signals that Codex cares about replayability, indexing, persistence, and out-of-session visibility — the system feels more like an execution recorder than a live conversation manager.

## 3.4 The difference is where state sovereignty lives

Claude Code has state, Codex has loops — the difference is not presence or absence but sovereignty. Claude Code gives more sovereignty to the query loop: "how the session continues" is a runtime-core problem, and many issues are solved directly inside the loop. Codex gives sovereignty to thread and rollout structures: continuity should not remain a by-product of internal control flow; it should become an explicit fact carried by thread and state infrastructure. That is why `Thread` in the TypeScript SDK already feels like a product concept, and developers think about agent turns through it directly. Claude Code's query loop is more like the engine room — important, but not every user has to organize their mental model around it.

### Invariants: continuity sovereignty

```
// Claude Code (src: src/query.ts)
assert loop owns {messages, toolUseContext, compactTracking, turnCount}
assert each loop iteration recomputes "what matters now"
assert pending tool_use closed or synthetic-filled before iteration ends

// Codex (src: core/src/lib.rs, sdk/typescript/src/thread.ts)
assert thread.id stable across runs; rollout records every turn
assert turn-level {approvalPolicy, sandboxMode, workingDirectory} explicit in exec.run() args
assert thread.started event emitted before any tool call
assert state_db_bridge persists before the main loop exits
```

### Failure matrix: interrupt with pending tool_use

| Event order | Pre-state | Trigger | Claude Code next | Codex next |
|---|---|---|---|---|
| user interrupt + tool in flight | tool_use unclosed | user abort | synthesize tool_result in loop, close ledger | thread-level abort, write rollout "interrupted" event |
| model output truncated | max_output_tokens | cap hit | raise cap or append meta user msg to continue | thread records truncation, caller restarts turn |
| prompt too long | session bloated | `prompt_too_long` | collapse / reactive compact / surface inside loop | thread_manager trims history, next turn |
| process restart | crash mid-session | crash / kill | rely on external PR / Git to rebuild; loop state fragile | rollout + state_db_bridge replay by thread.id |
| recovery exhausted | consecutive compact failures | breaker threshold | skip stop hook, faithful error | return state-bridge error, keep thread record |

## 3.5 Different implications for recovery and auditability

State placement directly affects recovery and auditability. Claude Code's recovery strength comes from proximity to the scene — many problems are discovered and handled inside the loop itself (reactive compaction, output-token recovery, tool-interruption cleanup), without lifting them into a higher-order state model first. Codex's recovery strength lies in traceability: threads have IDs, rollouts have records, state bridges plus message history provide clearer external structure, making "what exactly happened last turn" answerable from archives rather than runtime recollection. `core/src/lib.rs` read together with the SDK layer makes the archive-minded design obvious — exporting not only `CodexThread` but also `ThreadManager`, `RolloutRecorder`, `state_db_bridge`, and `message_history` near the root module effectively declares continuity as infrastructure, not a side effect of looping. Plain language: Claude Code is closer to an emergency crew on site, Codex closer to a dispatch center with archives — the former is better at keeping execution going, the latter at explaining how continuity is maintained.

## 3.6 Different effects on product and team interfaces

Sovereignty in the loop steers teams toward runtime questions: which failures need recovery, which actions should be interruptible, when compaction triggers, how tool results return to the main conversation. Sovereignty in threads and state structures steers teams toward interface and governance questions: thread lifecycle, which events rollout should retain, where the state store lives, how approval policy becomes a turn-level option. Claude Code is closer to making the agent operational first and embedding institutions afterward; Codex is closer to defining institutional interfaces first and letting the agent operate inside them.

## 3.7 Chapter conclusion

The conclusion can be stated plainly:

> Claude Code places more of continuity inside the query loop, while Codex places more of continuity inside thread, rollout, and state infrastructure.

The former emphasizes runtime heartbeat.

The latter emphasizes a persisted session substrate.

This is not an aesthetic difference. It is a distribution of system power. Whoever owns continuity defines the center of the harness.

The next chapter moves into the hardest layer of all: tools, sandboxes, approvals, and execution policy. Once shell enters the picture, romantic narratives usually leave on their own.
