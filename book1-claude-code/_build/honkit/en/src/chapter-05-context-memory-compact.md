# Chapter 5 Context Governance: Memory, CLAUDE.md, and Compact as a Budgeting Regime

## 5.1 As context grows, systems develop a low-level illusion

Once people can keep stuffing content into context, they easily believe a simple myth: more information makes systems smarter. It sounds plausible. Knowing more should be better than knowing less. Unfortunately, agent systems are not libraries and models are not librarians. Context is not a warehouse where "stored" equals "owned." It is an expensive, inflation-prone, self-polluting budget.

Claude Code source is unsentimental about this. It does not design context as an infinite memory pool. It repeatedly reminds itself that what to load, what to truncate, what to preserve long-term, and what to summarize short-term are serious runtime governance decisions.

So this chapter asks: how does Claude Code avoid being crushed by what it remembers? It may look close to "remember more," but engineering-wise these are different regimes. One is accumulation instinct; the other is governance discipline.

## 5.2 The `CLAUDE.md` system: long-lived instructions cannot be mixed with ad hoc chat

At the top of `src/utils/claudemd.ts`, Claude Code already defines memory layers clearly. Instruction sources are split into:

- managed memory, such as `/etc/claude-code/CLAUDE.md`
- user memory, such as `~/.claude/CLAUDE.md`
- project memory, such as root `CLAUDE.md`, `.claude/CLAUDE.md`, `.claude/rules/*.md`
- local memory, such as `CLAUDE.local.md`

These files are loaded by precedence and directory proximity. Project rules closer to current working directory get higher priority. More private and local rules are loaded later, thus placed closer to model attention front.

This is critical. It shows Claude Code refuses to blend long-lived collaboration policy with temporary chat context. Team norms, personal preferences, and repository constraints outlive any single user message. If you force all of them into chat history, systems oscillate between two bad extremes: either reinject everything every turn (context waste), or rely on model recollection (eventual failure).

`claudemd.ts` solves this by making stable rules discoverable, layered, and composable persistent instruction systems. One detail is revealing: it supports `@include`, but only for explicitly allowed text extensions. This shows design balancing convenience against a common failure mode: accidental inclusion of binaries, giant docs, or prompt-toxic artifacts.

That is practical restraint. The system asks first: what deserves memory entry, and what becomes pollution if admitted?

## 5.3 `MEMORY.md` is an index, not a diary

If `CLAUDE.md` governs policy layer, `memdir` governs fine-grained persistent memory. In `src/memdir/memdir.ts`, one design decision is worth revisiting: `ENTRYPOINT_NAME` is `MEMORY.md`, but it is not intended for direct content dumping. It is explicitly an index.

`buildMemoryLines()` states memory writing as two steps:

1. write concrete memory into dedicated files
2. add one-line pointers in `MEMORY.md`

Why this extra step? Because entrypoint files are loaded frequently. Once they bloat, context is gradually dragged by index weight.

That is why `memdir.ts` sets hard limits: `MAX_ENTRYPOINT_LINES = 200` and `MAX_ENTRYPOINT_BYTES = 25_000`. Beyond those, runtime triggers `truncateEntrypointContent()` and appends an explicit warning: only partial load performed; move details into topic files.

This feels like design from someone who has seen too many runaway indexes. It does not trust everyone to stay concise, so it enforces "entrypoint must stay short." Once an entry file tries to be both table of contents and full text, it eventually becomes neither.

From a Harness Engineering perspective, the principle is clear: long-term memory must split into entrypoint and body. Entrypoint gives low-cost addressing; body carries dense content. Mix them and entrypoint fails, then the memory system degrades into decoration.

## 5.4 Session memory: short-term continuity cannot be brute-forced by chat logs

Long-term memory alone is insufficient. The hardest real issue in agent sessions is often "where exactly were we before this turn?" That is a continuity problem inside one session.

Claude Code builds dedicated templates for this in `src/services/SessionMemory/prompts.ts`. Default sections include:

- `Current State`
- `Task specification`
- `Files and Functions`
- `Workflow`
- `Errors & Corrections`
- `Codebase and System Documentation`
- `Learnings`
- `Key results`
- `Worklog`

These are clearly not for journaling. They track status, pitfalls, changed files, and next actionable continuation. The update prompt tone is equally explicit:

- Use Edit tool only to update notes file
- Do not talk about note-taking itself
- Do not alter template structure
- Keep `Current State` aligned with latest work
- Keep every section dense but budget-aware

This means session memory in Claude Code is not "save another copy of chat history." It distills the session into an operational continuation brief. It does not seek full replay; it seeks the minimum structure needed to continue working.

There is also a highly practical detail: `prompts.ts` sets `MAX_SECTION_LENGTH = 2000` and `MAX_TOTAL_SESSION_MEMORY_TOKENS = 12000`. Beyond budget, runtime asks for aggressive condensation, with explicit priority on `Current State` and `Errors & Corrections`.

This says a lot. Mature systems treat "preserve what is most useful for continuation" as virtue. Context budget is working memory, and working memory must stay operable.

