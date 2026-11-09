ShadowSaaS Radar

Explainable Shadow AI Detection | Identity Security | IAM Behavioral Analytics

Turning Identity Telemetry into Explainable Security Intelligence

---

Project Overview

ShadowSaaS Radar is an independent full-stack cybersecurity research and engineering prototype that explores how identity and authentication telemetry can help organizations identify potential Shadow AI access patterns and investigate identity-related security risks.

The project combines identity log ingestion, application identification, behavioral analytics, explainable risk assessment, and an interactive web application.

It is designed around one central engineering principle:

«Detect what the available evidence supports. Explain why a finding was generated. Make the limitations explicit.»

Live Application:
https://shadow-saa-s-radar-1--alishuayb.replit.app

Source Code:
https://github.com/alishoaip111am-arch/ShadowSaaS-Radar

Public Docker Image:
"ghcr.io/alishoaip111am-arch/shadowsaas-radar:latest"

Docker Package:
https://github.com/users/alishoaip111am-arch/packages/container/package/shadowsaas-radar

«Demo Safety: Use synthetic or non-sensitive sample data only. Do not upload confidential organizational logs or personally identifiable information to the public demo.»

---

1. Executive Summary

The rapid adoption of generative AI introduces a growing identity security and governance challenge.

Employees may access AI applications using corporate identities without sufficient organizational visibility. Security teams therefore need better ways to identify potentially unauthorized application access and understand its significance.

ShadowSaaS Radar investigates how existing identity telemetry can contribute to this challenge.

The platform provides:

- Authentication event ingestion and normalization.
- Application catalog matching for known generative AI services.
- Shadow AI authentication pattern detection.
- Explainable risk scoring and severity classification.
- IAM behavioral analytics.
- Evidence-based security reporting.
- REST API development using FastAPI.
- An interactive React and TypeScript frontend.
- Docker-based application packaging.
- Automated CI/CD workflows using GitHub Actions.

Rather than treating every authentication event as a security incident, the system analyzes observable access patterns and generates contextual findings to support investigation and risk prioritization.

---

2. The Security Problem

Generative AI adoption creates new challenges for identity visibility and data governance.

Organizations may face situations where:

- Employees authenticate to AI services without formal organizational approval.
- Security teams have incomplete visibility into AI application access.
- Corporate identities are used with services outside approved application inventories.
- Repeated authentication patterns are difficult to investigate manually.
- Existing identity logs contain useful security signals but provide limited visibility into activity inside applications.

Traditional authentication monitoring can identify access events. Understanding their security significance requires application identification, event correlation, behavioral analysis, and contextual risk assessment.

ShadowSaaS Radar explores how existing identity telemetry can be transformed into explainable indicators of potential Shadow AI access.

---

3. Results at a Glance

The project has been evaluated through two separate experimental tracks.

3.1 Synthetic Shadow AI Benchmark

Metric| Result
Simulated employees| 200
Authentication events| 1,688
Expected AI usage pairs| 90
Detected pairs| 90
True positives| 90
False positives| 0
False negatives| 0
Precision| 100%
Recall| 100%
F1-score| 100%

Research integrity: These metrics apply exclusively to predefined synthetic scenarios. Expected labels were defined by the project author using the same pattern definitions as the detector. They demonstrate consistency against the synthetic benchmark, not independently established real-world detection accuracy.

3.2 Real Anonymized IAM Behavioral Analysis

Metric| Result
Real anonymized IAM events| 2,184,272
Target behavioral events examined| 18,542
Users analyzed| 8,890
Behavioral alerts generated| 48
HIGH severity alerts| 8
MEDIUM severity alerts| 40
Reported processing time| Approximately 5.85 seconds

The real IAM dataset evaluates a separate behavioral analysis pipeline. It does not identify specific AI application usage.

3.3 Engineering Achievements

- Full-stack application using React, TypeScript, and FastAPI.
- Modular Python ingestion and detection architecture.
- HENNGE-style authentication CSV adapter.
- Processing of more than 2.18 million real anonymized IAM events.
- Automated Docker image build and runtime smoke testing.
- Public Docker image published through GitHub Container Registry.
- GitHub Actions workflow for image publication and container verification.

