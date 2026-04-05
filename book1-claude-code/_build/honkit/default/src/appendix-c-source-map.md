# 附录 C 源码地图：本书各章主要依据哪些文件

这本书虽然不是源码导读，但终究是基于源码写的。这里把每一章最主要的依据文件整理成一份地图。

这份地图不是完整索引，只列与本书论点直接相关的主文件。

这里也补一句版权边界：这份源码地图的作用，是说明分析依据来自哪些文件，而不是承诺随内容提供这些文件的正文内容。这里仅保留必要的工程性引用、模块定位和结构分析，不附源码副本，不做大段实现转载。

## C.1 第 1 章 为什么需要 Harness Engineering

核心文件：

- `src/constants/prompts.ts`
- `src/utils/systemPrompt.ts`
- `src/query.ts`
- `src/services/tools/toolOrchestration.ts`
- `src/tools/BashTool/prompt.ts`

本章主要论点来源：

- prompt 属于控制面组成部分，而不是人格包装
- query loop 才是代理系统骨架
- 工具和 Bash 风险说明 harness 的必要性

## C.2 第 2 章 Prompt 是控制面，不是人格装修

核心文件：

- `src/constants/prompts.ts`
- `src/utils/systemPrompt.ts`
- `src/utils/claudemd.ts`
- `src/memdir/memdir.ts`
- `src/constants/systemPromptSections.ts`
- `src/main.tsx`

本章主要论点来源：

- system prompt 的分层拼装
- `CLAUDE.md` 与 memory 作为控制面输入
- 动态系统提醒与上下文注入

## C.3 第 3 章 Query Loop：代理系统的心跳

核心文件：

- `src/query.ts`
- `src/QueryEngine.ts`

本章主要论点来源：

- query loop 的状态机性质
- 输入治理先于模型调用
- 流式事件消费与恢复分支
- QueryEngine 对 conversation lifecycle 的所有权

## C.4 第 4 章 工具、权限与中断

核心文件：

- `src/services/tools/toolOrchestration.ts`
- `src/services/tools/toolExecution.ts`
- `src/services/tools/StreamingToolExecutor.ts`
- `src/hooks/useCanUseTool.tsx`
- `src/utils/permissions/PermissionResult.ts`
- `src/tools/BashTool/prompt.ts`
- `src/tools/BashTool/bashPermissions.ts`

本章主要论点来源：

- 并发安全与上下文顺序回放
- 工具执行包裹层
- `allow / deny / ask` 权限语义
- streaming 工具中断与 synthetic result
- Bash 的特殊高压治理

## C.5 第 5 章 上下文治理：Memory、CLAUDE.md 与 Compact

核心文件：

- `src/utils/claudemd.ts`
- `src/memdir/memdir.ts`
- `src/services/SessionMemory/prompts.ts`
- `src/services/compact/autoCompact.ts`
- `src/services/compact/compact.ts`
- `src/query.ts`

本章主要论点来源：

- `CLAUDE.md` 的分层发现和加载
- `MEMORY.md` 作为入口索引而非正文仓库
- session memory 的结构化连续性
- autocompact 阈值、buffer 与 circuit breaker
- compact 后的工作语义重建

## C.6 第 6 章 错误与恢复

核心文件：

- `src/query.ts`
- `src/services/compact/autoCompact.ts`
- `src/services/compact/compact.ts`
- `src/services/api/withRetry.ts`

本章主要论点来源：

- withheld recoverable errors
- prompt-too-long 的 collapse drain 与 reactive compact
- `max_output_tokens` 的 escalate 与 resume
- autocompact failure 熔断
- compaction 自身 PTL 重试

## C.7 第 7 章 多代理与验证

核心文件：

- `src/utils/forkedAgent.ts`
- `src/coordinator/coordinatorMode.ts`
- `src/tasks/LocalAgentTask/LocalAgentTask.tsx`
- `src/utils/hooks/hooksConfigManager.ts`
- `src/skills/bundled/verify.ts`
- `src/memdir/memoryTypes.ts`

本章主要论点来源：

- forked agent 的 cache-safe 参数与状态隔离
- coordinator 的 synthesis 责任
- verification 独立成阶段
- subagent lifecycle hook
- task cleanup 与父子 abort 传播
- 对 stale memory 的 verify discipline

## C.8 第 8 章 团队落地

核心文件：

- `src/utils/claudemd.ts`
- `src/tools/SkillTool/prompt.ts`
- `src/tools/SkillTool/SkillTool.ts`
- `src/utils/forkedAgent.ts`
- `src/utils/hooks/hooksConfigManager.ts`
- `src/main.tsx`

本章主要论点来源：

- 团队 `CLAUDE.md` 的分层稳定性
- skill 作为制度切片而非 prompt 收藏夹
- approval 边界与 allow rules
- hook 生命周期治理
- session startup 与 instructions / skill loading

## C.9 第 9 章 十条原则

第 9 章并非直接从单一文件推出，它是对前面所有章节的压缩。它的依据，就是全书已经使用过的这些核心模块共同呈现出的系统结构：

- prompt assembly
- query loop
- tool orchestration
- permission model
- context governance
- recovery system
- multi-agent orchestration
- team governance hooks
