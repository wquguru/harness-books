# Chapter 2: Two control planes—dynamic prompt layers vs structured fragments

![Control plane comparison diagram](diagrams/diag-01-control-plane-comparison.png)

## 2.1 Control is not about tone

Treating prompts as a tone exercise is misleading. Claude Code and Codex both treat prompts as part of a behavioral control plane; the difference is in the mechanism that assembles them. Claude Code assembles dynamically — baseline text, append prompts, agent roles, `CLAUDE.md`, memory, and output styles layered at runtime according to task, tools, and team context; the art is priority, conflict resolution, and how each layer folds into the next. Codex treats instructions as structured fragments — `AGENTS.md`, user messages, and skills become chunks with clear markers, start/end boundaries, and serialization rules, turning instructions from free-form narrative into identifiable contextual units.

## 2.2 Claude Code's busy assembly line

System prompts here are not fixed documents but a production line: defaults form the foundation, append prompts drop requirements, agent prompts add roles, `CLAUDE.md` and memory inject local conditions. Flexibility lets one loop handle many scenarios, but ordering is critical — wrong ordering dilutes instructions or lets conflicts slip through. Runtime governance is therefore essential: control is constantly injected, overwritten, compressed, or pruned as tasks shift, and the loop recalculates "what matters now" each round. The guiding intuition: control follows the scene — it cannot freeze into static rules.

## 2.3 Codex's filing-room approach

Codex insists on identifiable fragments. Names like `ContextualUserFragmentDefinition` highlight type, boundaries, wrapping rules, and message transformation. AGENTS, skills, and user instructions are tagged contextual units the system can recognize and manipulate — stronger debuggability, and a path to more programmatic governance because every instruction already fits a type hierarchy.

And this is not merely elegant naming. `fragment.rs` defines constants like `AGENTS_MD_START_MARKER`, `AGENTS_MD_END_MARKER`, `SKILL_OPEN_TAG`, and `SKILL_CLOSE_TAG`; `ContextualUserFragmentDefinition::wrap()` and `into_message()` turn those fragments into `ResponseItem::Message`. In `user_instructions.rs`, `UserInstructions` serializes the directory into `# AGENTS.md instructions for ...`, while `SkillInstructions` carries explicit `<name>` and `<path>` fields. Codex tries hard not to make the model guess where a rule came from.

### Skeleton: two control-plane assemblies

```
// skeleton: Claude Code dynamic assembly  (src: constants/prompts.ts, utils/systemPrompt.ts, claudemd.ts)
system_prompt = concat(
    default_prompt,           // baseline
    append_prompt,            // overlay requirements
    agent_prompt,             // role
    claudemd_layers,          // team / personal / project
    memory_sections,          // session memory
    output_style              // expression discipline
)
// recomputed every loop: memory prefetch, collapse, microcompact, autocompact

// skeleton: Codex fragment assembly  (src: instructions/src/fragment.rs, user_instructions.rs)
for frag in [agents_md, skill, user_instructions]:
    body = ContextualUserFragmentDefinition::wrap(
        START_MARKER, content, END_MARKER,
        meta { source_dir, name, path }
    )
    msg  = frag.into_message()              // -> ResponseItem::Message
    thread.append(msg)
```

### Invariants

```
assert every fragment has matching (START_MARKER, END_MARKER)   # markers paired
assert fragment.source ∈ {AGENTS_MD, SKILL, USER}              # type is identifiable
assert precedence(project) > precedence(team) > precedence(default)  # monotonic priority
assert claudemd_layers overlay order = team → personal → project  # later overrides earlier
assert child_agents_md enabled ⇒ append scope/precedence notes  # scope is explicit
```

## 2.4 CLAUDE.md vs AGENTS.md

`CLAUDE.md` is a local bulletin board: close to the task directory, paired with memory and skills, good for registering common sense, taboos, and local rules. `AGENTS.md` is pulled into Codex's hierarchy discussion — `docs/agents_md.md` says that even when no `AGENTS.md` is present, enabling `child_agents_md` appends scope and precedence notes. Codex cares not just whether rules exist, but whether their applicability and inheritance are explicitly stated. Claude Code brings local rules into the conversation; Codex brings them into the institution.

## 2.5 The trade-offs

Runtime assembly is flexible but hard to formalize, leaning on the main loop and engineering judgment; once rules multiply, overlap and semantic dilution become real risks. Structured fragments are explicit but heavier: markers, types, serialization, and injection all need definitions, plus calls on what deserves first-class status. The former grows experience-driven control, the latter grows institutional control — one agile but under-declared, the other clear but carrying ongoing structural cost.

## 2.6 This chapter's conclusion

> Claude Code views prompts as dynamic runtime builds; Codex views instructions as identifiable fragments.

One feels like a production floor, the other like a bureaucracy. The right choice depends on whether your primary worry is volatile sessions or unclear rule sources. The next chapter goes deeper: does continuity live in the query loop, or in thread, rollout, and state infrastructure?
