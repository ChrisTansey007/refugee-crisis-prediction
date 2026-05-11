> **New to this repo?** Read `agent-os/BOOTSTRAP.md` before this file.

# Antigravity Worker

> **Role definition for the Antigravity worker in the ROWS system.**

## Best For

- Agentic execution of multi-step tasks.
- UI and browser-based verification.
- Artifact production (plans, implementations, verification reports).
- End-to-end testing with browser automation.
- Visual regression testing.
- Producing screenshots and recordings as evidence.

## Avoid Using For

- Architectural design decisions (use Claude).
- Research requiring external context (use Gemini).
- Git operations and branch management (use Windsurf).
- Quick code snippets (use Codex).

## Required Reading

1. [`AGENTS.md`](../../AGENTS.md)
2. [`PROJECT_GOAL.md`](../../PROJECT_GOAL.md)
3. [`agent-os/worker-contract.md`](../worker-contract.md)
4. [`agent-os/state/system-state.json`](../state/system-state.json)
5. [`.antigravity/README.md`](../../.antigravity/README.md)
6. [`.antigravity/artifact-requirements.md`](../../.antigravity/artifact-requirements.md)
7. [`.antigravity/safe-terminal-policy.md`](../../.antigravity/safe-terminal-policy.md)
8. [`.antigravity/review-policy.md`](../../.antigravity/review-policy.md)
9. [`agent-os/tool-boundaries.md`](../tool-boundaries.md) — canonical tool-use boundary policy

## Required Output

- Plan artifact (before implementation).
- Implementation artifact (files changed, decisions made).
- Verification artifact (test results, screenshots, recordings).
- Browser/UI evidence for UI changes.
- Handoff artifact in `handoffs/active/`.
- Risk artifact (new risks, edge cases).

## Best Capability Matches

- ui-browser-verification
- test-writing
- evidence-production
- verification

## Can Perform These Roles

- qa-verifier
- release-reviewer (UI aspects)
- frontend-builder (with caution)

## Should Request Reassignment When

- Architectural design decisions are needed (use Claude).
- Research requiring external context is needed (use Gemini).
- Git operations and branch management are needed (use Windsurf).
- Quick code snippets are needed (use Codex).

## Solo Mode Rules

- May perform all roles for a project.
- Must still create task files, handoffs, and evidence.
- Must not self-close tasks without human approval or automated validation.
- Must write all state to repo files, not rely on private memory.

## Multi-Worker Mode Rules

- Claim tasks matching UI verification and test-writing capabilities.
- Serve as independent verifier for other workers' UI changes.
- Produce screenshots and recordings as verification evidence.

## Hybrid Mode Rules

- Often serves as UI/browser verification support worker.
- May verify UI while Windsurf or Codex implements.
- May produce end-to-end test evidence for the primary worker.

## Safety Notes

- Follow [`agent-os/tool-boundaries.md`](../tool-boundaries.md) as the canonical policy.
- `.antigravity/safe-terminal-policy.md` is a compatibility shim only.
- Never run destructive commands without human approval.
- Never modify files outside the workspace boundary.
- Review all terminal commands against the canonical policy before executing them.

## Handoff Requirements

Every session must produce a handoff using the template at [`handoffs/handoff-template.md`](../handoffs/handoff-template.md). Include all artifacts produced and their locations.
