# 第 5 章 上下文治理：Memory、CLAUDE.md 与 Compact 是预算制度

## 5.1 上下文一多，系统就容易产生一种低级幻觉

人一旦可以往上下文里不停塞东西，就很容易相信一个朴素的神话：信息越多，系统越聪明。这个神话听起来甚至有点合情合理。毕竟知道得多，总比知道得少强。可惜代理系统不是图书馆，模型也不是藏书管理员。上下文不是一个“存进去就算拥有”的仓库，它首先是一笔昂贵、易膨胀、还会自我污染的预算。

Claude Code 的源码在这件事上很不浪漫。它并没有把上下文设计成一个可以无限堆叠的记忆池，反而在很多地方反复提醒自己：该加载什么、该截断什么、什么东西要长期保留、什么东西只能短期摘要，都是运行时必须严肃治理的事。

所以这一章要讨论的是：Claude Code 怎样防止自己被记住的东西拖死。这件事和“记住更多”看起来相近，工程上却是两种制度。前者偏向收藏癖，后者才接近治理术。

## 5.2 `CLAUDE.md` 体系说明，长期指令不能和临场对话混在一起

Claude Code 在 `src/utils/claudemd.ts` 开头就把记忆层次说得很清楚。它把 instruction source 分成几层：

- managed memory，例如 `/etc/claude-code/CLAUDE.md`
- user memory，例如 `~/.claude/CLAUDE.md`
- project memory，例如项目根目录里的 `CLAUDE.md`、`.claude/CLAUDE.md`、`.claude/rules/*.md`
- local memory，例如 `CLAUDE.local.md`

而且这些文件会按优先级和目录距离加载。离当前工作目录越近的 project 规则，优先级越高；越偏向私有、越偏向本地的规则，越晚加载，因而越靠近模型的注意力前沿。

这件事特别要紧。因为它说明 Claude Code 从一开始就拒绝把“长期协作规则”和“本轮临时对话”混成一锅粥。团队规范、个人偏好、仓库约束，这些东西的寿命远长于某一轮用户消息；如果把它们全都塞进聊天记录里，系统就会在两个极端之间摇摆：要么每轮都重复注入，浪费上下文；要么靠模型自己回忆，迟早失手。

`claudemd.ts` 给出的答案，是把这些稳定规则做成可发现、可分层、可组合的持久指令系统。还有个细节很有意思：它支持 `@include`，并且只允许一大批明确列出的文本扩展名。这说明工程师除了追求 include 的便利，也在提防另一种常见事故：有人把二进制、巨型文档、甚至不该进 prompt 的东西糊里糊涂带进来了。

这是正经工程师才有的克制。系统会先问：”什么东西值得进入系统记忆，什么东西一旦进入就是污染。”

## 5.3 `MEMORY.md` 是索引，不是日记本

如果 `CLAUDE.md` 管的是规则层，那么 `memdir` 处理的就是另一类更细的长期记忆。`src/memdir/memdir.ts` 里有一段设计很值得反复看：`ENTRYPOINT_NAME` 被定义成 `MEMORY.md`，但这个文件并不被鼓励用来直接堆内容，它被定义为 index。

源码里写得很实在。`buildMemoryLines()` 明确告诉模型，保存 memory 是两步：

1. 把具体 memory 写进独立文件
2. 再在 `MEMORY.md` 里加一个一行指针

为什么这么麻烦？因为系统知道入口文件天然会被频繁加载，而频繁加载的东西一旦变胖，整套上下文就会被它慢慢拖成一个不好收拾的胖子。

这也是为什么 `memdir.ts` 里专门有 `MAX_ENTRYPOINT_LINES = 200` 和 `MAX_ENTRYPOINT_BYTES = 25_000`。超过了，系统会直接 `truncateEntrypointContent()`，并在结尾追加明确警告：只加载了一部分，请把细节移到 topic files。

这套做法特别像一个见过太多失控索引的人。它不相信大家会天然克制，所以把“入口必须短”做成硬约束。因为入口文件一旦既当目录又当正文，最后就既不是目录，也不是正文，只是一个谁都不愿再读第二遍的烂尾摘要。

