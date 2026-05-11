# Glossary

> **Customize after forking. Define project-specific terminology so all workers share a common vocabulary.**

## Project Terms

| Term | Definition |
|------|------------|
| Migration Forecasting System | The AI-powered platform for predicting forced migration patterns using multi-modal spatiotemporal data. |
| Forced Migration | The movement of people who have been compelled to leave their homes due to conflict, persecution, disaster, or other compelling reasons. |
| IDP | Internally Displaced Person - someone forced to flee their home but who remains within their country's borders. |
| Refugee | Someone who has been forced to flee their country due to persecution, war, or violence. |
| Asylum Seeker | Someone who has left their country and is seeking protection from persecution and serious human rights violations in another country, but who hasn't yet been legally recognized as a refugee. |
| Spatiotemporal Data | Data that has both spatial (location-based) and temporal (time-based) dimensions. |
| ETL | Extract, Transform, Load - the process of extracting data from sources, transforming it into a suitable format, and loading it into a destination. |
| ML Model | Machine Learning model - an algorithm that learns patterns from data to make predictions or decisions. |
| LSTM | Long Short-Term Memory - a type of recurrent neural network capable of learning long-term dependencies, particularly suited for sequence prediction problems. |
| Ensemble Model | A machine learning model that combines multiple individual models to improve predictive performance. |
| API | Application Programming Interface - a set of rules and specifications that software programs can follow to communicate with each other. |
| Connector | A software component that interfaces with an external data source to extract data. |
| Ingestion | The process of importing data from external sources into the system for processing and storage. |
| Staging Table | A temporary database table used to hold data during the ETL process before it is moved to its final destination. |
| Data Displacement | In the context of this project, refers to the measured movement of people (refugees, IDPs) from one location to another. |
| Economic Indicators | Statistical metrics that provide insights into the economic performance of a country or region (e.g., GDP, unemployment rate). |
| Conflict Data | Information about violent events, including battles, explosions, and violence against civilians, often used to predict migration. |
| Climate Data | Meteorological and environmental data (e.g., temperature, precipitation, vegetation health) that can influence migration patterns. |
| Explainable AI (XAI) | Techniques and methods in artificial intelligence that make the results of AI models understandable to humans. |
| Feature Engineering | The process of using domain knowledge to extract features from raw data that make machine learning algorithms work more effectively. |
| Hyperparameter Tuning | The process of finding the optimal set of hyperparameters for a learning algorithm. |
| Cross-validation | A technique for assessing how the results of a statistical analysis will generalize to an independent data set. |
| Model Drift | The degradation of a model's predictive power over time due to changes in the underlying data distribution. |
| CI/CD | Continuous Integration/Continuous Deployment - a method to frequently deliver apps to customers by introducing automation into the stages of app development. |
| Docker | A platform for developing, shipping, and running applications in containers. |
| Kubernetes | An open-source system for automating deployment, scaling, and management of containerized applications. |
| Render | A cloud platform for deploying and scaling web applications, APIs, and static sites. |
| Swagger UI | A tool for visualizing and interacting with API documentation generated from OpenAPI specifications. |
| Alembic | A lightweight database migration tool for usage with SQLAlchemy. |
| Redis | An in-memory data structure store, used as a database, cache, and message broker. |
| PostgreSQL | A powerful, open source object-relational database system. |
| PostGIS | A spatial database extender for PostgreSQL object-relational database. It adds support for geographic objects. |
| FastAPI | A modern, fast (high-performance), web framework for building APIs with Python based on standard Python type hints. |
| React | A JavaScript library for building user interfaces, particularly single-page applications. |
| TypeScript | A strongly typed programming language that builds on JavaScript, giving you better tooling at any scale. |
| Unit Test | A test that validates the behavior of a small, isolated unit of code (e.g., a function or method). |
| Integration Test | A test that verifies that different modules or services used by your application work well together. |
| End-to-End Test | A test that validates the entire flow of an application from start to finish, simulating real user scenarios. |
| Linting | The process of running a program that will analyse code for potential errors. |
| Code Coverage | A measure used to describe the degree to which the source code of a program is executed when a particular test suite runs. |
| Pull Request (PR) | A method of submitting contributions to a development project, typically used in Git-based version control systems. |
| Issue | A feature request, bug report, or general task tracked in a project management system (e.g., GitHub Issues). |
| Milestone | A specific point in time within a project lifecycle used to measure progress toward a ultimate goal. |
| Roadmap | A strategic plan that defines a goal or desired outcome and includes the major steps or milestones needed to reach it. |
| User Story | An informal, natural language description of one or more features of a software system, written from the perspective of an end user. |
| Acceptance Criteria | Conditions that a software product must satisfy to be accepted by a user, customer, or other stakeholders. |
| PRD | Product Requirements Document - a document that describes the capabilities that a product must have in order to be considered complete. |
| ADR | Architecture Decision Record - a document that captures an important architectural decision made along with its context and consequences. |
| Handoff | A Markdown file documenting a worker session's work, placed in `agent-os/handoffs/active/`. |
| Lock | An advisory JSON file in `agent-os/locks/` that declares a worker's intent to modify specific files. |
| Verification Gate | A checkpoint that must be passed before a task can be marked done. |
| Worker | An AI tool (Windsurf, Codex, Claude, Gemini, Hermes, Antigravity) that executes repo-defined tasks. |
| Task | A unit of work defined as a Markdown file in `agent-os/tasks/`. |
| Agent OS | The Reliable Orchestration of Worker Systems (ROWS) - a system for managing AI-assisted development workflows. |
| Backlog | A list of tasks that are planned but not yet started. |
| Ready | A list of tasks that are ready to be worked on (dependencies met, blockers resolved). |
| In Progress | A list of tasks that are currently being worked on. |
| Review | A list of tasks that have been completed and are awaiting review. |
| Done | A list of tasks that have been completed and reviewed. |
| System State | A JSON file that tracks the current phase, task counts, and other metadata about the project's progress. |

## ROWS System Terms

| Term | Definition |
|------|------------|
| Worker | An AI tool (Windsurf, Codex, Claude, Gemini, Hermes, Antigravity) that executes repo-defined tasks. |
| Task | A unit of work defined as a Markdown file in `agent-os/tasks/`. |
| Handoff | A Markdown file documenting a worker session's work, placed in `agent-os/handoffs/active/`. |
| Lock | An advisory JSON file in `agent-os/locks/` that declares a worker's intent to modify specific files. |
| Verification Gate | A checkpoint that must be passed before a task can be marked done. |
| ADR | Architecture Decision Record — a document capturing a significant architectural choice. |

## How to Add Terms

When you introduce a new concept, add it to this glossary. Workers should reference this file to ensure consistent terminology.

## Related Files

- [`AGENTS.md`](../../AGENTS.md) — System constitution
- [`../05-decisions/decision-register.md`](../05-decisions/decision-register.md) — Decision register