# Appendix A Source Map: Which Files This Comparison Primarily Relies On

This appendix does one thing only: it states which files each chapter's judgments mainly rely on. It is not a directory of reproduced source, nor does it imply that the book ships source code together with its arguments.

The same boundary applies here:

- only the minimum engineering citation and module location is used
- the body of Claude Code or Codex implementation is not reproduced
- no long source transcription is provided

## A.1 Primary references on the Claude Code side

Overall control plane and prompt:

- `src/constants/prompts.ts`
- `src/utils/systemPrompt.ts`
- `src/utils/claudemd.ts`
- `src/memdir/memdir.ts`

Runtime loop and recovery:

- `src/query.ts`
- `src/QueryEngine.ts`
- `src/services/compact/autoCompact.ts`
- `src/services/compact/compact.ts`

Tools and permissions:

- `src/services/tools/toolOrchestration.ts`
- `src/services/tools/toolExecution.ts`
- `src/services/tools/StreamingToolExecutor.ts`
- `src/hooks/useCanUseTool.tsx`
- `src/tools/BashTool/prompt.ts`
- `src/tools/BashTool/bashPermissions.ts`

Multi-agent work, skills, and hooks:

- `src/utils/forkedAgent.ts`
- `src/coordinator/coordinatorMode.ts`
- `src/tasks/LocalAgentTask/LocalAgentTask.tsx`
- `src/tools/SkillTool/SkillTool.ts`
- `src/tools/SkillTool/prompt.ts`
- `src/utils/hooks/hooksConfigManager.ts`

## A.2 Primary references on the Codex side

Core module skeleton:

- `core/src/lib.rs`
- `tools/src/lib.rs`
- `skills/src/lib.rs`
- `hooks/src/lib.rs`

Instruction fragments and user injection:

- `instructions/src/lib.rs`
- `instructions/src/fragment.rs`
- `instructions/src/user_instructions.rs`

Tools, approvals, and execution policy:

- `tools/src/local_tool.rs`
- `execpolicy/src/lib.rs`
- `docs/execpolicy.md`
- `docs/sandbox.md`

Threads and state:

- `sdk/typescript/src/thread.ts`
- `core/src/lib.rs`

Hook event engine:

- `hooks/src/engine/mod.rs`

## A.3 Chapter-to-file mapping

Chapter 1:

- Claude Code's `query.ts`, `toolOrchestration.ts`
- Codex's `core/src/lib.rs`

Chapter 2:

- Claude Code's prompt assembly and `CLAUDE.md`
- Codex's `fragment.rs`, `user_instructions.rs`

Chapter 3:

- Claude Code's query loop and `QueryEngine`
- Codex's `thread.ts`, plus exposed modules around `thread_manager`, `rollout`, and `state_db_bridge`

Chapter 4:

- Claude Code's tool orchestration, Bash restrictions, and permission semantics
- Codex's `tools/src/lib.rs`, `local_tool.rs`, and `execpolicy/src/lib.rs`

Chapter 5:

- Claude Code's skill, hook, and memory system
- Codex's skills system and hook engine

Chapter 6:

- Claude Code's forked-agent design and verification discipline
- Codex's agent-tool set and its thread / rollout / state structures

Chapter 7:

- the cumulative judgment produced by the whole file set above
