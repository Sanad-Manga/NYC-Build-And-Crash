# NYC Build and Crash — Technical Contract

## 1. Purpose

This document defines the technical agreements and conventions used by contributors and AI coding agents working on the NYC Build and Crash project.

Its purpose is to ensure that independently developed components can be integrated without unnecessary modifications, inconsistencies, or data loss.

This contract covers:

* File and folder naming conventions.
* Shared dataset schemas.
* Data types and formatting.
* Geographic and temporal standardization.
* Dataset integration.
* Data handoffs.
* Validation requirements.
* Website data interfaces.
* Git collaboration.
* Contract changes.

### 1.1 Team Rules

The following collaboration rules are agreed and mandatory:

* Development uses local VS Code and Jupyter, not Google Colab.
* AI prompts are recorded in the root-level `AI_PROMPTS.txt` using the existing team format: date, student, tool, related requirement, prompt or clearly labelled summary, and how the output was used.
* The repository uses one shared root-level `requirements.txt`; contributor-specific requirements files are not permitted.
* A pull request may merge only after a fresh-clone reproducibility test.
* The fresh-clone test uses a new virtual environment, installs the shared requirements with `pip install -r requirements.txt`, and executes each relevant notebook from top to bottom with **Run All** and zero errors.
* Each task uses its own branch created from the latest `origin/main`.

#### Agreed Technical Requirements

The following requirements are agreed for the shared Phase 2 interface:

* `zip_code` is a five-digit string.
* `year` is an integer.
* The integration grain is one row per ZIP code and year.
* The project analysis scope is 2022 onward.

These four requirements apply even where later sections describe other, still-proposed standards.

### 1.2 Related Documentation

* [Project Specification](SPEC.md) — University requirements.
* [Team Development Plan](TEAM_PLAN.md) — Contributors, phases, and responsibilities.
* [AI Agent Instructions](../AGENTS.md) — General instructions for coding agents.
* [README](../README.md) — Repository overview and setup.

### 1.3 Contract Status

This document contains the team's existing decisions and proposed technical standards.

The following decisions are already established:

* The project uses two NYC Open Data datasets.
* Housing and collisions are the selected domains.
* ZIP code and year are the planned integration keys.
* The project follows three internal development phases.
* Individual contributors work on assigned components.
* The repository uses GitHub for collaboration.

Except for the four agreed requirements in Section 1.1, technical standards introduced by this document must be reviewed by the team before being treated as finalized agreements.

Changes to an established contract require coordination with affected contributors.

---

### 2. File Naming Conventions

## 2.1 General Rules

All new project files should use consistent, descriptive names.

For contributor-owned development artifacts, use:

`phase<NUMBER>_<COMPONENT>_<TASK>_<CONTRIBUTOR>.<EXTENSION>`

### Naming Requirements

1. Use lowercase letters.
2. Separate words using underscores (`_`).
3. Do not use spaces in filenames.
4. Include the development phase number when applicable.
5. Include the relevant dataset or component.
6. Include a descriptive task identifier.
7. Include the contributor identifier for individually owned artifacts.
8. Preserve the appropriate file extension.
9. Avoid unnecessarily long filenames.
10. Do not rename existing teammate files without authorization.

### Contributor Identifiers

| Contributor   | Identifier |
| ------------- | ---------- |
| Mohamed Issa  | `issa`     |
| Mohamed Walid | `walid`    |
| Yassin        | `yassin`   |
| Ahmed         | `ahmed`    |

Additional identifiers must be agreed upon by the team.

### Required Phase 1 Notebook Names

All Phase 1 contributor notebooks must use the following names:

| Contributor   | Responsibility             | Required filename                                    |
| ------------- | -------------------------- | ---------------------------------------------------- |
| Mohamed Issa  | Housing initial cleaning   | `phase1_housing_initial_cleaning_issa.ipynb`         |
| Yassin        | Collision initial cleaning | `phase1_collisions_initial_cleaning_yassin.ipynb`    |
| Ahmed         | Collision EDA and cleaning | `phase1_collisions_eda_cleaning_ahmed.ipynb`         |
| Mohamed Walid | Housing EDA and cleaning   | `phase1_housing_eda_cleaning_walid.ipynb`            |

Issa's legacy `01_housing_cleaning.ipynb` must be renamed to `phase1_housing_initial_cleaning_issa.ipynb`. Any required rename belongs to the notebook's contributor and must be coordinated with consumers; this contract does not authorize one contributor to rename another contributor's file.

