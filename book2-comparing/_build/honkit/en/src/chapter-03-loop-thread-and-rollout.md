# Chapter 3 Where the Heartbeat Lives: Query Loop Versus Thread, Rollout, and State

![Continuity Comparison](diagrams/diag-02-continuity-comparison.png)

## 3.1 The core of an agent system is continuity

If you understand an agent system as "multi-turn chat," that is like understanding a database as "a patient notebook." It is not entirely false, but it hides the real architectural problem.

The hard problem in an agent system is continuity:

- what happened last turn, and how this turn picks it up
- how tool results are merged back into the session
- how interruption gets closed out
- how overgrown context is reorganized
- whether failure should trigger retry, compaction, or faithful reporting

These questions determine whether a system is really an agent, rather than merely a question-answering interface that happens to support tool calls.

The difference between Claude Code and Codex here is more revealing than almost any feature table.

## 3.2 Claude Code: continuity is compressed into the main loop

Claude Code's axis is easy to locate around `query()` and `queryLoop()`. It pushes many crucial issues into loop state:

- current message sequence
- tool-use context
- compact tracking
- output-token recovery counters
- pending summaries
- turn counts
- transitions

That means Claude Code answers the question "how does an agent stay alive?" in runtime terms. Continuity is maintained mainly by the loop. The skeleton therefore feels more like a conversation engine that keeps correcting itself than a system driven first by a strong external state model.

Its advantage is very concrete. Much of the real trouble in sessions happens exactly inside the loop: tool-return ordering, abrupt truncation of model output, prompt-too-long events, history snips, microcompact, and user interjections. Claude Code does not avoid these issues. It treats them as legitimate states inside the loop.

That gives the design a rough engineering texture. It is not always elegant, but it often survives.

## 3.3 Codex: continuity is split across thread, rollout, and state bridges

Codex looks more ledger-like. Even from `core/src/lib.rs`, continuity is clearly not concentrated in one large loop. It is distributed across:

- `codex_thread`
- `thread_manager`
- `rollout`
- `state_db_bridge`
- `state`
- `message_history`

Then look at `sdk/typescript/src/thread.ts`. There, `Thread` is already a first-class concept that outside developers can understand and manipulate directly. A thread has an `id`, can `runStreamed()` or `run()`, and `thread.started` reports back the thread ID. Turn-level execution conditions such as approval policy, working directory, sandbox mode, network access, and additional directories are all exposed as explicit parameters tightly coupled to thread execution.

What matters most is that continuity is no longer merely "the loop is still going." It becomes "a thread is being recorded and constrained by a more explicit state structure." The existence of rollout is especially telling: Codex cares deeply about replayability, indexing, persistence, and visibility outside the immediate live session.

That makes the system feel more like a true execution recorder and less like a live conversation manager alone.

## 3.4 The difference is where state sovereignty lives

One clarification matters. Claude Code obviously has state. Codex obviously has loops. The difference is not presence or absence, but sovereignty.

Claude Code gives more sovereignty to the query loop. It treats "how the session continues" as a runtime-core problem, and many issues are meant to be solved directly inside the loop.

Codex gives sovereignty more explicitly to thread and rollout structures. It treats continuity as something that should not remain a by-product of internal control flow; it should become an explicit fact carried by thread and state infrastructure.

That is why `Thread` in the TypeScript SDK already feels like a product concept rather than an implementation detail. Developers are allowed to think about agent turns directly through the thread abstraction.

Claude Code's query loop is more like the engine room. You know it matters, but not every user has to organize their mental model explicitly around it.

## 3.5 Different implications for recovery and auditability

This placement of state directly affects recovery and auditability.

Claude Code's recovery strength comes from proximity to the scene. Many problems are discovered and handled inside the loop itself: reactive compaction, output-token recovery, and tool-interruption cleanup. It does not first need to lift the problem into a higher-order state model before deciding what rollback should mean.

Codex's recovery strength is more likely to appear in traceability. Threads have IDs, rollouts have records, and state bridges plus message history provide clearer external structure. That makes it easier for the system to answer the question, "What exactly happened last turn?" rather than relying on runtime recollection alone.

In plain language:

- Claude Code is closer to an emergency crew on site
- Codex is closer to a dispatch center with archives

Both matter. The former is better at surviving. The latter is better at explaining how it survived.

## 3.6 Different effects on product and team interfaces

This difference also changes how teams integrate with the system.

If sovereignty lives in the loop, teams naturally organize around runtime questions:

- which failures need recovery
- which actions should be interruptible
- when compaction should trigger
- how tool results return to the main conversation

If sovereignty lives in threads and state structures, teams organize more around interface and governance questions:

- what the thread lifecycle is
- which events rollout should retain
- where the state store lives
- how approval policy becomes a turn-level option

So Claude Code is closer to making the agent operational first and embedding institutions afterward. Codex is closer to defining institutional interfaces first and letting the agent operate inside them.

## 3.7 Chapter conclusion

The conclusion can be stated plainly:

> Claude Code places more of continuity inside the query loop, while Codex places more of continuity inside thread, rollout, and state infrastructure.

The former emphasizes runtime heartbeat.

The latter emphasizes a persisted session substrate.

This is not an aesthetic difference. It is a distribution of system power. Whoever owns continuity defines the center of the harness.

The next chapter moves into the hardest layer of all: tools, sandboxes, approvals, and execution policy. Once shell enters the picture, romantic narratives usually leave on their own.
