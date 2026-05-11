# Example Proposal: Multi-Worker Delivery Sequence

> **Illustrative only. Not active repo state.**

## Proposal ID

PROPOSAL-0001

## Title

Coordinate a three-worker delivery sequence for a complex template update

## Problem / Opportunity

A complex change touches docs, validation, and examples. One worker can do it, but a split sequence would reduce merge risk.

## Proposed Approach

1. Hermes decomposes the work and writes the task set.
2. Windsurf implements file changes in a worktree.
3. Antigravity verifies the final state and captures evidence.

## Expected Benefits

- Lower risk of overwriting shared files
- Clearer evidence trail
- Faster review loop

## Risks / Tradeoffs

- More coordination overhead
- Requires clean task handoffs

## Evidence / Context

- `agent-os/task-lifecycle.md`
- `agent-os/worktree-strategy.md`
- `examples/sample-multi-worker-walkthrough.md`

## Next Step

Promote this into a real task or milestone if the change set is approved.
