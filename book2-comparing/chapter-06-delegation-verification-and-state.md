# 第 6 章 委派、验证与持久状态：谁来防止系统自己给自己打高分

## 6.1 多代理的真正问题是责任

一听多代理就想到效率提升，像听公司扩编——其实真正棘手的从来是多出来的责任怎么切。若同一系统既执行又总结又验证，还顺手给自己写评语，结论多半令人宽慰但不可靠："干得不错"。Claude Code 清醒地把 explore、execute、synthesis、verification 拆开，verify 是独立纪律而非礼貌动作——系统不愿让"完成"由执行代理自己宣布。Codex 也走这条路：`tools/src/lib.rs` 里 `create_spawn_agent_tool_v*`、`create_wait_agent_tool_v*`、`create_send_message_tool`、`create_close_agent_tool_v*` 说明委派是正式工具能力，不是黑魔法。

## 6.2 Claude Code：多代理服务于运行时职责分区

Claude Code 的多代理围绕主循环和任务推进展开——主代理不该什么都自己干，尤其不该既干活又验收。因此多代理主要用于：探索外包、执行分流、synthesis 汇总、verification 独立复核。这很符合它的强项在运行时编排——多代理被纳入"当前这轮怎么推进"的治理框架，而不是先有 agent platform 再往里塞任务。

## 6.3 Codex：多代理服务于显式工具化协作

Codex 把委派定义成工具接口，多代理更像正式子系统。两个直接影响：委派动作更易被记录、审计和组合（显式工具调用，不是 runtime 魔法）；协作更易与线程、状态和审批体系对齐（thread/rollout/policy 本就一等公民）。`agent_tool.rs` 里 `spawn_agent`、`send_input`、`wait_agent`、`close_agent` 各有 schema：`send_input` 区分 `interrupt=true` 立即打断和默认排队；`wait_agent` 有 default/min/max timeout；`close_agent` 连 open descendants 一起关闭——抢占、等待、收尾都是协议字段。适合做成平台能力，不见得更灵巧但更易长期维护。

## 6.4 持久状态让验证不只是礼仪

验证流于形式的一个主因是系统没有足够好的状态承接——上一步干了什么、为什么、哪些工具动过、哪些文件变过，若只在执行代理脑子里，验证就容易沦为貌似认真实则缺材料的表演。Claude Code 让会话状态、工具结果和恢复分支在 runtime 里连续可见，配合独立验证纪律降低自我美化。Codex 通过 thread、rollout、message history、state DB bridge 给验证提供更清楚的材料基础。二者并不冲突——前者补执行者过于沉浸现场的问题，后者补系统协作必须留下结构化证据的问题。

## 6.5 对恢复与收尾的不同态度

Claude Code 很在乎 task cleanup、父子 abort 传播、subagent lifecycle hook——在它的世界里，多代理首先是运行时现场的一部分，出问题必须能及时收口。Codex 则把代理生命周期纳入显式状态管理和调用协议：不只关心"子代理死没死"，还关心"委派行为作为系统事件该如何留存"。前者像现场总工，担心人散场后地上还留坑；后者像带项目管理系统的组织者，担心每个协作动作是否进入记录体系。

### 骨架：Codex 代理委派协议 (skeleton)

```
// 骨架: agent_tool.rs spawn/wait/send/close
handle = spawn_agent { role, prompt, timeout, inherit_approval }
for msg in updates:
    send_input(handle, msg, interrupt ∈ {true, false})  // true=立即打断, false=排队
result = wait_agent(handle, timeout ∈ [min, default, max])
close_agent(handle, cascade=true)                        // 连同 open descendants 一并关闭
```

### 孤儿与超时故障矩阵

| 事件顺序 | 前置状态 | 触发 | 下一步 | 阈值 |
|---|---|---|---|---|
| 父代理 abort | 子代理在飞 | parent.abort | cascade abort 传到 handle；写 rollout 事件 | — |
| `wait_agent` 超时 | 子代理未返回 | timeout ≥ max | 关闭 handle，返回 timeout 结果 | `wait_agent.max` |
| `send_input(interrupt=true)` | 子代理排队中 | 抢占 | 丢弃队列，注入新输入 | — |
| `close_agent` | 有 open descendants | 显式关闭 | 级联关闭所有后代 | `cascade=true` |
| 子代理崩溃 | — | 异常退出 | 返回 error，保留 thread 记录 | — |
| handle 泄漏 | 任务结束未 close | finalize | 强制 close + evict | 不允许悬挂句柄 |

## 6.6 本章结论

这一章的结论不难写：

> Claude Code 的多代理设计更强调运行时职责分离与现场收尾，Codex 的多代理设计更强调工具化委派、状态承接与可审计协作。

二者都试图避免系统自己给自己打高分。

只是 Claude Code 更靠角色分离和验证纪律。

Codex 更靠显式接口、线程状态和协作记录。

最后一章，我们把前面六章压成总判断，回答书名里的问题：究竟是殊途同归，还是根本不同种。