从 Harness Engineering 的角度看，这里抽出来的原则非常清楚：长期记忆必须分成“入口”和“正文”。入口负责低成本寻址，正文负责高密度承载。把两者混为一谈，最终一定是入口失效，随后整套记忆系统退化成摆设。

## 5.4 Session memory 说明，短期连续性也不能靠聊天记录硬扛

只有长期 memory 还不够。代理系统真正难受的地方，常常在于“这轮之前我们到底做到哪一步了”。这是一次会话内部的连续性问题。

Claude Code 在 `src/services/SessionMemory/prompts.ts` 里专门给这件事建了一套模板。默认模板里有这些栏目：

- `Current State`
- `Task specification`
- `Files and Functions`
- `Workflow`
- `Errors & Corrections`
- `Codebase and System Documentation`
- `Learnings`
- `Key results`
- `Worklog`

你一看就知道，这不是给人抒情的。它关心的是：现在做到哪了，踩过什么坑，改过哪些文件，后面该接什么。更有意思的是更新 prompt 的语气。源码里明确要求：

- 只能用 Edit tool 更新 notes file
- 不要提 note-taking 这件事本身
- 不要改模板结构
- `Current State` 必须始终反映最近工作
- 每节都要信息密集，但要控制预算

这说明 session memory 在 Claude Code 里并非“另存一份聊天记录”，它会把当前会话萃取成一种可继续工作的操作说明书。它不求完整复刻对话，而求压缩出未来继续干活所必需的骨架。

这里有个极其工程化的细节。`prompts.ts` 里定义了 `MAX_SECTION_LENGTH = 2000` 和 `MAX_TOTAL_SESSION_MEMORY_TOKENS = 12000`。超过预算，系统不会夸你记得细，而是要求你 aggressively condense，尤其优先保留 `Current State` 和 `Errors & Corrections`。

这很能说明问题。真正成熟的系统，会把“为继续工作保留最有用的部分”当成美德。因为上下文预算是工作内存。工作内存的第一职责是可操作。

## 5.5 自动 compact 说明，上下文治理首先是预算治理

到这里，长期规则、持久 memory、session memory 都有了，但上下文还是会膨胀。于是 Claude Code 在 `src/services/compact/autoCompact.ts` 里进一步承认一个现实：不管你多会整理，只要对话够长，总会逼近窗口边缘。

`getEffectiveContextWindowSize()` 先把模型 context window 减去一笔保留给 summary 输出的预算。`MAX_OUTPUT_TOKENS_FOR_SUMMARY` 直接预留了 20,000 tokens。也就是说，系统先假定 compact 本身要花钱，绝不把窗口吃到只剩一口气时才想起求生。

接着 `getAutoCompactThreshold()` 又在有效窗口上再扣掉 `AUTOCOMPACT_BUFFER_TOKENS = 13_000`。警告阈值、错误阈值、手动 compact 预留空间，也都各自分出 buffer。

这套数字背后有个很朴素的道理：上下文治理需要提前为失败和恢复留出余地。不留余地的系统，平时看着像节俭，出事时才暴露真相——不过是把风险账单留给了下一轮。

更有意思的是 `AutoCompactTrackingState`。它不仅记 `compacted`，还记 `turnCounter`、`turnId` 和 `consecutiveFailures`。这说明 autocompact 是一段会被追踪、会失败、会被限流的运行时行为。

源码甚至写了一个很直白的注释：全球每天曾经浪费大量 API calls 在连续失败的 autocompact 上，所以 `MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES = 3`，再失败就触发 circuit breaker。这里的气质非常好，像一个终于受不了浪费的人：你可以失败，但不能无限次、无记忆地失败。

## 5.6 `compactConversation()` 说明，摘要要重建可继续工作的上下文

很多人一听 compact，会以为就是“把前面聊天摘要一下”。Claude Code 的实现要复杂得多。`src/services/compact/compact.ts` 里的 `compactConversation()` 真正做的，是把原有上下文拆开、摘要、再注入必要附件，重新搭出一个还能工作的后 compact 世界。

先看压缩前的清洗。`stripImagesFromMessages()` 会把图片、文档替成 `[image]`、`[document]` 之类的标记；`stripReinjectedAttachments()` 会把反正之后还要重新注入的 attachment 先剥掉，免得浪费 token。仅这两个动作就说明，compact 会有选择地丢掉那些”对摘要没用、但 token 开销极大”的部分。

