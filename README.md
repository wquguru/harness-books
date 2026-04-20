# Harness Books

[中文 README](./README.zh-CN.md)

[![Read Online](https://img.shields.io/badge/Read%20Online-Harness%20Books-16a34a?style=flat-square&logo=googlechrome&logoColor=white)](https://harness-books.agentway.dev/en/)
[![About AgentWay](https://img.shields.io/badge/About-AgentWay-22c55e?style=flat-square&logo=bookstack&logoColor=white)](https://agentway.dev)

Two books on harness engineering. They pursue the same engineering question: once a code-writing model is placed inside terminals, repositories, permission systems, and team workflows, what keeps the overall system bounded, continuous, and accountable for consequences?

<table>
  <tr>
    <td align="center" valign="top" width="50%">
      <a href="https://harness-books.agentway.dev/en/book1-claude-code/">
        <img src="./book1-claude-code/assets/cover-wxb-en.svg" alt="Harness Engineering: A Design Guide to Claude Code" width="280">
      </a>
      <br>
      <strong>Harness Engineering: A Design Guide to Claude Code</strong>
      <br>
      <a href="https://harness-books.agentway.dev/en/book1-claude-code/">Read online</a> ·
      <a href="https://harness-books.agentway.dev/en/book1-claude-code/exported/book1-claude-code-en.pdf">Download PDF</a> ·
      <a href="https://harness-books.agentway.dev/en/book1-claude-code/exported/book1-claude-code-en.epub">Download EPUB</a>
    </td>
    <td align="center" valign="top" width="50%">
      <a href="https://harness-books.agentway.dev/en/book2-comparing/">
        <img src="./book2-comparing/assets/cover-wxb-en.svg" alt="The Harness Design Philosophies of Claude Code and Codex" width="280">
      </a>
      <br>
      <strong>The Harness Design Philosophies of Claude Code and Codex</strong>
      <br>
      <a href="https://harness-books.agentway.dev/en/book2-comparing/">Read online</a> ·
      <a href="https://harness-books.agentway.dev/en/book2-comparing/exported/book2-comparing-en.pdf">Download PDF</a> ·
      <a href="https://harness-books.agentway.dev/en/book2-comparing/exported/book2-comparing-en.epub">Download EPUB</a>
    </td>
  </tr>
</table>

These books are not meant to walk line by line through the source code. They focus on how a harness organizes constraints and execution, and how an inherently unstable model can be folded into a sustainable engineering order. Prompt layering, query loops, permission decisions, context governance, failure recovery, multi-agent verification, local rules, and team institutions together form the organ system of a harness. The real danger is not that a model occasionally says something wrong, but that the system has no structure for handling consequences.

## Core Claims

- Harness engineering is about how constraint structures organize execution.
- Once a code-writing model enters a real engineering environment, the main problem is no longer answer quality but behavioral consequences.
- Prompts, tools, permissions, state, recovery, verification, and institutions are not accessories around the system. They are organs in the same control structure.
- When comparing agent systems, the key question is not the feature checklist but where order is actually placed.
- If a team cannot turn individual experience into reusable rules, it will struggle to turn an agent into a stable system.

## What The Two Books Focus On

### Book 1: A Design Guide to Claude Code

The first book uses Claude Code as the observation target and concentrates on runtime structure. Its concern is why a system eventually has to grow components such as a control plane, query loop, tool permissions, context governance, recovery paths, multi-agent verification, and team rules.

Start with Book 1 if these are the questions you care about:

- Why harness engineering is not just prompt engineering at a larger scale
- Why prompts are fundamentally part of the control plane rather than a chat box
- Why model mistakes should be treated as a runtime norm rather than an exceptional event
- Why multi-agent work and verification should not be blended into one vague mechanism
- How a team can solidify personal experience into reusable engineering institutions

### Book 2: Comparing Claude Code and Codex

The second book places Claude Code and Codex side by side and asks where each harness places order. One path starts from runtime discipline; the other starts from a more structured control layer. Both systems can work, but they distribute authority differently.

Start with Book 2 if you care more about system choice, architectural judgment, or what to learn when building your own harness:

- What the biggest control-plane divergence is between Claude Code and Codex
- How to align the roles of query loops, threads, rollouts, and state
- What governance roles are played by permissions, sandboxes, and policy languages
- How skills, hooks, and local rules encode organizational habits into the system
- If you want to build your own harness, who to learn from first and which layer to study first

## Suggested Reading Paths

- Want the full frame first: read Book 1, then Book 2.
- Already familiar with coding-agent tools and want the architectural split directly: start with Book 2.
- Only want the conclusions: read Book 1 Chapter 9 plus Book 2 Chapter 7.

<details>
<summary><strong>Full Table of Contents</strong></summary>

### Book 1 — Harness Engineering: A Design Guide to Claude Code

- [Introduction](./book1-claude-code/locales/en/index.md)
- [Preface: Harness, Terminals, and Engineering Constraints](./book1-claude-code/locales/en/preface.md)
- [Chapter 1 Why Harness Engineering Matters](./book1-claude-code/locales/en/chapter-01-why-harness-engineering.md)
- [Chapter 2 Prompt Is Not Personality, Prompt Is the Control Plane](./book1-claude-code/locales/en/chapter-02-prompt-is-control-plane.md)
- [Chapter 3 Query Loop: The Heartbeat of an Agent System](./book1-claude-code/locales/en/chapter-03-query-loop-heartbeat.md)
- [Chapter 4 Tools, Permissions, and Interrupts: Why Agents Cannot Touch the World Directly](./book1-claude-code/locales/en/chapter-04-tools-permissions-interrupts.md)
- [Chapter 5 Context Governance: Memory, CLAUDE.md, and Compact as a Budgeting Regime](./book1-claude-code/locales/en/chapter-05-context-memory-compact.md)
- [Chapter 6 Errors and Recovery: An Agent System That Keeps Working After Failure](./book1-claude-code/locales/en/chapter-06-errors-and-recovery.md)
- [Chapter 7 Multi-Agent Work and Verification: Managing Instability Through Division of Labor](./book1-claude-code/locales/en/chapter-07-multi-agent-and-verification.md)
- [Chapter 8 Team Adoption: Turning a Smart Tool into a Reusable Institution](./book1-claude-code/locales/en/chapter-08-team-landing-practices.md)
- [Chapter 9 Ten Principles of Harness Engineering](./book1-claude-code/locales/en/chapter-09-ten-principles.md)
- [Appendix A Checklists: Turning Principles into Executable Constraints](./book1-claude-code/locales/en/appendix-a-checklists.md)
- [Appendix B Diagrams: Drawing the Runtime Skeleton](./book1-claude-code/locales/en/appendix-b-diagram-notes.md)
- [Appendix C Source Map: Which Files Ground Each Chapter](./book1-claude-code/locales/en/appendix-c-source-map.md)

### Book 2 — The Harness Design Philosophies of Claude Code and Codex

- [Introduction](./book2-comparing/locales/en/index.md)
- [Reading Map: How to Understand Book 1 and This Comparative Book Together](./book2-comparing/locales/en/chapter-00-reading-map.md)
- [Preface: Two Harnesses, Not Accessories on the Same Horse](./book2-comparing/locales/en/preface.md)
- [Chapter 1: Why We Compare Claude Code and Codex](./book2-comparing/locales/en/chapter-01-why-this-comparison.md)
- [Chapter 2: Two Control Planes: Prompt Assembly and Instruction Fragments](./book2-comparing/locales/en/chapter-02-two-control-planes.md)
- [Chapter 3: Where the Heartbeat Lives: Query Loop Compared with Thread, Rollout, and State](./book2-comparing/locales/en/chapter-03-loop-thread-and-rollout.md)
- [Chapter 4: Tools, Sandboxes, and Policy Languages: Who Stops the Model from Moving Too Fast](./book2-comparing/locales/en/chapter-04-tools-sandbox-and-exec-policy.md)
- [Chapter 5: Skills, Hooks, and Local Rules: How a System Learns Local Discipline](./book2-comparing/locales/en/chapter-05-skills-hooks-and-local-governance.md)
- [Chapter 6: Delegation, Verification, and Persistent State: Who Prevents a System from Grading Itself](./book2-comparing/locales/en/chapter-06-delegation-verification-and-state.md)
- [Chapter 7: Convergence Through Different Roads, or Separate Branches](./book2-comparing/locales/en/chapter-07-convergence-and-divergence.md)
- [Chapter 8: If You Are Building Your Own Harness, What to Study First](./book2-comparing/locales/en/chapter-08-how-to-choose-or-build.md)
- [Appendix A: Source Map That Underpins the Comparison](./book2-comparing/locales/en/appendix-a-source-map.md)
- [Appendix B: Checklist to Determine Where Your Harness Sits](./book2-comparing/locales/en/appendix-b-checklists.md)

</details>

## Want To Keep Practicing? Try AgentWay

<table>
<tr>
<td width="180" align="center" valign="middle">
  <a href="https://agentway.dev/">
    <img src="assets/agentway-logo.svg" alt="AgentWay" width="150">
  </a>
</td>
<td valign="middle">
  <b><a href="https://agentway.dev/">AgentWay</a></b> is a related but separate practice platform. Harness Books explains control structures, engineering judgments, and architectural divergences. AgentWay is where these ideas continue into training paths, drills, project exercises, and agent PoCs.
</td>
</tr>
</table>

## Local Build

Build the two locale-aware Honkit sites and then assemble the unified Pages site:

```bash
python3 tools/book-kit/build_honkit.py book1-claude-code
python3 tools/book-kit/build_honkit.py book1-claude-code --locale en
python3 tools/book-kit/build_honkit.py book2-comparing
python3 tools/book-kit/build_honkit.py book2-comparing --locale en
python3 tools/book-kit/build_pages_site.py
```

Final output is written to `dist/`.

### EPUB Export

Export both books to EPUB format for e-readers:

```bash
# Install dependencies (pandoc, librsvg, poppler)
# See system-dependencies.md for detailed installation instructions
# Example using conda: conda create -n epub pandoc librsvg poppler -c conda-forge

# Export Chinese versions (default)
python3 tools/book-kit/export_epub.py book1-claude-code
python3 tools/book-kit/export_epub.py book2-comparing

# Export English versions
python3 tools/book-kit/export_epub.py book1-claude-code --locale en
python3 tools/book-kit/export_epub.py book2-comparing --locale en
```

EPUB files are written to each book's `exported/` directory:
- Chinese: `book1-claude-code/exported/book1-claude-code.epub`, `book2-comparing/exported/book2-comparing.epub`
- English: `book1-claude-code/exported/book1-claude-code-en.epub`, `book2-comparing/exported/book2-comparing-en.epub`

---

<sub>Keywords: Harness Engineering, Claude Code guide, Claude Code vs Codex, AI coding agent, control plane, query loop, agent recovery, agent verification, local governance, approval policy</sub>
