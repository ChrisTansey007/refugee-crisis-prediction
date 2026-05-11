# TASK-0002-fix-backend-startup-error

## Goal
Fix the backend startup error caused by extra environment variables that are not defined in the Settings class.

## Context
When starting the backend server, we get a pydantic validation error: "Extra inputs are not permitted" for various environment variables (openrouter_api_key, terminal_modal_image, etc.). This prevents the server from starting.

## Acceptance Criteria
- The backend server starts without validation errors.
- The health endpoint returns 200 OK.

## Steps
1. Identify the source of the extra environment variables (likely from the shell environment).
2. Either unset these variables or adjust the Settings class to ignore extra fields.
3. Verify the server starts and the health endpoint works.

## Definition of Done
- The backend server is running and responding to health checks.