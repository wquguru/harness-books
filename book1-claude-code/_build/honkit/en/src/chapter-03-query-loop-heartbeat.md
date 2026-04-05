# Chapter 3 Query Loop: The Heartbeat of an Agent System

## 3.1 To judge maturity, first ask whether the system has a loop

If we treat a code-writing model as an agent system, the easiest mistake is imagining it as an upgraded Q&A API: user sends one message, model returns one output, task done. This idea is not baseless because many model products do work like this. But once the system starts calling tools, spanning turns, handling interrupts, persisting state, retrying failures, and compacting context, one-shot Q&A understanding collapses quickly.

Claude Code does not make that mistake. Structurally, it explicitly admits that agents depend on continuous, stateful execution.

You can see this clearly in `query()` at `src/query.ts:219` and `queryLoop()` at `src/query.ts:241`. The former is shell; the latter is core. `queryLoop()` is not a model call wrapped in `try/catch`. It maintains cross-iteration state, performs pre-governance steps, enters model streaming stage, then decides whether to execute tools, recover, compact, continue next turn, or terminate.

![Claude Code Query Loop Core](diagrams/diag-ch03-01-query-loop-core.png)

This means Claude Code's center is execution order inside one conversation. The key word is lifecycle. Whether a system deserves to be called an agent is often determined less by how it talks and more by whether it still knows what it is doing several turns later.

## 3.2 State is core business, not baggage

Many systems initially treat state as a burden and statelessness as elegance. For agent systems this preference has limited value. Once an agent enters real workflows, state emerges naturally. Ignoring state does not remove it; it only makes it return in less manageable form.

Claude Code is explicit here. In `src/query.ts:203` to `:217`, mutable query-loop state is clearly defined:

- `messages`
- `toolUseContext`
- `autoCompactTracking`
- `maxOutputTokensRecoveryCount`
- `hasAttemptedReactiveCompact`
- `pendingToolUseSummary`
- `stopHookActive`
- `turnCount`
- `transition`

At `src/query.ts:268`, these are assembled into one `State` object when query loop starts, and updated as a whole through continue branches.

This matters. Claude Code does not scatter recovery, compaction, budget, hooks, and turn counting across ad hoc local booleans. It treats them as one basis for "how next turn continues after this turn ends." State is part of heartbeat.

That is a key difference between mature agent systems and disposable scripts. Scripts ask only whether this step finished. Agent systems must also ask whether the next step can continue from the state left by a failed step.

## 3.3 The first duty of query loop is input governance

From outside, people often assume the core action of an agent is "call the model." In engineering, what matters more is often the long preparation before that call. Claude Code makes this explicit in `queryLoop()`.

Before entering model stage, runtime does all of the following:

- Start memory prefetch, see `src/query.ts:297`
- Prefetch skill discovery, see `src/query.ts:323`
- Slice valid messages after compact boundary, see `src/query.ts:365`
- Apply tool result budget, see `src/query.ts:369`
- Perform history snip, see `src/query.ts:396`
- Perform microcompact, see `src/query.ts:412`
- Perform context collapse, see `src/query.ts:428`
- Attempt autocompact last, see `src/query.ts:453`

This sequence is an architectural statement by itself. It tells you Claude Code puts context governance before model reasoning. In other words, it does not delegate "turn chaos into order" to the model. Runtime governs first, then passes cleaner inputs to the model.

This is critical because many systems do the opposite: stuff huge context in, then hope the model will decide what matters. That looks convenient but shifts runtime responsibility onto probability distributions.

Claude Code takes a more traditional engineering posture: clean the site first, then execute. It is less elegant, but usually more stable.

## 3.4 Model invocation is one phase of the loop, not the loop itself

Only after those governance steps does Claude Code enter model invocation, around `src/query.ts:652`. One detail is worth isolating: output is consumed with `for await` streaming, not as one synchronous complete response.

That means model output in Claude Code is an event stream, not just final prose. Events may contain:

- assistant text
- `tool_use` blocks
- usage updates
- stop reasons
- API errors

This is particularly clear after `src/query.ts:826`. The system stores assistant messages, extracts `tool_use` blocks, decides follow-up needs, and can dispatch tools to `StreamingToolExecutor` while streaming is still in progress.

Engineering-wise, this is a structural shift. Once output becomes event stream, architecture is no longer plain request-response, but a drive-schedule-feedback process. Streaming is not just about seeing words sooner; it lets runtime schedule next actions before model output fully ends.

That is why query loop, not model call, is the heartbeat. Model call is one contraction inside heartbeat. What keeps the system alive is the full cycle: input intake, stream consumption, tool scheduling, failure recovery, and turn continuation.

## 3.5 A heartbeat must handle interrupts, or it is just inertia

A real heartbeat not only keeps beating, it can also stop when necessary. If it cannot stop, what remains is inertia.

Claude Code handles interrupts very concretely. After `src/query.ts:1011`, streaming abort is handled first. If `streamingToolExecutor` is active, remaining results must be consumed and synthetic tool results generated, so issued `tool_use` blocks are not left without paired results. Otherwise `yieldMissingToolResultBlocks()` fills missing interruption records.

