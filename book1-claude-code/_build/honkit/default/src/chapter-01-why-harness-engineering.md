# 第 1 章 为什么需要 Harness Engineering

## 1.1 问题在于让模型别乱来

这些年，人们很喜欢谈智能体。这个词常常带着轻快的预期，仿佛只要模型会写几段代码、会调几个工具，就可以像见习工程师一样在终端里独立工作。可终端和文件系统都带有明确后果。一个会说话的概率分布，一旦能接触 shell、Git、网络和本地文件，问题就从”回答得不够好”变成”执行造成实际破坏”。

所以问题的重点，一直是怎样把它约束成一个可管理的系统。所谓 Harness Engineering，讨论的就是这件事。Harness 是一整套制度化的控制平面，用来处理一个很现实的问题：模型并不天然值得信任。

这个判断未必轻松，但通常有用。一个代理系统要进入真实工程环境，首先要承认自己的核心部件是不稳定的。忽视这一点，问题最后通常会在日志和事故记录里出现。

## 1.2 Claude Code 的第一层 Harness：受约束的会话系统

如果只看表面，Claude Code 像一个能和用户对话、还能顺手改代码的 CLI。可从实现上看，它一开始就没有把自己当成“裸模型接口”来设计，而是当成一个带有上下文边界、运行时状态和行为规约的会话系统。

这一点从 system prompt 的组织方式就能看出来。

- 在 `src/constants/prompts.ts:175` 开始，系统先定义身份和总任务。
- 在 `src/constants/prompts.ts:186` 开始，补上关于工具、权限、系统提醒和上下文压缩的系统级说明。
- 在 `src/constants/prompts.ts:199` 开始，再补上做任务时的工程约束，比如不要越权改动、不要把验证说成已经完成、不要为了省事发明抽象。

这里值得停一下。很多人谈 prompt，还停留在“你是一个什么样的助手”这种修辞层面。Claude Code 在实现上把 prompt 放进了运行时控制结构里，这些文字用来规定执行边界、失败行为和报告责任。

更重要的是，这个 prompt 采用分段拼装方式。在 `src/constants/prompts.ts:444` 的 `getSystemPrompt()` 里，静态部分和动态部分被明确拆开，memory、language、output style、MCP instructions、scratchpad 等内容按段注入。到了 `src/utils/systemPrompt.ts:28`，系统又把默认 prompt、自定义 prompt、agent prompt 和 append prompt 组织成一套优先级规则。

这说明了一个朴素的工程事实：一个真正可用的代理系统，不能依赖一段“万能提示词”解决所有问题。它必须把控制拆成层，把层次拆成职责。否则，新增提醒和禁令很快就会互相冲突，系统行为也会变得难以预测。

## 1.3 第二层 Harness：代理依赖持续循环

如果说 prompt 规定了它应该成为什么样的东西，那么 query loop 规定了它实际上如何运行。

Claude Code 的核心不在某个单独的 API 调用，而在 `src/query.ts:219` 开始的 `query()`，以及 `src/query.ts:241` 开始的 `queryLoop()`。这段实现里最重要的一点，是它明确承认代理系统依赖带状态的多轮执行。

在 `src/query.ts:268`，系统把 `messages`、`toolUseContext`、`autoCompactTracking`、`maxOutputTokensRecoveryCount`、`hasAttemptedReactiveCompact`、`pendingToolUseSummary`、`turnCount`、`transition` 等内容放进同一个跨迭代状态里。一个会话系统一旦这样设计，就等于正式承认：上一轮留下的问题会进入下一轮，系统必须有能力继续处理。

这是 Harness 思维的核心。真正的问题在于系统能不能在连续多轮里保持行为一致：

- 有没有预算概念
- 有没有恢复概念
- 有没有上下文膨胀后的自救机制
- 有没有在工具调用失败后继续推进任务的能力

缺少这些结构，所谓智能体就只是一个不稳定的执行者。

在 `src/query.ts:365` 往后，这个循环还会在每轮调用前处理消息裁剪、tool result budget、history snip、microcompact、context collapse、autocompact 等内容。实现细节虽然很多，但共同指向一点：Claude Code 在调用发生前就尽量把控制权收回到运行时一侧。

这也是为什么 Harness Engineering 不能被看作 prompt engineering 的附属品。前者关心状态机，后者关心措辞。措辞当然重要，但状态机决定系统行为最终由谁负责。

## 1.4 第三层 Harness：工具调用必须服从调度

一个模型如果只能输出文本，顶多让人觉得它有时说得太满。可一旦它能调用工具，系统风险就立刻从修辞风险变成执行风险。这时候最重要的问题是：谁决定工具怎么跑。

