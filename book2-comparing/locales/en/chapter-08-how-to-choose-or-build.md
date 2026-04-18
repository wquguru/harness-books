# Chapter 8 If You Need to Build Your Own Harness: Whom to Learn From, and What to Learn First

## 8.1 The real use of comparison is to avoid unnecessary detours

The least interesting ending is the consumerist one — choose A or B. Engineering systems are not headphones and do not ship through ranking charts. The useful question is: if you are about to build your own harness or refactor an existing agent, whose lessons should you learn first, and which part first. Claude Code and Codex offer two opening moves, not two final answers. Claude Code warns you not to make runtime problems sound too elegant — what drags systems down are the dirty jobs inside the query loop (closing tool-result ledgers, managing context inflation, recovering from interrupts, cleaning up subagents, keeping verification independent, preventing failure handling from looping on itself); treating those problems lightly gives a system that looks smart and feels lethal to operate. Codex warns you not to let the control layer dissolve into tacit understanding — instruction sources, tool schemas, approval policy, thread state, hook events, and skill assets become easier to govern the earlier they are made explicit; teams that keep asking runtime improvisation to replace institution eventually find their system resembles a shed built out of verbal agreement.

## 8.2 Three common team shapes, three opening directions

### Type one: the team already has an agent prototype, but long sessions frequently lose control

This kind of team usually needs Claude Code first.

Their problem is rarely that "the control plane is underdefined." Their problem is that the system cannot stay alive long enough. Typical symptoms include:

- context gets noisier over time
- tool-call chains break
- state becomes unclear after interruption
- no one closes subagent work cleanly
- verification degenerates into something people merely say

When those are your symptoms, the first thing to repair is runtime heartbeat, not more configuration. Stabilize the loop first. Institutional aesthetics can wait.

### Type two: the team already has many rules, but rule sources are scattered and permission boundaries are unclear

This kind of team usually needs Codex first.

Their problem is not that the live scene is impossible to survive. Their problem is that the system becomes harder and harder to govern. Common symptoms include:

- local rules are scattered everywhere
- no one can say which constraints live in prompt and which live in tools
- approval logic is mixed into code and hard to explain
- once multiple extensions are introduced, boundaries blur further

What these teams need is an explicit control layer. Turn instruction, tool, policy, and thread into explicit concepts before asking runtime to work inside them.

### Type three: there is no mature system yet and the team is starting from scratch

This is the most dangerous case, because it is easiest to envy the strengths of both sides at once and build a failed compromise.

A steadier route is usually:

- choose one primary contradiction
- design the main skeleton around that contradiction
- add the opposite side only at minimum level for now

If your first-phase risk is mainly "the model will behave recklessly," start with runtime discipline in the Claude Code sense.

If your first-phase risk is mainly "the team will lose institutional order," start with an explicit control layer in the Codex sense.

The worst move is trying to learn both sides fully at the same time and ending up with neither a stable main loop nor a clear control plane.

### Staged builder checklists for the three team shapes

```
# Type one: prototype exists, long sessions lose control (learn Claude Code first)
- [ ] Week 1: name the loop state set {messages, toolUseContext, compactTracking, turnCount}
- [ ] Week 1: every tool_use closed or synthetic-filled; abort path wired
- [ ] Week 2: context governance trio — memory / collapse / autocompact thresholds frozen in table
- [ ] Week 2: verification independent of implementation (verifier ≠ implementer)
- [ ] Week 3: subagent lifecycle SubagentStart/Stop observable
Gate: 24h continuous session without token breaker, orphan subagents, or tool_result leaks

# Type two: rules multiply, sources scattered, boundaries unclear (learn Codex first)
- [ ] Week 1: all instructions become fragments — marker, source, precedence all three declared
- [ ] Week 1: tools schema-typed with additional_properties=false
- [ ] Week 2: approval policy lifted into rules — deny/ask/allow independently evaluable
- [ ] Week 2: thread.id / rollout established; turn-level {approvalPolicy, sandboxMode} explicit
- [ ] Week 3: hooks split into pre/post/session_start/stop; skill assets installed by fingerprint
Gate: any rule change lands via PR diff alone, no runtime code edits required

# Type three: starting from scratch (pick one primary contradiction first)
- [ ] Week 1: declare primary contradiction — "model runs wild" or "team loses order"
- [ ] Week 1: define minimum permission model (deny/ask list for high-risk actions)
- [ ] Week 2: stand up skeleton on the primary side (loop OR fragment+thread, pick one)
- [ ] Week 3: bring the other side up to minimum-viable only (recovery path OR basic hooks)
- [ ] Week 4: land 1–2 skills/tools; prove the loop closes end to end
Gate: a new member can advance the checklist without verbal tutoring from the original author
```

