# Harness Engineering：Claude Code 设计指南

![封面：Harness Engineering：Claude Code 设计指南](assets/cover-wxb.svg)

> 这本书关心的不是“模型会不会写代码”，而是“一个会写代码的模型被放进终端、仓库和团队流程以后，怎样才不会把系统带偏”。

这不是源码注释汇编，也不是产品功能介绍。它关注的是 Claude Code 如何把不稳定模型收束进可持续运行的工程秩序，让控制面、主循环、工具权限、上下文治理、恢复路径、多代理验证与团队制度长成一套完整骨架。

本书有三个阅读前提：

- 重点不在模型能力，而在 harness 如何组织约束与执行
- 重点不在函数逐条解释，而在运行时结构为什么必须这样长出来
- 重点不在个人技巧，而在这些结构怎样变成团队可以复用的制度

建议阅读顺序：

1. [前言](preface.md)
2. [第 1 章 为什么 Harness Engineering 不是 Prompt Engineering 的大号别名](chapter-01-why-harness-engineering.md)
3. [第 2 章 Prompt 不是输入框，而是控制面](chapter-02-prompt-is-control-plane.md)
4. [第 3 章 Query Loop：Agent 不是在答题，而是在持续接管工作流](chapter-03-query-loop-heartbeat.md)
5. [第 4 章 工具、权限与中断：怎样让模型动手，但不让它乱动手](chapter-04-tools-permissions-interrupts.md)
6. [第 5 章 上下文、记忆与压缩：怎样让系统长期工作而不是越聊越糊](chapter-05-context-memory-compact.md)
7. [第 6 章 错误与恢复：模型犯错不是异常，而是运行时常态](chapter-06-errors-and-recovery.md)
8. [第 7 章 多 Agent 与验证：不要让系统自己给自己当裁判](chapter-07-multi-agent-and-verification.md)
9. [第 8 章 团队落地：把个人技巧变成组织能力](chapter-08-team-landing-practices.md)
10. [第 9 章 十条原则：如何判断一个 AI 编程系统是不是工程系统](chapter-09-ten-principles.md)
11. [附录 A 检查清单](appendix-a-checklists.md)
12. [附录 B 图稿说明](appendix-b-diagram-notes.md)
13. [附录 C 源码地图](appendix-c-source-map.md)

如果只想先看总判断，可以直接跳到[第 9 章](chapter-09-ten-principles.md)。
