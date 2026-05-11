# Development Setup

> **Customize after forking. How to set up [PROJECT_NAME] for local development.**

## Prerequisites

- [Node.js](https://nodejs.org/) v20+
- [Git](https://git-scm.com/)
- Any project-specific services your fork requires (database, queue, etc.)

## Quick Start

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO

# Initialize the fork
npm run init

# Install dependencies
npm install

# Set up environment
cp .env.example .env
# Edit .env with your configuration
# Keep .env.example committed; keep .env local and secret-free

# Run database migrations
npm run migrate

# Start development server
npm run dev
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | `3000` |
| `DATABASE_URL` | Database connection string | — |
| `[OTHER_VAR]` | [Description] | — |

## Scripts

See [`commands.md`](./commands.md) for all available commands.

`npm run validate:json` validates JSON syntax and enforces the repo's state schemas when a matching schema exists in `agent-os/schemas/`.

For multi-worker work, run `npm run setup:worktree -- <worker> <task-id>` before starting parallel edits so each worker gets an isolated checkout.

## Related Files

- [`commands.md`](./commands.md) — Available commands
- [`coding-standards.md`](./coding-standards.md) — Coding standards
- [`../../agent-os/state/system-state.json`](../../agent-os/state/system-state.json) — System state
