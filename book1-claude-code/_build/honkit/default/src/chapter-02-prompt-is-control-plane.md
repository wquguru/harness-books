# 第 2 章 Prompt 不是人格，Prompt 是控制平面

## 2.1 把 prompt 当成人设，是一种常见误会

很多人一说起 system prompt，首先想到的是一段熟悉的话术：你是谁，你擅长什么，你应该温柔、专业、简洁，最好再有一点稳定的人格。对于只负责聊天的系统，这种理解倒也够用；但对一个要读文件、调工具、动 shell、处理权限、跨轮执行的代理系统来说，这种理解明显不够。

原因很简单。人设描述解决的是“它像什么”，控制平面解决的是“它能做什么、什么时候做、做错了怎么办、谁来兜底”。两者不在同一层。一个系统可以有讨人喜欢的人设，同时在执行层面缺少规矩。那种系统出事时往往会显得很真诚，因为它很会道歉。但道歉并不能替代运行时设计。

Claude Code 的实现恰好说明了这一点。它的 system prompt 是一组分层拼装的行为区块。换句话说，这里的 prompt 更接近一套运行时协议，而不是一篇人物小传。

## 2.2 从源码看，Claude Code 的 prompt 从一开始就是分层的

在 `src/constants/prompts.ts:444` 的 `getSystemPrompt()` 里，Claude Code 返回的是一个由多个 section 组成的数组，而不是一段完整字符串。这个细节很重要。因为一旦 prompt 变成多个块，系统就正式承认它内部包含一组职责不同的约束。

这些 section 至少包含几类东西。

首先是身份和总任务说明。在 `src/constants/prompts.ts:175`，系统说明自己是一个交互式代理，要用可用工具帮助用户完成软件工程任务。这里同时嵌入了一些安全约束，比如不要乱猜 URL。

然后是系统级规则。在 `src/constants/prompts.ts:186` 开始，系统明确规定：

- 用户能看见的是哪些文本
- 工具调用可能触发权限审批
- 用户拒绝后不能机械重试
- tool result 和 user message 里可能混入 system-reminder
- 上下文会被自动压缩

这些内容有一个显著特征：它们并不关心模型“像不像一个聪明助手”，而是关心它是否是一个守规矩的执行体。这就是控制平面的语气，它的核心任务是定义边界。

再往下，在 `src/constants/prompts.ts:199` 开始，是做任务时的工程性指令：不要随意增加需求，不要越权优化，不要为了看起来体面而隐瞒验证失败，不要在没有必要时制造抽象。这些内容看起来像写作风格要求，其实它们和工程约束绑得很紧。一个会自动“顺手优化一切”的模型，从产品角度看也许很热情，从工程角度看则相当危险。

所以，从源码结构上就能看出来：Claude Code 的 prompt 要解决的是如何让模型在复杂运行时里遵守边界。

## 2.3 Prompt 的真正价值，不在文字本身，而在优先级

如果 prompt 只是写在那里，还不够说明问题。真正决定它是否属于控制平面的，是系统是否给它定义了严格优先级。

这一点可以看 `src/utils/systemPrompt.ts:28` 开始的 `buildEffectiveSystemPrompt()`。这段代码把 prompt 的来源明确排成一条链：

1. override system prompt
2. coordinator system prompt
3. agent system prompt
4. custom system prompt
5. default system prompt

最后还会统一拼接 `appendSystemPrompt`。

这个设计很说明问题。它表明 Claude Code 并不相信“默认 prompt 一劳永逸”。相反，它承认系统里存在多种语境：

- 协调者模式需要自己的系统行为
- agent 模式需要自己的职责说明
- 用户可以通过 CLI 覆盖或追加 prompt
- 默认 prompt 只是没有更高优先级时的基线

更朴素地说，成熟系统不会迷信唯一版本的 prompt。它会把 prompt 看成一个有层级的配置系统，让不同职责在不同上下文里生效。

这里还有一个很值得注意的细节。在 `src/utils/systemPrompt.ts:99` 往后，系统对 proactive mode 做了特殊处理：如果 agent prompt 和 proactive mode 同时存在，agent prompt 不再替换默认 prompt，而是附加在默认 prompt 之后。这个决定本身就很说明问题。它意味着系统知道，有时候默认约束不能丢，新增 agent 只能在默认约束之上叠加领域行为，而不能把整套纪律换掉。

可以把它理解为一套通用制度外加岗位说明书。岗位说明书可以补充职责，但不能直接冲掉底层制度，否则系统很快就会各自为政。

## 2.4 Prompt 不是静态文案，它还连接着记忆系统

如果说前面这些内容已经像一套运行时说明书，那么看到 Claude Code 如何处理 memory 和 `CLAUDE.md` 后，就会更清楚地意识到：这里的 prompt 已经是整个上下文治理入口，而不只是“写给模型看的一段话”。

在 `src/utils/claudemd.ts:1153` 的 `getClaudeMds()` 里，系统会把 project instructions、local instructions、team memory、auto memory 等不同来源的内容整理成统一格式，再拼接进 prompt 相关上下文中。这里连每种内容的来源说明都写得很细，比如这是项目级指令、用户私有项目指令、共享 team memory，还是跨会话持久化的 auto memory。

而在 `src/memdir/memdir.ts:187` 开始的 `buildMemoryLines()` 里，系统连“如何保存记忆”这件事都变成了 prompt 的一部分。它会明确告诉模型：

