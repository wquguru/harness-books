# Appendix C Source Map: Which Files Ground Each Chapter

This book is not a full source walkthrough, but it is source-grounded. This appendix maps each chapter to its primary supporting files.

This is not a complete index. It lists only files directly relevant to the book's arguments.

One copyright boundary note: this map is for citing analytical basis, not for promising source-text reproduction. It preserves necessary engineering references, module positioning, and structural analysis, without shipping source copies or long implementation excerpts.

## C.1 Chapter 1 Why Harness Engineering Matters

Core files:

- `src/constants/prompts.ts`
- `src/utils/systemPrompt.ts`
- `src/query.ts`
- `src/services/tools/toolOrchestration.ts`
- `src/tools/BashTool/prompt.ts`

Primary argument basis:

- prompt as control-plane component rather than personality packaging
- query loop as agent-system skeleton
- tool and Bash risk profiles as proof harness is necessary

## C.2 Chapter 2 Prompt Is the Control Plane, Not Persona Decoration

Core files:

- `src/constants/prompts.ts`
- `src/utils/systemPrompt.ts`
- `src/utils/claudemd.ts`
- `src/memdir/memdir.ts`
- `src/constants/systemPromptSections.ts`
- `src/main.tsx`

Primary argument basis:

- layered system-prompt assembly
- `CLAUDE.md` and memory as control-plane inputs
- dynamic reminders and context injection

## C.3 Chapter 3 Query Loop: The Heartbeat of an Agent System

Core files:

- `src/query.ts`
- `src/QueryEngine.ts`

Primary argument basis:

- state-machine properties of query loop
- input governance before model invocation
- streaming event consumption and recovery branches
- QueryEngine ownership of conversation lifecycle

## C.4 Chapter 4 Tools, Permissions, and Interrupts

Core files:

- `src/services/tools/toolOrchestration.ts`
- `src/services/tools/toolExecution.ts`
- `src/services/tools/StreamingToolExecutor.ts`
- `src/hooks/useCanUseTool.tsx`
- `src/utils/permissions/PermissionResult.ts`
- `src/tools/BashTool/prompt.ts`
- `src/tools/BashTool/bashPermissions.ts`

Primary argument basis:

- concurrency safety and ordered context replay
- wrapped tool execution stack
- `allow / deny / ask` authorization semantics
- streaming-tool interruption and synthetic closure
- special high-pressure governance for Bash

## C.5 Chapter 5 Context Governance: Memory, CLAUDE.md, and Compact

Core files:

- `src/utils/claudemd.ts`
- `src/memdir/memdir.ts`
- `src/services/SessionMemory/prompts.ts`
- `src/services/compact/autoCompact.ts`
- `src/services/compact/compact.ts`
- `src/query.ts`

Primary argument basis:

- layered discovery and loading of `CLAUDE.md`
- `MEMORY.md` as entry index, not content warehouse
- structured continuity in session memory
- autocompact thresholds, buffers, and circuit breaker
- post-compact reconstruction of working semantics

## C.6 Chapter 6 Errors and Recovery

Core files:

- `src/query.ts`
- `src/services/compact/autoCompact.ts`
- `src/services/compact/compact.ts`
- `src/services/api/withRetry.ts`

Primary argument basis:

- withheld recoverable errors
- prompt-too-long handling via collapse drain and reactive compact
- `max_output_tokens` escalation and continuation strategy
- autocompact failure circuit breaking
- compaction self-recovery under PTL

## C.7 Chapter 7 Multi-Agent and Verification

Core files:

- `src/utils/forkedAgent.ts`
- `src/coordinator/coordinatorMode.ts`
- `src/tasks/LocalAgentTask/LocalAgentTask.tsx`
- `src/utils/hooks/hooksConfigManager.ts`
- `src/skills/bundled/verify.ts`
- `src/memdir/memoryTypes.ts`

Primary argument basis:

- cache-safe fork parameters and state isolation
- coordinator synthesis responsibility
- independent verification stage
- subagent lifecycle hooks
- task cleanup and parent-child abort propagation
- stale-memory verification discipline

## C.8 Chapter 8 Team Adoption

Core files:

- `src/utils/claudemd.ts`
- `src/tools/SkillTool/prompt.ts`
- `src/tools/SkillTool/SkillTool.ts`
- `src/utils/forkedAgent.ts`
- `src/utils/hooks/hooksConfigManager.ts`
- `src/main.tsx`

Primary argument basis:

- layered stability in team `CLAUDE.md`
- skills as institutional slices rather than prompt collections
- approval boundaries and allow-rule scoping
- lifecycle governance through hooks
- session startup behavior around instructions and skill loading

## C.9 Chapter 9 Ten Principles

Chapter 9 is not derived from one single file. It compresses cross-chapter structures jointly reflected in:

- prompt assembly
- query loop
- tool orchestration
- permission model
- context governance
- recovery system
- multi-agent orchestration
- team governance hooks
