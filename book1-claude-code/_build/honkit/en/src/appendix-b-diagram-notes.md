# Appendix B Diagrams: Drawing the Runtime Skeleton

Previous chapters explained runtime structure in text. Text is necessary, but some structures become clearer as diagrams: Claude Code is an explicit state-machine system, not "a pile of prompts plus a few tools."

## B.1 Diagram 1: Claude Code global control plane

![Claude Code global control plane](diagrams/diag-01-claude-code-control-plane.png)

This should not be drawn as a children-book flowchart like "user -> model -> tool -> output," because that hides the actual organs. A more accurate view is five layers:

1. user interaction layer
2. control plane layer
3. execution loop layer
4. external capability layer
5. persistence and observability layer

The point is not listing every module. The point is:

- model is neither topmost nor bottommost
- model is one phase inside query loop
- control and recovery planes are what hold the system together

## B.2 Diagram 2: Query loop main cycle and recovery branches

![Query loop main cycle](diagrams/diag-b02-01-query-loop-main.png)

![Query loop recovery branches](diagrams/diag-b02-02-query-loop-recovery-branches.png)

## B.3 Diagram 3: Tool batch ordering and StreamingToolExecutor

![Tool batch ordering](diagrams/diag-b03-01-tool-batch-ordering.png)

![StreamingToolExecutor lifecycle](diagrams/diag-b03-02-streaming-tool-executor.png)

## B.4 Diagram 4: Context sources and compact rebuild

![Context sources and budget](diagrams/diag-b04-01-context-sources-and-budget.png)

![Compact rebuild pipeline](diagrams/diag-b04-02-compact-rebuild-pipeline.png)

## B.5 Diagram 5: Coordinator-worker flow and verification separation

![Coordinator and worker flow](diagrams/diag-b05-01-coordinator-worker-flow.png)

![Verification separation](diagrams/diag-b05-02-verification-separation.png)

## B.6 Diagram 6: Team governance map

![Team governance map](diagrams/diag-06-team-governance-map.png)
