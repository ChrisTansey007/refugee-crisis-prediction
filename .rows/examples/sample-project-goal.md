# Example: Filled-Out PROJECT_GOAL.md

> **This is a fictional example. It shows what a completed `PROJECT_GOAL.md` looks like for "TaskFlow Lite" — a small task tracking app for solo builders. This is NOT a real project.**

---

## Project Name

TaskFlow Lite

## One-Sentence Goal

A minimal task tracking app that lets solo builders organize projects, track tasks across customizable columns, and see progress at a glance.

## Long-Form Goal

Solo builders — freelancers, indie hackers, and side-project developers — need a simple way to track their work without the overhead of Jira, Notion, or Trello. Existing tools are either too complex or too generic.

TaskFlow Lite provides a focused task board with three columns (To Do, In Progress, Done), project organization, and a daily summary view. It runs entirely in the browser with local storage, so there is no account creation, no server, and no setup.

Success means a solo builder can open the app, create a project, add tasks, move them between columns, and see what they accomplished today — all in under 30 seconds.

## Target Users

- **Primary persona:** Solo builders — freelancers, indie hackers, and side-project developers who want minimal task tracking without account creation or setup.
- **Secondary persona:** None. The app is intentionally single-user.

## Primary Outcomes

1. Users can create projects and add tasks in under 30 seconds.
2. Users can move tasks between To Do, In Progress, and Done columns via drag-and-drop.
3. Users can see a daily summary of completed tasks.

## Non-Goals

1. Multi-user collaboration or sharing.
2. Mobile apps (web-only, responsive).
3. Integrations with external tools (GitHub, Slack, etc.).

## Constraints

- **Budget:** $0 (personal project)
- **Timeline:** 2 weeks for MVP
- **Team size:** Solo developer + AI workers
- **Platform:** Web (browser-based, local storage)
- **Compliance:** None
- **Other:** Must work offline; no server required

## Preferred Tech Stack

- **Frontend:** React with TypeScript
- **Backend:** None (localStorage only)
- **Database:** None (localStorage)
- **Hosting:** Vercel (static site)
- **CI/CD:** GitHub Actions
- **Other:** TailwindCSS for styling, Vitest for tests

## Deployment Target

- **Environment:** Web (static site)
- **Hosting provider:** Vercel
- **Domain:** [DOMAIN_PLACEHOLDER]

## Success Criteria

1. All three primary outcomes are functional.
2. App loads in under 2 seconds on a 3G connection.
3. Zero runtime errors in production build.
4. 100% of tasks persist across browser sessions.

## First Milestone

MVP with project creation, three-column task board, drag-and-drop, and daily summary.

## Initial Risks

1. localStorage limits may restrict task volume.
2. Drag-and-drop may have accessibility issues.
3. No backend means no data recovery if localStorage is cleared.

## Preferred Execution Mode

Solo Worker Mode — one worker (Windsurf) does everything with human review.

## Worker Preferences

- **Primary:** Windsurf
- **For architecture:** Claude (advisory)
- **For implementation:** Windsurf
- **For UI verification:** Antigravity (if available)

## Human Review Preference

Review critical only — I will review architecture and major features.

## Worker Autonomy

Full autonomy — workers may claim, implement, and submit for review without asking.
