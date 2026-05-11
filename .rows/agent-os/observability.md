# Observability

> **ROWS does not mandate any specific observability stack.** This document explains where external observability tools can attach without becoming part of the repo's source of truth.

## Core rule

Use task IDs, handoff IDs, milestone IDs, and report filenames as the stable correlation IDs for logs, traces, screenshots, and external dashboards.

## What belongs outside the repo

- Hosted logging
- APM / tracing platforms
- LLM observability SaaS
- Browser session recordings

## What belongs in the repo

- Handoffs
- Verification reports
- Status reports
- Milestone and proposal records
- Explicit notes about which task or milestone an external artifact belongs to

## Guidance

If a tool emits external telemetry, reference it in the relevant handoff or verification report rather than copying secrets or raw payloads into the repo.
