# ROWS Bootstrap — Agent Entry Point

> **Read this first. Before AGENTS.md. Before touching any task.**
>
> This file equips you to operate ROWS effectively. It takes 2–4 minutes to complete. Do not skip it.

---

## What Is ROWS?

ROWS (Repo-Orchestrated Worker System) is a file-based multi-agent orchestration framework. Tasks are physical files that move through directories. The repo is the single source of truth. You are one worker in a larger system that may include other agents or human collaborators.

You need to understand the system before you can work inside it safely. That is what this bootstrap does.

---

## Step 1 — Identify Your Agent Type

Find your type in this table:

| You are... | Your type |
|---|---|
| Windsurf (Cascade AI) | `windsurf` |
| OpenAI Codex / codex-1 | `codex` |
| Claude (Anthropic) | `claude` |
| Cursor AI | `cursor` |
| Any other agent | `generic` |

---

## Step 2 — Go To Your Agent Folder

Navigate to your agent-specific resources:

```
agent-os/agents/[your-type]/
```

That folder contains:

- **`install.md`** — your self-installation procedure (do this now)
- **`reading-list.md`** — ordered list of what to read and in what priority

---

## Step 3 — Run Your Self-Install

Read `agent-os/agents/[your-type]/install.md` and follow it completely.

Self-install will do one of two things depending on your capabilities:

**If you can write files to the repo** (Windsurf, Cursor):
- Copy platform-specific skill/workflow files into your expected locations (`.windsurf/workflows/`, `.cursor/rules/`, etc.)
- After this, your platform's native skill-loading mechanism will pick them up automatically

**If you are read-only or session-based** (Claude, Codex, generic):
- You will receive a structured reading list
- Load each required file into your active context before proceeding
- Mark optional files based on the work you are about to do

---

## Step 4 — Load Universal Skills

Regardless of agent type, read the universal skills index:

```
agent-os/agents/universal/index.md
```

This lists every ROWS skill, organized by phase, with required vs optional marked. Load the required ones now.

## Layer Model

Before you proceed, internalize ROWS's two-layer model:

- **Knowledge layer:** what is true and why. Read `PROJECT_GOAL.md`, `PROJECT_CONTEXT.md`, ADRs, the decision register, and operating docs here.
- **Work layer:** what is happening now. Read tasks, handoffs, blockers, locks, and triggers here.

The short version:

- knowledge tells you how to think
- work tells you what to do next

Read [`agent-os/knowledge-model.md`](./knowledge-model.md) for the canonical explanation.

---

## Step 5 — Proceed to AGENTS.md

You are now equipped. Read `AGENTS.md` for the full ruleset, then follow the startup sequence defined there.

**Do not read AGENTS.md before completing steps 1–4.** The rules reference skills and concepts you need context on before encountering them.

---

## If You Do Not Know Your Agent Type

Read `agent-os/agents/registry.md` — it maps capability signals to agent types so you can self-identify.

If you genuinely cannot determine your type, use `generic`.

---

## Why This Exists

Every agent that has operated in this repo left their mark in the handoffs, decisions, and task files. You need to understand ROWS conventions before you read those files or you will misinterpret them. Bootstrap is the guarantee that any agent — no matter where it came from — starts from a shared foundation.