---

4. Core Capabilities

4.1 Shadow AI Detection

The detection pipeline identifies potential access to known generative AI applications through authentication telemetry.

Capabilities include:

- Matching authentication targets against a structured application catalog.
- Identifying known generative AI application names, domains, and configured SSO service names.
- Detecting one-off, repeated, and habitual authentication patterns.
- Analyzing successful authentication frequency across active days.
- Generating explainable risk scores.
- Providing supporting evidence for each finding.
- Separating application identification from assumptions about actual application activity.

The application catalog currently includes:

Application| Category
ChatGPT| Generative AI
Claude| Generative AI
Google Gemini| Generative AI
Microsoft Copilot| Generative AI
Perplexity| Generative AI
DeepSeek| Generative AI
Dropbox| File Sharing

Catalog entries are maintained independently of the detection engine.

4.2 Identity and Authentication Log Engineering

The ingestion architecture supports multiple authentication data sources through a common event representation.

Capabilities include:

- Generic authentication CSV ingestion.
- HENNGE Access Control CSV adapter.
- Event normalization into a shared data model.
- Authentication outcome validation.
- Preservation of additional source metadata.
- Handling of source-specific fields and optional values.
- Separation of successful authentication events from failed sign-ins.

4.3 IAM Behavioral Analytics

A separate experimental pipeline analyzes real anonymized IAM telemetry to identify identity-related behavioral patterns.

Capabilities include:

- Large-scale IAM event processing.
- Behavioral event filtering.
- Failed-password threshold event analysis.
- Repeated behavioral activity detection within a 15-minute window.
- Severity-based alert generation.
- Optimized CSV processing.
- Comparison of optimized results against the original implementation.

4.4 Explainable Security Reporting

The reporting layer transforms analysis results into structured security findings.

Each finding can include:

- User identification.
- Application identification.
- Risk score and severity classification.
- Authentication event counts.
- Number of active days.
- Supporting behavioral evidence.
- Relevant assumptions and limitations.

The objective is to make security findings understandable and reviewable rather than presenting unexplained risk scores.

4.5 Full-Stack Web Application

The application combines:

- React and TypeScript frontend.
- Vite frontend build system.
- Python backend using FastAPI.
- REST API endpoints for security analysis.
- Authentication log upload and analysis workflows.
- Interactive findings and risk presentation.
- Backend-powered security analysis.

---

5. Technical Architecture

The project follows a modular architecture that separates ingestion, application identification, behavioral detection, risk analysis, and reporting.

Component| Responsibility
Frontend| Interactive analysis interface
API Layer| Backend application and analysis requests
Ingestion Layer| Parses, validates, and normalizes authentication events
Event Model| Common representation for different log sources
Application Catalog| Matches known applications and SSO service names
Detection Engine| Identifies authentication behavior patterns
Risk Engine| Calculates explainable risk scores and severity
Reporting Layer| Produces structured findings and supporting evidence
IAM Behavioral Engine| Analyzes identity-related behavioral events
Data Processing Pipeline| Processes large IAM datasets efficiently

Engineering Approach

The implementation emphasizes:

- Separation of responsibilities across modules.
- Reusable event normalization.
- Explicit input validation.
- Explainable detection decisions.
- Reproducible experimental datasets.
- Automated regression testing.
- Separation of synthetic evaluation from real-data analysis.
- Clear distinction between observed evidence and inferred risk.

---

6. Technology Stack

Backend and Data Processing

- Python 3.11
- FastAPI
- CSV processing
- Modular Python architecture
- pytest
- REST API development

Frontend

- React
- TypeScript
- Vite
- CSS
- npm

Cybersecurity and Analytics

- Identity and Access Management (IAM)
- Single Sign-On (SSO)
- User and Entity Behavior Analytics (UEBA)
- Shadow AI access monitoring
- Authentication security
- Behavioral pattern detection
- Explainable risk scoring

DevOps and Engineering

- Git and GitHub
- Docker
- GitHub Actions
- GitHub Container Registry (GHCR)
- Multi-stage Docker builds
- Container runtime health verification
- Automated frontend build
- Reproducible evaluation