This follows a basic engineering principle: once the system has committed to execution externally, interruption still requires ledger closure. You cannot pretend earlier `tool_use` calls never happened just because the user interrupted later. External systems, UI, and transcripts need a consistent causal chain. Even "interrupted" must be complete interruption.

This matters because once an agent enters multi-tool, multi-turn mode, external expectations become more than "did it answer." The system must leave interpretable traces. Non-interpretable traces eventually become operations problems, audit problems, or latent team liabilities no one can explain.

So interrupt handling is core runtime duty. Started actions need closure, even if closure says "not finished."

## 3.6 A heartbeat must also recover, or it is fragile repetition

If interrupts are external shocks, recovery is internal slack. Loops without recovery capability eventually expose one common flaw: they treated luck as design.

Claude Code's recovery is layered, not simplistic retry. Prompt-too-long and max-output-tokens are typical cases.

After `src/query.ts:1065`, the system checks whether the last assistant message is a withheld `prompt too long`. If yes, it first tries to flush staged context collapse (`:1086` to `:1116`); if still insufficient, it enters reactive compact (`:1119` to `:1166`). So recovery proceeds from lower cost and lower destructiveness upward.

`max_output_tokens` is handled similarly. After `src/query.ts:1185`, runtime first tries raising token cap; if still insufficient, it appends a meta message telling the model to continue exactly from truncation point, not apologize, recap, or write polite filler.

This reveals Claude Code's design posture. Recovery is part of main runtime path, not post-failure etiquette. Recovery exists to preserve ability to continue work. In real engineering, continuity is usually more valuable than surface polish.

## 3.7 Stop conditions cannot be singular, or failure and completion get conflated

In ordinary chat systems, stop condition is simple: answer exists, end. Agent systems cannot be this lazy. In one session, "this turn ended" does not equal "task completed," and does not equal "system succeeded."

Claude Code query loop distinguishes at least:

- Streaming completed with `tool_use`, requiring follow-up
- No `tool_use`, entering stop hooks and further checks
- User interruption
- Prompt-too-long recovery branch
- Max-output-tokens recovery branch
- Stop-hook blockage requiring loop re-entry
- API errors returning directly

You can see this from `src/query.ts:1062` through `:1305`. The stop-hooks section around `:1267` to `:1305` is especially important: it explicitly prevents dead loops like "still too long after compact, blocked by hook, compact again forever."

This is worth attention. Many systems have only one naive rule: retry if failed. Claude Code admits retry itself needs governance. Runtime must know why retrying, what already tried, which protection state cannot reset, and what patterns lead to infinity. These decisions separate systems that "keep trying" from systems that "know when not to try again."

## 3.8 QueryEngine proves this belongs to conversation lifecycle

If `queryLoop()` were not enough evidence, `QueryEngine` makes it explicit.

At `src/QueryEngine.ts:176`, source states:

> QueryEngine owns the query lifecycle and session state for a conversation.

![Claude Code QueryEngine Turn Flow](diagrams/diag-ch03-02-queryengine-turn-flow.png)

![Claude Code QueryEngine State Carry-Over](diagrams/diag-ch03-03-queryengine-state-carryover.png)

This line states the chapter's point directly. QueryEngine owns conversation lifecycle, not one call. At `src/QueryEngine.ts:180`, source further states one `QueryEngine` maps to one conversation, and each `submitMessage()` opens a new turn inside that conversation while preserving state.

After `src/QueryEngine.ts:675`, QueryEngine hands prepared `messages`, `systemPrompt`, `userContext`, `systemContext`, and `toolUseContext` to `query()`, then writes assistant/user/compact-boundary messages back into transcript.

This means query loop is the actual execution center of conversation runtime. Outer UI, SDK, and session persistence all orbit it. To understand Claude Code you cannot stop at listing tools or reading prompt text. You must inspect how this loop turns those constraints into continuous behavior.

## 3.9 The third principle extractable from source

This chapter can be compressed into one line:

> The core capability of an agent system is maintaining a recoverable execution loop.

Claude Code source supports this across key points:

- `query.ts` uses explicit `State` for cross-turn execution, not ad hoc locals
- Long input-governance stages before model call show runtime precedes reasoning
- Streaming consumption treats output as events, not final prose
- Interrupt paths synthesize missing tool results, preserving causal closure
- Prompt-too-long, max-output-tokens, and stop hooks each have explicit recovery branches, making failure part of main path
- `QueryEngine.ts` explicitly treats query lifecycle as conversation-owned object

This implies that mature agent heartbeat must satisfy at least:

- explicit cross-turn state
- active input governance rather than passive input consumption
- stream-based model output handling
- ledger closure after interrupt
- clear distinction among completion, failure, recovery, and continuation

Without these structures, systems may still produce attractive demos, but they are closer to staged performances than runtimes. Performances have value, but they do not replace order.

Next chapter moves to where heartbeat most directly touches the external world: tools, permissions, and interrupts. This chapter explained why loops exist. Next we explain why once loops own tools, they must also learn restraint.
