# Chapter 6 Delegation, Verification, and Persistent State: Who Stops the System from Grading Itself

## 6.1 The real problem in multi-agent systems is responsibility

When people hear "multi-agent," they often react as if they were hearing a corporate headcount plan and immediately imagine higher efficiency. But the truly difficult part is never the mere presence of more agents. It is how responsibility gets divided.

If the same system executes, summarizes, verifies, and casually writes its own review, the result is usually comforting and not especially reliable: good job.

Claude Code is unusually clear-eyed about this. As the earlier material already showed, it separates explore, execute, synthesis, and verification, and it treats verify as an independent discipline rather than as a polite closing flourish. That matters because it means the system refuses to let "done" be declared solely by the executing agent.

Codex is clearly moving down the same road. The many agent-related tools in `tools/src/lib.rs`, such as `create_spawn_agent_tool_v*`, `create_wait_agent_tool_v*`, `create_send_message_tool`, and `create_close_agent_tool_v*`, show that delegation in Codex is formal tool capability rather than runtime black magic.

## 6.2 Claude Code: multi-agent work serves runtime separation of responsibility

Claude Code's multi-agent mechanism remains centered on the main loop and task progression. It is close to saying: the primary agent should not do everything itself, and it definitely should not both implement and certify the implementation.

So multi-agent work is primarily used to handle:

- outsourced exploration tasks
- split implementation tasks
- synthesis of results
- independent verification

This architecture fits its overall temperament. Claude Code's strength already lies in runtime orchestration, so multi-agent naturally becomes part of the governance framework for getting the current task forward. It did not begin with a grand agent platform and then insert tasks into it. It began with field-dispatch problems and developed agent partitioning from there.

## 6.3 Codex: multi-agent work serves explicit tool-mediated collaboration

In Codex, delegation is more visibly defined as tool interface. That pushes multi-agent closer to the status of a formal subsystem.

That has two direct effects.

First, delegation actions become easier to record, audit, and compose, because they are explicit tool calls rather than hidden runtime maneuvers.

Second, collaboration aligns more naturally with threads, state, and approval systems. Since Codex already treats thread, rollout, and policy as first-class infrastructure, multi-agent work slips into that same infrastructure rather than remaining a local field technique.

This is a strong foundation for treating multi-agent behavior as platform capability. It may not always feel as nimble, but it is easier to maintain durably.

## 6.4 Persistent state keeps verification from becoming etiquette

Verification so often turns ceremonial for one major reason: the system lacks a good enough state handoff. What was just done, why it was done, which tools were used, and which files were touched all matter. If that information lives only in the executing agent's head, the verification phase turns into a performance that looks serious but is starved of material.

Claude Code addresses this by keeping session state, tool results, and recovery branches continuously visible inside runtime, then pairing that continuity with an independent verification discipline to reduce self-flattery.

Codex is more likely to provide explicit material foundations for verification through thread, rollout, message history, and state DB bridge structures. A system with session-archive awareness is simply better at answering, "What exactly happened just now?"

That means the two systems are not in conflict on verification. They repair different deficits:

- Claude Code repairs the problem of an executor becoming too immersed in the live scene
- Codex repairs the problem that collaboration must leave structured evidence

## 6.5 Different attitudes toward recovery and closure

Multi-agent systems face another practical question: how do they close things out?

A great many details in Claude Code show that it cares deeply about task cleanup, parent-child abort propagation, subagent lifecycle hooks, and similar concerns. In its world, multi-agent work is first a live runtime phenomenon, and if the live scene goes wrong, the system must be able to close it down quickly.

Codex, judging by toolized agents and thread-state structures, leans more toward bringing agent lifecycle under explicit state management and invocation protocol. It cares not only whether a subagent died, but also how that delegated act should persist as a system event.

Again, the difference is temperamental:

- Claude Code resembles a chief engineer on site, worrying about what holes remain after people leave
- Codex resembles an organizer with project infrastructure, worrying whether every collaboration act entered the record system

## 6.6 Chapter conclusion

The conclusion is not difficult to state:

> Claude Code's multi-agent design emphasizes runtime separation of responsibility and field closure, while Codex's multi-agent design emphasizes tool-mediated delegation, state handoff, and auditable collaboration.

Both are trying to stop the system from giving itself inflated grades.

Claude Code leans more on role separation and verification discipline.

Codex leans more on explicit interfaces, thread state, and collaboration records.

The final chapter compresses the previous six into one overall judgment and answers the book's title question directly: convergence through different roads, or genuinely different species?