## 5.5 Autocompact: context governance is budget governance first

By now we have long-term rules, persistent memory, and session memory. Context still inflates. So in `src/services/compact/autoCompact.ts`, Claude Code admits another reality: regardless of organization quality, long enough sessions approach window limits.

`getEffectiveContextWindowSize()` first subtracts reserved output budget for summary generation. `MAX_OUTPUT_TOKENS_FOR_SUMMARY` reserves 20,000 tokens directly. Runtime assumes compact itself costs budget and never waits until oxygen is almost gone.

Then `getAutoCompactThreshold()` subtracts another `AUTOCOMPACT_BUFFER_TOKENS = 13_000`. Warning thresholds, error thresholds, and manual compact reserve all have dedicated buffers.

The logic is simple: context governance must pre-reserve room for failure and recovery. Systems that reserve nothing may look frugal in normal cases but simply defer risk billing to later turns.

`AutoCompactTrackingState` is also revealing. It tracks not only `compacted`, but also `turnCounter`, `turnId`, and `consecutiveFailures`. So autocompact is a tracked runtime behavior that can fail and be rate-limited.

Source even notes a hard lesson: large amounts of API calls were once wasted on repeated autocompact failure, therefore `MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES = 3` with circuit breaker after that. You may fail, but you may not fail infinitely without memory.

## 5.6 `compactConversation()` shows summaries must rebuild working context

Many people hear compact and assume "summarize the previous chat." Claude Code does much more. In `compactConversation()` within `src/services/compact/compact.ts`, runtime disassembles old context, summarizes, then reinjects required runtime attachments to rebuild a post-compact world that can still work.

Look at pre-summary cleaning first. `stripImagesFromMessages()` replaces images and docs with markers like `[image]` and `[document]`. `stripReinjectedAttachments()` removes attachments that will be reinjected anyway, to avoid token waste. These two actions alone show compact explicitly drops content with high token cost and low summary value.

Now look at summary failure handling. Source includes `truncateHeadForPTLRetry()` for the awkward case where compact request itself hits prompt-too-long. The system admits not only main path can explode, but rescue tooling can also explode.

After compact succeeds, Claude Code does not keep only one summary line. It also:

- clears stale `readFileState`
- regenerates post-compact file attachments
- reinjects plan attachments
- reinjects plan mode attachments
- reinjects invoked-skills attachments
- reinjects deferred tools, agent listing, and MCP instruction delta attachments
- runs session start hooks and post-compact hooks
- writes compact boundary messages with pre-compact token counts and boundary metadata

Taken together, compact in Claude Code is controlled reboot, not chat recap. Old context is translated into new operating substrate. Many systems do only the first half, then discover that after compact they "remember roughly" but lost tool state, plan state, and attachment state, and must spend turns rediscovering themselves.

## 5.7 Context governance is about preserving work semantics

If you read the latter half of `compact.ts`, one consistent preference appears: Claude Code preserves working semantics.

It restores recently accessed file attachments because they encode local working reality. It restores plan mode because otherwise models may forget they still operate under planning discipline. It keeps invoked-skill content but token-caps each skill so post-compact stage is not hijacked by skill payloads.

One source phrase captures this well: per-skill truncation beats dropping. Even when cutting, keep critical leading constraints rather than dropping whole blocks. That is governance, not brute throttling. Throttling cuts blindly. Governance decides what to cut and what to preserve.

A stable lesson follows: context systems should prioritize preserving action semantics, not preserving the highest apparent information volume. File specifics, current plans, error corrections, and skill constraints directly determine whether next action can be correct. Long repetitive chat history and easily retrievable runtime data do not deserve permanent seats.

## 5.8 The fifth principle extractable from source

This chapter can be compressed into one sentence:

> Context is working memory. Governance exists to keep the system able to continue work.

Claude Code source supports this on several layers:

- `claudemd.ts` loads long-lived instructions in layers, separating stable rules from temporary dialogue
- `memdir.ts` defines `MEMORY.md` as index and hard-truncates it, forcing entrypoint brevity and addressability
- `SessionMemory/prompts.ts` structures short-term continuity with fixed template plus section/global budgets
- `autoCompact.ts` reserves summary budget, buffers, and failure circuit breaker, treating window operation as risk-managed budgeting
- `compact.ts` restores plans, files, skills, tool attachments, and hook state after summarization, showing compact aims to rebuild working semantics, not produce pretty summaries

Portable engineering principles from this:

- Layer long-term rules, persistent memory, and session continuity instead of mixing them
- Keep index-like memory artifacts small or they drag down the entire system
- Session summaries should serve continuation, not complete recollection
- Compact is a primary path, not an emergency side path
- Post-compact context must preserve runtime semantics, not merely language surface

Next chapter asks what happens when this governance system meets hard limits: prompt too long, max output tokens, hook dead loops, and competing recovery branches. That is where you can finally tell whether a system is "hoping nothing breaks" or "designed to survive breakage."
