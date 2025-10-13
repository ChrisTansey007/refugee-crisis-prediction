# Contributing Guidelines

## Branching Strategy
- `main`: Protected, releases only
- `develop`: Integration branch
- `feature/<ticket>`: Feature branches (e.g., `feature/p1-backend-skeleton`)

## Conventional Commits
- `feat: add health endpoint`
- `fix: correct db url parsing`
- `docs: update README with quick start`
- `chore: bump dependencies`

## Pull Requests
- Link issue/ticket in description
- Include screenshots for UI changes
- Add/Update tests for changed code
- Update docs where applicable

## Code Style
- Backend: Black, Ruff, isort; type hints required
- Frontend: ESLint, Prettier, TS strict
- No TODOs in merged code; use issues instead

## Testing
- Backend: `pytest` with coverage (≥80% for touched files)
- Frontend: Vitest/RTL (once scaffolded)
- E2E: Playwright (Phase 5)

## Review Process
- 1+ reviewer approval required
- CI must be green (lint + tests)
- Keep PRs small (<400 loc) where possible
