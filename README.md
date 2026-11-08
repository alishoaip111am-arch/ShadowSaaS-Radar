ShadowSaaS Radar

An Open-Source Security Analytics Platform for Shadow AI Visibility and IAM Behavioral Analysis

ShadowSaaS Radar is a full-stack security analytics project designed to help security teams examine identity authentication events, identify authentication activity associated with AI applications, and analyze selected IAM behavioral signals.

It combines a Python-based detection and risk assessment engine with a FastAPI backend and a React dashboard.

The project focuses on a practical security question:

What can identity authentication logs reveal about access to AI applications, and where do those logs stop providing evidence?

ShadowSaaS Radar emphasizes evidence-based analysis, explainable findings, and transparent limitations rather than claiming to detect activities that authentication logs cannot establish.

---

1. Project Overview

Organizations are increasingly adopting AI applications such as ChatGPT, Claude, Gemini, Microsoft Copilot, and Perplexity.

Employees may access these services using corporate identities, including through Single Sign-On (SSO). This creates an identity visibility challenge: security teams may need to understand which AI-related services appear in authentication records and whether the observed activity warrants further review.

ShadowSaaS Radar provides an analytical workflow for examining these records.

Core capabilities

- Shadow AI Authentication Analysis: Identifies authentication events associated with known AI applications in supported identity-log formats.
- HENNGE Access Log Adapter: Supports a documented HENNGE Access Log column format.
- Application Catalog: Maps application names and SSO identifiers to categorized services.
- Risk Assessment: Produces explainable, rule-based risk scores and findings.
- IAM Behavioral Analysis: Analyzes selected IAM event patterns using a separate behavioral detection pipeline.
- CSV Upload: Allows users to submit supported datasets through a browser interface.
- Interactive Dashboard: Presents metrics, findings, evidence, assumptions, and analysis reports.
- REST API: Exposes analysis functionality through FastAPI endpoints.

What the project does not claim

Authentication evidence does not establish that a user uploaded a file, submitted sensitive information, transferred data, or violated organizational policy.

The project does not claim to detect data exfiltration, compromise, or actual AI prompt activity from SSO authentication records alone.

---

2. Architecture

The application uses a layered architecture that keeps the original Python analysis engines separate from the web interface.

                    USER
                     |
                     v
          React + TypeScript Dashboard
                     |
                     v
                FastAPI
                     |
          +----------+----------+
          |                     |
          v                     v
   Shadow AI API           IAM Analysis API
          |                     |
          v                     v
   CSV / HENNGE Adapter    IAM-UEBA Adapter
          |                     |
          v                     v
   Normalized Events       IAM Event Stream
          |                     |
          v                     v
   Application Catalog    Behavioral Engine
          |                     |
          v                     |
   Shadow AI Detection          |
          |                     |
          v                     v
      Risk Engine          IAM Findings
          |                     |
          +----------+----------+
                     |
                     v
              JSON Results
                     |
                     v
              React Dashboard

Technology stack

Layer| Technology
Backend| Python
API| FastAPI
Frontend| React
Language| TypeScript
Frontend tooling| Vite
Data processing| CSV-based ingestion
Testing| pytest
API testing| FastAPI TestClient / HTTPX
Deployment| Replit Autoscale
Version control| Git / GitHub

The web application calls the original Python analysis modules. The detection and risk logic is not reimplemented in JavaScript.

---

3. Detection and Analysis Modules

3.1 Shadow AI Detection

The Shadow AI pipeline processes normalized authentication events and compares application targets against a maintained application catalog.

The catalog includes:

- ChatGPT
- Claude
- Google Gemini
- Microsoft Copilot
- Perplexity
- DeepSeek
- Dropbox

Applications are categorized according to their service type, including generative AI and file-sharing services.

Application identification uses catalog mappings and supported SSO target names. Results depend on the quality and completeness of the supplied authentication records.

3.2 Risk Assessment Engine

The risk engine evaluates detected application usage patterns and produces explainable risk findings.

Its analysis can consider:

- Application classification
- Observed authentication frequency
- Repeated access patterns
- Available account metadata
- Organizational approval status

