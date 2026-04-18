# Chapter 6 Delegation, Verification, and Persistent State: Who Stops the System from Grading Itself

## 6.1 The real problem in multi-agent systems is responsibility

Hearing "multi-agent" and jumping to efficiency is like hearing a headcount plan — the truly difficult part is never more agents but how responsibility gets divided. If one system executes, summarizes, verifies, and casually writes its own review, the result is comforting and unreliable: "good job." Claude Code separates explore, execute, synthesis, and verification and treats verify as an independent discipline rather than a polite closing flourish — "done" is not declared by the executing agent alone. Codex walks the same road: `tools/src/lib.rs` exposes `create_spawn_agent_tool_v*`, `create_wait_agent_tool_v*`, `create_send_message_tool`, `create_close_agent_tool_v*` — delegation is formal tool capability, not runtime black magic.

## 6.2 Claude Code: multi-agent serves runtime separation of responsibility

The mechanism stays centered on the main loop and task progression: the primary agent should not do everything itself, and must not both implement and certify. Multi-agent handles outsourced exploration, split implementation, synthesis, and independent verification. That fits the strength in runtime orchestration — multi-agent enters the governance framework of "how the current task moves forward," rather than a grand agent platform into which tasks are slotted.

## 6.3 Codex: multi-agent serves explicit tool-mediated collaboration

Delegation is defined as tool interface, pushing multi-agent toward a formal subsystem. Two effects: delegation becomes easier to record, audit, and compose because it is an explicit tool call, not hidden runtime maneuvering; collaboration aligns with threads, state, and approval systems, inheriting the first-class infrastructure Codex already built. In `agent_tool.rs`, `spawn_agent`, `send_input`, `wait_agent`, and `close_agent` each have their own schemas: `send_input` distinguishes `interrupt=true` from default queued delivery; `wait_agent` is parameterized with default/min/max timeouts; `close_agent` explicitly closes open descendants. Codex turns preemption, waiting, and cleanup into protocol fields — a strong foundation for platform capability, not always nimble but durable.

## 6.4 Persistent state keeps verification from becoming etiquette

Verification turns ceremonial mainly because state handoff is weak. What was done, why, which tools, which files — if that only lives in the executor's head, verification becomes serious-looking theater without material. Claude Code keeps session state, tool results, and recovery branches continuously visible inside runtime, then pairs that continuity with an independent verification discipline. Codex provides explicit material via thread, rollout, message history, and state DB bridge — a system with session-archive awareness is simply better at answering "what exactly happened just now." The two are not in conflict: Claude Code repairs executors too immersed in the scene; Codex repairs collaboration that must leave structured evidence.

## 6.5 Different attitudes toward recovery and closure

Claude Code cares deeply about task cleanup, parent-child abort propagation, and subagent lifecycle hooks — in its world multi-agent work is first a live runtime phenomenon that must close down quickly when the scene goes wrong. Codex leans the other way, bringing agent lifecycle under explicit state management and invocation protocol: it cares not only whether a subagent died, but how that delegated act should persist as a system event. One resembles a site chief worrying about holes left behind; the other resembles an organizer with project infrastructure worrying whether every collaboration act entered the record.

### Skeleton: Codex delegation protocol

```
// skeleton: agent_tool.rs spawn/wait/send/close
handle = spawn_agent { role, prompt, timeout, inherit_approval }
for msg in updates:
    send_input(handle, msg, interrupt ∈ {true, false})  // true=preempt, false=queue
result = wait_agent(handle, timeout ∈ [min, default, max])
close_agent(handle, cascade=true)                        // closes open descendants too
```

### Orphan and timeout failure matrix

| Event order | Pre-state | Trigger | Next | Threshold |
|---|---|---|---|---|
| parent abort | child in flight | parent.abort | cascade abort to handle; write rollout event | — |
| `wait_agent` timeout | child unreturned | timeout ≥ max | close handle, return timeout result | `wait_agent.max` |
| `send_input(interrupt=true)` | child queued | preemption | drop queue, inject new input | — |
| `close_agent` | open descendants | explicit close | cascade-close all descendants | `cascade=true` |
| child crash | — | abnormal exit | return error, keep thread record | — |
| handle leak | task ends without close | finalize | force close + evict | no dangling handles |

## 6.6 Chapter conclusion

The conclusion is not difficult to state:

> Claude Code's multi-agent design emphasizes runtime separation of responsibility and field closure, while Codex's multi-agent design emphasizes tool-mediated delegation, state handoff, and auditable collaboration.

Both are trying to stop the system from giving itself inflated grades.

Claude Code leans more on role separation and verification discipline.

Codex leans more on explicit interfaces, thread state, and collaboration records.

The final chapter compresses the previous six into one overall judgment and answers the book's title question directly: convergence through different roads, or genuinely different species?
