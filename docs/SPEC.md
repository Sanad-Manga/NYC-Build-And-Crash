# NYC Build and Crash — Project Specification

## 1. Project Information

| Field                | Details                                 |
| -------------------- | --------------------------------------- |
| University           | German International University (GIU)   |
| Faculty              | Informatics and Computer Science        |
| Course               | Data Engineering and Visualization      |
| Semester             | Winter 2026                             |
| Instructor           | Dr. Nada Sharaf                         |
| Teaching Assistants  | Mariam Ali, May Magdy, Mohamed El Dagla |
| University Milestone | Milestone 1                             |
| Submission Deadline  | November 9, 2026                        |
| Project Name         | NYC Build and Crash                     |

**GitHub Repository:** [NYC Build and Crash](https://github.com/Sanad-Manga/NYC-Build-And-Crash)

**Submission Email:** [ICS503Data@gmail.com](mailto:ICS503Data@gmail.com)

### 1.1 Purpose of This Document

This document describes the official university project requirements and the team's selected research direction.

It serves as the reference for understanding what must be implemented, documented, tested, and submitted.

Internal responsibilities, team phases, and deadlines are documented separately in [TEAM_PLAN.md](TEAM_PLAN.md).

The official university project description takes precedence if any information in this document conflicts with it.

---

## 2. Project Overview

The university requires students to complete a data engineering project connecting two domains:

1. **Housing and Development**
2. **Transportation**

The project must demonstrate the complete data engineering workflow:

* Dataset selection.
* Exploratory Data Analysis (EDA).
* Pre-integration data cleaning.
* Dataset integration.
* Post-integration data cleaning.
* Research question formulation.
* Data visualization.
* Interactive website development.
* Documentation and deployment.

The objective is to discover meaningful relationships between datasets that were not originally designed to work together.

The completed project should communicate an evidence-based data story rather than simply display statistics.

### 2.1 Project Mission

The project should explain:

* **The Question:** What are we investigating, and why does it matter?
* **The Data:** Which datasets were selected, and how were they integrated?
* **The Discovery:** What meaningful relationships or patterns were identified?
* **The Limitations:** What conclusions cannot be supported by the available data?
* **The Impact:** How could the findings benefit New York City?

---

## 3. Selected Research Direction

### 3.1 Project Title

The selected project title is **NYC Build and Crash: Urban Development and Road Safety**.

### 3.2 Main Research Question

How is building development activity associated with traffic collisions in New York City, and how do these relationships vary across geographic areas, construction types, and years?

### 3.3 Research Objectives

The project aims to:

1. Examine building development activity across NYC.
2. Examine geographic and temporal patterns in traffic collisions.
3. Integrate housing and transportation information.
4. Investigate relationships between development activity and road safety.
5. Compare patterns across boroughs, ZIP codes, and years.
6. Communicate findings using interactive visualizations.
7. Identify limitations and potential implications for NYC.

### 3.4 Scientific Limitations

Building job applications do not necessarily represent completed construction projects.

Traffic collisions may be influenced by population, traffic volume, road infrastructure, and other factors.

**Correlation does not establish causation.**

Research findings must distinguish observed associations from unsupported causal explanations.

---

## 4. Dataset Requirements

The university requires exactly two primary datasets:

* One from Housing and Development.
* One from Transportation.

Each dataset must:

* Contain at least nine columns.
* Provide meaningful geographic or temporal attributes for integration.
* Support a relevant research question.
* Be documented and justified in the notebook.

The recommended dataset catalog is not exclusive.

Datasets outside the recommended catalog may be selected if they satisfy the project requirements.

### 4.1 Selected Housing Dataset

**Name:** DOB NOW: Build Job Application Filings

**Catalog ID:** H5

**Dataset ID:** `w9ak-ipjd`

**Source:** [DOB NOW: Build Job Application Filings — NYC Open Data](https://data.cityofnewyork.us/d/w9ak-ipjd)

The dataset contains information about building job applications, including:

* Filing identifiers.
* Job types.
* Building types.
* Filing statuses.
* Filing dates.
* Approval and permit dates.
* Boroughs.
* ZIP codes.
* Geographic coordinates.
* Construction costs.
* Construction floor areas.
* Existing and proposed dwelling units.

#### Housing Data Considerations

A construction job may have multiple filings.

Therefore, filing counts and unique job counts must not be confused.

Additionally:

* Filing dates do not necessarily indicate construction start dates.
* Proposed dwelling units are not necessarily completed housing units.
* Estimated construction costs may differ from actual costs.
* Application approval does not necessarily mean construction has been completed.

These distinctions must be considered when selecting metrics and interpreting findings.

### 4.2 Selected Transportation Dataset

**Name:** Motor Vehicle Collisions — Crashes

**Dataset ID:** `h9gi-nx95`

**Source:** [Motor Vehicle Collisions — Crashes — NYC Open Data](https://data.cityofnewyork.us/d/h9gi-nx95)

The dataset contains information about reported traffic collisions in NYC, including:

* Collision dates.
* Collision times.
* Boroughs.
* ZIP codes.
* Geographic coordinates.
* Injuries.
* Fatalities.
* Contributing factors.
* Vehicle information.

#### Transportation Data Considerations

Crash counts and injury counts represent different measurements.

One collision can involve multiple injured people.

Additionally:

* Not every collision results in an injury.
* Missing geographic information does not indicate zero collisions.
* Raw crash counts should not be described as crash rates without an appropriate denominator.

This dataset appears under NYC Open Data's Public Safety category rather than the recommended transportation dataset catalog.

Its selection must therefore be justified as relevant to transportation and road safety. The team should confirm its acceptability with the teaching staff if necessary.

### 4.3 Dataset Feasibility Documentation

For datasets selected outside the recommended catalog, the notebook must include a short feasibility assessment covering:

1. Number of rows.
2. Number of columns.
3. Available geographic or temporal attributes.
4. Expected integration granularity.
5. Justification for the selected combination.
6. Explanation of how integration supports the research question.

If sampling is necessary because of dataset size, the sampling strategy must be justified.

Do not present an undocumented sample as the complete dataset.

---

## 5. Exploratory Data Analysis Requirements

Both datasets must undergo exploratory analysis before integration.

EDA should include:

* Dataset dimensions.
* Column names and data types.
* Missing-value analysis.
* Duplicate investigation.
* Descriptive statistics.
* Categorical distributions.
* Numerical distributions.
* Initial visualizations.
* Outlier investigation.
* Relevant geographic and temporal patterns.

EDA must identify potential data-quality issues and support later cleaning decisions.

Charts must be appropriate for the variables being analyzed.

All meaningful observations should be supported by actual dataset results.

---

## 6. Pre-Integration Cleaning

Both datasets must be cleaned independently before integration.

### 6.1 Missing Values

Required activities include:

* Investigating missing values.
* Determining whether dropping or imputing is appropriate.
* Justifying important decisions.
* Avoiding unsupported value replacements.

Not every missing value represents an error.

For example, a missing permit date might indicate that a construction application has not yet reached the permitting stage.

### 6.2 Outliers

Required activities include:

* Detecting potential outliers.
* Using statistical techniques or domain-specific rules where appropriate.
* Investigating suspicious observations before modifying them.
* Avoiding the automatic deletion of legitimate extreme values.

Possible detection methods include:

* Interquartile Range (IQR).
* Descriptive statistics.
* Distribution analysis.
* Domain-specific validation rules.

A statistically unusual observation is not necessarily incorrect.

### 6.3 Inconsistent Values

Investigate and correct relevant inconsistencies in:

* Categories.
* Strings.
* Geographic identifiers.
* Numerical attributes.
* Date formats.

Standardization should preserve the original meaning of the data.

### 6.4 Duplicate Records

Required activities include:

* Identifying potential duplicates.
* Determining whether duplicates are genuine or represent legitimate repeated events.
* Removing or resolving duplicates when justified.

Duplicate detection should consider the meaning of record identifiers.

### 6.5 Standardization

Standardize relevant fields to support integration.

Examples include:

* ZIP codes.
* Borough names.
* Date representations.
* Geographic identifiers.

All important transformations must be explained in notebook Markdown cells.

---

## 7. Dataset Integration

The university requires meaningful integration between the selected datasets.

Possible integration methods include:

* Shared geographic identifiers.
* ZIP codes.
* Boroughs.
* Community districts.
* Census tracts.
* Time periods.
* Spatial proximity.

### 7.1 Team's Planned Integration Strategy

The selected integration key is **ZIP Code + Year**.

Housing and collision records will be aggregated to a compatible geographic and temporal level before joining.

The exact aggregation metrics must be selected and justified according to the research questions.

### 7.2 Integration Requirements

The notebook must explain:

1. Why the selected integration fields are appropriate.
2. Why the selected granularity is meaningful.
3. Which transformations were required.
4. How the datasets were aggregated.
5. Which join strategy was used.
6. How unmatched records were handled.
7. What limitations the integration introduces.

A direct row-level join is not required.

**Do not perform an uncontrolled many-to-many join between individual housing and collision records.**

Such joins can artificially multiply observations and produce misleading statistics.

### 7.3 Example Integrated Structure

An aggregated dataset might contain:

| ZIP Code | Year | Building Jobs | Traffic Crashes |
| -------- | ---- | ------------- | --------------- |
| 10001    | 2022 | 150           | 320             |
| 10002    | 2022 | 210           | 450             |
| 10003    | 2022 | 100           | 180             |

*These values are illustrative and do not represent actual dataset findings.*

The final structure may contain additional attributes required by the research questions.

---

## 8. Post-Integration Cleaning

**Post-integration cleaning is mandatory.**

After joining the datasets, investigate and resolve:

* Missing values introduced by the join.
* Inconsistent or redundant columns.
* Data type mismatches.
* Unexpected duplicate records.
* Invalid or mismatched geographic identifiers.

The integrated dataset must be validated before research visualizations are generated.

Missing values introduced by unmatched records must not automatically be interpreted as zero.

The notebook must document the cleaning operations performed after integration.

---

## 9. Research Questions and Visualizations

### 9.1 Team Size

The university requires teams of four to six members.

Every team member must contribute at least:

* Two research questions.
* Two visualizations.

| Team Size | Research Questions | Visualizations |
| --------- | -----------------: | -------------: |
| 4 members |                  8 |              8 |
| 5 members |                 10 |             10 |
| 6 members |                 12 |             12 |

The final number of required research questions and visualizations depends on the official registered team size.

### 9.2 Research Question Requirements

Each research question must investigate a meaningful relationship between the two selected datasets.

Questions should preferably explore:

* Geographic patterns.
* Temporal relationships.
* Differences between regions.
* Relationships between development activity and traffic conditions.
* Unexpected or useful findings.

Avoid relying exclusively on simple descriptive counts.

### 9.3 Visualization Requirements

Each research question must have one supporting visualization that directly helps answer it.

Possible visualization types include:

* Bar charts.
* Line charts.
* Scatter plots.
* Heatmaps.
* Geographic maps.

Visualizations must:

* Use appropriate chart types.
* Have clear titles.
* Have readable labels.
* Represent the data accurately.
* Support meaningful conclusions.

Exploratory charts used only for understanding a single dataset do not automatically satisfy the cross-domain research requirement.

### 9.4 Contribution Documentation

The project must clearly identify each team member's contributions.

This includes:

* Research questions.
* Visualizations.
* Data cleaning tasks.
* Dataset integration.
* Website components.
* Other substantial project work.

---

## 10. Interactive Website Requirements

The university requires a fully functional interactive website.

Permitted technologies include:

* Python Dash and Plotly.
* React and Plotly.js.
* Flask.
* Django.
* Other appropriate web frameworks.

The team may choose the implementation framework.

### 10.1 Dropdown Filters

The website must provide multiple dropdown filters.

Potential examples include:

* Borough.
* Year.
* Housing category.
* Transportation category.

Filters must meaningfully affect the displayed data.

### 10.2 Search Mode

Users must be able to enter search expressions.

Example:

`Brooklyn 2022 new buildings`

The website should interpret supported terms and automatically apply the relevant filters.

An external AI language model is not required for this feature.

### 10.3 Generate Report Button

The website must contain a central **Generate Report** button.

When activated, it must dynamically update all relevant visualizations according to the selected filters or search terms.

This functionality is explicitly required.

Missing Generate Report functionality results in grading deductions.

### 10.4 Interactive Visualizations

Charts must support appropriate interactive behavior, such as:

* Hover information.
* Zooming.
* Filter updates.
* Dynamic data exploration.

The website must use multiple visualization types where appropriate.

At least one visualization must explicitly show a relationship between the housing and transportation domains.

### 10.5 Storytelling Section

The website must explain:

1. The research question.
2. Why the research matters.
3. The datasets and methods.
4. Important findings.
5. Research limitations.
6. Potential benefits for NYC.

The website must have a user-friendly and visually consistent layout.

### 10.6 Real-Time Interaction

The website should respond dynamically to user interactions.

Selected filters, search terms, and report generation must produce appropriate updates.

The website should handle invalid inputs and empty results without displaying misleading information.

### 10.7 Deployment

The completed website must be publicly accessible.

Possible deployment services include:

* Vercel.
* Render.
* Heroku.

The team must verify that the deployed website functions correctly before submission.

---

## 11. Jupyter Notebook Requirements

The final Jupyter or Google Colab notebook must document the complete data engineering process.

Required content includes:

1. Introduction and project objective.
2. Dataset selection and justification.
3. Dataset dimensions and relevant attributes.
4. Initial EDA.
5. Pre-integration cleaning.
6. Dataset integration.
7. Post-integration cleaning.
8. Supporting visualizations.
9. Research findings.
10. Conclusions and limitations.
11. Individual contributions.
12. Dataset source links.
13. AI prompts used during the project.

Markdown cells must explain important decisions.

Examples include:

* Why missing rows were removed.
* Why values were imputed.
* Why certain outliers were retained.
* Why a particular join key was selected.
* How the findings were interpreted.

The notebook should demonstrate the reasoning behind the implementation, not only the final code.

### 11.1 Multiple Development Notebooks

The team may use separate notebooks during development.

However, the final submitted workflow must remain understandable and reproducible.

Individual notebooks should clearly identify their responsibilities and dependencies.

The team may assemble a final notebook presenting the complete workflow.

---

## 12. Code Quality Requirements

The university evaluates code quality and documentation.

Implementations should use:

* Descriptive variable names.
* Clear notebook organization.
* Modular functions where appropriate.
* Readable code.
* Comments for complex operations.
* Reproducible processing steps.

Avoid unnecessary complexity and undocumented transformations.

All important conclusions must be supported by actual data.

---

## 13. Grading Considerations

The university evaluates several categories.

### 13.1 Implementation

* Thorough EDA.
* Effective pre-integration cleaning.
* Effective post-integration cleaning.
* Quality of dataset integration.
* Meaningful research questions.
* Relevant visualizations.
* Website interactivity.
* Research originality.
* Quality of the data story.

### 13.2 Documentation

* Clear Markdown explanations.
* Justified cleaning decisions.
* Integration documentation.
* Discussion of alternatives.
* Accurate conclusions.

### 13.3 Code Quality

* Clean structure.
* Descriptive naming.
* Appropriate comments.
* Maintainability.

### 13.4 Explicit Deductions

The specification identifies deductions for:

* Missing or poor contribution documentation.
* Inappropriate visualization choices.
* Unclear chart labels.
* Messy or uncommented code.
* Incorrect or trivial conclusions.
* Unsupported causal claims.
* Missing Generate Report functionality.
* Missing post-integration cleaning.

These should be treated as important quality checks before submission.

---

## 14. Required Deliverables

### 14.1 GitHub Repository

The repository must contain:

* Project source code.
* Notebooks.
* Website files.
* Required documentation.
* README.

### 14.2 Jupyter Notebook

The notebook must demonstrate the complete data engineering workflow, research analysis, and important implementation decisions.

### 14.3 Interactive Website

The website must:

* Be functional.
* Be interactive.
* Support filtering and searching.
* Generate updated reports.
* Present the research story.
* Be publicly deployed.

### 14.4 README

The README must include:

* Project overview.
* Setup instructions.
* Deployment instructions.
* Short descriptions of individual contributions.

---

## 15. Submission Instructions

### 15.1 Official Deadline

The official submission deadline is **November 9, 2026**.

### 15.2 Submission Method

Submission is performed through one email sent to:

**[ICS503Data@gmail.com](mailto:ICS503Data@gmail.com)**

The email must include:

1. University IDs of all team members.
2. GitHub repository link.
3. Deployed website URL.
4. Both selected dataset URLs.

### 15.3 Submission Rules

All required project files must be present in the GitHub repository before the deadline.

The university states that:

* No deadline extensions will be granted.
* Late submissions will not be graded.
* Changes made after the deadline will not be considered.

The team should verify the repository and deployed website before submitting.

---

## 16. Source of Requirements

This document is based on the official GIU Winter 2026 materials:

1. **Project Description.pdf** — Data Engineering and Visualization, Milestone 1.
2. **Data Catalog.pdf** — Recommended Housing and Transportation datasets.

The original university documents are authoritative.

If this summary conflicts with the official project description, the original university instructions take precedence.

The team's internal implementation plan is maintained separately in [TEAM_PLAN.md](TEAM_PLAN.md).

### 16.1 Document Scope

This file documents:

* Official university requirements.
* Selected datasets.
* The team's research direction.
* The planned integration strategy.
* Required deliverables.
* Submission instructions.

It does not define individual implementation assignments.

Team responsibilities, internal phases, and development deadlines belong in `TEAM_PLAN.md`.

AI development instructions belong in the repository's root `AGENTS.md`.