Other contributor-owned artifacts continue to follow the general pattern. Proposed examples include `phase2_data_integration_issa.ipynb` and `phase2_data_post_cleaning_yassin.ipynb`.

## 2.2 Exceptions

Standard repository files do not follow contributor-based naming.

Examples:

```text
AGENTS.md
README.md
.gitignore
requirements.txt
package.json
docs/SPEC.md
docs/TEAM_PLAN.md
docs/CONTRACT.md
```

Shared application components should follow the conventions of the selected framework.

For example, React components may use PascalCase rather than snake_case.

Do not force Python notebook naming conventions onto frontend components.

## 2.3 Shared Dataset Naming

Shared datasets should use stable, descriptive names that do not depend on contributor ownership.

Proposed examples:

```text
housing_step1.csv.gz
housing_cleaned.csv.gz
collisions_cleaned.csv.gz
integrated_data.csv.gz
```

The existing `housing_step1.csv.gz` filename must be preserved unless the team agrees to change it.

Names for future outputs are proposals until the receiving contributor confirms them.

### Important Rule

Once a shared output filename becomes part of an agreed interface, do not change it without coordinating with its consumers.

---

### 3. Folder Organization

The repository should separate source code, documentation, datasets, and application components where practical.

A possible structure is:

```text
NYC-Build-And-Crash/
│
├── AGENTS.md
├── README.md
├── .gitignore
│
├── docs/
│   ├── SPEC.md
│   ├── TEAM_PLAN.md
│   └── CONTRACT.md
│
├── data/
│   ├── housing_step1.csv.gz
│   ├── housing_cleaned.csv.gz
│   ├── collisions_cleaned.csv.gz
│   └── integrated_data.csv.gz
│
├── notebooks/
│   └── ...
│
└── website/
    └── ...
```

This is a proposed organizational structure, not a requirement to reorganize the repository immediately.

## Folder Rules

* Store large datasets separately from source code.
* Avoid committing virtual environments.
* Keep generated temporary files out of Git.
* Use project-relative paths where possible.
* Avoid hardcoded personal filesystem paths.
* Preserve existing project structure unless reorganization is authorized.

Notebooks may remain in the repository root until the team agrees to move them, but Phase 1 notebook filenames must follow Section 2.1.

---

### 4. Column Naming Conventions

## 4.1 General Naming Rules

Shared data columns should use:

`snake_case`

Examples:

```text
zip_code
filing_date
crash_date
job_type
initial_cost
total_construction_floor_area
```

### Requirements

1. Use lowercase letters.
2. Separate words using underscores.
3. Avoid spaces.
4. Avoid special characters.
5. Use descriptive names.
6. Preserve consistent meanings across datasets.
7. Avoid ambiguous abbreviations.

Existing source columns may be renamed during cleaning when necessary.

All renaming decisions should be documented.

## 4.2 Shared Integration Columns

The agreed shared integration schema is:

| Column     | Data Type | Description                              |
| ---------- | --------- | ---------------------------------------- |
| `zip_code` | String    | Five-digit ZIP code                      |
| `year`     | Integer   | Calendar year associated with the record |

Both cleaned datasets must use compatible representations before integration.

The actual data types must be validated before the integration stage.

## 4.3 Geographic Attributes

The proposed standard column names are:

| Column      | Data Type | Description          |
| ----------- | --------- | -------------------- |
| `borough`   | String    | NYC borough          |
| `zip_code`  | String    | Postal ZIP code      |
| `latitude`  | Float     | Geographic latitude  |
| `longitude` | Float     | Geographic longitude |

Missing geographic values must not be fabricated.

Additional geographic columns may be retained when they support research or validation.

---

### 5. Geographic Data Standards

## 5.1 ZIP Code Format

ZIP codes must be treated as identifiers rather than numerical measurements.

### Agreed Standard

Column name:

`zip_code`

Data type:

String.

Expected format:

Five numeric characters.

### Valid Examples

```text
"10001"
"11201"
"10451"
```

### Invalid Representations

```text
10001.0
"10001.0"
"ABCDE"
""
```

A missing ZIP code must remain missing unless a verified source provides the correct value.

### Standardization Rules

* Remove irrelevant surrounding whitespace.
* Preserve leading zeros.
* Remove decimal formatting only when the original value is clearly an integer ZIP code.
* Validate the five-digit format.
* Investigate unexpected ZIP codes.
* Document invalid or excluded records.

