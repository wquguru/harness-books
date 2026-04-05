# 附录 A 源码地图：这套比较主要依据哪些文件

这份附录只做一件事：说明各章判断主要基于哪些文件。它不是源码转载目录，也不意味着内容会提供相关源代码副本。

这里仍然保留同样的边界：

- 仅做必要的工程性引用和模块定位
- 不附带 Claude Code 或 Codex 的实现正文
- 不做大段源码转录

## A.1 Claude Code 侧主要依据

总体控制面与 prompt：

- `src/constants/prompts.ts`
- `src/utils/systemPrompt.ts`
- `src/utils/claudemd.ts`
- `src/memdir/memdir.ts`

运行时循环与恢复：

- `src/query.ts`
- `src/QueryEngine.ts`
- `src/services/compact/autoCompact.ts`
- `src/services/compact/compact.ts`

工具与权限：

- `src/services/tools/toolOrchestration.ts`
- `src/services/tools/toolExecution.ts`
- `src/services/tools/StreamingToolExecutor.ts`
- `src/hooks/useCanUseTool.tsx`
- `src/tools/BashTool/prompt.ts`
- `src/tools/BashTool/bashPermissions.ts`

多代理、skills、hooks：

- `src/utils/forkedAgent.ts`
- `src/coordinator/coordinatorMode.ts`
- `src/tasks/LocalAgentTask/LocalAgentTask.tsx`
- `src/tools/SkillTool/SkillTool.ts`
- `src/tools/SkillTool/prompt.ts`
- `src/utils/hooks/hooksConfigManager.ts`

## A.2 Codex 侧主要依据

核心模块骨架：

- `core/src/lib.rs`
- `tools/src/lib.rs`
- `skills/src/lib.rs`
- `hooks/src/lib.rs`

instruction fragment 与用户注入：

- `instructions/src/lib.rs`
- `instructions/src/fragment.rs`
- `instructions/src/user_instructions.rs`

工具、审批与执行策略：

- `tools/src/local_tool.rs`
- `execpolicy/src/lib.rs`
- `docs/execpolicy.md`
- `docs/sandbox.md`

线程与状态：

- `sdk/typescript/src/thread.ts`
- `core/src/lib.rs`

hook 事件引擎：

- `hooks/src/engine/mod.rs`

## A.3 各章对照

第 1 章：

- Claude Code 的 `query.ts`、`toolOrchestration.ts`
- Codex 的 `core/src/lib.rs`

第 2 章：

- Claude Code 的 prompt assembly 与 `CLAUDE.md`
- Codex 的 `fragment.rs`、`user_instructions.rs`

第 3 章：

- Claude Code 的 query loop / QueryEngine
- Codex 的 `thread.ts`、`thread_manager`、`rollout`、`state_db_bridge` 暴露模块

第 4 章：

- Claude Code 的工具编排、Bash 限制、权限语义
- Codex 的 `tools/src/lib.rs`、`local_tool.rs`、`execpolicy/src/lib.rs`

第 5 章：

- Claude Code 的 skill / hook / memory 体系
- Codex 的 skills 体系、hooks engine

第 6 章：

- Claude Code 的 forked agent / verification 纪律
- Codex 的 agent tool 集合、thread / rollout / state

第 7 章：

- 综合前述所有文件形成总判断