Claude Code 给出的答案很直接。运行时会根据工具属性决定并发还是串行。

在 `src/services/tools/toolOrchestration.ts:19` 的 `runTools()` 里，工具调用先经过 `partitionToolCalls()` 分组。到了 `src/services/tools/toolOrchestration.ts:91`，系统会读取工具 schema，并调用 `isConcurrencySafe()` 判断一个工具是否适合并发执行。能并发的归成一批，不能并发的按顺序一个个来。并发路径里，context modifier 会先缓存，再按原始 block 顺序回放，见 `src/services/tools/toolOrchestration.ts:31` 到 `:63`。

这件事很有代表性。它说明 Claude Code 没有把工具当成模型能力的自然延伸，而是当成需要调度纪律的受管执行单元。缺少调度纪律的工具系统，只会把模型的不稳定性放大到外部世界。

并发如果不受约束，就会扩大事故半径。Claude Code 在这里采取了偏保守的策略。在会碰到文件、终端和权限的场景里，这种保守通常更可靠。

## 1.5 第四层 Harness：最危险的工具，必须配最细的规矩

在所有工具里，Bash 最值得警惕。因为它几乎不受领域边界约束，可以直接接触文件、进程、网络和 Git 仓库，还会带上重定向、管道等复杂 shell 语义。一个系统如果对 Bash 过度信任，后果通常会很具体。

Claude Code 对 Bash 的态度，可以在 `src/tools/BashTool/prompt.ts:42` 往后看得很清楚。这里写了一整段操作规约，尤其是围绕 git 和 PR 的那部分：不要乱改 git config，不要跳过 hooks，不要随手 `git add .`，不要在 pre-commit 失败后用 `--amend` 把上一条提交也搭进去，不要在没有明确要求时提交，更不要默认 push。

写到这个地步，有人会觉得它过于细碎。但高风险接口通常就需要高密度约束。Bash 一旦进入真实工作流，很多规则都必须明确写出来。

Harness Engineering 的一个重要原则，就是把高风险能力包装成高约束能力。能力越强，控制越细。原因很简单：外部世界不会因为模型语气坚定，就自动原谅一次错误执行。

## 1.6 第五层 Harness：错误属于主路径的一部分

很多软件把失败路径看成例外，把成功路径看成正文。代理系统不能这样做。因为代理系统的失败不是偶发性的，它是一种稳定存在。模型会超 token，会触发 `prompt too long`，会撞上 `max_output_tokens`，还会遇到工具拒绝、用户打断、hook 阻塞、API 重试等各种中断。要是这些情况都只在最后用几个 `catch` 打发一下，那系统表面上在运行，实际上只是不断把麻烦往后滚。

Claude Code 在 query loop 里没有这样处理。光看 `src/query.ts:453` 往后关于 autocompact 的处理，以及 `src/query.ts:592` 往后对上下文上限和阻断逻辑的注释，就能看出它把失败当作会持续发生的结构性条件来处理。

这也是 Harness 和普通助手的重要差别之一。普通助手常见的设计逻辑是先回答，错了再道歉。Harness 更强调先约束，再执行；即使出错，也要按恢复路径处理，而不是靠临场发挥补救。

一个会道歉的系统，不一定成熟。一个知道何时不该开始、何时该重试、何时该中止、何时该准确汇报失败的系统，才更接近成熟。

## 1.7 从源码里可以提炼出的第一个原则

到这里，第一章其实只想说一件事：

> 代理系统的关键能力是约束执行。

Claude Code 的源码在几个关键位置都指向同一个结论：

- `constants/prompts.ts` 说明 prompt 是控制平面的一部分，而不是人格装饰
- `utils/systemPrompt.ts` 说明系统行为必须有清楚的分层优先级
- `query.ts` 说明代理运行依赖持续的循环状态，而不是单次问答
- `services/tools/toolOrchestration.ts` 说明工具调用必须服从调度纪律
- `tools/BashTool/prompt.ts` 说明高风险工具必须伴随高密度约束

把这些放在一起看，就会发现 Harness Engineering 并不神秘。它只是坚持几条常被忽视的工程常识：

- 模型会犯错
- 工具会扩大错误后果
- 上下文会膨胀
- 状态会污染下一轮
- 用户会打断你
- 失败会反复出现

既然如此，系统就不能靠“聪明”维持秩序，只能靠结构维持秩序。结构不像聪明那样显眼，但通常更可靠。

下一章要谈的，是这套结构里最容易被误解的一层：system prompt。很多人把它看成人设文本，本书会说明它更接近操作系统里的规章制度。人设可以改善观感，规章才能约束机器。
