# Chapter 1 Why Harness Engineering Matters

## 1.1 The core problem is keeping the model from going off script

In recent years people have loved talking about agents. The word often carries an easy optimism: if a model can write some code and call some tools, it can work independently in a terminal like a junior engineer. But terminals and filesystems have consequences. Once a speaking probability distribution can touch shell, Git, networks, and local files, the problem shifts from "the answer is not good enough" to "execution caused real damage."

So the center of the problem has always been how to constrain it into a manageable system. Harness Engineering is exactly about that. A harness is an institutional control plane that addresses one practical fact: models are not trustworthy by default.

That judgment is not always pleasant, but it is usually useful. If an agent system is going into real engineering environments, it first has to admit that its core component is unstable. Ignore that, and the problem usually resurfaces in logs and incident reports.

## 1.2 Claude Code's first harness layer: a constrained conversation system

On the surface, Claude Code looks like a CLI that talks with users and can patch code. In implementation terms, it was never designed as a bare model wrapper. It was designed as a conversation system with context boundaries, runtime state, and behavior rules.

You can see this immediately in how the system prompt is organized.

- Starting at `src/constants/prompts.ts:175`, the system defines identity and top-level mission
- Starting at `src/constants/prompts.ts:186`, it adds system-level rules for tools, permissions, reminders, and context compression
- Starting at `src/constants/prompts.ts:199`, it adds engineering constraints for task execution, such as avoiding unauthorized edits, not claiming validation is done when it is not, and not inventing abstractions for convenience

Pause on this point. Many prompt discussions still sit at the rhetorical level of "what kind of assistant are you." Claude Code places prompt inside runtime control structure. These texts define execution boundaries, failure behavior, and reporting responsibility.

More importantly, this prompt is assembled in segments. In `getSystemPrompt()` at `src/constants/prompts.ts:444`, static and dynamic parts are explicitly split, with memory, language, output style, MCP instructions, and scratchpad injected by section. In `src/utils/systemPrompt.ts:28`, default prompt, custom prompt, agent prompt, and appended prompt are then composed via explicit precedence rules.

This reflects a plain engineering fact: a truly usable agent system cannot rely on one "universal prompt" to solve everything. It must split control into layers, then split layers into responsibilities. Otherwise every new reminder and prohibition quickly conflicts with others, and behavior becomes unpredictable.

## 1.3 The second harness layer: the agent depends on a continuous loop

If prompt defines what it should be, the query loop defines how it actually runs.

Claude Code's core is not one isolated API call. It is `query()` starting at `src/query.ts:219` and especially `queryLoop()` starting at `src/query.ts:241`. The key point in this implementation is explicit acknowledgment that agent systems depend on stateful multi-turn execution.

At `src/query.ts:268`, the system puts `messages`, `toolUseContext`, `autoCompactTracking`, `maxOutputTokensRecoveryCount`, `hasAttemptedReactiveCompact`, `pendingToolUseSummary`, `turnCount`, `transition`, and more into one cross-iteration state object. Once a conversation system is designed this way, it is formally admitting that unresolved issues from the last turn enter the next turn, and the system must continue from there.

That is the core harness mindset. The real question is whether behavior remains consistent across continuous turns:

- Is there a budget concept?
- Is there a recovery concept?
- Is there a self-rescue mechanism after context expansion?
- Can the task continue after tool failure?

Without these structures, an agent is just an unstable executor.

After `src/query.ts:365`, the loop also handles message slicing, tool result budget, history snip, microcompact, context collapse, and autocompact before each model call. There are many details, but they point to one thing: Claude Code tries to pull control back to runtime before model invocation.

This is why Harness Engineering cannot be reduced to prompt engineering. The former governs state machines; the latter governs wording. Wording matters, but state machines decide who is accountable for behavior.

## 1.4 The third harness layer: tool calls must obey scheduling discipline

When a model can only output text, at worst it sounds overconfident. Once it can call tools, risk shifts from rhetoric risk to execution risk. Then the key question is: who decides how tools run?

