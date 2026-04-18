# 附录 B 检查清单：如何判断你的 Harness 更像 Claude Code、Codex，还是半成品

比较如果不能落成检查清单，最后很容易只剩一些表述完整却难落地的判断。下面这份附录，就是把前面几章压成团队可直接讨论的清单。

## B.1 控制面清单 (invariants)

```
assert every instruction has {source, type, precedence}        # fragment 可识别
assert prompt 中 control-plane 与 output-style 明确区分         # 文风不等于秩序
assert 本地规则的作用域（CLAUDE.md / AGENTS.md）显式标注
assert team 规则变更可通过 diff 追踪                           # 非口头约定
```
答不清这些，说明控制面还停留在"能用就行"。

## B.2 连续性清单 (invariants)

```
assert 连续性主权 ∈ {main loop, thread+rollout+state}          # 明确归属
assert 中断 ⇒ tool_result 同步闭账（synthetic 兜底也算）
assert 长会话有 compact / truncation / recovery 三件套
assert thread.id / 会话索引 / 状态落地为系统一等概念
```
长会话若主要靠模型自己"记得住"，基本不必再看。

## B.3 工具与审批清单 (invariants)

```
assert tool = schema 化接口，additional_properties=false
assert approval policy 可独立评估（不混在代码 if/else 里）
assert 危险工具（Bash 等）有专门治理                           # 非一视同仁
assert {workdir, network, sandbox, approval} 可显式表达
```
系统只能回答"我们也有权限控制"，基本等于没设计权限。

## B.4 本地治理清单 (invariants)

```
assert 本地规则可按 {目录, 团队, 任务类型} 分层
assert skill 视为可复用制度切片，非长 prompt                   # 有版本/来源
assert hook 挂在明确生命周期事件（pre/post/session_start/stop）
assert {skill, rule, hook} 具备 {version, source, trigger boundary}
```

## B.5 多代理与验证清单 (invariants)

```
assert 多代理的第一目的是职责分离，并行是附带           # 否则是把混乱并行化
assert 存在独立 verifier（verifier ≠ implementer）
assert 委派为显式工具或显式状态事件，非 runtime 魔法
assert 子代理 {failure, timeout, cancel} ⇒ 明确 cleanup owner
```

## B.6 你更像哪一类系统

更像 Claude Code 的信号：

- 你最重视 query loop、工具编排、中断、compact 与恢复
- 你擅长让规则快速进入现场会话
- 你更关心 agent 如何在复杂任务里持续运行

更像 Codex 的信号：

- 你最重视 instruction fragment、tool schema、approval policy、thread / rollout / state
- 你擅长把本地规则做成结构化资产
- 你更关心 agent 如何在组织里被长期治理

更像半成品的信号：

- 两边的名词都说得出来，但谁负责秩序说不清
- 有很多能力入口，但没有清楚的恢复路径
- 有很多规则文本，但没有作用域和优先级
- 有多代理，但没有责任分离和收尾机制

## B.7 最后六问

要是时间不够，只问这六句：

- 谁拥有最终控制权，模型还是 harness
- 连续性主要住在 loop 里，还是住在线程和状态里
- 工具动手前，谁来拦最后一道
- 本地规则怎么进入系统，怎么分层
- 验证由谁负责，如何独立
- 出事以后，团队靠什么追溯

这六句问下来，系统大概属于哪一派，通常也就露出来了。

## B.8 阈值与顺序速查 (thresholds & orderings)

| 名称 | 值 | 作用 | 源引用 |
|---|---|---|---|
| `MAX_ENTRYPOINT_LINES` | 200 | 入口文件行数上限 | 书一 ch5 / `memdir/memdir.ts` |
| `MAX_SECTION_LENGTH` | 2_000 | session memory 单节上限 | `SessionMemory/prompts.ts` |
| `MAX_TOTAL_SESSION_MEMORY_TOKENS` | 12_000 | 会话记忆总预算 | `SessionMemory/prompts.ts` |
| `AUTOCOMPACT_BUFFER_TOKENS` | 13_000 | autocompact 警戒缓冲 | `compact/autoCompact.ts` |
| `MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES` | 3 | 熔断阈值 | `compact/autoCompact.ts` |
| `yield_time_ms` | per-tool | 单次 exec 阻塞毫秒上限 | `local_tool.rs` |
| `wait_agent.timeout` | min/default/max | 子代理等待窗口 | `agent_tool.rs` |
| Bash 子命令数 cap | implicit | 复合子命令上限 | `bashPermissions.ts` |

事件顺序速查：

- session_start → user_prompt_submit → pre_tool_use → tool exec → post_tool_use → stop
- spawn_agent → send_input* → wait_agent → close_agent（cascade 关闭后代）
- PTL → collapse → reactive compact → 若仍 PTL 则 surface 错误（不再循环）
