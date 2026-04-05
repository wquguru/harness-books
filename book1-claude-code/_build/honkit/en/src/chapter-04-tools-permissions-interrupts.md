# Chapter 4 Tools, Permissions, and Interrupts: Why Agents Cannot Touch the World Directly

## 4.1 Once models call tools, the nature of risk changes

A text-only model mostly increases communication cost when wrong. If it explains badly, we ask again. Once it starts calling tools, risk changes in kind. Tools are not opinions. Tools are actions. Actions leave effects, and effects touch the real world.

Shell makes this obvious. If a model writes a wrong explanation, impact usually stays at understanding level. If it runs the wrong command, files get deleted, processes are terminated, and Git history becomes hard to repair. Capability increases usually come with consequence increase.

So the most important question in tool systems is: who constrains these tools? Claude Code answers by turning tools into managed execution interfaces, preventing models from touching the world directly.

## 4.2 Tool orchestration is part of behavioral constitution

In `runTools()` at `src/services/tools/toolOrchestration.ts:19`, Claude Code first does something representative: it does not directly execute a list of `tool_use` calls. It batches them by concurrency safety.

In `partitionToolCalls()` at `src/services/tools/toolOrchestration.ts:91`, the system reads each tool's `inputSchema`, then calls `isConcurrencySafe()` to decide whether execution can be parallel. Safe calls go into parallel batches; unsafe calls are split into serial units.

This may look like performance tuning, but it is really consistency design. Once a tool system allows concurrency, it must answer an old question: who decides context evolution, and in what order? In parallel paths (`toolOrchestration.ts:31` to `:63`), Claude Code does not let the fastest tool mutate context first. It buffers `contextModifier` callbacks and replays them in original block order. Execution can be parallel while semantic context evolution remains deterministic.

This is classic engineering conservatism: concurrency may improve throughput, but must not break causality. If tools only run faster without preserving context consistency, they inject new randomness into the system.

Mature agent systems do not idolize parallelism. They treat it as an exception that must prove safety, not default freedom. Claude Code clearly optimizes for bounded risk spread.

## 4.3 A lot happens before a tool actually runs

Many people assume once `tool_use` appears, execution naturally follows. Claude Code shows robust systems do not work that way.

After `src/services/tools/toolExecution.ts:30`, execution in `runToolUse()` is already wrapped with permission logic, hooks, telemetry, and synthetic error materialization. Even without reading every branch, the structure is clear: tool execution is a full lifecycle with:

- pre-checks
- in-flight events
- post-execution correction
- failure compensation

This shows tools here are not ordinary internal library functions. Internal functions assume stable callers who own consequence. Tool interfaces sit between models and external world, so runtime cannot assume stable caller judgment. That is why so many wrappers exist around execution: caller is the most unstable variable.

Design-wise this is crucial: tools should not be modeled as "extensions of model capability." They should be modeled as external capabilities whose risk must be managed by runtime. Once you accept that, permission, hooks, interrupts, and synthetic results look like basics, not burdens.

## 4.4 Permission comes before capability

Claude Code's permission entry point is after `src/hooks/useCanUseTool.tsx:27`. The very existence of `CanUseToolFn` says something important: tool allowance is not decided by model intent alone; it goes through an authorization chain.

Inside `useCanUseTool()`, runtime does not auto-run just because the model requested a tool. It first calls `hasPermissionsToUseTool(...)`, see `useCanUseTool.tsx:37`. Results are split into `allow`, `deny`, or `ask`. This may look ordinary, but it is fundamental. Mature authorization systems need more than yes/no; they need a third state where system itself should not decide on behalf of user.

After `useCanUseTool.tsx:64`, branches continue:

- `deny`: reject directly
- `ask`: route to coordinator, swarm worker, classifier, or interactive approval
- `allow`: execute

This structurally rejects a common dangerous idea: if the model understood user intent, it has authority to execute. It does not. Intent understanding is not authorization, and certainly not persistent authorization. Systems must split "can do" from "may do."

From this angle, permission clarifies agent role: model can propose actions, but runtime, rules, and user decide release. Capability and authority are deliberately separated.

![Claude Code Permission Decision Layers](diagrams/diag-ch04-01-permission-decision-layers.png)

## 4.5 Permission results are runtime semantics, not booleans

After `src/utils/permissions/PermissionResult.ts:23`, Claude Code even defines explicit describers for permission semantics: `allow`, `deny`, and `ask`. This detail matters. Permission is not an internal bool; it is a runtime object with independent meaning.

Why this matters: a permission system must let runtime clearly express why a step did not continue. When an agent says "I need confirmation," it is declaring responsibility boundaries. Once boundaries are explicit, refusal, approval, cache rules, temporary grant, and persistent grant all have a place.

Put simply, if an agent cannot distinguish "I can do this," "I cannot do this," and "I must ask," it should not touch a terminal. Terminals do not fill missing semantics. Terminals only execute.

