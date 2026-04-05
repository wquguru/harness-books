# Appendix B Checklists: How to Tell Whether Your Harness Resembles Claude Code, Codex, or an Unfinished Prototype

If comparison cannot be reduced into checklists, what remains is usually a set of elegant but hard-to-use conclusions. This appendix compresses the previous chapters into questions a team can actually discuss.

## B.1 Control-plane checklist

Check these questions:

- Are local rules assembled as free text, or injected as typed fragments with bounded structure?
- Can the sources, scope, and precedence of instructions be explained clearly?
- Which parts of prompt are real control plane, and which are merely output style?
- Are team rules closer to `CLAUDE.md`-style field notes, or closer to `AGENTS.md`-style structured institutional entry points?

If these questions cannot be answered clearly, the control plane is probably still at the "good enough to use" stage rather than the "good enough to govern" stage.

## B.2 Continuity checklist

Check these questions:

- Is continuity maintained mainly by a main loop, or mainly by thread / rollout / state?
- After interruption, who guarantees closure for tool ledger, message sequence, and state handoff?
- When long sessions inflate, is there an explicit compact / truncation / recovery mechanism?
- Are thread IDs, session indexing, and persisted state first-class concepts?

If long sessions rely mostly on the model to "remember," there is usually no need to continue the evaluation.

## B.3 Tool and approval checklist

Check these questions:

- Are tools runtime objects, or schema-defined interfaces?
- Are approvals based mainly on field judgment, or on an explicit policy / rule system?
- Are dangerous tools specially governed, rather than treated like ordinary read operations?
- Can boundaries such as `workdir`, network, sandbox, and approval be expressed explicitly?

If the system can only answer "we also have permission controls," that usually means the permission system has not actually been designed.

## B.4 Local governance checklist

Check these questions:

- Can local rules be layered by directory, team, and task type?
- Can skills be treated as reusable slices of institution rather than merely long prompts?
- Are hooks attached to explicit lifecycle events?
- Do skills, rules, and hooks have version, origin, and trigger boundaries?

When team governance relies mainly on oral explanation, the system eventually learns to pretend it understands.

## B.5 Multi-agent and verification checklist

Check these questions:

- Is multi-agent used for parallelism, or for separation of responsibility?
- Is there an independent verification mechanism?
- Is delegation represented as explicit tools or explicit state events?
- When a child agent fails, times out, or is cancelled, who owns cleanup?

A multi-agent system that cannot verify independently and cannot close out cleanly is usually just parallelized disorder.

## B.6 Which kind of system are you closer to?

Signals that you are closer to Claude Code:

- you care most about query loop, tool orchestration, interrupts, compaction, and recovery
- you are good at getting rules into the live session quickly
- you care primarily about how an agent survives inside complex tasks

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
