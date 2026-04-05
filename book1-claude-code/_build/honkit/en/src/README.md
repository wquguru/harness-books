# Harness Engineering: A Design Guide to Claude Code

![Cover: Harness Engineering: A Design Guide to Claude Code](assets/cover-wxb-en.svg)

Subtitle: Engineering principles for controllable AI coding systems distilled from source-level runtime design

> This book is not asking whether a model can write code. It asks how to keep a code-writing model from steering an engineering system off course once it is plugged into terminals, repositories, and team workflows.

This is not a stitched set of source comments, and not a feature tour. It focuses on how Claude Code constrains an unstable model into a sustainable engineering order, where control plane, main loop, tool permissions, context governance, recovery paths, multi-agent verification, and team practices form one coherent skeleton.

This book starts from three reading assumptions:

- The center of gravity is not model capability, but how the harness organizes constraints and execution
- The goal is not line-by-line function narration, but why the runtime had to grow this way
- The value is not personal trick collection, but turning structure into reusable team practice

Recommended reading order:

1. [Preface: Harness, Terminals, and Engineering Constraints](preface.md)
2. [Chapter 1 Why Harness Engineering Matters](chapter-01-why-harness-engineering.md)
3. [Chapter 2 Prompt Is Not Personality, Prompt Is the Control Plane](chapter-02-prompt-is-control-plane.md)
4. [Chapter 3 Query Loop: The Heartbeat of an Agent System](chapter-03-query-loop-heartbeat.md)
5. [Chapter 4 Tools, Permissions, and Interrupts: Why Agents Cannot Touch the World Directly](chapter-04-tools-permissions-interrupts.md)
6. [Chapter 5 Context Governance: Memory, CLAUDE.md, and Compact as a Budgeting Regime](chapter-05-context-memory-compact.md)
7. [Chapter 6 Errors and Recovery: An Agent System That Keeps Working After Failure](chapter-06-errors-and-recovery.md)
8. [Chapter 7 Multi-Agent Work and Verification: Managing Instability Through Division of Labor](chapter-07-multi-agent-and-verification.md)
9. [Chapter 8 Team Adoption: Turning a Smart Tool into a Reusable Institution](chapter-08-team-landing-practices.md)
10. [Chapter 9 Ten Principles of Harness Engineering](chapter-09-ten-principles.md)
11. [Appendix A Checklists: Turning Principles into Executable Constraints](appendix-a-checklists.md)
12. [Appendix B Diagrams: Drawing the Runtime Skeleton](appendix-b-diagram-notes.md)
13. [Appendix C Source Map: Which Files Ground Each Chapter](appendix-c-source-map.md)

If you only want the consolidated judgment first, jump to [Chapter 9](chapter-09-ten-principles.md).