Claude Code's answer is direct. Runtime chooses parallel or serial execution according to tool properties.

In `runTools()` at `src/services/tools/toolOrchestration.ts:19`, tool calls are first grouped by `partitionToolCalls()`. At `src/services/tools/toolOrchestration.ts:91`, the system reads tool schema and calls `isConcurrencySafe()` to decide whether a tool is safe for parallel execution. Concurrency-safe calls run in batches; unsafe calls run one by one. In parallel paths, context modifiers are buffered first and then replayed in original block order, see `src/services/tools/toolOrchestration.ts:31` to `:63`.

This is representative. It shows Claude Code does not treat tools as natural extension of model capability, but as managed execution units requiring scheduling discipline. A tool system without scheduling discipline only amplifies model instability into the external world.

Unconstrained parallelism increases blast radius. Claude Code takes a conservative strategy here. In environments touching files, terminals, and permission boundaries, that conservatism is usually more reliable.

## 1.5 The fourth harness layer: the most dangerous tool needs the strictest rules

Among all tools, Bash is the one to distrust most. It barely has domain boundaries: it can touch files, processes, networks, and Git repositories directly, with shell redirection and pipeline semantics on top. Any system that overtrusts Bash usually gets concrete consequences.

Claude Code's position is very clear in `src/tools/BashTool/prompt.ts:42` and below. It contains extensive operating rules, especially around Git and PRs: do not randomly modify git config, do not skip hooks, do not casually `git add .`, do not use `--amend` to fold previous commits after pre-commit failures, do not commit unless explicitly asked, and do not default to push.

Some people call this too granular. But high-risk interfaces usually require high-density constraints. Once Bash enters real workflow, many rules must be explicit.

One key Harness Engineering principle is to package high-risk capability as high-constraint capability. The stronger the capability, the finer the control. External systems do not forgive bad execution just because model tone sounds confident.

## 1.6 The fifth harness layer: errors are part of the main path

Many software systems treat failure paths as exceptions and success paths as the main text. Agent systems cannot do that. Failures here are not occasional; they are structurally present. Models hit token limits, trigger `prompt too long`, hit `max_output_tokens`, face tool denial, user interrupts, hook blockage, API retries, and more. If all these are handled as afterthought `catch` blocks, the system may look alive while constantly rolling trouble forward.

Claude Code does not do this in query loop. Look at autocompact handling after `src/query.ts:453`, and comments around context limit and blocking logic after `src/query.ts:592`: failures are handled as persistent structural conditions.

This is one major difference between harnesses and ordinary assistants. Ordinary assistants often follow "answer first, apologize if wrong." Harnesses emphasize constrain first, execute next; and if errors happen, route through recovery paths rather than improvising.

A system that can apologize is not necessarily mature. A system that knows when not to start, when to retry, when to terminate, and how to report failure accurately is closer to maturity.

## 1.7 The first principle extractable from source

By now, Chapter 1 really says one thing:

> The key capability of an agent system is constrained execution.

Claude Code source points to the same conclusion in key places:

- `constants/prompts.ts` shows prompt is part of the control plane, not personality decoration
- `utils/systemPrompt.ts` shows behavior must follow explicit layered precedence
- `query.ts` shows agent runtime depends on continuous loop state, not one-shot Q&A
- `services/tools/toolOrchestration.ts` shows tool calls must obey scheduling discipline
- `tools/BashTool/prompt.ts` shows high-risk tools require high-density constraints

Seen together, Harness Engineering is not mysterious. It just insists on engineering common sense that is often ignored:

- Models make mistakes
- Tools amplify consequence
- Context expands
- State contaminates later turns
- Users interrupt
- Failures recur

Given that, systems cannot preserve order through "smartness." They preserve order through structure. Structure is less flashy than smartness, but usually more reliable.

The next chapter turns to the most misunderstood layer in this structure: system prompt. Many people treat it as persona text. We will show it is closer to institutional policy in an operating system. Persona improves feel; policy constrains machines.
