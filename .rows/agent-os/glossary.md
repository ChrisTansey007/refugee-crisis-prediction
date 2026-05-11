# Glossary

> **Concise ROWS vocabulary for new contributors and workers.**

- **Agent OS** — The file-based operating system under `agent-os/` that coordinates workers.
- **Agent** — A worker tool or human performing a role.
- **Artifact** — A durable repo file that records state, evidence, or work output.
- **Assignment** — The mapping from task to role, capability, preferred worker, and active worker.
- **Capability** — A skill the task requires, such as code implementation or verification.
- **Control plane** — The repository itself; the source of truth for coordination.
- **DoD** — Definition of Done; the criteria required before a task can close.
- **Execution mode** — Solo, multi-worker, or hybrid coordination style.
- **Handoff** — A session summary that enables continuation by another worker.
- **Intentional placeholder** — A bracketed token like `[PROJECT_NAME]` meant to be replaced after forking.
- **Lock** — A required advisory file that marks claimed work and reduces collisions.
- **MCP** — Model Context Protocol, a structured way to connect tools and resources.
- **Objective** — The task's measurable goal.
- **Prompt injection** — Untrusted external content that tries to steer a worker.
- **Role** — The job being performed, such as backend-builder or qa-verifier.
- **Task** — A claimable unit of work represented by a file in the task lifecycle.
- **Template neutrality** — The requirement that this repo stay reusable and app-agnostic until forked.
- **Verification evidence** — Output proving the work meets acceptance criteria.
- **Worker** — The AI tool or human performing a task.
- **Worker contract** — The rules all workers must follow.
- **Worker replaceability** — The ability to switch tools without losing continuity.