---

7. Docker Deployment and Container Registry

ShadowSaaS Radar is packaged as a Docker image and published publicly through GitHub Container Registry.

Published Image

Registry: GitHub Container Registry (GHCR)

Image:

"ghcr.io/alishoaip111am-arch/shadowsaas-radar:latest"

Package:

https://github.com/users/alishoaip111am-arch/packages/container/package/shadowsaas-radar

The package is publicly accessible.

Pull the Docker Image

docker pull ghcr.io/alishoaip111am-arch/shadowsaas-radar:latest

Run the Container

docker run -d \
  --name shadowsaas-radar \
  -p 8000:8000 \
  ghcr.io/alishoaip111am-arch/shadowsaas-radar:latest

Verify Application Health

curl http://localhost:8000/api/health

Open the application:

"http://localhost:8000"

Docker Engineering

The Docker implementation uses a multi-stage build:

1. Frontend build stage: Uses Node.js to install dependencies and generate the production frontend.
2. Backend runtime stage: Uses Python 3.11 slim to install backend dependencies and run FastAPI.
3. Production assets: Copies the compiled frontend into the backend image.
4. Runtime configuration: Exposes port 8000 and supports the PORT environment variable.
5. Container security: Runs the application using a non-root application user.

Automated Docker Workflow

GitHub Actions automates the Docker delivery process.

The workflow:

- Checks out the repository.
- Configures Docker Buildx.
- Authenticates to GHCR using the repository-provided GitHub token.
- Builds and publishes the Docker image.
- Publishes the "latest" and commit-specific tags.
- Pulls the published image.
- Runs the container.
- Checks the backend health endpoint.
- Verifies the frontend HTTP response.
- Cleans up the test container.

This provides an automated build and runtime smoke-test process before considering a container release successful.

Important: GHCR publication and container verification do not, by themselves, constitute deployment to a production hosting environment.

---

8. Data Sources and Experimental Methodology

ShadowSaaS Radar uses two distinct data sources for different evaluation purposes.

Their results are intentionally reported separately to avoid confusing synthetic Shadow AI detection performance with real-world IAM behavioral analysis.

8.1 HENNGE Access Control Adapter

The HENNGE adapter follows publicly available HENNGE Access Control access-log documentation.

Documentation:

https://support.hdeone.com/hc/en-us/articles/11374378879641

The adapter supports documented authentication fields, including:

- "Timestamp"
- "Username"
- "Login successful"
- "SSO Target"

Additional documented fields are preserved as event metadata where available.

Data Validation

The adapter:

- Accepts TRUE and FALSE login-success values case-insensitively.
- Rejects invalid authentication outcome values.
- Preserves optional documented metadata.
- Accepts empty SSO Target values where a login type does not identify a connected service.
- Rejects missing usernames.
- Distinguishes authentication outcomes from application activity.

Validation Status

The HENNGE adapter was evaluated using reproducible synthetic HENNGE-style authentication records.

No real HENNGE customer access logs were available for this research. Compatibility with actual customer exports has therefore not yet been independently validated.

HENNGE Synthetic Evaluation

Metric| Result
Simulated employees| 200
Authentication events| 1,688
Expected AI usage pairs| 90
Detected pairs| 90
True positives| 90
False positives| 0
False negatives| 0
Precision| 100%
Recall| 100%
F1-score| 100%

These results apply only to the generated dataset and its predefined scenarios.

8.2 Real Anonymized IAM-UEBA Dataset

The project also includes an experimental IAM behavioral analysis pipeline evaluated using a real anonymized IAM dataset published on Zenodo.

Dataset information

- Dataset: IAM-UEBA Dataset
- Authors: Mayor Gallego, Vicente Jesús; Estepa Alonso, Rafael María; Estepa Alonso, Antonio José; Diaz-Verdejo, Jesús E.
- Source: Zenodo
- DOI: "10.5281/zenodo.22871318"
- License: Creative Commons Attribution 4.0 International (CC BY 4.0)

Original dataset:

https://zenodo.org/records/22871318