再看摘要失败时的处理。源码里有 `truncateHeadForPTLRetry()`，专门应对“compact 请求自己都 prompt too long”的尴尬场面。也就是说，系统不仅承认主流程会爆，还承认“救火工具本身也会爆”。这很像真实世界，而不是 demo。

而在 compact 成功之后，Claude Code 做的不是简单保留一条 summary。它还会：

- 清空旧的 `readFileState`
- 重新生成 post-compact file attachments
- 把 plan attachment 补回来
- 把 plan mode attachment 补回来
- 把 invoked skills attachment 补回来
- 把 deferred tools、agent listing、MCP instructions 的 delta attachment 重新补回来
- 执行 session start hooks 和 post-compact hooks
- 写 compact boundary message，记录 pre-compact token 数与边界信息

这些动作合在一起，意思很明确：compact 的目标是把“继续干活所需的运行时环境”重新铺平。摘要只是中间产物，不是最终目的。

所以 compact 在 Claude Code 里更像一次受控重启，而不是一次聊天总结。旧上下文会被转译成新的工作底座。这种设计很值得记住，因为很多系统只做前半截，结果 compact 之后虽然“还记得大概”，却已经失去了工具状态、计划状态、附件状态，接下来还得再花几轮找回自己。

## 5.7 上下文治理的关键是保留工作语义

如果只看 `compact.ts` 的后半段，会发现一个贯穿始终的倾向：Claude Code 真正在意的是把工作语义保住。

例如它会恢复最近访问文件的 attachment，因为这些文件往往构成当前工作面的局部现实；它会恢复 plan mode，因为否则模型压缩完以后可能忘了自己还处在 plan discipline 里；它会保留 invoked skills 的内容，但又给每个 skill 设置 token cap，避免 skill 本身在 post-compact 阶段反客为主。

源码里这句话很有味道：per-skill truncation beats dropping。意思是，即使要裁，也优先保住开头那一段最关键指令，而不是整个扔掉。这就是治理，不是纯粹节流。纯节流是砍，治理是知道该砍哪里、该保什么。

从这里可以抽出一个相当稳妥的经验：上下文系统应该优先保留能维持行动语义的东西，而不是优先保留看起来信息量最大的东西。文件细节、当前计划、错误修正、技能约束，这些都直接决定下一步能不能做对。反过来，冗长的历史对话、重复出现的附件、运行时随时可以重新拿到的东西，就没必要再占着座位。

## 5.8 从源码里可以提炼出的第五个原则

这一章最后可以压成一句话：

> 上下文是工作内存。治理它的目标是支持系统继续工作。

Claude Code 的源码在几个层面共同支持这个判断：

- `claudemd.ts` 把长期指令分层加载，说明稳定规则要和临时对话分开治理
- `memdir.ts` 把 `MEMORY.md` 定义成索引并强行截断，说明入口文件必须短而可寻址
- `SessionMemory/prompts.ts` 用固定模板提炼会话连续性，并对 section 和总量设预算，说明短期记忆也必须结构化
- `autoCompact.ts` 为 compact 预留输出预算、缓冲区和失败熔断，说明上下文窗口要按风险来经营
- `compact.ts` 在摘要后恢复计划、文件、技能、工具附件和 hook 状态，说明 compact 的目标是重建工作语义，而不是写一段好看的总结

如果把这些抽象成可迁移的工程原则，大概有这样几条：

- 长期规则、长期记忆、会话连续性，应该分层，不该混写
- 入口型记忆必须短小，否则整个系统会被入口拖垮
- session summary 应该服务于“继续工作”，而不是服务于“回忆完整”
- compact 是上下文治理主路径
- 压缩后的上下文必须保住运行语义，而不是只保住语言表面

下一章要讲的是这套治理系统碰到极限时怎么办。因为一个真系统终究会出错：prompt too long，max output tokens，hook 死循环，恢复分支相互打架。到那时你才看得出来，一个代理系统到底是在“赌不出事”，还是在认真设计出事之后怎么活下去。
