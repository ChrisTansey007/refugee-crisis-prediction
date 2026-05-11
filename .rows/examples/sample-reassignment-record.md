# Example: Reassignment Record

> **This is a fictional example for "TaskFlow Lite." This is NOT an active reassignment record.**

---

# Reassignment Record: TASK-0008

## Metadata

- **Task ID:** TASK-0008
- **Task Title:** Research State Management Libraries
- **Original Worker:** gemini
- **New Worker:** claude
- **Date of Reassignment:** 2026-05-06
- **Reason:** Gemini API unavailable. Claude has research and long-context reasoning capabilities that match the task requirements.

## Pre-Reassignment State

- **Task Status:** in-progress
- **Original Lock:** `locks/TASK-0008-gemini.json` — marked stale
- **Handoff Written:** Yes — `handoffs/active/TASK-0008-gemini-2026-05-06.md`
- **Work Completed:** Initial research on 3 of 5 candidate libraries. Comparison table partially filled.

## Handoff Summary from Original Worker

Gemini researched Zustand, Jotai, and Redux Toolkit. Created a comparison table with bundle size, learning curve, and community size. Two libraries remaining: MobX and Recoil. Key finding so far: Zustand is the lightest option and best fit for TaskFlow Lite's simple state needs.

## Reassignment Conditions

- [x] Original worker wrote handoff
- [x] Original lock marked stale
- [x] Reassignment reason documented
- [x] New worker has required capabilities (research, documentation)
- [x] Human owner notified

## Instructions for New Worker

1. Read this reassignment record.
2. Read the original handoff: `handoffs/active/TASK-0008-gemini-2026-05-06.md`
3. Read the task file: `tasks/in-progress/TASK-0008.md`
4. Review the partial comparison table created by Gemini.
5. Complete research on remaining libraries (MobX, Recoil).
6. Finalize the comparison table and write a recommendation.
7. Create a new lock: `locks/TASK-0008-claude.json`
8. Write your own handoff upon completion.

## Continuity Notes

The comparison table format is: Library | Bundle Size | Learning Curve | Community | Best For | Recommendation. Gemini completed 3 of 5 rows. The table is in the handoff file. Do not restart research from scratch — continue from where Gemini left off.