The dataset contains 2,184,272 real anonymized IAM events collected from a cloud identity and access management environment.

It includes authentication, provisioning, administrative, service, and system events.

The dataset is not redistributed with this repository.

Experimental Results

Metric| Result
Total dataset events| 2,184,272
Target behavioral events| 18,542
Users analyzed| 8,890
Total alerts| 48
HIGH severity alerts| 8
MEDIUM severity alerts| 40
Reported processing time| Approximately 5.85 seconds

The experiment analyzes "exceed_failed_password_limit" events using a 15-minute behavioral window.

The optimized CSV processing pipeline produced the same 48 alerts as the original implementation.

Interpretation and Limitations

- The dataset contains real anonymized IAM telemetry.
- It is not an AI application usage dataset.
- Anonymized application identifiers cannot reliably be mapped to ChatGPT, Claude, Gemini, or other specific AI services.
- "exceed_failed_password_limit" represents a failed-password threshold event, not an individual failed password attempt.
- The dataset does not provide ground-truth labels for calculating detection precision or recall.
- Generated alerts indicate behavior requiring security review; they do not prove an attack or compromised account.

This experiment demonstrates ingestion, IAM behavioral analysis, and processing performance on real public telemetry. It does not validate Shadow AI detection accuracy.

---

9. Authentication Pattern Classification

The Shadow AI detection engine classifies authentication behavior into three patterns.

Pattern| Definition
"one_off"| One authentication event
"repeated"| Multiple events on fewer than three distinct days
"habitual"| Events across three or more distinct days

The detection engine analyzes successful authentication events per user and application according to its implemented event-selection logic.

These patterns represent authentication behavior, not confirmed application usage.

---

10. Explainable Risk Model

The current risk model uses initial engineering weights.

These are configurable design assumptions, not a validated security standard.

Factor| Rule
Active days| +10 per day, up to 5 days
Authentication events| +2 per event, up to 10 events
Free account, when available| +20
Approved application, account not marked free| Score capped at 25
Single authentication event| Score capped at 15
Maximum score| 100

Severity Classification

Severity| Score
LOW| 0–29
MEDIUM| 30–59
HIGH| 60–100

Risk Interpretation

The score is a prioritization aid, not a probability of compromise or proof of a policy violation.

The model follows several important principles:

1. Approved applications are not automatically risk-free.
2. Enterprise accounts are not automatically approved.
3. Free accounts are not evidence of compromise.
4. Unknown account types are not automatically classified as free.
5. A single authentication event should not be interpreted as confirmed misuse.

Risk weights and thresholds require further calibration using independently labeled data.

---

11. Input Formats

HENNGE Access Control CSV

Required columns:

Timestamp,Username,Login successful,SSO Target

Additional documented fields are preserved as metadata where available.

Important: The HENNGE format does not provide account-type information. Free-account status cannot be inferred from these logs.

Generic Authentication CSV

The generic ingestion format converts supported CSV records into the common event model.

The event model supports:

- Timestamp
- User
- Source
- Event type
- Target
- Authentication outcome
- Optional device ID
- Optional IP address
- Additional metadata

Refer to the project implementation and sample data for the exact supported input conventions.

---

12. Reproducibility and Local Execution

Clone the Repository

git clone https://github.com/alishoaip111am-arch/ShadowSaaS-Radar.git
cd ShadowSaaS-Radar

Install Python Dependencies

python -m pip install -r requirements.txt

Generate Synthetic HENNGE-Style Logs

python scripts/generate_hennge_logs.py \
  --employees 200 \
  --days 90 \
  --failure-rate 0.05 \
  --seed 42

Run HENNGE Analysis

python main.py data/hennge_synthetic.csv --source hennge

Run Automated Tests

python -m pytest -q

Run IAM Behavioral Analysis

The IAM-UEBA dataset is not included in this repository.

Download the original dataset from Zenodo and place the extracted "events.csv" file at:

"data/real/events.csv"

This path is excluded from version control through ".gitignore".

Then run:

python iam_main.py data/real/events.csv

Build the Frontend

cd frontend
npm install
npm run build

---

13. Security Limitations and Responsible Use

