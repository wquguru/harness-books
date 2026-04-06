# Chapter 7 Convergence and Divergence

## 7.1 Start with the part where they converge

If I had to give the shortest conclusion first, I would say: yes, they genuinely converge.

The reason is straightforward. Neither Claude Code nor Codex treats the model as an executor worthy of direct trust. Both systems accept:

- prompt does not control everything
- tools must be constrained
- long sessions require state governance
- local rules must enter the system
- multi-agent execution requires role partitioning and verification

In other words, both have already moved beyond the naive stage where people imagine that stronger models will somehow dissolve systems problems by themselves. Once a system reaches this point, it no longer treats an agent as merely a chatbot with a few tools attached.

So at the level of direction, they do meet at the same destination: harness is the true control layer, and the model is the most productive but also most unstable component underneath it.

## 7.2 Now the part where they branch

But it would be far too rough to call them fundamentally identical.

Claude Code's main axis looks something like this:

- begin from the query loop
- handle continuity in runtime
- preserve order with compaction, tool orchestration, interrupts, and recovery
- connect field rules and team institutions through skills, hooks, and verification

Codex's main axis looks more like this:

- begin from explicit module boundaries and explicit control layers
- turn instructions into fragments
- turn tools into schemas
- turn execution boundaries into policy
- turn sessions into thread / rollout / state
- turn local rules and hooks into structured assets and event systems

The first feels like a system grown from mechanical experience.

The second feels like a system grown from institutional design.

That is where the branching really lies. The difference is not destination. It is skeleton.

## 7.3 If I had to give them a harsher but more accurate label

I would even be willing to call them two different political forms of harness.

Claude Code is closer to a runtime republic. A great deal of power is concentrated in the main loop and field dispatch, and order is maintained through continuous negotiation with reality. It is not anti-institution; institutions just tend to exist in service of the live session.

Codex is closer to a constitutional control plane. Power is first written into types, fragments, policy, threads, and event systems. Runtime still judges, of course, but it judges inside a more explicit framework.

That is an exaggerated description, but it clarifies an important point: harness is never only a pile of technical parts. It is also a way of distributing power. Who defines the boundary, who interprets state, and who owns the final authority of execution all eventually appear in architecture.

## 7.4 What later builders should learn

If a team intends to build its own coding agent, the true value of this comparison is not side-picking. It is avoiding two categories of mistake.

The first mistake is thinking a feature table is enough. It is not. A team has to decide what its primary contradiction is. Is the real problem that long sessions go out of control, or that rule sources are too scattered and permission boundaries remain unclear? Different contradictions push you toward different harness shapes.

The second mistake is trying to splice together the most attractive features of both systems without making actual tradeoffs. In engineering, what is most dangerous is often not tradeoff itself but the refusal to make one. If you want fully dynamic runtime flexibility and a completely explicit structured control plane at the same time, you usually end up with neither.

The saner approach is:

- if you fear loss of control on site, strengthen the runtime heartbeat first
- if you fear institutional drift, make instruction, tool, policy, and state explicit first
- once the primary contradiction stabilizes, gradually build the opposite side

One more caution belongs here. In practice many younger systems do neither job fully. They neither harden runtime discipline nor make the control layer truly explicit. Instead they take a third, easier-looking road: keep stuffing more bootstrap files, role descriptions, skill explanations, and workspace text into prompt, hoping that informational fullness will compensate for a weak skeleton. Such systems often appear workable in the short term, but over longer sessions they expose the same double failure: tokens are expensive, and working semantics are still unstable.

## 7.5 Final judgment

The question in the title can now be answered directly.

They are convergence through different roads.

They are also distinct branches of the same larger problem.

"Convergence" names the reality they both accept: the model is unreliable, and harness is where order comes from.

"Different branches" names the different political economy through which that reality is implemented: Claude Code trusts runtime discipline more, while Codex trusts explicit control layers more.

Systems that rely mainly on prompt stacking to hold context together sit in a less settled middle zone. They have already realized that models forget and drift, so they add memory, skills, and compaction. But if context governance still follows a "inject first, rescue later" logic, then the system still has not decided clearly which layer should own order.

Neither path is inherently nobler. The real question is this: in which layer is your system prepared to cage uncertainty?

The location of that cage determines what the system will later become.