## 8.3 What to learn from Claude Code, and what to learn from Codex

Prioritize Claude Code on: the state mind-set of the query loop, compaction and context governance, tool orchestration and interrupt handling, subagent lifecycle and verification independence, treating failure paths as main paths. Prioritize Codex on: instruction fragmentation, tool schemas, explicit expression of approval and policy, infrastructure for thread / rollout / state, hook events and skill-asset management. This is not compromise — it assumes you know what you are learning. The right reason to borrow something is that it repairs your weakness, not that someone else already built it.

<p>Carry the context-governance judgments from the first volume into third-party harnesses and a common but costly route becomes easy to identify. It does not separate context into units with different lifetimes, duties, and entry costs. Instead it packs bootstrap files, skill descriptions, identity settings, and workspace text into prompt as far as possible, then leans on truncation, compaction, and recovery chains once the window gets tight. These systems may still have memory, skills, compaction, even upper bounds — the governing axis remains "inject first, rescue later." Once context is organized mainly by piling up text, token waste is only the first cost; signal dilution is the deeper one: the model sees more, but is not necessarily clearer about which working semantics matter next.</p>

<p>Three routes in one line: Claude Code treats context as working memory (what must survive, what should be compressed); Codex treats context as structured units (source type, scope, state handoff); the OpenClaw family treats context as a prompt container (what else can still be packed in before the limit). That is why teams on the third route feel "more informed" at first, then complain about two things at once — tokens burn fast and quality does not climb as context fattens. It is solving how much can be inserted, not what must be preserved for continued work.</p>

<p><img src="diagrams/diag-05-context-governance-three-paths.png" alt="Three-path comparison of context governance" /></p>

## 8.4 One dangerous misconception: explicitness and flexibility are not natural enemies

System builders often rely on a lazy false opposition. Say "explicit control layer" and they imagine a heavy, slow, rigid system; say "runtime flexibility" and they imagine experience can carry the system now while structure is deferred. Neither instinct is intelligent. Explicitness is not inherently rigid, and flexibility is not inherently chaotic. The real question is whether you have defined clearly which things must be explicit and which can be left to field judgment. Claude Code's strength is not rejecting structure but knowing which troubles must be faced inside runtime; Codex's strength is not rejecting flexibility but knowing which boundaries will turn into endless disputes if not declared early. A good third harness does not average the two — it distinguishes which rules must be written down first, which judgments can remain in runtime, which state must persist, and which experience only needs to live inside session memory.

## 8.5 A practical order of operations for later builders

From zero, the recommended sequence: (1) high-risk actions and the minimum permission model; (2) main loop or thread lifecycle; (3) context governance and recovery paths; (4) skills, local rules, and hooks; (5) multi-agent, platform capability, and complex ecosystem. Not glamorous, but roughly the order in which incidents appear. In engineering, many design orders should follow the order of failure, not the order of demo aesthetics.

## 8.6 Chapter conclusion

This chapter only wants to leave one plain sentence behind:

> Learn from Claude Code mainly to understand how a system stays stable on site; learn from Codex mainly to understand how a system sustains order over time inside an organization.

Teams that learn only the first tend to become rich in experience and poor in institution.

Teams that learn only the second tend to produce elegant institutions and fragile field behavior.

The better move is not side-picking. It is deciding which bone your system must grow first according to its primary contradiction.