Do not invent geographic identifiers.

Do not automatically assume that every five-digit number is a valid NYC ZIP code.

## 5.2 Borough Naming

The agreed canonical borough values are the following Title Case strings:

```text
Manhattan
Brooklyn
Queens
Bronx
Staten Island
```

Source values may use other representations.

Examples include:

```text
MANHATTAN
Manhattan
manhattan
```

These can be standardized to the agreed canonical form.

Ahmed's collision-cleaning pipeline already produces these Title Case values. This was independently verified in `phase1_collisions_eda_cleaning_ahmed.ipynb`: the cleaning step strips surrounding whitespace and applies `.str.title()` to `borough` while preserving missing values.

Unknown or invalid values must not automatically be mapped to a borough.

Document any mapping rules.

## 5.3 Geographic Consistency

Where practical, validate geographic information for:

* Invalid coordinates.
* Missing locations.
* ZIP code inconsistencies.
* Borough mismatches.
* Duplicate geographic identifiers.

Do not silently overwrite one geographic attribute based on another.

If ZIP code and borough information conflict, investigate the source and document the resolution.

---

### 6. Date and Time Standards

## 6.1 Date Representation

The proposed standardized date format is:

`YYYY-MM-DD`

Example:

`2023-05-14`

In Pandas, dates should use an appropriate datetime type when processing.

When exporting to CSV, use a consistent date representation.

## 6.2 Relevant Date Columns

Housing data may contain:

```text
filing_date
approved_date
first_permit_date
current_status_date
```

Transportation data may contain:

```text
crash_date
crash_time
```

Agents must verify the exact available columns before using them.

## 6.3 Year Extraction

The agreed shared integration column is:

`year`

Housing data should derive its integration year from the agreed housing event date, normally the filing date.

Collision data should derive its integration year from the collision date.

These choices must be documented and validated.

## Important Rule in year Extraction

A housing filing date and a collision date represent different events.

Integration by year aligns observations temporally; it does not imply that the events are causally related.

## 6.4 Date Validation

Date processing must check for:

* Invalid formats.
* Parsing failures.
* Missing dates.
* Implausible values.
* Unexpected future dates.
* Inconsistent representations.

Do not silently replace invalid dates with arbitrary values.

If datetime fields contain timezone information, handle it explicitly and consistently.

---

### 7. Data Type Standards

The following types are proposed for shared processed datasets.

| Category               | Preferred Data Type        |
| ---------------------- | -------------------------- |
| ZIP codes              | String                     |
| Borough names          | String                     |
| Dates                  | Datetime during processing |
| Year                   | Integer                    |
| Counts                 | Integer                    |
| Costs                  | Numeric                    |
| Floor areas            | Numeric                    |
| Geographic coordinates | Float                      |
| Boolean indicators     | Boolean                    |

Nullable Pandas types may be used when missing values are possible.

For example:

* `string`
* `Int64`
* `boolean`

Do not replace missing values merely to force a non-nullable data type.

### Numeric Validation

Numeric fields should be checked for:

* Unexpected strings.
* Invalid characters.
* Negative values where inappropriate.
* Implausible magnitudes.
* Incorrect decimal formatting.
* Overflow or conversion problems.

Do not automatically remove valid extreme observations.

---

### 8. Housing Dataset Contract

## 8.1 Source

Dataset:

DOB NOW: Build Job Application Filings.

Source:

