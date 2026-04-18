# Chapter 4 Tools, Sandboxes, and Policy Languages: Who Stops the Model from Acting Too Fast

![Tool Governance Comparison](diagrams/diag-03-tool-governance-comparison.png)

## 4.1 The truly dangerous moment is the start of execution

A model saying the wrong thing wastes time; running the wrong command takes the directory, repository, processes, and workflow down with it. What distinguishes AI coding systems is who owns the final interpretive authority before a tool acts. Both Claude Code and Codex take this seriously in different ways. Claude Code pulls tools into runtime scheduling discipline — `toolOrchestration.ts`, `toolExecution.ts`, `StreamingToolExecutor.ts`, `useCanUseTool.tsx`, Bash-specific prompts, explicit allow/deny/ask semantics — deciding whether a call may run, how, whether concurrently, whether the user rejected, how to interrupt, and how results return to context. Codex turns tools into typed interfaces first — `tools/src/lib.rs` exports tool constructors, `local_tool.rs` defines schemas for `exec_command`, `shell`, `shell_command`, `request_permissions`. Tools in Codex are first a normalized API, only secondarily an execution unit.

## 4.2 Claude Code: runtime orchestration and dangerous-action constraints

The tool system has a strong field-dispatch feel: concurrency depends on schema and `isConcurrencySafe()`, context modifications preserve replay order, streaming execution must handle interrupts, synthetic results, and UI feedback. Tool invocation is treated as a process with consequences, not a single point action — the harness resembles a site supervisor attached to the model, watching which tool goes first, which can be parallelized, which must serialize, how results are accounted for, and what happens when work is halted halfway. Bash is treated with near-obsessive explicitness — mature systems are usually fussy around the most dangerous interface.

## 4.3 Codex: tool schemas, approval parameters, and a policy engine

Codex expresses control over risky actions as formal interface constraints. In `local_tool.rs`, `exec_command` explicitly owns fields — `cmd`, `workdir`, `shell`, `tty`, `yield_time_ms`, `max_output_tokens`, `login`, approval-related parameters — rather than accepting a single string command. `shell` / `shell_command` descriptions require `workdir` and warn against careless `cd`. Correct usage is encoded in the tool definition itself. Approvals and escalation are explicit parameters, `request_permissions` is a separate tool, and `execpolicy` is its own crate — `Policy`, `Rule`, `Evaluation`, `Decision`, parser — execution boundaries have become a small policy language rather than a handful of `if / else` checks. And it is not rhetorical: schemas mark required fields and disable stray properties via `additional_properties = false`; `execpolicy/src/lib.rs` exports parser, `PolicyParser`, plus helpers like `blocking_append_allow_prefix_rule` and `blocking_append_network_rule`. Codex evaluates policy and also amends it in structured ways.

## 4.4 Runtime approvals versus policy language

Claude Code leans toward a runtime approval chain; Codex leans toward explicit policy language and parameterized approvals. Claude Code's ask/allow/deny is tightly coupled to the call site, deciding by context, tool type, user action, and session state — sensitive, but rules stay buried in runtime logic. Codex's exec-policy pulls rules outward as separately parsable and evaluable entities — better readable and portable, a natural fit for team governance; the cost is weight and real ongoing design work. Bluntly: shift manager making the call on site vs. a company that writes policy first and checks compliance second.

### Skeleton: two risk gates

```
// skeleton: Claude Code runtime approval  (src: src/hooks/useCanUseTool.tsx, StreamingToolExecutor.ts)
decision = hasPermissionsToUseTool(tool, input, ctx)  // allow | deny | ask
match decision:
    allow: schedule_with_concurrency_check(tool)       // isConcurrencySafe()
    deny:  reject(reason)                              // sticky
    ask:   route_to(coordinator | swarm | interactive)
interrupt_semantics = tool.interruptBehavior ∈ {cancel, block}

// skeleton: Codex exec-policy evaluation  (src: execpolicy/src/lib.rs, local_tool.rs)
policy = PolicyParser.parse(source)
for rule in policy.rules:
    eval = rule.evaluate(exec_command { cmd, workdir, shell, tty,
                                         yield_time_ms, max_output_tokens, login })
    if eval.matches: return Decision::{Allow | Deny | RequestPermissions}
return Decision::default
```

### Approval decision tree

```
tool_call
  ├─ schema validation fails    → deny (additional_properties=false blocks stray args)
  ├─ matches deny rule (prefix) → deny
  ├─ matches ask rule (net/esc) → request_permissions (explicit tool)
  ├─ no match + sandbox relaxed → allow (bounded by workdir / sandbox mode)
  └─ no match + sandbox strict  → ask
```

### Timeout and parameter thresholds

| Name | Purpose | Source |
|---|---|---|
| `yield_time_ms` | max ms a single exec may block | `local_tool.rs (exec_command)` |
| `max_output_tokens` | cap on tool output admitted into context | `local_tool.rs` |
| `additional_properties=false` | blocks model from injecting stray args | `local_tool.rs (schema)` |
| Bash subcommand cap | max compound subcommands per Bash call | `bashPermissions.ts` |

## 4.5 Sandbox and approval define the product

Sandbox, approval, and permission are not security accessories — for a coding agent they define what the product is. A system that lets the model run arbitrary commands in a user directory is an agent that transfers risk to the user, not just a "more powerful" one. Explicitly expressing sandbox mode, network access, approval policy, additional directories, state-store location, and MCP tool approvals is what delivers capability plus behavioral boundaries. Codex exposes these turn-level conditions in `thread.ts` as part of thread semantics; Claude Code pushes the boundary into runtime — tool handling, interrupts, permission hooks, Bash restrictions. One "executes while being watched," the other "declares the execution contract before starting."

## 4.6 MCP, external tools, and boundary migration

Both systems can attach more capabilities, but the difference remains. Claude Code weaves skills, hooks, permissions, and tool prompts into a situational governance chain so local rules ride the main loop. Codex pulls external capabilities into one unified tool system — MCP resources, dynamic tools, and tool discovery in `tools/src/lib.rs` expect extensions to become schema-defined, rule-governed tool objects rather than runtime understandings. Once the ecosystem grows, "how extensions obey the general rules" becomes the ballast: the team that thinks through boundary migration early keeps its extension ecosystem from degenerating into a junk closet.

## 4.7 Chapter conclusion

This chapter can be reduced to a hard sentence:

> Claude Code's tool governance depends more on runtime orchestration and situational approvals, while Codex's tool governance depends more on schemas, parameterized permissions, and an independent policy system.

The former is like an experienced foreman.

The latter is like a contractor with a compliance office and legal department.

If you look only at the fact that both can run commands, you miss the meaningful difference. The real question is who owns order before the tool starts moving.

The next chapter looks at a more grounded layer: skills, hooks, local rule files, and team institutions. Once a technical system has to enter a team, it eventually has to learn village law.
