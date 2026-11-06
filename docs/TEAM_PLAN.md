# NYC Build and Crash — Team Development Plan

## 1. Purpose and Scope

This document records the internal development plan established by the team
coordinator, Sanad. It describes the contributors, responsibilities, deadlines,
dependencies, and handoffs for the **NYC Build and Crash** project.

The university's requirements are documented in [SPEC.md](SPEC.md). General
instructions for AI coding agents belong in [AGENTS.md](../AGENTS.md).

The university assignment is **Milestone 1**. The three phases below are the
team's **internal work stages**, not three separate university milestones.
Changes to task ownership or deadlines require team agreement.

## 2. Project Overview

| Field | Details |
| --- | --- |
| Project | NYC Build and Crash |
| Course | Data Engineering and Visualization |
| University | German International University (GIU) |
| Semester | Winter 2026 |
| Team coordinator | Sanad |
| Internal phases | 3 |
| University submission deadline | November 9, 2026 |
| GitHub repository | [Sanad-Manga/NYC-Build-And-Crash](https://github.com/Sanad-Manga/NYC-Build-And-Crash) |

### 2.1 Research Direction

The project investigates whether areas with more building-related development
activity also experience more motor vehicle collisions, and how the relationship
varies by construction type, borough, ZIP code, and year.

### 2.2 Selected Datasets

| Domain | Dataset | Identifier | Link |
| --- | --- | --- | --- |
| Housing | DOB NOW: Build Job Application Filings | `w9ak-ipjd` | [Housing data](https://data.cityofnewyork.us/d/w9ak-ipjd) |
| Transportation | Motor Vehicle Collisions — Crashes | `h9gi-nx95` | [Collision data](https://data.cityofnewyork.us/d/h9gi-nx95) |

The planned integration key is **ZIP code + year**, after both datasets have
been cleaned and aggregated to a suitable level. The meaning of each metric
must be clear: filings are not necessarily unique jobs or completed projects,
and crash counts are different from injury counts.

## 3. Team and Responsibilities

Sanad coordinates the team and establishes the internal schedule. The supplied
plan lists four implementation contributors:

| Contributor | Main responsibilities |
| --- | --- |
| Mohamed Issa | Initial housing cleaning; ZIP/year integration; two research questions and charts; deployment |
| Mohamed Walid | Housing EDA and follow-up cleaning; website layout and story; two research questions and charts |
| Yassin | Initial collision cleaning; post-integration cleaning; maps; final notebook assembly; two research questions and charts |
| Ahmed | Collision EDA and follow-up cleaning; website filters and report logic; README; two research questions and charts |

The university requires **two research questions and two visualizations per
officially registered team member**. Because Sanad is named as coordinator but
not among the four implementation contributors, confirm the official team
roster before assuming eight questions and eight charts are sufficient. Do not
invent university IDs or unassigned tasks for Sanad.

### 3.1 Shared Collaboration Rules

- Use the shared GitHub repository and coordinate changes to common interfaces.
- Respect file ownership and preserve other contributors' work.
- Record contributions in notebooks and project documentation.
- Agree on shared ZIP-code, date, and column formats before integration.
- Review prior work when needed; a completed stage is not automatically correct.
- Document decisions to drop, fill, transform, or retain data.

## 4. Schedule

| Phase | Work | Internal deadline |
| --- | --- | --- |
| 1 | Clean and explore both datasets | Tuesday, November 3, 2026, 5:00 PM |
| 2 | Integrate datasets; start website | Thursday, November 5, 2026, 11:00 PM |
| 3 | Finish charts, website, notebook, and deployment | Monday, November 9, 2026 (time not specified) |

All times above are local team times in Egypt. **November 9, 2026** is also
the university's submission date. Passing a deadline does not by itself prove
that a phase is complete; verify current repository state and team updates.

### 4.1 Final Internal Checkpoints

These checkpoints supplement the original phase schedule above; they do not replace the university deadline or existing contributor responsibilities.

| Date | Internal checkpoint |
| --- | --- |
| Friday, November 6, 2026 | Everything works locally. |
| Saturday, November 7, 2026 | Website deployed and tested. |
| Sunday, November 8, 2026 | Fixes only. |
| Monday, November 9, 2026 | Final submission email sent to [ICS503Data@gmail.com](mailto:ICS503Data@gmail.com). |

## 5. Phase 1 — Independent Dataset Cleaning and EDA

### 5.1 Goal and Working Pairs

**Deadline:** Tuesday, November 3, 2026, at 5:00 PM.

Prepare both datasets separately for integration. Work in two pairs:

- **Housing:** Mohamed Issa, then Mohamed Walid.
- **Collisions:** Yassin, then Ahmed.

### 5.2 Mohamed Issa — Initial Housing Cleaning

- Load the DOB NOW: Build Job Application Filings dataset.
- Inspect and handle missing values and duplicate records.
- Preserve fields needed for later research and integration.
- Document cleaning choices and provide a cleaned table.

Existing housing artifacts reported by the team:

- Notebook: `01_housing_cleaning.ipynb`
- Output: `data/housing_step1.csv.gz`
- Reported output shape: **972,679 rows × 25 columns**.

These are historical project facts, not guarantees about the current checkout.
Verify the file and relevant decisions before relying on them. Do not modify
Issa's notebook without authorization.

### 5.3 Mohamed Walid — Housing EDA and Follow-Up Cleaning

Use Issa's cleaned housing data as input. Responsibilities:

- Explore distributions with descriptive statistics and meaningful plots.
- Investigate outliers; handle genuinely invalid values with justification.
- Investigate and correct inconsistent values.
- Standardize ZIP-code and date formats for the planned join.
- Validate the resulting table and document decisions in Markdown cells.

Development notebook: `phase1_housing_eda_cleaning_walid.ipynb`.

Housing handoff:

```text
Original housing data
  -> Issa: missing values + duplicates
  -> housing_step1.csv.gz
  -> Walid: EDA + outliers + inconsistencies + ZIP/date standards
  -> Final cleaned housing table
  -> Phase 2 integration
```

The final housing-output filename must be agreed upon by the team rather than
assumed to exist.

### 5.4 Yassin — Initial Collision Cleaning

- Load the Motor Vehicle Collisions — Crashes dataset.
- Inspect and handle missing values and duplicate records.
- Preserve relevant collision, location, date, and injury attributes.
- Document cleaning choices and hand over a cleaned table.

Crash counts and injury counts are different measures. Missing locations do not
mean there were zero collisions.

### 5.5 Ahmed — Collision EDA and Follow-Up Cleaning

- Explore collision statistics and distributions with useful plots.
- Investigate outliers and inconsistent values.
- Standardize ZIP codes and dates.
- Validate and document the cleaned collision output for integration.

Collision handoff:

```text
Original collision data
  -> Yassin: missing values + duplicates
  -> Ahmed: EDA + outliers + inconsistencies + ZIP/date standards
  -> Final cleaned collision table
  -> Phase 2 integration
```

### 5.6 Phase 1 Acceptance Criteria

- Both datasets have documented EDA and justified cleaning decisions.
- Missingness, duplicates, inconsistent values, and outliers were investigated.
- ZIP-code and date formats are suitable for integration.
- Both cleaned tables are validated, accessible, and handed off with schemas.
- Individual contributors are credited accurately.

Do not automatically remove statistical outliers that could be real records.

## 6. Phase 2 — Integration and Website Foundation

### 6.1 Goal and Working Pairs

**Deadline:** Thursday, November 5, 2026, at 11:00 PM.

- **Integration:** Mohamed Issa and Yassin.
- **Website foundation:** Mohamed Walid and Ahmed.

### 6.2 Mohamed Issa — Integration

- Receive the final cleaned housing and collision datasets.
- Verify compatible ZIP-code and year fields.
- Aggregate each dataset at an appropriate ZIP/year grain.
- Join the aggregates by ZIP code and year.
- Explain the join type, aggregation, exclusions, and limitations.
- Validate that no unintended many-to-many expansion occurred.

**Never join individual housing filings directly to individual crashes solely
because ZIP code and year match.** That can multiply records and distort counts.

### 6.3 Yassin — Post-Integration Cleaning

- Investigate new missing values after the join.
- Resolve redundant columns and incorrect data types.
- Inspect unexpected duplicates and unmatched ZIP/year combinations.
- Validate the integrated dataset and document decisions.

**Post-integration cleaning is mandatory** under the university requirements.
Missing values from unmatched rows must not automatically be converted to zero.

### 6.4 Mohamed Walid — Website Structure and Story

- Create the page structure and chart placeholders.
- Establish major sections such as introduction, filters, charts, and findings.
- Write an introductory story using only supported project context.
- Prepare space for the final conclusions and limitations.

Do not invent findings before the combined dataset has been analyzed.

### 6.5 Ahmed — Filters, Search, and Generate Report

- Create dropdown filters, search mode, and the Generate Report button.
- Implement the initial reporting logic.
- Use clearly labeled dummy data until the joined data is available.
- Coordinate component and data interfaces with Walid.

The framework is not fixed by this plan. Inspect the repository and confirm
the team's choice before assuming React, Dash, or another framework.

### 6.6 Phase 2 Acceptance Criteria

- An aggregated, documented ZIP/year join exists.
- Post-integration cleaning and validation are documented.
- A website foundation exists, with working initial filters and report logic.
- Temporary data is identifiable and can be replaced by integrated data.

## 7. Phase 3 — Research, Website, and Submission

### 7.1 Goal

**Deadline:** Monday, November 9, 2026; no exact internal time was specified.

Complete the interactive website, final notebook, research questions, charts,
documentation, and deployment.

### 7.2 Contributor Assignments

| Contributor | Website/documentation responsibility | Research contribution |
| --- | --- | --- |
| Mohamed Issa | His charts and website deployment | 2 questions + 2 charts |
| Mohamed Walid | Layout, styling, story, limitations | 2 questions + 2 charts |
| Yassin | Map visualization; final notebook assembly | 2 questions + 2 charts |
| Ahmed | Filters, report logic, README | 2 questions + 2 charts |

### 7.3 Proposed Research Topics From Sanad's Plan

These topics are **proposals**, not findings or final question wording. Confirm
that the integrated data supports the necessary variables and metrics.

| Contributor | Proposed question 1 | Proposed question 2 |
| --- | --- | --- |
| Mohamed Issa | New-building filings versus crashes by ZIP | How both measures change by year |
| Mohamed Walid | Dwelling-unit changes versus traffic injuries | Demolition and new-building trends versus crash trends |
| Yassin | Pedestrian/cyclist injury hotspots versus construction areas | Contributing factors in high- versus low-construction areas |
| Ahmed | Construction cost/size versus crash severity by borough | Borough and year development growth versus crash changes |

Clarify denominators before using the term *rate*. Do not describe proposed
units as completed homes or correlations as proof of causation.

### 7.4 Phase 3 Acceptance Criteria

- Required cross-domain questions and charts are finished and evidence-based.
- Charts use validated integrated data, not dummy data.
- Filters, search, and Generate Report update the relevant visualizations.
- Website story, limitations, and styling are complete.
- Yassin has assembled a coherent, reproducible final notebook.
- Individual contributions, data sources, and AI prompts are documented.
- README is complete, the website is publicly deployed, and links work.
- Repository and submission materials are verified before the deadline.

## 8. Dependencies and Handoffs

| Dependency | Required handoff |
| --- | --- |
| Issa -> Walid | Initial cleaned housing dataset and cleaning notes |
| Yassin -> Ahmed | Initial cleaned collision dataset and cleaning notes |
| Walid and Ahmed -> Issa | Final cleaned housing and collision tables |
| Issa -> Yassin | Aggregated, joined dataset and integration explanation |
| Yassin -> website team | Validated integrated dataset and schema |
| All contributors -> Yassin | Notebooks, charts, explanations, contribution records |
| Website contributors -> deployment | Integrated website, configuration, tested features |

Each dataset handoff should specify filename, location, row/column counts,
dtypes, cleaning choices, known limitations, and standardized key formats.
Each notebook should explain inputs, outputs, execution order, and authorship.

## 9. GitHub and AI-Agent Collaboration

- Use the shared repository and appropriate feature branches.
- Review the current branch and working tree before editing files.
- Do not overwrite teammates' work, discard uncommitted changes, or force-push.
- Do not commit or push unless authorized by the user/team workflow.
- Verify implementation and report what was tested versus unverified.
- Follow the active user request for the current contributor and task.
- Do **not** interpret this schedule as permission to implement every phase.

The project status is not defined solely by this document. Inspect the actual
repository, notebook outputs, pull requests, and team communications to
establish what has been completed.

## 10. Official Submission

The university submission deadline is **November 9, 2026**. The team sends
**one email** to [ICS503Data@gmail.com](mailto:ICS503Data@gmail.com) containing:

1. University IDs for all officially registered members.
2. [GitHub repository URL](https://github.com/Sanad-Manga/NYC-Build-And-Crash).
3. Publicly deployed website URL.
4. Both original dataset URLs.

The plan does not explicitly assign sending the email to one contributor;
Sanad should coordinate and confirm the submission arrangements.

Before sending, verify the notebook, website, filters, Generate Report button,
README, contribution documentation, repository state, and deployed URL.

## 11. Document Maintenance

Update this plan only when the team agrees to changes in roles, schedule, or
technical handoffs. Preserve the distinction between assigned work and work
actually completed.

Related references:

- [SPEC.md](SPEC.md) — University requirements and deliverables.
- [AGENTS.md](../AGENTS.md) — AI-agent instructions.
- [README.md](../README.md) — Project setup and overview.
