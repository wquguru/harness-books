# Claude Code 和 Codex 的 Harness 设计哲学

![封面：Claude Code 和 Codex 的 Harness 设计哲学](assets/cover-wxb.svg)

副标题：殊途同归，还是各表一枝

> “人活在世上，就是为了忍受摧残。”  
> 做 harness 也是。区别只在于，有人把摧残写进控制流，有人把摧残写进制度层。

这不是一份功能表，也不是一篇产品评测。它要比较的是两套系统如何承认模型不可靠，并把这种不可靠驯化成可持续工作的工程秩序，而不只是看“谁支持更多工具”。

本书有三个判断前提：

- Claude Code 和 Codex 比较的重点不在模型，而在 harness
- harness 是一种权力分配方式，而不是若干功能的拼盘
- 工程系统的差别，常常不在名词，而在秩序住在哪一层

建议阅读顺序：

1. [序言](preface.md)
2. [第 1 章 为什么要把 Claude Code 和 Codex 放在一起看](chapter-01-why-this-comparison.md)
3. [第 2 章 两种控制面：Prompt 拼装与 Instruction Fragment](chapter-02-two-control-planes.md)
4. [第 3 章 心跳放在哪：Query Loop 对照 Thread、Rollout 与 State](chapter-03-loop-thread-and-rollout.md)
5. [第 4 章 工具、沙箱与策略语言：谁来阻止模型动手太快](chapter-04-tools-sandbox-and-exec-policy.md)
6. [第 5 章 技能、Hook 与本地规则：系统如何学会守乡约](chapter-05-skills-hooks-and-local-governance.md)
7. [第 6 章 委派、验证与持久状态：谁来防止系统自己给自己打高分](chapter-06-delegation-verification-and-state.md)
8. [第 7 章 殊途同归，还是各表一枝](chapter-07-convergence-and-divergence.md)
9. [第 8 章 如果你要自己做：该向谁学，先学什么](chapter-08-how-to-choose-or-build.md)
10. [附录 A 源码地图](appendix-a-source-map.md)
11. [附录 B 检查清单](appendix-b-checklists.md)

如果只想先看总判断，可以直接跳到[第 7 章](chapter-07-convergence-and-divergence.md)。
