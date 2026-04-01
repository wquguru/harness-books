# Harness Books

[![Read Online](https://img.shields.io/badge/Read%20Online-harness--books.agentway.dev-16a34a?style=flat-square&logo=googlechrome&logoColor=white)](https://harness-books.agentway.dev)
[![Continue on AgentWay](https://img.shields.io/badge/Continue%20on-AgentWay-22c55e?style=flat-square&logo=bookstack&logoColor=white)](https://agentway.dev)

<table>
  <tr>
    <td align="center" valign="top" width="50%">
      <a href="https://harness-books.agentway.dev/book1-claude-code/">
        <img src="./book1-claude-code/assets/cover-wxb.svg" alt="Harness Engineering：Claude Code 设计指南" width="280">
      </a>
      <br>
      <strong>Harness Engineering：Claude Code 设计指南</strong>
      <br>
      <a href="https://harness-books.agentway.dev/book1-claude-code/">在线阅读</a>
      <a href="https://harness-books.agentway.dev/book1-claude-code/exported/book1-claude-code.pdf">PDF下载</a>
    </td>
    <td align="center" valign="top" width="50%">
      <a href="https://harness-books.agentway.dev/book2-comparing/">
        <img src="./book2-comparing/assets/cover-wxb.svg" alt="Claude Code 和 Codex 的 Harness 设计哲学" width="280">
      </a>
      <br>
      <strong>Claude Code 和 Codex 的 Harness 设计哲学</strong>
      <br>
      <a href="https://harness-books.agentway.dev/book2-comparing/">在线阅读</a>
      <a href="https://harness-books.agentway.dev/book2-comparing/exported/book2-comparing.pdf">PDF下载</a>
    </td>
  </tr>
</table>

这个仓库里放着两本关于 Harness Engineering 的书。它们追问同一个工程问题：一个会写代码的模型进了终端、仓库、权限系统和团队流程，系统凭什么还能保持边界、连续性和后果控制。

English index terms: `Harness Engineering`, `Claude Code guide`, `Claude Code vs Codex`, `AI coding agent`, `control plane`, `query loop`, `agent recovery`, `agent verification`, `local governance`, `approval policy`.

- 第一本是 [book1-claude-code](https://harness-books.agentway.dev/book1-claude-code/)：`Harness Engineering：Claude Code 设计指南`
- 第二本是 [book2-comparing](https://harness-books.agentway.dev/book2-comparing/)：`Claude Code 和 Codex 的 Harness 设计哲学`

这两本书不打算把源码拆成零件逐条讲解。它们关心的是 harness 怎样组织约束与执行，怎样把一个本质上不稳定的模型，收束进可持续运行的工程秩序里。

这里讨论的是控制结构。Prompt 分层、Query Loop、权限判定、上下文治理、失败恢复、多 agent 验证、本地规则和团队制度，合在一起才构成 harness 的器官系统。工程里最怕的事，不是模型偶尔犯傻，而是系统对后果毫无准备。

## About AgentWay

[AgentWay](https://agentway.dev) 是这套内容的实践落点。两本书负责把 Harness 的控制结构讲清楚；`agentway.dev` 负责把这些判断继续压到学习路径、练习、项目和 agent PoC 上。

它更像这两本书的后半程：先用书把问题看明白，再去 AgentWay 把理解变成动作。你可以先免费注册，从基础路径开始；如果要进入更完整的进阶路线、练习和项目，再往更深的版本走。

## 核心判断

- Harness Engineering 讨论的是约束结构怎样组织执行。
- 一个会写代码的模型进入真实工程环境以后，主要问题不再是回答质量，而是行为后果。
- Prompt、工具、权限、状态、恢复、验证和制度，不是外围配件，而是同一套控制结构的不同器官。
- 比较不同 agent 系统，重点不该是功能表，而该是秩序被安放在哪一层。
- 一个团队如果不能把个人经验沉淀成可复用制度，就很难把 agent 变成稳定系统。

## 两本书，各自把问题逼到哪里

### 第一本：Claude Code 设计指南

第一本书拿 Claude Code 当观察对象，重点放在运行时骨架上。它关心的是，一套系统为什么最终必须长出控制面、Query Loop、工具权限、上下文治理、恢复路径、多 agent 验证和团队制度这些结构。

如果你更关心这些问题，建议先读第一本：

- 为什么 Harness Engineering 不是 Prompt Engineering 的放大版
- Prompt 为什么本质上是控制面，而不是聊天输入框
- 模型犯错为什么应该被视为运行时常态，而不是异常事件
- 多 Agent 和验证机制为什么不能混成一团
- 团队怎么把个人经验固化成可复用的工程制度

入口见 [book1-claude-code](https://harness-books.agentway.dev/book1-claude-code/)。

### 第二本：Claude Code 与 Codex 比较书

第二本书把 Claude Code 和 Codex 放在一起，关注的是两套 harness 各自把秩序安放在哪一层。有人更从运行时纪律出发，有人更从结构化控制层出发；系统都能运转，权力分配方式却并不一样。

如果你更关心选型、架构判断或自己做系统时该学谁，建议读第二本：

- Claude Code 和 Codex 在控制面设计上最大的分歧是什么
- Query Loop、Thread、Rollout、State 的职责边界怎么对齐来看
- 权限、沙箱、策略语言各自承担什么治理角色
- 技能、Hook、本地规则怎样把“组织习惯”写进系统
- 如果要自己做 harness，应该先学谁、先学哪一层

入口见 [book2-comparing](https://harness-books.agentway.dev/book2-comparing/)。

## 建议阅读路径

- 如果你想先建立完整框架，先读第一本，再读第二本。
- 如果你已经熟悉 agent coding 工具，想直接看架构分歧和选型判断，可以先读第二本。
- 如果你只关心结论，可以直接看第一本的“第 9 章 十条原则”和第二本的“第 7 章 殊途同归，还是各表一枝”。

前面这些段落讲的是主张，下面这份目录讲的是证据链。Harness 这种题目，最怕只剩口号，不见结构，所以两本书的章节顺序都尽量保留为一条完整的推理路径。

## Table Of Contents

### Book 1

- [封面与导读](./book1-claude-code/index.md)
- [序言 Harness、终端与工程约束](./book1-claude-code/preface.md)
- [第 1 章 为什么 Harness Engineering 不是 Prompt Engineering 的大号别名](./book1-claude-code/chapter-01-why-harness-engineering.md)
- [第 2 章 Prompt 不是输入框，而是控制面](./book1-claude-code/chapter-02-prompt-is-control-plane.md)
- [第 3 章 Query Loop：Agent 不是在答题，而是在持续接管工作流](./book1-claude-code/chapter-03-query-loop-heartbeat.md)
- [第 4 章 工具、权限与中断：怎样让模型动手，但不让它乱动手](./book1-claude-code/chapter-04-tools-permissions-interrupts.md)
- [第 5 章 上下文、记忆与压缩：怎样让系统长期工作而不是越聊越糊](./book1-claude-code/chapter-05-context-memory-compact.md)
- [第 6 章 错误与恢复：模型犯错不是异常，而是运行时常态](./book1-claude-code/chapter-06-errors-and-recovery.md)
- [第 7 章 多 Agent 与验证：不要让系统自己给自己当裁判](./book1-claude-code/chapter-07-multi-agent-and-verification.md)
- [第 8 章 团队落地：把个人技巧变成组织能力](./book1-claude-code/chapter-08-team-landing-practices.md)
- [第 9 章 十条原则：如何判断一个 AI 编程系统是不是工程系统](./book1-claude-code/chapter-09-ten-principles.md)
- [附录 A 检查清单](./book1-claude-code/appendix-a-checklists.md)
- [附录 B 图稿说明](./book1-claude-code/appendix-b-diagram-notes.md)
- [附录 C 源码地图](./book1-claude-code/appendix-c-source-map.md)

### Book 2

- [封面与导读](./book2-comparing/index.md)
- [阅读地图：如何理解第一本书与这本比较书](./book2-comparing/chapter-00-reading-map.md)
- [序言 两套 Harness，不必假装是同一匹马的附件](./book2-comparing/preface.md)
- [第 1 章 为什么要把 Claude Code 和 Codex 放在一起看](./book2-comparing/chapter-01-why-this-comparison.md)
- [第 2 章 两种控制面：Prompt 拼装与 Instruction Fragment](./book2-comparing/chapter-02-two-control-planes.md)
- [第 3 章 心跳放在哪：Query Loop 对照 Thread、Rollout 与 State](./book2-comparing/chapter-03-loop-thread-and-rollout.md)
- [第 4 章 工具、沙箱与策略语言：谁来阻止模型动手太快](./book2-comparing/chapter-04-tools-sandbox-and-exec-policy.md)
- [第 5 章 技能、Hook 与本地规则：系统如何学会守乡约](./book2-comparing/chapter-05-skills-hooks-and-local-governance.md)
- [第 6 章 委派、验证与持久状态：谁来防止系统自己给自己打高分](./book2-comparing/chapter-06-delegation-verification-and-state.md)
- [第 7 章 殊途同归，还是各表一枝](./book2-comparing/chapter-07-convergence-and-divergence.md)
- [第 8 章 如果你要自己做：该向谁学，先学什么](./book2-comparing/chapter-08-how-to-choose-or-build.md)
- [附录 A 源码地图：这套比较主要依据哪些文件](./book2-comparing/appendix-a-source-map.md)
- [附录 B 检查清单：如何判断你的 Harness 更像 Claude Code、Codex，还是半成品](./book2-comparing/appendix-b-checklists.md)

## 在线阅读

这个仓库支持把两本书发布到同一个 GitHub Pages 站点中。它们是两本独立的书，但共享同一个控制入口：

- `/` 是官网首页
- `/book1-claude-code/` 是第一本书
- `/book2-comparing/` 是第二本书

发布后，书内顶部会提供统一切换入口，并对移动端做响应式适配。

- 第一本 PDF：<https://harness-books.agentway.dev/book1-claude-code/exported/book1-claude-code.pdf>
- 第二本 PDF：<https://harness-books.agentway.dev/book2-comparing/exported/book2-comparing.pdf>

## Continue On AgentWay

如果这两本书帮你建立了判断，下一步就该把判断变成训练。可以继续去 [agentway.dev](https://agentway.dev)：

- 免费注册，先进入基础学习路径，确认自己对 Harness、agent runtime 和控制结构的理解有没有站稳。
- 继续往下，把这些概念压进练习、项目和 agent PoC，而不是只停在“看懂了”。
- 如果你要更完整的进阶路径、更多练习和更完整的项目训练，再解锁高级版本。

## 本地生成

如果你想在本地把这个“双书同站”的结构跑起来，步骤也不复杂。先分别构建两个 Honkit 站点：

```bash
cd book1-claude-code && npx --yes honkit build . _book
cd book2-comparing && npx --yes honkit build . _book
```

再组装统一的 Pages 静态站点：

```bash
python3 tools/book-kit/build_pages_site.py
```

最终输出目录为 `dist/`。
