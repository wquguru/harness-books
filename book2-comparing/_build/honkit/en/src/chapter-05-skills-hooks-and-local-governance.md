# Chapter 5 Skills, Hooks, and Local Rules: How a System Learns to Respect Village Law

![Local Governance Comparison](diagrams/diag-04-local-governance-comparison.png)

## 5.1 Any deployable agent becomes local

Any general-purpose coding agent that starts doing real work for a team eventually collides with the same fact: companies have their own rules, repositories have their own rules, directories have their own rules, and people have their own peculiar habits. If a system cannot absorb those local institutions, it remains trapped in demo environments.

Both Claude Code and Codex offer answers. They simply point in different directions.

## 5.2 Claude Code: local institutions as field memory

Much of Claude Code's localizing capacity lands in:

- `CLAUDE.md`
- skills
- hooks
- session memory

Together these feel strongly like accumulated field experience:

- `CLAUDE.md` tells the system what counts as common sense in this repo, this directory, and this team
- skills package repeatable workflows
- hooks attach team governance to lifecycle points
- session memory prevents each turn from starting human life over from zero

What all four share is proximity to the task scene. The point is to get rules into the current session and into current execution rather than to establish one eternal organization-wide constitution first. Claude Code resembles an engineer willing to carry a notebook and copy down local custom wherever it goes.

That is highly practical. It fits environments where multiple projects, directories, and local constraints coexist. The downside is obvious too: without deliberate cleanup, knowledge expands as field patches.

## 5.3 Codex: local institutions as structured injection and event systems

Codex also has skills, local rules, and hooks, but the temperament is more institutional.

Start with skills. `codex-rs/skills/src/lib.rs` shows that system skills are installed into `CODEX_HOME/skills/.system` and tracked with hashes or fingerprints. That is revealing, because it means a skill in Codex is not merely text temporarily read into context. It is an installed, managed, versionable asset.

Then look at `AGENTS.md`. In Codex this does not merely mean "read a local note." It comes with ideas of scope and hierarchy. In other words, local rules are not only content. They carry positional relationships.

Finally, look at hooks. `hooks/src/engine/mod.rs` splits hook events explicitly into:

- `session_start`
- `pre_tool_use`
- `post_tool_use`
- `user_prompt_submit`
- `stop`

Each handler also carries structured information such as event name, matcher, timeout, status message, source path, and display order. This makes Codex hooks feel less like "drop in a callback wherever convenient" and more like a formal lifecycle event system.

## 5.4 Claude Code absorbs experience; Codex mounts institutions

Viewed side by side, the difference becomes very clear.

Claude Code's local governance is closer to continuously absorbing field experience into the neighborhood of the main loop. It is strong at making the agent learn quickly how things are done here.

Codex's local governance is closer to mounting local rules onto an explicit control plane and lifecycle system. It is strong at making rules not only readable but also categorized, ordered, installed, and triggered.

That produces two different team feels.

Claude Code's team feel is like an old employee who knows the floor and can read the room.

Codex's team feel is like a newcomer with strong institutional instincts: first post the rules, then start coordinating the work.

## 5.5 Different consequences for organizational reproducibility

This difference matters most when an organization tries to reproduce itself.

If a system relies mainly on injected field experience, it adapts faster to a new repository and survives more easily in dense local context. But when it spreads to many teams, it usually requires extra editorial work, otherwise everyone writes their own `CLAUDE.md`, invents their own skills, and the organization starts printing its own textbooks by province.

If a system relies mainly on structured injection and lifecycle mounting, it has greater expansion potential. Rules are easier to distribute consistently, version, and audit. The price is learning cost: the team must first accept more explicit institution.

It is a classic engineering tradeoff:

- the closer you stay to the scene, the more elastic the system becomes
- the more institutionalized you become, the easier you are to reproduce

Neither path guarantees happiness. The real determinant is which kind of stability the team actually needs.

## 5.6 Chapter conclusion

This chapter can be summarized as:

> Claude Code tends to turn local governance into field memory and runtime injection, while Codex tends to turn local governance into structured assets and lifecycle event systems.

That is not just another way of saying "both support skills and hooks."

The difference is that Claude Code asks, "How do we make the agent work here more like a local?" while Codex asks, "How do we make local rules enter a governable institutional framework?"

The next chapter moves into a higher-risk layer: multi-agent work, verification, persistent state, and recovery. Once several agents begin working at once, rules alone are not enough; responsibility has to be partitioned too.