The engine distinguishes between observed evidence and inferred risk.

Important: Risk scores are experimental rule-based indicators. They are not probabilities of compromise, validated security ratings, or proof of policy violations.

An approved application is not automatically considered risk-free, and an authentication event alone does not establish whether an account is free or enterprise.

3.3 IAM Behavioral Analysis

The separate IAM behavioral pipeline analyzes selected identity and access management events.

It supports the examination of behavioral patterns such as repeated failed-password-limit events.

The IAM pipeline is independent of the Shadow AI application detector.

Its findings must not be interpreted as evidence of AI application usage.

---

4. Supported Data Sources

HENNGE Access Log Format

ShadowSaaS Radar includes a HENNGE Access Log adapter based on publicly documented log fields.

The adapter supports the following columns:

Field| Purpose
Timestamp| Authentication event time
Username| Identity associated with the event
Login successful| Authentication outcome
SSO Target| Target SSO service
IP address| Optional network metadata
Device Type| Optional device metadata
Detail| Optional event details
Reason| Optional authentication reason
Login Type| Optional login classification

The adapter validates required fields and accepts case-insensitive TRUE/FALSE authentication outcomes.

Optional fields are retained as event metadata where available.

An empty SSO Target is accepted because some documented login types may not contain a target service.

Integration status: The adapter is implemented against publicly documented HENNGE Access Log fields. It has not been validated against a private customer export.

The HENNGE dataset used in the included benchmark is synthetic, not real HENNGE customer data.

ShadowSaaS Radar is an independent project and is not affiliated with, sponsored by, or endorsed by HENNGE.

Generic CSV

The generic ingestion pipeline supports the project's normalized event format.

It converts supported CSV records into normalized event objects before analysis.

IAM-UEBA Dataset

The project also includes a separate integration with the IAM-UEBA dataset.

Dataset source:

- Title: IAM-UEBA
- DOI: https://doi.org/10.5281/zenodo.22871318
- License: Creative Commons Attribution 4.0 International (CC BY 4.0)
- Dataset size: 2,184,272 events
- Users / actors: 27,893

The dataset contains anonymized IAM activity, including login portal, provisioning API, service API, administrative console, and system job events.

It is used to evaluate the IAM behavioral analysis pipeline.

It is not an AI application usage dataset and does not establish access to ChatGPT, Claude, Gemini, or other AI services.

The original dataset is not included in the Git repository because of its size.

---

5. Research and Evaluation

The project uses two separate evaluation tracks. Their results must not be combined into a single accuracy claim.

Track A — Synthetic Shadow AI Benchmark

A reproducible synthetic dataset was generated to evaluate the Shadow AI detection pipeline against predefined scenarios.

Metric| Result
Synthetic employees| 200
Authentication events| 1,688
Expected AI-related pairs| 90
Detected pairs| 90
True positives| 90
False positives| 0
False negatives| 0
Precision| 100%
Recall| 100%
F1-score| 100%
Pattern classification accuracy| 100%

The 90 expected pairs consisted of:

Scenario| Count
Habitual access| 24
Repeated access| 27
One-off access| 39
Total| 90

The benchmark also included account-type metadata scenarios:

Account metadata| Count
Unknown| 31
Enterprise| 29
Free| 30
Total| 90

Interpretation and limitation

These metrics describe performance against the benchmark's own synthetic ground-truth labels.

The labels were defined using the same scenario definitions that guide the detector. Therefore, the results demonstrate implementation consistency on controlled synthetic cases, not real-world detection accuracy or independently validated generalization.

The dataset does not represent real employee activity or HENNGE customer records.

Track B — Real IAM-UEBA Dataset

The second evaluation uses the real anonymized IAM-UEBA dataset.

Recorded execution results:

Metric| Result
Dataset events| 2,184,272
Events examined for the reported failed-password analysis| 18,542
Users examined| 8,890
Generated alerts| 48
High-severity alerts| 8
Medium-severity alerts| 40
Reported analysis time| Approximately 5.85 seconds

The reported alert counts are outputs of the configured behavioral rules.

No independently established ground-truth labels were available for this experiment. Consequently, precision, recall, and F1-score are not claimed for this IAM evaluation.

