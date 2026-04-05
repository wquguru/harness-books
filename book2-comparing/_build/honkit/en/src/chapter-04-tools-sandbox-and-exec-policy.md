# Chapter 4 Tools, Sandboxes, and Policy Languages: Who Stops the Model from Acting Too Fast

![Tool Governance Comparison](diagrams/diag-03-tool-governance-comparison.png)

## 4.1 The truly dangerous moment is the start of execution

When a model says the wrong thing, the usual cost is wasted time. When it runs the wrong command, it can take the directory, repository, processes, and workflow down with it. So what truly distinguishes AI coding systems is who owns the final interpretive authority before a tool starts acting.

Both Claude Code and Codex take this seriously, but they take it seriously in different ways.

Claude Code is closer to pulling tools into runtime scheduling discipline. It has `toolOrchestration.ts`, `toolExecution.ts`, `StreamingToolExecutor.ts`, `useCanUseTool.tsx`, Bash-specific prompts, and explicit `allow / deny / ask` semantics. It cares about whether this tool call may run, how it runs, whether it can run concurrently, whether the user has rejected it, how interruption works midway through execution, and how the result returns to context.

Codex instead starts by turning tools into typed interfaces. `tools/src/lib.rs` exports a whole set of tool constructors, while `local_tool.rs` defines schema-based structures for things like `exec_command`, `shell`, `shell_command`, and `request_permissions`. In Codex, tools are first a normalized API surface and only secondarily an execution unit.

## 4.2 Claude Code: runtime orchestration and constraints on dangerous action

Claude Code's tool system has a strong feel of field dispatch. Concurrency depends on schema and `isConcurrencySafe()`. Context modifications have to preserve replay order. Streaming tool execution must consider interruptions, synthetic results, and UI feedback.

What feels most like real engineering is that the system admits tool invocation is a process with consequences, not a single point action. In that sense, Claude Code's harness resembles a site supervisor attached to the model. Workers may work, but the supervisor must keep watching:

- which tool goes first
- which calls can be parallelized
- which must remain serial
- how results are accounted for
- what to do if work is halted halfway

Bash, especially, is treated with a near-obsessive explicitness. That may sound fussy, but mature systems are usually fussy around the most dangerous interface. Anyone who still approaches shell with youthful swagger probably has not accumulated enough incident memory yet.

## 4.3 Codex: tool schemas, approval parameters, and a policy engine

Codex is closer to expressing control over risky actions as formal interface constraints.

Take `local_tool.rs`. A tool such as `exec_command` explicitly owns fields like:

- `cmd`
- `workdir`
- `shell`
- `tty`
- `yield_time_ms`
- `max_output_tokens`
- `login`
- approval-related parameters

And `shell` / `shell_command` descriptions explicitly require `workdir`, warning against careless `cd` habits. This reveals an important design belief: Codex does not settle for "the runtime should quietly do the right thing." It wants correct usage patterns encoded in the tool definition itself.

More than that, approvals and escalation are modeled as explicit parameters, `request_permissions` exists as a separate tool, and `execpolicy` is implemented as its own crate. That language already goes beyond simple permission gates into an actual policy layer:

- `Policy`
- `Rule`
- `Evaluation`
- `Decision`
- parser

These names are practically announcing that execution boundaries have become a small policy language rather than a handful of `if / else` checks.

## 4.4 Runtime approvals versus policy language

The split between Claude Code and Codex around tool risk can be compressed like this:

- Claude Code leans toward a runtime approval chain
- Codex leans toward explicit policy language and parameterized approvals

Claude Code's `ask / allow / deny` logic is tightly coupled to the scene of the tool call. The system can decide according to current context, tool type, user action, and session state. Its strength is sensitivity; its weakness is that rules can remain buried inside runtime logic.

Codex's exec-policy approach tries to pull rules outward and make them separately parsable and separately evaluable. The strength is better readability and portability of rules, and a much more natural fit for team-level governance. The cost is weight: the system feels heavier, and policy design must be treated as real design work rather than as commentary.

Put bluntly:

Claude Code is closer to a shift manager making the call on site.

Codex is closer to a company that writes the policy first and then checks whether the action is compliant.

## 4.5 Sandbox and approval are not merely security features

Many teams treat sandboxing, approvals, and permissions as security accessories. That is too light. In a coding agent, these things define what the product actually is.

If the system lets the model run arbitrary commands directly in a user directory, it is not simply "more powerful." It is an agent that transfers risk to the user. Conversely, if a system can explicitly express sandbox mode, network access, approval policy, additional directories, state-store location, and MCP tool approvals, then it is offering not just capability but behavioral boundaries.

Codex exposes these turn-level conditions in `thread.ts`, which shows it treats them as part of thread semantics rather than as hidden implementation detail. Claude Code instead pushes the boundary into runtime execution through tool handling, interrupts, permission hooks, and Bash restrictions.

That means the two systems differ at the level of product philosophy too:

- Claude Code is closer to "execute while being watched"
- Codex is closer to "declare the execution contract before starting"

## 4.6 MCP, external tools, and boundary migration

Both systems can attach more capabilities, but their differences remain.

Claude Code is closer to building a situational governance chain out of skill, hook, permission, and tool prompt. Its strength is getting local rules into the main loop together with the task.

Codex is more willing to pull external capabilities into one unified tool system. MCP resources, dynamic tools, and tool discovery interfaces in `tools/src/lib.rs` show that extensions are expected to become schema-defined, rule-governed tools rather than temporary runtime understandings.

That is a consequential divergence. Once the ecosystem grows, the whole system becomes more dependent on how extensions obey the general rules. The team that thinks through boundary migration early is the team whose extension ecosystem is less likely to degenerate into a junk closet later.

## 4.7 Chapter conclusion

This chapter can be reduced to a hard sentence:

> Claude Code's tool governance depends more on runtime orchestration and situational approvals, while Codex's tool governance depends more on schemas, parameterized permissions, and an independent policy system.

The former is like an experienced foreman.

The latter is like a contractor with a compliance office and legal department.

If you look only at the fact that both can run commands, you miss the meaningful difference. The real question is who owns order before the tool starts moving.

The next chapter looks at a more grounded layer: skills, hooks, local rule files, and team institutions. Once a technical system has to enter a team, it eventually has to learn village law.