- memory 是文件化持久系统
- `MEMORY.md` 是索引，不是正文
- 要如何写 frontmatter
- 哪些信息不该保存
- plan 和 task 不该被误用成 memory

这件事非常关键。它把 prompt 的职责从“约束当前行为”扩展到了“约束未来知识的沉淀方式”。这已经超出了通常意义上的提示词，更接近一份写给运行时参与者的知识治理协议。

换句话说，Claude Code 不只是用 prompt 规定“这一轮怎么说话”，还用 prompt 规定“长期记忆如何形成”。一个系统只要走到这一步，它的 prompt 就不可能再只是语气问题，而必然进入制度问题。

## 2.5 真正的控制平面，还要考虑缓存与计算成本

多数人理解 prompt 时，很少会想到性能。常见想法是 prompt 只是喂给模型的文本，写好即可。Claude Code 的实现更务实：prompt 同时也是计算成本。它越复杂、变化越频繁，缓存命中就越差，系统运行就越贵、越慢。

在 `src/constants/systemPromptSections.ts:16` 往后，系统把 prompt section 区分成两类：

- 可缓存的 `systemPromptSection`
- 会打破缓存的 `DANGEROUS_uncachedSystemPromptSection`

而 `resolveSystemPromptSections()` 会优先从缓存里拿已经计算过的内容，只在必要时重算。到了 `clearSystemPromptSections()`，系统又会在 `/clear` 或 `/compact` 之后清空这些状态。

这件事看起来像优化，实际上同样属于控制平面。一个真正可运行的 prompt 系统，不可能只考虑表达能力，而不考虑它对吞吐、延迟和缓存的影响。Claude Code 在 `getSystemPrompt()` 里甚至把静态部分和动态部分用 boundary 显式分开，见 `src/constants/prompts.ts:560` 往后。这说明它在设计时已经承认：有些内容在会话中相对稳定，有些内容会逐轮变化，二者不能混在一起消耗缓存。

一个工程系统只要开始关心“哪部分 prompt 会导致缓存失效”，它就已经不再把 prompt 当作文案创作。文案追求完整表达，控制平面追求可治理、可复用、可预测的行为成本。两者关注的问题不同。

## 2.6 用户可以覆盖 prompt，但不能跳过这套结构

Claude Code 并没有把用户锁死在默认 prompt 上。相反，CLI 明确支持覆盖和追加。

在 `src/main.tsx:1342` 往后，系统处理 `--system-prompt`、`--system-prompt-file`、`--append-system-prompt`、`--append-system-prompt-file` 这些选项。也就是说，用户当然可以带着自己的规约来。

但这里有个关键点。系统虽然允许覆盖和追加，却仍然坚持用统一的 `buildEffectiveSystemPrompt()` 做最终装配。这说明它允许自定义，但不放弃秩序。用户可以改内容，系统仍然保留结构。

没有结构的可定制，最后往往会退化成另一种随意。今天加一段，明天减一段，后天某个 agent 又替换掉基线约束，系统行为就会越来越像临时口头通知。Claude Code 的选择是让用户修改，但修改必须发生在既定优先级和分层机制里。

## 2.7 为什么说 prompt 在这里更像宪法，而不是台词

如果把前面各节放在一起看，可以得到一个相当明确的结论：

Claude Code 的 prompt 更像宪法。

所谓台词，是给角色在场上说的；所谓宪法，是规定权力边界、责任关系和例外情况如何处理。Claude Code 的 prompt 更接近后者，因为它满足了几个结构条件：

- 它分层，而不是一块写到底
- 它有优先级，而不是谁后写谁说了算
- 它与 memory、CLAUDE.md、agent instructions、MCP instructions 一起组成完整控制平面
- 它有缓存和动态 section 机制，不是随手拼一段文本
- 它和 runtime 紧密耦合，而不是游离于系统之外的装饰物

这也是为什么“写一个好 prompt”单独拿出来时价值有限。更重要的问题是：prompt 在系统里处于什么位置，它和哪些模块配合，它是否参与权限、状态、上下文和长期记忆的治理。如果不回答这些问题，所谓好 prompt 往往只是在某个顺利场景里暂时成立。

## 2.8 从源码里可以提炼出的第二个原则

这一章最后可以归纳成一句话：

> Prompt 的价值，在于它是否被纳入一套清楚的控制结构。

Claude Code 的源码在几个地方共同证明了这一点：

- `constants/prompts.ts` 把 prompt 写成分段控制结构，而不是一段统一宣言
- `utils/systemPrompt.ts` 明确规定了 prompt 来源的优先级
- `utils/claudemd.ts` 把项目级和长期记忆内容纳入上下文装配
- `memdir/memdir.ts` 用 prompt 规定了长期记忆的保存规则
- `constants/systemPromptSections.ts` 则把 prompt 进一步变成可缓存、可失效、可按段重算的运行时对象

所以，一个成熟代理系统里的 prompt，不该被理解成“让模型入戏的开场白”。它更像一套运行中的制度文本。制度文本当然也可以写得清楚，但最重要的部分始终是约束力。

下一章要讨论的，是另一根更硬的骨头：query loop。因为再好的控制平面，最后都要落到执行循环里。prompt 规定边界，循环决定命运。一个系统最终会成为什么样子，往往体现在它每一轮如何继续、如何中断、如何恢复的那套状态机里。