The two evaluation tracks measure different capabilities and use different datasets.

---

6. Full-Stack Dashboard

The frontend provides a browser-based interface for running the analysis engines.

Shadow AI Analysis

Users can:

1. Select the input format.
2. Choose Generic CSV or HENNGE Access Log.
3. Upload a supported CSV file.
4. Submit the dataset for analysis.
5. Review detected application activity.
6. Examine risk findings and supporting evidence.
7. Read assumptions and limitations.

IAM Behavioral Analysis

Users can:

1. Select the IAM analysis tab.
2. Upload a supported IAM CSV dataset.
3. Run the behavioral analysis.
4. Review event and user metrics.
5. Examine generated alerts and severity levels.

Dashboard output

The dashboard presents:

- Analysis metrics
- Application findings
- Risk levels and scores
- Evidence associated with findings
- Behavioral alerts
- Assumptions and limitations
- Generated analysis reports

The dashboard is intended to support investigation and review, not to replace security analyst judgment.

---

7. REST API

The FastAPI backend exposes the following endpoints:

Method| Endpoint| Description
GET| "/api/health"| Health check
POST| "/api/analyze/shadow-ai"| Shadow AI authentication analysis
POST| "/api/analyze/iam"| IAM behavioral analysis

Interactive API documentation is available at:

/docs

The application serves the production frontend from the FastAPI application after the frontend build is generated.

API implementation

The backend uses the existing project modules, including:

shadowsaas/ingestion/
shadowsaas/catalog/
shadowsaas/detection/
shadowsaas/engine/
shadowsaas/reporting/

Uploaded files are processed through temporary storage and cleaned up after analysis.

The current upload limit is 10 MB. The API validates CSV file extensions and rejects empty uploads.

Deployment security note: The current public API does not implement user authentication, authorization, or rate limiting. It should be treated as a research demonstration, not as a production-secure enterprise service. Do not upload confidential employee logs or sensitive organizational data to a publicly accessible deployment.

---

8. Project Structure

ShadowSaaS-Radar/
|
|-- api.py
|-- main.py
|-- iam_main.py
|-- requirements.txt
|-- .replit
|-- .gitignore
|-- LICENSE
|-- README.md
|
|-- shadowsaas/
|   |
|   |-- ingestion/
|   |   |-- event.py
|   |   |-- csv_loader.py
|   |   |-- hennge_adapter.py
|   |   |-- iam_ueba_adapter.py
|   |
|   |-- catalog/
|   |   |-- loader.py
|   |   |-- app_catalog.json
|   |
|   |-- detection/
|   |   |-- shadow_ai.py
|   |
|   |-- engine/
|   |   |-- risk_engine.py
|   |   |-- iam_behavioral_engine.py
|   |
|   |-- reporting/
|       |-- report_generator.py
|
|-- frontend/
|   |-- src/
|   |   |-- App.tsx
|   |   |-- App.css
|   |   |-- index.css
|   |   |-- main.tsx
|   |-- package.json
|   |-- package-lock.json
|   |-- vite.config.ts
|
|-- scripts/
|
|-- tests/
|
|-- data/
    |-- samples/
    |-- hennge_synthetic.csv
    |-- real/
        |-- events.csv  (not committed)

Generated build artifacts and large real datasets are excluded from version control.

---

9. Run Locally

Requirements

- Python 3.11 or compatible version
- Node.js 20 or compatible version
- npm

Step 1 — Clone the repository

git clone https://github.com/alishoaip111am-arch/ShadowSaaS-Radar.git

cd ShadowSaaS-Radar

Step 2 — Create a Python environment

python -m venv .venv

Activate it:

source .venv/bin/activate

Step 3 — Install backend dependencies

pip install -r requirements.txt

Step 4 — Install frontend dependencies

cd frontend

npm ci

Step 5 — Build the frontend

npm run build

Return to the project root:

cd ..

Step 6 — Start the application

.venv/bin/python -m uvicorn api:app --host 0.0.0.0 --port 8000

Open:

http://localhost:8000

API documentation:

http://localhost:8000/docs

