# Chapter 8 If You Need to Build Your Own Harness: Whom to Learn From, and What to Learn First

## 8.1 The real use of comparison is to avoid unnecessary detours

The least interesting ending for a comparison book is to push the reader back into a consumer posture: choose A or B. Engineering systems are not headphones. You do not buy them through ranking charts. The useful question is this: if you are about to build your own harness, or refactor the agent you already have, whose lessons should you learn first, and which part should you learn first?

Claude Code and Codex offer two opening moves, not two final answers.

Claude Code is useful because it warns you not to make runtime problems sound too elegant. What actually drags systems down are often the dirty jobs inside the query loop: closing tool-result ledgers, managing context inflation, recovering from interrupts, cleaning up subagents, keeping verification independent, and preventing failure handling from becoming a loop. Anyone who treats those problems lightly usually ends up with a system that looks smart and feels lethal to operate.

Codex is useful because it warns you not to let the control layer dissolve into tacit understanding. Instruction sources, tool schemas, approval policy, thread state, hook events, and skill assets become easier to govern the earlier they are made explicit. Teams that keep asking runtime improvisation to replace institution eventually discover that the whole system resembles a shed built out of verbal agreement.

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

## 8.3 What to learn from Claude Code, and what to learn from Codex

This is worth stating more bluntly.

Prioritize learning from Claude Code when it comes to:

- the state mind-set of the query loop
- compaction and context governance
- tool orchestration and interrupt handling
- subagent lifecycle and verification independence
- treating failure paths as main paths

Prioritize learning from Codex when it comes to:

- instruction fragmentation
- tool schemas
- explicit expression of approval and policy
- infrastructure for thread / rollout / state
- hook events and skill-asset management

This is not compromise for its own sake. It contains a hidden requirement: you must know what you are learning and why. The correct reason to borrow something is that it repairs your weakness, not merely that someone else already built it.

## 8.4 One dangerous misconception: explicitness and flexibility are not natural enemies

System builders often rely on a lazy false opposition.

Say "explicit control layer" and they imagine a system that must become heavy, slow, and rigid.

Say "runtime flexibility" and they imagine experience can carry the system now while structure is deferred to later.

Neither instinct is very intelligent. Explicitness is not inherently rigid, and flexibility is not inherently chaotic. The real question is whether you have defined clearly which things must be explicit and which things can be left to field judgment.

Claude Code's strength is not that it rejects structure. Its strength is that it knows which troubles must be faced directly inside runtime.

Codex's strength is not that it rejects flexibility. Its strength is that it knows which boundaries will turn into endless disputes if they are not declared early.

A good third harness should not average the two. It should distinguish:

- which rules must be written down first
- which judgments can remain in runtime
- which state must persist
- which experience only needs to survive inside session memory

## 8.5 A practical order of operations for later builders

If I were starting a harness from zero, I would recommend this sequence:

1. define high-risk actions and the minimum permission model
2. define the main loop or thread lifecycle
3. define context governance and recovery paths
4. define skills, local rules, and hooks
5. only then scale into multi-agent, platform capability, and a more complex ecosystem

This sequence is not glamorous, but it roughly follows the order in which incidents appear. In engineering, many design orders should be arranged according to the order of failure, not according to what looks nicest in a demo.

## 8.6 Chapter conclusion

This chapter only wants to leave one plain sentence behind:

> Learn from Claude Code mainly to understand how a system survives on site; learn from Codex mainly to understand how a system sustains order over time inside an organization.

Teams that learn only the first tend to become rich in experience and poor in institution.

Teams that learn only the second tend to produce elegant institutions and fragile field behavior.

The better move is not side-picking. It is deciding which bone your system must grow first according to its primary contradiction.
