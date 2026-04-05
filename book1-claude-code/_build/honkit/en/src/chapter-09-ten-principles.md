# Chapter 9 Ten Principles of Harness Engineering

Technical writing has a bad habit: after presenting enough detail, it avoids making judgments, as if showing complexity exempts conclusion responsibility. It does not. Complexity remains complexity, but judgment is still required. Teams carry principles forward, not function names from one source version.

Across the previous eight chapters, we kept circling one fact: models are unreliable, but systems can still be reliable if reliability is built into harness rather than delegated to models.

This chapter does not re-argue details. It compresses the book into ten principles. They are not slogans. They come from working judgments reflected in Claude Code source and engineering structure.

## 9.1 Treat models as unstable components, not teammates

Teammates can be trusted with stable responsibility. Models cannot. Models may speak like teammates, but they do not automatically gain teammate-grade stability, accountability, or sustained judgment. The earlier this is acknowledged, the earlier systems grow permission boundaries, recovery paths, verification gates, and rollback ability.

## 9.2 Prompt is part of the control plane

System prompts define behavioral protocol. Together with runtime, tool schema, memory, and hooks, they form the control plane. If prompt is treated as persona decoration, you get systems that perform well rhetorically and behave without discipline.

## 9.3 Query loop is the heartbeat of agent systems

Real agents depend on continuous execution loops. Input governance, stream consumption, tool scheduling, recovery branches, and stop conditions all belong to heartbeat. Without query loop, systems may demo well but are not runtimes.

## 9.4 Tools are managed execution interfaces

Once models touch shell, filesystem, Git, and networks, the question shifts from "can it say it" to "can it leave consequences." Therefore tools must be scheduled, authorized, interruptible, and ledger-closed. The more dangerous a tool is, the less it should be treated like ordinary capability.

## 9.5 Context is working memory

Being able to stuff context does not mean context should be stuffed. Long-lived rules, persistent memory, session continuity, and temporary dialogue should be governed in layers. Compact exists to preserve semantic substrate for continued work. Good context management optimizes not for "more," but for "governable."

## 9.6 Error paths are main paths

Prompt-too-long, max-output-tokens, interrupts, hook loops, and compact failures are ordinary weather for long-session agents. Recovery, circuit breaking, retry limits, and anti-loop guards must exist at design time, not post-incident patch time.

## 9.7 Recovery should optimize for continuation

After truncation, continuation is usually better than recap. When compaction fails, first restore breathing. True engineering politeness is not trapping users inside failure states.

## 9.8 Multi-agent matters because it partitions uncertainty

Multi-agent places research, implementation, verification, and synthesis into different responsibility containers. State is isolated, roles are separated, and coordinator reconverges understanding. The real value of parallelism is not speed alone, but sharper responsibility boundaries.

## 9.9 Verification must be independent

Implementers naturally overtrust their own changes. Models do so even more. For important work, verification should be a dedicated independent phase, ideally with independent role ownership. Otherwise "done" quickly degrades into "written and feels fine."

## 9.10 Team institutions matter more than personal tricks

An expert can tame an agent by experience. A team cannot rely on that. Teams need:

- layered `CLAUDE.md`
- explicit approval boundaries
- executable skills
- lifecycle hooks
- traceable transcripts
- unified verification definitions

Only when personal technique is institutionalized can agent systems become organizational capability rather than personal craft.

## 9.11 One final sentence

If the whole book must be compressed one more time:

> Harness Engineering asks how systems can still behave like engineering systems when models themselves are not reliable.

What Claude Code source really teaches is restraint: treat instability as known input, then design prompt, loop, tools, memory, compact, recovery, verification, and team workflow around that input. That is exactly why it is worth studying as a design specimen.

At this point the conclusion is simpler than the path. The hard part is not saying principles, but accepting them: harness over excitement, institutions over cleverness, and verification over confidence. Teams that internalize these three are already standing at the door of Harness Engineering.
