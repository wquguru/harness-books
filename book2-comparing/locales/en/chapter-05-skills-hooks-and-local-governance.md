# Chapter 5 Skills, Hooks, and Local Rules: How a System Learns to Respect Village Law

![Local Governance Comparison](diagrams/diag-04-local-governance-comparison.png)

## 5.1 Any deployable agent becomes local

Any general-purpose coding agent that starts real work for a team collides with the same fact: companies, repositories, directories, and people all have their own rules and habits. A system that cannot absorb those local institutions stays trapped in demo environments. Claude Code and Codex both answer, in different directions.

## 5.2 Claude Code: local institutions as field memory

Localizing capacity lives in `CLAUDE.md`, skills, hooks, and session memory — together they feel like accumulated field experience: `CLAUDE.md` states what counts as common sense in this repo, directory, and team; skills package repeatable workflows; hooks attach team governance to lifecycle points; session memory keeps each turn from starting life over from zero. The common trait is proximity to the task scene — get rules into the current session and current execution, not a single eternal constitution first. Claude Code resembles an engineer who copies down local custom wherever it goes — highly practical across projects, directories, and local constraints, but without cleanup, knowledge expands as field patches.

## 5.3 Codex: local institutions as structured injection and event systems

Codex also has skills, local rules, and hooks, but the temperament is more institutional. Skills: `skills/src/lib.rs` installs system skills into `CODEX_HOME/skills/.system` and tracks them by fingerprint — a skill is an installed, managed, versionable asset, not text casually reread at startup. `install_system_skills()` reinstalls only when the marker fails to match. `AGENTS.md` carries scope and hierarchy rather than meaning "read a local note" — local rules carry positional relationships, not just content. Hooks: `hooks/src/engine/mod.rs` splits events into `session_start`, `pre_tool_use`, `post_tool_use`, `user_prompt_submit`, `stop`, and each handler has `event_name`, matcher, timeout, status message, source path, display order — more a formal lifecycle event system than a "drop a callback wherever convenient" pattern. The engine separates `preview_*` from `run_*` paths (preview which handlers fire before executing), and on Windows disables `codex_hooks` with an explicit warning when support is incomplete — hook capability is made explainable.

## 5.4 Claude Code absorbs experience; Codex mounts institutions

Claude Code's local governance continuously absorbs field experience into the neighborhood of the main loop — strong at making the agent learn quickly how things are done here. Codex mounts local rules onto an explicit control plane and lifecycle system — strong at making rules categorized, ordered, installed, and triggered. Team feel diverges: the former is an old employee who can read the room; the latter is a newcomer with strong institutional instincts who posts the rules first, then coordinates the work.

### Skeleton: Codex hook lifecycle

```
// skeleton: Codex hook engine  (src: hooks/src/engine/mod.rs)
events = [session_start, user_prompt_submit, pre_tool_use, post_tool_use, stop]
for ev in events:
    handlers = preview_handlers(ev, ctx)        // preview matches first
    emit(preview_event { ev, handlers })
    for h in handlers sorted by display_order:
        if match(h.matcher, ctx) and not timed_out(h.timeout):
            run_handler(h)                      // actually fire
        else:
            log_skip(h, reason)
on platform == windows: disable(codex_hooks); warn("incomplete support")
```

### Invariants: hook event ordering

```
assert session_start fires once per thread before any tool_use
assert pre_tool_use fires immediately before execution; post_tool_use after
assert stop fires exactly once per thread termination path
assert preview_* path never executes handlers; only run_* does
assert each handler has {event_name, matcher, timeout, source_path, display_order}
assert stable display_order ⇒ replayable ordering across runs
assert skill fingerprint mismatch ⇒ reinstall; match ⇒ skip  (skills/src/lib.rs)
```

## 5.5 Different consequences for organizational reproducibility

A system that relies on injected field experience adapts faster to new repositories and stays effective in dense local context. But when it spreads across teams, it usually needs editorial cleanup — otherwise everyone writes their own `CLAUDE.md` and invents their own skills, and the organization ends up printing textbooks by province. A system that relies on structured injection and lifecycle mounting has more expansion potential: rules are easier to distribute uniformly, version, and audit. The cost is learning: the team must accept more explicit institutions first. Classic tradeoff — closer to the scene gives elasticity, more institutionalized gives reproducibility. What decides the outcome is which stability the team actually needs.

## 5.6 Chapter conclusion

This chapter can be summarized as:

> Claude Code tends to turn local governance into field memory and runtime injection, while Codex tends to turn local governance into structured assets and lifecycle event systems.

That is not just another way of saying "both support skills and hooks."

The difference is that Claude Code asks, "How do we make the agent work here more like a local?" while Codex asks, "How do we make local rules enter a governable institutional framework?"

The next chapter moves into a higher-risk layer: multi-agent work, verification, persistent state, and recovery. Once several agents begin working at once, rules alone are not enough; responsibility has to be partitioned too.
