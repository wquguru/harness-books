# 附录 B 图示：把运行时骨架画出来

前面的章节一直在用文字解释运行时结构。文字当然能说清楚，但有些东西画成图以后，读者会更快意识到：Claude Code 是一套相当明确的状态机，不只是“一团 prompt 加几个工具”。

## B.1 图一：Claude Code 总体控制面

![Claude Code 总体控制面](diagrams/diag-01-claude-code-control-plane.png)

这张图不该画成“用户 -> 模型 -> 工具 -> 输出”那种幼儿读物，因为那种画法会把真正重要的器官都藏起来。更合理的理解方式，是把 Claude Code 分成五层：

1. 用户交互层
2. 控制面层
3. 执行循环层
4. 外部能力层
5. 持久化与观测层

图的重点是强调以下几点，而不是把模块都列全：

- 模型不在最上层，也不在最底层
- 模型只是 query loop 中的一环
- 真正把系统绑在一起的，是控制面和恢复面

## B.2 图二：Query Loop 主循环与恢复分支

![Query Loop 主循环](diagrams/diag-b02-01-query-loop-main.png)

![Query Loop 恢复分支](diagrams/diag-b02-02-query-loop-recovery-branches.png)

## B.3 图三：Tool Batch Ordering 与 StreamingToolExecutor

![Tool Batch Ordering](diagrams/diag-b03-01-tool-batch-ordering.png)

![StreamingToolExecutor Lifecycle](diagrams/diag-b03-02-streaming-tool-executor.png)

## B.4 图四：Context Sources 与 Compact Rebuild

![Context Sources And Budget](diagrams/diag-b04-01-context-sources-and-budget.png)

![Compact Rebuild Pipeline](diagrams/diag-b04-02-compact-rebuild-pipeline.png)

## B.5 图五：Coordinator-Worker Flow 与 Verification Separation

![Coordinator And Worker Flow](diagrams/diag-b05-01-coordinator-worker-flow.png)

![Verification Separation](diagrams/diag-b05-02-verification-separation.png)

## B.6 图六：团队治理图

![团队治理图](diagrams/diag-06-team-governance-map.png)
