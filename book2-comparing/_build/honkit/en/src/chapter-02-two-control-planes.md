# Chapter 2: Two control planes—dynamic prompt layers vs structured fragments

![Control plane comparison diagram](diagrams/diag-01-control-plane-comparison.png)

## 2.1 Control is not about tone

Talking about prompts as if it were just a tone exercise is misleading. Claude Code and Codex both treat prompts as parts of a behavioral control plane. The difference lies not in the copy but in the mechanisms that assemble and surface it.

Claude Code assembles prompts dynamically. Baseline text, append prompts, agent roles, `CLAUDE.md`, memory, and output styles are layered at runtime according to the task, tools, and team context. The art is in priority, conflict resolution, and how each layer folds into the next. The control plane is a living pipeline that must adapt every loop.

Codex treats instructions as structured fragments. `AGENTS.md`, user messages, and skills become chunks with clear markers, start and end boundaries, and serialization rules. Tools and instructions stop being free-form narrative and become identifiable contextual units. This gives the control plane traceability and the ability to grow more governance artifacts without losing clarity.

## 2.2 Claude Code’s busy assembly line

Claude Code’s system prompts are not fixed documents; they are a production line. Defaults provide the foundation; append prompts drop requirements; agent prompts add roles; `CLAUDE.md` and memory inject local conditions. This flexibility lets the same loop handle different scenarios, but it makes the order of assembly critical: wrong ordering can dilute instructions or let conflicts slip through.

Because of this, runtime governance is essential. Control is constantly injected, overwritten, compressed, or pruned when tasks shift. The query loop recalculates “what matters now” each round. Claude Code’s guiding intuition is: control has to follow the scene—it cannot be frozen into static rules.

## 2.3 Codex’s filing-room approach

Codex insists on identifiable fragments. Names like `ContextualUserFragmentDefinition` highlight type, boundaries, wrapping rules, and transformation into messages. AGENTS, skills, and user instructions are not just textual—they are tagged contextual units that the system can recognize and manipulate. This yields stronger debuggability and a path to more programmatic governance, because every instruction already fits into a type hierarchy.

## 2.4 CLAUDE.md vs AGENTS.md

The distinction between CLAUDE.md and AGENTS.md is revealing. Claude Code’s CLAUDE.md feels like a local bulletin board—an on-site rule set tailored to a directory or workspace. It is pragmatic, local, and mission-focused. Codex’s AGENTS.md, by contrast, names scope, priority, and inheritance. Even when `child_agents_md` is not present, Codex injects scoped instructions to clarify applicability. Claude Code brings local rules into the conversation; Codex brings local rules into the institution.

## 2.5 The trade-offs

Claude Code’s runtime assembly is flexible but hard to formalize. Fragmented instruction is explicit but structural. Claude Code builds experience-driven control; Codex builds institutional control. The former trades explicitness for agility; the latter trades simplicity for clarity and maintenance cost.

## 2.6 This chapter’s conclusion

Claude Code views prompts as dynamic runtime builds; Codex views instructions as identifiable fragments. One feels like a production floor; the other feels like a bureaucracy. The right choice depends on whether your primary worry is volatile sessions or unclear rule sources.
