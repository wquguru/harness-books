# Chapter 8 Team Adoption: Turning a Smart Tool into a Reusable Institution

## 8.1 If an expert can use it, that still does not mean a team can absorb it

Many AI tools look impressive in expert hands. Skilled users know when to patch context, when to watch the model closely, and when one sentence like "do not touch this directory" can keep it aligned temporarily. This easily creates an illusion: if power users can drive it smoothly, team rollout is just writing more best-practice docs.

Reality is usually different. Personal technique works precisely because it relies on continuous human supervision, background knowledge, and situational judgment. Once a team takes over, assumptions change. You can no longer assume everyone knows which commands are dangerous, which memories are stale, which skills fork tasks, which approvals can be skipped, and which approvals are mandatory.

So the key to team adoption is converting order that previously lived in expert heads into system-level institutions. Claude Code source is useful because it already hardens many "expert tricks" into deterministic loading order, permission semantics, hook lifecycle, and skill execution boundaries.

## 8.2 Team `CLAUDE.md` value is layered stability, not maximal content

Earlier chapters covered layered loading in `src/utils/claudemd.ts`. For team adoption, this stops being implementation trivia and becomes organization design.

A team using Claude Code seriously should first classify what belongs in managed, user, project, and local layers before writing many skills. If rules are not layered, every later skill, hook, and policy will conflict.

What belongs in team-level `CLAUDE.md`:

- repository-level hard constraints, such as forbidden directories or dangerous command classes
- unified validation policy, including what checks are required and what "looks passed" shortcuts are disallowed
- output discipline, such as findings-first review reporting
- collaboration constraints, such as do not overwrite user-unrequested changes or reset dirty worktrees without explicit instruction

What does not belong:

- rapidly changing task-specific details
- niche instructions relevant only to small subsets
- procedural details that should be encoded in skills

If `CLAUDE.md` becomes encyclopedia-like, it soon becomes unmaintainable, and the system learns a common bad habit: treating obsolete norms as active law.

So ideal team `CLAUDE.md` should be stable, clear, and low-dispute. It is foundational policy, not a dump site for temporary conversations.

## 8.3 Skills are reusable institutional slices

A common failure in team skill design is treating skills as longer prompt templates. Claude Code's SkillTool design clearly treats them differently.

In `src/tools/SkillTool/prompt.ts`, rules are strict: if user intent matches a skill, calling Skill tool is a blocking requirement. You cannot merely mention a skill without invoking it. Already-loaded skills should not be reloaded.

In `src/tools/SkillTool/SkillTool.ts` and `utils/forkedAgent.ts`, another fact emerges: skills often run in forked subagent contexts with independent token budget, context isolation, and sometimes explicit tool allowlists.

So in Claude Code, skills are not soft speech suggestions. They are closer to executable institutional slices: packaged knowledge, tool boundaries, workflow order, and verification requirements for a task class.

For teams, this is crucial. Only when skills are treated as institutional slices do teams consistently define:

- applicability boundaries
- allowed tool sets
- direct execution versus forked execution
- required artifacts and verification methods

Otherwise skills degrade into nicely named but semantically vague slogans no one can predict at runtime.

## 8.4 Approval defines team responsibility boundaries

Claude Code's permission system, from `useCanUseTool.tsx` to `PermissionResult.ts`, plus local `alwaysAllowRules` injection in `forkedAgent.ts`, all point to one team-level truth: one of the most important institutions is separating "can do" from "is authorized."

This is easy to underestimate in solo use because individuals can grant themselves ad hoc authority. Teams cannot. Once agents start:

- writing files
- mutating Git state
- accessing networks
- calling MCP endpoints
- persisting memory

every step is both technical action and responsibility action. Team policy must define:

- who approved
- why auto-pass is acceptable
- which scenarios must ask
- which rules hooks may override
- which rules are non-overridable

`hooksConfigManager.ts` even provides structured hook points such as `PermissionDenied`, `PreToolUse`, `UserPromptSubmit`, and `Notification`. You need not use all of them, but the design shows approval is an observable, extensible governance chain, not a UI popup.