## 4.6 StreamingToolExecutor proves interrupt is first-class semantics

Once tools are parallel and streaming, interrupt handling becomes immediately complex. Runtime now faces a queue with states like queued, executing, completed, yielded, not one single action.

After `src/services/tools/StreamingToolExecutor.ts:34`, Claude Code explicitly makes this a dedicated streaming executor. Most important is how it handles interruption and discard.

At `StreamingToolExecutor.ts:64` to `:70`, runtime can discard the current tool set during streaming fallback. At `:153` to `:205`, it generates synthetic error messages for different causes:

- sibling error
- user interrupted
- streaming fallback

After `:210`, it further distinguishes interruption causes:

- cancelled due to sibling tool failure
- cancelled due to user interrupt
- dropped due to fallback

At `:233` and below, each tool can define `interruptBehavior`, deciding whether to `cancel` or `block` when user interjects.

This design matters because Claude Code does not treat interruption as "a special execution error." It treats interruption as semantics equal in importance to execution itself. Runtime must know not only whether a tool may start, but how it ends when interrupted, how results are closed, and whether new messages can interleave.

That is a core Harness Engineering trait: design start and stop both. Execution systems without stop semantics eventually depend on user-side hard interruption to finish design.

![Claude Code Tool Execution Lifecycle](diagrams/diag-ch04-02-tool-execution-lifecycle.png)

## 4.7 Why Bash is always more suspect than other tools

In Claude Code's tool world, Bash is not a normal tool. It is a risk amplifier. It is too general. The more general an interface, the harder it is to constrain by domain logic. A file-read tool will not casually kill processes. A grep tool will not secretly push commits. Bash can do almost everything.

Claude Code's distrust is explicit.

First layer is prompt guidance in `src/tools/BashTool/prompt.ts:42` and below. It sets detailed rules for git, PRs, dangerous commands, hooks, force push, and interactive flags. It looks verbose, but it is disciplined verbosity: where consequences are large, rules are explicit.

Second layer is permission and safety classification. `src/tools/BashTool/bashPermissions.ts:1` onward is extensive handling of shell semantics, command prefixes, redirection, wrappers, safe env vars, classifier routing, and rule matching. After `bashPermissions.ts:95`, there is even an explicit subcommand-count limit to prevent complex command bundles from escaping checks.

This shows Bash is treated as a dangerous channel requiring special governance, not a generic command interface. Engineering is acknowledging a simple fact: Bash is powerful, therefore exceptional.

This judgment is worth reusing: high-risk capability should not receive generic capability treatment. The more general capability is, the more special governance it needs. Treating Bash as ordinary tool is usually design laziness.

## 4.8 Tool systems protect users and protect runtime itself

Permissions, scheduling, and interrupts look like user protection mechanisms, but they also protect runtime consistency itself. If an agent system allows unresolved problems such as incomplete `tool_result`, out-of-order context mutation, unbounded parallel side effects, and ambiguous interrupt semantics, the first thing to break is internal consistency.

This is tightly coupled across `query.ts` and tool execution layers. Chapter 3 discussed how query loop synthesizes missing tool results on interrupt. This chapter shows StreamingToolExecutor has its own discarded/errored/sibling abort/interrupt behavior mechanics. Together they preserve a traceable causal chain for:

- what was executed
- what was unfinished
- why it stopped

That is another core harness meaning: preserving order for the system itself. Many constraints look like misoperation prevention on the surface, but at deeper level they prevent runtime from collapsing into unexplainable state fragments.

## 4.9 The fourth principle extractable from source

This chapter can be compressed to one line:

> Tools are managed execution interfaces; permission is an organ of the agent system.

Claude Code source supports this jointly:

- `toolOrchestration.ts` batches before execution, so scheduling comes before impulse
- `toolExecution.ts` wraps hooks, permission, telemetry, and synthetic errors around execution, so calls are never bare
- `useCanUseTool.tsx` splits authorization into `allow / deny / ask`, making authority a first-class semantic branch
- `StreamingToolExecutor.ts` defines interruption, fallback, and sibling-failure semantics, making stopping as important as starting
- `BashTool/prompt.ts` and `bashPermissions.ts` apply high-pressure special governance to Bash, proving high-risk capability must carry denser constraints

If you turn this into portable engineering principles:

- Let models propose actions, but do not grant authority automatically
- Preserve causality order in tool scheduling, even under parallel execution
- Give interruption first-class semantics; do not leave it to generic exception handling
- Treat high-risk tools as explicit exceptions, not generic channels
- A tool system protects both users and runtime consistency

Next chapter addresses another common illusion in this system: "more context is always better." Claude Code implementation says the opposite. Experienced systems treat context as a resource, not a warehouse. We now turn to how memory, `CLAUDE.md`, and compact form one context-governance regime.