ShadowSaaS Radar is an educational research and engineering prototype.

Its findings must be interpreted within the limits of the available telemetry.

What Authentication Logs Can Show

Depending on the source, authentication records may provide evidence of:

- An authentication attempt.
- A successful or failed sign-in.
- An identity associated with an event.
- A configured SSO target.
- Repeated access patterns over time.

What Authentication Logs Cannot Establish

Authentication events alone do not prove:

- That a user submitted an AI prompt.
- That a file was uploaded or downloaded.
- That information was shared with an external service.
- That data exfiltration occurred.
- That an organizational policy was violated.
- That an account was compromised.
- That malicious intent existed.

An absence of an authentication event is not proof that an activity did not occur.

Additional Limitations

- Services accessed outside organizational SSO may not appear.
- HENNGE SSO Target values are organization-configured service names, not necessarily application domains.
- Generic service names must not be automatically mapped to AI applications.
- HENNGE logs do not provide free-versus-enterprise account information.
- Unknown account type is not treated as free.
- The application catalog covers a limited set of services.
- Risk weights and thresholds require independent validation.
- The HENNGE adapter has not been validated against real customer exports.
- The IAM-UEBA dataset does not identify specific generative AI applications.
- Real-world Shadow AI detection accuracy has not yet been established.

Responsible Use

The project is intended for educational research, engineering experimentation, and security analytics prototyping.

Findings should be reviewed by qualified personnel before any operational decision is made.

The public demonstration should only be used with synthetic or non-sensitive sample data.

The current prototype should not be treated as a production-ready enterprise security monitoring platform.

---

14. Roadmap

Potential future development areas include:

- Additional identity-provider adapters.
- Expanded application catalog coverage.
- More authentication log formats.
- Configurable organizational policies.
- Explainable risk-factor breakdowns.
- Historical trend analysis.
- Improved user and session correlation.
- Authentication and authorization for the API.
- Role-based dashboard access.
- Rate limiting and audit logging.
- Integration with additional security telemetry.
- Validation against independently labeled real-world datasets.

A particularly important research direction is combining identity authentication evidence with authorized application telemetry to distinguish access from actual application activity.

---

15. License and Attribution

This project is released under the MIT License.

The IAM-UEBA dataset is separately distributed under the Creative Commons Attribution 4.0 International license.

Dataset source:

https://doi.org/10.5281/zenodo.22871318

The dataset's original attribution and license terms must be respected when using or redistributing it.

HENNGE and the names of third-party applications are referenced solely to describe supported log formats or application categories. Their trademarks remain the property of their respective owners.

ShadowSaaS Radar is an independent project and is not affiliated with, sponsored by, or endorsed by HENNGE or any of the referenced application providers.

---

16. Project Purpose

ShadowSaaS Radar explores how identity telemetry can contribute to AI application visibility and IAM security analysis.

Its central engineering principle is simple:

«Detect what the available evidence supports. Explain why a finding was generated. Make the limitations explicit.»

The project brings together:

- Data ingestion and event normalization.
- Application identification.
- Shadow AI authentication pattern detection.
- Explainable risk assessment.
- IAM behavioral analytics.
- REST API development.
- Frontend engineering.
- Automated testing.
- Docker packaging and distribution.
- CI/CD workflow engineering.
- Reproducible experimental evaluation.

It is an integrated engineering effort combining Python and TypeScript to investigate a growing identity security challenge.

---

Project Links

- Live Application: https://shadow-saa-s-radar-1--alishuayb.replit.app
- GitHub Repository: https://github.com/alishoaip111am-arch/ShadowSaaS-Radar
- Docker Image (GHCR): https://github.com/users/alishoaip111am-arch/packages/container/package/shadowsaas-radar
- IAM-UEBA Dataset: https://zenodo.org/records/22871318
- HENNGE Access Control Documentation: https://support.hdeone.com/hc/en-us/articles/11374378879641

---

ShadowSaaS Radar

Turning Identity Telemetry into Explainable Security Intelligence.

Status: Independent research and engineering prototype with a full-stack web interface and publicly published Docker image.

License: MIT (project code). Third-party dataset licensing remains separate.