[DOB NOW: Build Job Application Filings](https://data.cityofnewyork.us/d/w9ak-ipjd)

## 8.2 Existing Data Pipeline

The housing workflow begins with Mohamed Issa's initial cleaning stage.

Legacy notebook pending its contributor-owned rename:

`01_housing_cleaning.ipynb`

Required Phase 1 name:

`phase1_housing_initial_cleaning_issa.ipynb`

Existing output:

`data/housing_step1.csv.gz`

Mohamed Walid performs additional EDA, cleaning, and standardization.

The final housing output is consumed during Phase 2 integration.

## 8.3 Relevant Housing Attributes

Important attributes may include:

```text
job_filing_number
job_id
is_initial_filing
filing_status
job_type
building_type
filing_date
borough
zip_code
initial_cost
total_construction_floor_area
existing_dwelling_units
proposed_dwelling_units
```

The complete schema must be verified against the actual processed dataset.

Not every listed attribute must necessarily appear in the final aggregated output.

## 8.4 Housing Record Interpretation

One building job may have multiple filings.

Therefore:

* A filing is not automatically a unique construction job.
* Repeated job identifiers may represent legitimate records.
* Initial filings may be useful for avoiding repeated job counts.
* Counting methods must be documented.

A research question must explicitly identify whether it measures filings, unique jobs, or another unit.

## 8.5 Housing Handoff Requirements

Before housing data is handed to the integration pair:

1. ZIP codes must use the agreed format.
2. Required dates must be valid or explicitly marked missing.
3. The year must be derivable from the agreed date field.
4. Relevant numerical attributes must have appropriate types.
5. Important categorical inconsistencies must be resolved.
6. Duplicate handling must be documented.
7. Outlier decisions must be justified.
8. Data-quality limitations must be recorded.

The receiving contributor must be able to reproduce or verify the delivered dataset.

---

### 9. Transportation Dataset Contract

## 9.1 Source

Dataset:

Motor Vehicle Collisions — Crashes.

Source:

[Motor Vehicle Collisions — Crashes](https://data.cityofnewyork.us/d/h9gi-nx95)

## 9.2 Transportation Pipeline

The transportation workflow is:

1. Initial loading and cleaning by Yassin.
2. EDA and additional cleaning by Ahmed.
3. Delivery to the Phase 2 integration pair.

## 9.3 Relevant Transportation Attributes

Important attributes may include:

```text
collision_id
crash_date
crash_time
borough
zip_code
latitude
longitude
number_of_persons_injured
number_of_persons_killed
```

These names are expected examples and must be verified against the actual dataset.

Additional injury, vehicle, and contributing-factor attributes may be retained where needed.

## 9.4 Collision Record Interpretation

A collision record represents a reported traffic incident.

Agents must distinguish between:

* Number of collisions.
* Number of people injured.
* Number of fatalities.
* Types of road users involved.

Do not treat injury counts as collision counts.

## 9.5 Transportation Handoff Requirements

Before transportation data is handed to the integration pair:

1. ZIP codes must use the agreed format.
2. Collision dates must be consistently represented.
3. The year must be derivable from collision dates.
4. Duplicate collision records must be investigated.
5. Injury and fatality fields must have appropriate data types.
6. Missing geographic information must be documented.
7. Important cleaning decisions must be explained.

---

### 10. Integration Contract

## 10.1 Integration Keys

The planned integration keys are:

```text
zip_code
year
```

Both datasets must provide compatible values for these attributes.

## 10.2 Aggregation Rules

Housing and collision records should be aggregated before joining.

The expected integration granularity is:

**One row per ZIP code and year.**

Each aggregated input should have at most one record for each valid `(zip_code, year)` combination.

This prevents uncontrolled many-to-many joins.

### Proposed Housing Metrics

Depending on the research questions:

* Number of unique building jobs.
* Number of filings.
* Number of new-building applications.
* Total or median estimated construction cost.
* Total or median construction floor area.
* Proposed dwelling-unit changes.

Every metric must have a documented definition.

### Proposed Transportation Metrics

Depending on the research questions:

* Number of collisions.
* Number of injured people.
* Number of fatalities.
* Number of pedestrian injuries.
* Number of cyclist injuries.

These metrics must be calculated from the appropriate source attributes.

## 10.3 Proposed Integrated Schema

The minimum analytical structure may contain:

| Column              | Data Type | Description                    |
| ------------------- | --------- | ------------------------------ |
| `zip_code`          | String    | Integration ZIP code           |
| `year`              | Integer   | Integration year               |
| `housing_job_count` | Integer   | Number of unique building jobs |
| `collision_count`   | Integer   | Number of collisions           |

Additional attributes may be included as required by the research questions.

This schema is a proposed baseline, not a finalized list of required columns.

Metric definitions must be approved before the final integrated dataset is produced.

## 10.4 Join Validation

Before integration:

* Validate the join-key formats.
* Verify that the selected years overlap.
* Verify geographic coverage.
* Check key uniqueness in aggregated inputs.

After integration:

* Check the output dimensions.
* Check unexpected duplicates.
* Check unmatched ZIP/year combinations.
* Check missing values.
* Check numeric consistency.
* Verify that joins did not multiply records.

The selected join type must be documented.

## 10.5 Handling Missing Matches

If one dataset has a ZIP/year combination that does not appear in the other, the result must be handled deliberately.

Do not automatically replace every unmatched value with zero.

A missing match may reflect:

* Missing geographic information.
* Different temporal coverage.
* Filtering decisions.
* No recorded observations.
* Data-quality limitations.

The chosen interpretation must be justified.

---

### 11. Dataset Handoff Contract

Every shared dataset handoff should provide enough information for the next contributor to use it safely.

## 11.1 Required Handoff Information

The contributor should communicate:

| Field              | Description                        |
| ------------------ | ---------------------------------- |
| Dataset filename   | Exact output filename              |
| Location           | Relative path within the project   |
| Contributor        | Person responsible for the output  |
| Input source       | Dataset or previous pipeline stage |
| Row count          | Number of records                  |
| Column count       | Number of attributes               |
| Schema             | Column names and data types        |
| Cleaning summary   | Important transformations          |
| Integration fields | Geographic and temporal keys       |
| Limitations        | Known unresolved issues            |

This information may be documented in notebook Markdown cells or another agreed location.

## 11.2 Handoff Validation

The receiving contributor should verify:

* The file exists.
* The file can be loaded.
* The expected columns exist.
* Data types are compatible.
* Required identifiers are present.
* Documented transformations are consistent with the output.

If the handoff does not satisfy the agreed contract, the issue should be reported before dependent work proceeds.

## 11.3 Preserve Source Data

Do not overwrite the original input dataset during cleaning.

Use separate outputs for important pipeline stages.

This allows contributors to reproduce results and investigate errors.

---

### 12. Website Data Contract

The website must consume the validated integrated dataset or clearly documented derivatives of it.

## 12.1 Shared Data Consistency

All website components should use consistent definitions for:

* ZIP codes.
* Years.
* Boroughs.
* Housing metrics.
* Transportation metrics.

Different components must not independently reinterpret the same metric.

## 12.2 Data Interface

The website framework and exact interface are not yet fixed by this contract.

The team must agree on how the integrated data is exposed to the frontend.

Possible approaches include:

* Static JSON.
* Processed CSV files.
* Backend API endpoints.
* Server-side data loading.

The selected interface must be documented before components depend on it.

### Example JSON Record

```json
{
  "zip_code": "10001",
  "year": 2023,
  "housing_job_count": 150,
  "collision_count": 320
}
```

This example uses illustrative values.

It demonstrates the proposed representation, not actual project results.

## 12.3 Filtering Contract

Filters must operate consistently across all relevant charts.

For example:

If the user selects Brooklyn and 2023, the generated report must reflect those filters throughout the relevant dashboard components.

Do not combine filtered and unfiltered metrics without clearly indicating the difference.

## 12.4 Search Contract

Search functionality must:

* Recognize supported search terms.
* Apply corresponding filters.
* Handle unsupported queries.
* Handle empty results.
* Avoid silently producing misleading results.

## 12.5 Generate Report Contract

The Generate Report button must:

1. Read the current filter state.
2. Apply the requested filters.
3. Update relevant visualizations.
4. Handle empty results.
5. Avoid displaying stale data as updated results.

## 12.6 Chart Data Requirements

Every chart should have:

* A clearly defined data source.
* A documented metric.
* An appropriate aggregation level.
* A readable title.
* Correct axis labels.
* Appropriate units.
* Consistent filtering behavior.

Research charts must reflect actual integrated data rather than temporary demonstration data.

---

### 13. Validation Requirements

## 13.1 General Validation

Before handing over a component, validate the aspects relevant to that component.

### Dataset Validation

Check:

* File readability.
* Expected dimensions.
* Required columns.
* Data types.
* Missing values.
* Unexpected duplicates.
* Value ranges.
* Date formats.
* ZIP code formats.
* Geographic and temporal coverage.

### Integration Validation

Check:

* Compatible join keys.
* Unique aggregated keys.
* Expected join behavior.
* No accidental record multiplication.
* Correct aggregation.
* Missing matches.
* Output consistency.

### Website Validation

Check:

* Successful application build.
* Correct data loading.
* Working filters.
* Working search functionality.
* Working Generate Report functionality.
* Correct chart updates.
* Meaningful empty states.
* Responsive layout.

## 13.2 Validation Results

Validation outcomes should distinguish between:

| Status     | Meaning                               |
| ---------- | ------------------------------------- |
| PASS       | Check completed successfully          |
| FAIL       | Demonstrated problem                  |
| WARNING    | Potential problem requiring attention |
| UNVERIFIED | Check could not be completed          |

Do not report an unexecuted check as PASS.

## 13.3 Error Handling

When an error occurs:

1. Identify the failing operation.
2. Inspect the relevant error message.
3. Investigate the root cause.
4. Apply the smallest justified correction.
5. Re-run the relevant validation.
6. Check for unintended effects.

Do not suppress errors merely to make code appear functional.

---

### 14. Git Collaboration Contract

## 14.1 Repository Rules

All contributors work through:

[NYC Build and Crash Repository](https://github.com/Sanad-Manga/NYC-Build-And-Crash)

Use feature branches where appropriate.

### Branch Naming

Recommended format:

`feature/<component>-<task>-<contributor>`

Example:

`feature/housing-eda-walid`

Other branch types may be used when appropriate.

## 14.2 Protect Existing Work

Do not:

* Force-push without authorization.
* Overwrite another contributor's work.
* Delete shared branches without approval.
* Discard uncommitted changes.
* Modify unrelated files unnecessarily.
* Commit large datasets or secrets accidentally.

## 14.3 Commit Conventions

Prefer concise commit messages describing the change.

Examples:

```text
feat: add housing EDA visualizations
fix: standardize housing ZIP codes
docs: update dataset integration contract
refactor: simplify collision cleaning
```

Commit only files relevant to the authorized task.

## 14.4 Merge Conflicts

When conflicts occur:

1. Identify the affected files.
2. Inspect both sets of changes.
3. Preserve relevant work.
4. Resolve conflicts deliberately.
5. Validate the merged implementation.

Do not automatically discard another contributor's changes.

---

### 15. Contract Changes

## 15.1 Change Management

This document is intended to prevent incompatible implementation decisions.

If a contributor needs to change an agreed interface, they should:

1. Identify the required change.
2. Explain why it is necessary.
3. Identify affected contributors.
4. Communicate the proposal.
5. Obtain agreement from the relevant team members.
6. Update this document.
7. Update dependent implementations.

## 15.2 Breaking Changes

Examples of breaking changes include:

* Renaming shared columns.
* Changing ZIP code formats.
* Changing date representations.
* Changing shared output filenames.
* Changing the aggregation granularity.
* Changing the website data schema.
* Removing attributes required by another component.

Do not introduce breaking changes silently.

## 15.3 Responsibility Boundaries

Agents may identify inconsistencies in another contributor's work.

However, they should not automatically rewrite that work without authorization.

Report issues clearly and explain their impact on the shared contract.

---

## 16. AI Agent Compliance

AI coding agents working on this project must follow:

1. The active user's task instructions.
2. The agreed technical interfaces in this contract.
3. The team responsibilities in [TEAM_PLAN.md](TEAM_PLAN.md).
4. The university requirements in [SPEC.md](SPEC.md).
5. The general AI development guidelines in [AGENTS.md](../AGENTS.md).

## Before Implementing

Agents should:

* Understand the requested task.
* Inspect relevant existing files.
* Identify applicable contracts.
* Check dependencies.
* Avoid unnecessary changes outside the requested scope.

### During Implementation

Agents should:

* Respect naming conventions.
* Preserve existing source data.
* Follow agreed schemas.
* Validate important transformations.
* Avoid breaking dependent components.
* Document significant decisions.

### After Implementation

Agents should report:

* Files created or modified.
* Important transformations.
* Validation results.
* Contract compliance.
* Remaining problems.
* Any proposed contract changes.

Do not automatically implement every project phase simply because the phases are documented.

The active user request determines the authorized work.

---

## 17. Final Contract Principles

All contributors and AI agents should follow these principles:

1. Use consistent naming conventions.
2. Preserve source data.
3. Maintain compatible schemas.
4. Validate shared integration keys.
5. Avoid uncontrolled many-to-many joins.
6. Document important transformations.
7. Distinguish unique jobs from filing records.
8. Distinguish collision counts from injury counts.
9. Avoid unsupported causal claims.
10. Respect contributor responsibilities.
11. Preserve existing work.
12. Communicate breaking changes.
13. Validate before handoff.
14. Keep shared interfaces documented.
15. Prioritize correctness and reproducibility.

The goal of this contract is to ensure that every contributor can work independently while producing components that integrate into one reliable project.

The contract should evolve only when necessary and with appropriate team coordination.
