# 第 3 章 心跳放在哪：Query Loop 对照 Thread、Rollout 与 State

![连续性对比图](diagrams/diag-02-continuity-comparison.png)

## 3.1 代理系统的核心是连续性

把代理系统理解成“多轮聊天”，就像把数据库理解成“一个比较耐心的记事本”。不能说全错，但这种说法掩盖了真正的架构问题。

代理系统真正的难题，是连续性：

- 上一轮做了什么，这一轮怎么接
- 工具结果怎么回填
- 中断之后怎么收口
- 上下文太长以后怎么整理
- 失败时要重试、压缩、还是忠实汇报

这些问题决定系统是不是 agent，而不只是某个”支持工具调用的问答接口”。

Claude Code 与 Codex 在这里的差异，比任何功能对照都更有含金量。

## 3.2 Claude Code：把连续性压进主循环

Claude Code 的主轴很明显，就在 `query()` 和 `queryLoop()` 一带。它把很多关键问题都压进循环状态里处理：

- 当前消息序列
- tool use context
- compact 跟踪
- output token 恢复计数
- pending summary
- turn count
- transition

这意味着 Claude Code 对“代理如何活着”这个问题的回答，是运行时性的。连续性主要由 loop 维护。系统的骨架因此更接近一个不断自我校正的会话发动机，而非一个先有强外部状态模型、再由状态模型驱动执行的体系。

它的优势非常现实。因为很多会话里的真实麻烦，恰好都发生在 loop 里：工具返回的顺序、模型输出突然截断、prompt too long、history snip、microcompact、用户插话。Claude Code 不试图回避这些问题，而是把它们作为 loop 内部的合法状态来处理。

这种设计有一种很工程的粗粝感。它不优雅，但通常能活下来。

## 3.3 Codex：把连续性拆成线程、rollout 与状态桥

Codex 则显得更“账本化”。从 `core/src/lib.rs` 就可以看到，连续性并不只存在于一个巨大的循环里，它被分摊到：

- `codex_thread`
- `thread_manager`
- `rollout`
- `state_db_bridge`
- `state`
- `message_history`

再看 `sdk/typescript/src/thread.ts`，thread 是外部开发者可以直接理解和操作的一级概念。`Thread` 持有 `id`，可以 `runStreamed()`，也可以 `run()`；`thread.started` 会回填线程 ID；approval policy、working directory、sandbox mode、network access、additional directories 等 turn 级执行条件，都是和线程运行紧密耦合的显式参数。

这里最有意思的地方，是连续性已经不只是“循环还在继续”，而是“一个线程正在被一套更显式的状态结构持续记录和约束”。rollout 的存在尤其说明 Codex 很在乎回放、索引、持久化和会话外可见性。

这会让系统更接近一个真正的执行记录器，而不只是一个现场对话管理器。

## 3.4 差别在于状态安放的位置

需要说明一点：Claude Code 当然也有状态，Codex 当然也有循环。真正不同的，不在有没有，而在主权在哪。

Claude Code 把状态主权更多交给 query loop。换句话说，系统认为“会话怎么继续”是 runtime 核心问题，许多事情要在 loop 里直接解决。

Codex 则把状态主权更明确地交给 thread 和 rollout 结构。它认为连续性不该只是一段内部控制流的副产物，还应当是一套被线程和状态基础设施承接的显式事实。

这就是为什么看 `Thread` 那个 TypeScript SDK 文件，会觉得 Codex 的 thread 已经是产品概念，而不只是内部实现细节。开发者被允许直接围绕 thread 来思考 agent turn。

Claude Code 的 query loop 则更接近发动机室。你知道它重要，但用户不一定直接围着它组织所有心智模型。

## 3.5 对恢复与可审计性的影响

这种状态安放差异，会直接影响恢复和审计。

Claude Code 的恢复强项，在于它离现场近。因为很多问题就在 loop 内部被发现和修复，例如 reactive compact、token 上限恢复、工具中断处理。它不需要先把麻烦搬运到更高一层状态模型里，再考虑怎么回滚。

Codex 的恢复强项，则更可能体现在状态可追踪性。线程有 ID，rollout 有记录，state bridge 和 message history 提供了更清楚的外部结构。这使得系统更容易回答“上一轮到底发生了什么”，而不只是停留在一团运行时逻辑里的回想。

简单说：

- Claude Code 更接近现场救火队
- Codex 更接近带档案系统的调度中心

二者都重要。只是前者更擅长活下来，后者更擅长说清楚自己是怎么活下来的。

## 3.6 对产品和团队接口的影响

这种差异还会影响团队怎么接入系统。

如果系统主权在 loop，团队更容易沿着运行时问题组织工作：

- 哪些错误需要恢复
- 哪些动作应当中断
- compact 何时触发
- 工具结果如何串回主对话

如果系统主权在线程和状态结构，团队更容易沿着接口与治理组织工作：

- thread 的生命周期是什么
- rollout 要保留哪些事件
- 状态库放在哪
- approval policy 如何成为 turn 级选项

因此 Claude Code 更接近先把 agent 做会，再把制度嵌进去；Codex 更接近先把制度接口立起来，再让 agent 在里面工作。

## 3.7 本章结论

这一章的结论可以写得明确一点：

> Claude Code 的连续性更多由 query loop 承担，Codex 的连续性更多由 thread、rollout 与 state 基础设施承担。

前者强调 runtime heartbeat。

后者强调 persisted session substrate。

这不是审美差异，这是系统权力分配。谁来拥有连续性，谁就定义了 harness 的中心。

下一章进入最硬的一层：工具、沙箱、审批和执行策略。到了这里，浪漫叙事一般都会自动退场，因为 shell 不大关心文风。