---

10. Testing

The project includes tests for ingestion, application identification, risk assessment, IAM behavioral analysis, and API behavior.

Run the test suite:

.venv/bin/python -m pytest -q

Recorded project verification:

72 passed

The recorded full test run completed successfully.

Frontend production build:

cd frontend
npm ci
npm run build

The production build completed successfully using Vite and TypeScript.

API verification covered:

- Health endpoint
- Frontend serving
- Generic CSV analysis
- HENNGE CSV analysis
- IAM CSV analysis

Test results describe the tested project version and environment; they are not a guarantee of production reliability.

---

11. Replit Deployment

The project is configured to run as a single FastAPI application serving both the API and the built frontend.

The deployment process:

1. Creates a Python virtual environment.
2. Installs backend dependencies.
3. Installs frontend dependencies.
4. Builds the React application.
5. Starts Uvicorn on port 8000.

The production deployment uses:

.venv/bin/python -m uvicorn api:app --host 0.0.0.0 --port 8000

The frontend build is served from:

frontend/dist

Before deploying, verify that the dependencies install successfully, the frontend builds, and the API starts correctly.

Public deployment should use synthetic or non-sensitive demonstration data until appropriate authentication, access controls, rate limiting, and operational safeguards are implemented.

---

12. Security, Privacy, and Analytical Limitations

ShadowSaaS Radar is designed around an important distinction: observed authentication evidence is not the same as observed application activity.

What authentication logs can support

Depending on the source and available fields, authentication records can support analysis of:

- Identity associated with an authentication event
- Timestamp of the event
- Authentication success or failure
- SSO target or service identifier
- Available IP and device metadata
- Repeated authentication patterns

What authentication logs cannot establish by themselves

They do not establish:

- Whether an employee submitted a prompt to an AI service
- Whether a file was uploaded or downloaded
- Whether sensitive information was shared
- Whether a user transferred or exfiltrated data
- Whether an AI account was free or enterprise when this information is absent
- Whether a user violated organizational policy
- Whether an account or device was compromised

Data quality considerations

Results depend on:

- Source log completeness
- Correct timestamps and identity fields
- Application catalog coverage
- SSO naming consistency
- Available account metadata
- Dataset-specific event semantics

Missing fields must not be interpreted as proof that an activity did not occur.

Responsible use

The project is intended for educational research, engineering experimentation, and security analytics prototyping.

Findings should be reviewed by qualified personnel before any operational decision is made.

---

13. Roadmap

Potential future development areas include:

- Additional identity-provider adapters
- Expanded application catalog coverage
- More authentication log formats
- Configurable organizational policies
- Explainable risk-factor breakdowns
- Historical trend analysis
- Improved user and session correlation
- Authentication and authorization for the API
- Role-based dashboard access
- Rate limiting and audit logging
- Integration with additional security telemetry
- Validation against independently labeled real-world datasets

A particularly important research direction is combining identity authentication evidence with authorized application telemetry to distinguish access from actual application activity.

---

14. License and Attribution

This project is released under the MIT License.

The IAM-UEBA dataset is separately distributed under the Creative Commons Attribution 4.0 International license.

Dataset source:

https://doi.org/10.5281/zenodo.22871318

The dataset's original attribution and license terms must be respected when using or redistributing it.

HENNGE and the names of third-party applications are referenced solely to describe supported log formats or application categories. Their trademarks remain the property of their respective owners.

ShadowSaaS Radar is an independent project and is not affiliated with, sponsored by, or endorsed by HENNGE or any of the referenced application providers.

---

15. Project Purpose

ShadowSaaS Radar explores how identity telemetry can contribute to AI application visibility and IAM security analysis.

Its central engineering principle is simple:

Detect what the available evidence supports. Explain why a finding was generated. Make the limitations explicit.

The project brings together data ingestion, event normalization, application identification, risk assessment, behavioral analysis, REST API development, frontend engineering, testing, and reproducible evaluation in one integrated Python and TypeScript application.

Repository: https://github.com/alishoaip111am-arch/ShadowSaaS-Radar

Status: Research and engineering prototype with a full-stack web interface.
