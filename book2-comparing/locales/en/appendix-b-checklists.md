# Appendix B Checklists: How to Tell Whether Your Harness Resembles Claude Code, Codex, or an Unfinished Prototype

If comparison cannot be reduced into checklists, what remains is usually a set of well-phrased but hard-to-use conclusions. This appendix compresses the previous chapters into questions a team can actually discuss.

## B.1 Control-plane checklist (invariants)

```
assert every instruction has {source, type, precedence}        # fragments are identifiable
assert prompt separates control plane from output style        # tone ≠ order
assert local-rule scope (CLAUDE.md / AGENTS.md) explicitly labeled
assert team-rule changes land via diff                         # not oral agreement
```
If these cannot be answered, the control plane is still at "good enough to use" rather than "good enough to govern."

## B.2 Continuity checklist (invariants)

```
assert continuity sovereignty ∈ {main loop, thread+rollout+state}  # pick one explicitly
assert interrupt ⇒ tool_result closed (synthetic fallback counts)
assert long session has compact / truncation / recovery trio
assert thread.id / session indexing / persisted state = first-class concepts
```
If long sessions rely on the model to "remember," you do not need the rest of the evaluation.

## B.3 Tool and approval checklist (invariants)

```
assert tool = schema-typed interface, additional_properties=false
assert approval policy independently evaluable (not buried in code if/else)
assert high-risk tools (Bash etc) get dedicated governance       # not flat treatment
assert {workdir, network, sandbox, approval} explicitly expressible
```
If the only answer is "we also have permission controls," the permission system has not been designed.

## B.4 Local governance checklist (invariants)

```
assert local rules layerable by {directory, team, task type}
assert skill = reusable institutional slice, not long prompt    # has version / source
assert hooks attach to explicit lifecycle events (pre/post/session_start/stop)
assert {skill, rule, hook} carry {version, source, trigger boundary}
```

## B.5 Multi-agent and verification checklist (invariants)

```
assert multi-agent's first purpose is responsibility split; parallelism is a bonus  # else it is parallelized disorder
assert independent verifier exists (verifier ≠ implementer)
assert delegation = explicit tool or explicit state event, not runtime magic
assert child-agent {failure, timeout, cancel} ⇒ named cleanup owner
```

## B.6 Which kind of system are you closer to?

Signals that you are closer to Claude Code:

- you care most about query loop, tool orchestration, interrupts, compaction, and recovery
- you are good at getting rules into the live session quickly
- you care primarily about how an agent keeps running inside complex tasks

Signals that you are closer to Codex:

- you care most about instruction fragments, tool schemas, approval policy, thread / rollout / state
- you are good at turning local rules into structured assets
- you care primarily about how an agent is governed durably inside an organization

Signals that you are closer to an unfinished prototype:

- you can recite vocabulary from both sides, but cannot explain who owns order
- you have many capability entry points, but no clear recovery path
- you have many rule texts, but no scope or precedence
- you have multi-agent execution, but no separation of responsibility and no closure mechanism

## B.7 Six final questions

If time is short, ask only these six:

- Who owns the final control, the model or the harness?
- Does continuity live mainly in the loop, or in threads and state?
- Before tools act, who stops the last dangerous move?
- How do local rules enter the system, and how are they layered?
- Who owns verification, and how is it kept independent?
- After something goes wrong, what evidence lets the team trace the path back?

Once these six questions are asked, the system's political family usually reveals itself.

## B.8 Thresholds & orderings quick reference

| Name | Value | Purpose | Source |
|---|---|---|---|
| `MAX_ENTRYPOINT_LINES` | 200 | entry file line cap | Book 1 ch5 / `memdir/memdir.ts` |
| `MAX_SECTION_LENGTH` | 2_000 | session-memory per-section cap | `SessionMemory/prompts.ts` |
| `MAX_TOTAL_SESSION_MEMORY_TOKENS` | 12_000 | session-memory total budget | `SessionMemory/prompts.ts` |
| `AUTOCOMPACT_BUFFER_TOKENS` | 13_000 | autocompact warning buffer | `compact/autoCompact.ts` |
| `MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES` | 3 | breaker threshold | `compact/autoCompact.ts` |
| `yield_time_ms` | per-tool | max ms a single exec may block | `local_tool.rs` |
| `wait_agent.timeout` | min/default/max | child-agent wait window | `agent_tool.rs` |
| Bash subcommand cap | implicit | max compound subcommands per call | `bashPermissions.ts` |

Event orderings:

- session_start → user_prompt_submit → pre_tool_use → tool exec → post_tool_use → stop
- spawn_agent → send_input* → wait_agent → close_agent (cascades to descendants)
- PTL → collapse → reactive compact → if still PTL, surface error (no further loop)
