# NYC Build and Crash — AI Agent Instructions

## 1. Purpose

This file defines how AI coding agents should operate within the NYC Build and Crash repository.

The project is a collaborative Data Engineering and Visualization assignment at the German International University (GIU).

Its objective is to investigate relationships between NYC building development and motor vehicle collisions through data cleaning, integration, analysis, and an interactive website.

This file is not a task request. The active user prompt determines what an agent should implement.

## 2. Project Documentation

Detailed project information is maintained in separate documents.

| Document                          | Contains                                                                          | Read When                               |
| --------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------- |
| [SPEC.md](docs/SPEC.md)           | University requirements, datasets, research objectives, grading, and deliverables | Understanding project requirements      |
| [TEAM_PLAN.md](docs/TEAM_PLAN.md) | Contributors, responsibilities, phases, deadlines, and dependencies               | Working on assigned tasks               |
| [CONTRACT.md](docs/CONTRACT.md)   | Naming conventions, schemas, interfaces, data standards, and handoffs             | Creating or modifying shared components |
| [README.md](README.md)            | Project overview, setup, execution, and deployment                                | Setting up or running the project       |

### Documentation Guidelines

* Read only the documents and sections relevant to the current task.
* Avoid repeatedly reading unchanged documentation.
* Do not duplicate information already defined in these documents.
* Verify the actual repository state instead of relying entirely on documentation.
* Distinguish proposed technical standards from team-approved decisions.
* Report conflicting requirements instead of silently choosing an interpretation.

The official university requirements take precedence over internal plans.

## 3. Development Environment

The project currently uses:

* Python for data processing.
* Pandas and NumPy for analysis.
* Matplotlib for exploratory visualization.
* Jupyter Notebooks for development and documentation.
* Git and GitHub for collaboration.

The website framework and deployment platform must be determined from the repository and confirmed team decisions.

### Environment Rules

* Prefer the existing project virtual environment.
* Verify dependencies before installing additional packages.
* Use project-relative paths whenever possible.
* Do not hardcode contributor-specific filesystem locations.
* Follow existing project commands and configurations.
* Avoid introducing unnecessary dependencies.

## 4. Agent Workflow

### Before Implementation

1. Understand the user's current request and expected deliverables.
2. Identify the active contributor and relevant project phase.
3. Consult the relevant project documentation.
4. Inspect existing implementations and dependencies.
5. Check whether the requested functionality already exists.
6. Identify the files that require modification.

### During Implementation

* Work only within the authorized scope.
* Respect contributor ownership and existing implementations.
* Follow the technical standards in `docs/CONTRACT.md`.
* Prefer readable, maintainable, and efficient solutions.
* Preserve existing functionality and source data.
* Document important decisions.
* Avoid unnecessary changes to unrelated files.
* Do not assume previously completed work is correct without relevant verification.

### After Implementation

1. Execute appropriate checks.
2. Validate the affected functionality.
3. Review modified files for unintended changes.
4. Identify unresolved issues.
5. Report the implementation results.

Never claim that an unexecuted test passed.

## 5. Git and Collaboration

* Inspect the current branch and working tree before editing.
* Preserve teammates' work and uncommitted changes.
* Follow the repository's established branching workflow.
* Do not modify another contributor's files without authorization.
* Do not commit or push unless authorized by the user or an established workflow.
* Never force-push, perform destructive resets, or rewrite shared history without explicit permission.
* Do not commit credentials, virtual environments, or excluded datasets.
* Coordinate changes that affect shared interfaces.

File naming, schemas, and component compatibility are governed by `docs/CONTRACT.md`.

## 6. Error Handling and Validation

When encountering an error:

1. Identify the failing operation.
2. Inspect the error message and relevant inputs.
3. Investigate the root cause.
4. Apply the smallest justified correction.
5. Re-run the affected checks.
6. Report unresolved problems.

Do not suppress errors to create the appearance of success.

For data-related tasks, validate relevant inputs, transformations, and outputs.

For website tasks, validate the affected functionality and build when feasible.

Distinguish verified results from assumptions.

## 7. Efficiency and Task Boundaries

Agents should work autonomously within the user's authorized scope.

Avoid:

* Reimplementing completed functionality.
* Repeatedly processing large datasets unnecessarily.
* Reinstalling existing dependencies.
* Creating redundant files.
* Rewriting unrelated components.
* Expanding into other phases without authorization.
* Producing excessive progress reports.

If an issue is discovered outside the assigned task, report it rather than silently expanding the implementation.

If a task is blocked, explain the blocker and complete any remaining feasible work.

## 8. Completion Report

After completing an authorized task, provide a concise summary covering:

1. Files created or modified.
2. Work completed.
3. Validation performed and results.
4. Remaining errors, warnings, or dependencies.

Do not claim that code was committed, pushed, deployed, or tested unless the action actually succeeded.

### Final Principle

* `SPEC.md` defines **what the project requires**.
* `TEAM_PLAN.md` defines **who does what and when**.
* `CONTRACT.md` defines **how components must work together**.
* `AGENTS.md` defines **how AI agents should work**.
* The active user prompt defines **what to implement now**.

Follow these boundaries and prioritize correctness, reproducibility, maintainability, and efficient execution.