In practice, approvals should be tiered by irreversibility and environment sensitivity, not by tool names. File reads, listing, and pure analysis can often be relaxed. Workspace mutation, configuration changes, Git push, external network operations, and production-touching resources should be stricter. Otherwise "automation" just scales incident blast radius.

## 8.5 Hook value is attaching institutions to lifecycle timing

When teams hear hooks, they often think "another fragile script layer." That concern is not wrong. Hooks do add complexity. Claude Code reminds us that hook value is not script itself, but lifecycle anchoring.

Events listed in `src/utils/hooks/hooksConfigManager.ts` are effectively a governance insertion map:

- `SubagentStart` / `SubagentStop`
- `PreCompact` / `PostCompact`
- `StopFailure`
- `InstructionsLoaded`
- `SessionStart`
- `SessionEnd`
- `DirectoryChange`
- `FileChanged`

Read together, their purpose is clear: make rules happen at correct moments. Examples:

- record observability when instruction files load
- add organization-level notes before/after compact
- run verification checks before subagent shutdown
- perform archival/reclamation actions at session end

This is stronger than dumping all policy into `CLAUDE.md`. Not every institution is static knowledge; some are timing actions. Static rules belong in `CLAUDE.md`; timing actions belong in hooks. Mixing these creates two bad outcomes: giant `CLAUDE.md`, or chaotic hook scripts.

## 8.6 Teams must standardize definition of verification, not just skill reuse

One frequent failure in coding-agent rollout is no shared definition of done. One person thinks "it runs" is enough, another accepts half-tested, another accepts plausible model explanation. In that environment, even smart systems learn to satisfy the weakest bar.

Claude Code repeatedly resists this slide. Coordinator mode separates verification into a dedicated phase; the `verify` skill does not just check that code exists, it asks to prove change works by running the app.

This matters for teams because skills can replicate process, but only verification definitions replicate quality. Without a shared "what counts as verified," each skill evolves its own local standard. The more capable the system gets, the less consistent team quality becomes.

So during rollout, instead of building many fancy skills first, define these three first:

- which task classes require independent verification
- what minimum actions verification must include
- whether failures may be marked "completed with known issues"

Without this clarity, automation only accelerates ambiguity.

## 8.7 Observability and auditability: institutional rollout depends on replayable traces

In personal use, memory and intuition can patch many holes. Teams cannot rely on that. What teams need is the ability to reconstruct why a step happened after something goes wrong.

In Claude Code implementation, logs, telemetry, task outputs, transcript paths, hook events, and agent notifications are distributed pieces of one system: replayable trace.

- skill invocation is recorded
- forked-agent usage is tracked
- subagent stop hooks receive transcript paths
- task systems track state transitions and output files
- compact boundaries mark context rewrite points

This implies a basic team principle: deploy not only capability, but explainability capability. Without it teams quickly hit an awkward state where everyone roughly knows what happened but no one can state why, who authorized it, or where drift started.

Institutions need auditability because only traceability lets teams keep trusting institutions after incidents.

## 8.8 The eighth principle extractable from source

This chapter can be compressed into one sentence:

> Team adoption succeeds when personal techniques are hardened into layered rules, executable skills, approval boundaries, and replayable lifecycle governance.

Claude Code source supports this jointly:

- layered loading in `claudemd.ts` implies rules must be tiered before injection
- SkillTool mandatory invocation semantics and forked execution imply skills are institutional slices, not prompt collections
- permission chains and local allow-rule injection tie approval directly to responsibility boundaries
- lifecycle events in `hooksConfigManager.ts` show institutions should attach to timing points, not only static docs
- subagent/task/transcript/output systems provide observability and cleanup paths

Portable team principles:

- define layered `CLAUDE.md` first, then pursue complex automation
- standardize verification definition before scaling skill count
- tier approvals by consequence and environment sensitivity, not by tool labels
- use hooks for lifecycle timing, not universal scripts
- any auto-executable process should be auditable, reclaimable, and explainable

The next chapter closes the book. Across all previous chapters, one judgment is repeatedly approached: the model is the most unstable component, so what we really design is how the system still produces reliable behavior under model unreliability.
