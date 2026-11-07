ShadowSaaS Radar

Explainable Shadow AI Detection | Identity Security | IAM Behavioral Analytics

""Python" (https://img.shields.io/badge/Python-3.x-blue.svg)" (https://www.python.org/)
"Cybersecurity" (https://img.shields.io/badge/Domain-Cybersecurity-red.svg)
"IAM" (https://img.shields.io/badge/Focus-IAM%20%7C%20SSO%20%7C%20UEBA-purple.svg)
"Research" (https://img.shields.io/badge/Project-Independent%20Security%20Research-success.svg)

---

Executive Summary

What happens when employees access AI applications that remain invisible to an organization's security monitoring systems?

The rapid adoption of generative AI is creating a new identity security challenge: organizations need better visibility into which AI services are being accessed through corporate identities, particularly when application usage falls outside established security governance.

ShadowSaaS Radar is an independent Python-based cybersecurity research prototype designed to investigate this challenge through identity and authentication telemetry.

The system transforms raw authentication events into structured security intelligence by combining:

- Application catalog matching for known generative AI services.
- Authentication event ingestion and normalization.
- Behavioral analysis of user access patterns.
- Explainable risk scoring and severity classification.
- Evidence-based security reporting.
- Experimental IAM behavioral analytics using real anonymized identity telemetry.

Rather than treating every authentication event as a security incident, the system analyzes activity patterns and provides contextual evidence to support security investigation and risk prioritization.

The project emphasizes explainability, reproducibility, modular engineering, and responsible interpretation of security data.

The Security Problem

The widespread adoption of generative AI introduces significant identity visibility and data-governance challenges.

Organizations may encounter situations where:

- Employees access AI services without formal organizational approval.
- Security teams have incomplete visibility into AI application access.
- Corporate identities are used to authenticate against services outside approved application inventories.
- Repeated authentication patterns are difficult to investigate manually.
- Identity logs contain useful security signals but provide limited visibility into activity occurring inside applications.

Traditional authentication monitoring can identify access events, but extracting meaningful behavioral intelligence requires structured application identification, event correlation, and contextual risk analysis.

ShadowSaaS Radar investigates how existing identity telemetry can be transformed into explainable indicators of potential Shadow AI access.

Results at a Glance

The project has been evaluated through two distinct experimental tracks: a synthetic Shadow AI benchmark and a real anonymized IAM behavioral analysis dataset.

Metric| Result
Real anonymized IAM events processed| 2,184,272
IAM users analyzed| 8,890
Target behavioral events examined| 18,542
Behavioral alerts generated| 48
HIGH severity alerts| 8
MEDIUM severity alerts| 40
Synthetic expected AI usage pairs (self-labeled)| 90
Synthetic detected pairs| 90
Synthetic benchmark precision| 100%
Synthetic benchmark recall| 100%
Synthetic benchmark F1-score| 100%

«Research integrity: The 100% precision, recall, and F1-score results apply exclusively to predefined synthetic scenarios. The expected labels were defined by the project author using the same pattern definitions as the detector, so the result shows consistency with the benchmark, not real-world accuracy. These results do not establish real-world Shadow AI detection accuracy. The real IAM dataset evaluates a separate behavioral analysis pipeline and does not identify specific AI application usage.»

Core Capabilities

1. Shadow AI Detection

The detection pipeline identifies potential access to known generative AI applications through authentication telemetry.

Capabilities include:

- Matching authentication targets against a structured application catalog.
- Identifying known generative AI application names, domains, and configured SSO service names.
- Detecting one-off, repeated, and habitual authentication patterns.
- Analyzing successful authentication frequency across active days.
- Generating explainable risk scores with supporting evidence.
- Distinguishing application identification from assumptions about actual application usage.

2. Identity & Authentication Log Engineering

The ingestion architecture supports multiple authentication data sources through a common event representation.

Capabilities include:

- Generic authentication CSV ingestion.
- HENNGE Access Control CSV adapter.
- Normalization into a shared event model.
- Authentication outcome validation.
- Preservation of additional source metadata.
- Handling of source-specific fields and optional values.
- Separation of successful authentication events from failed sign-ins.

3. IAM Behavioral Analytics

A separate experimental pipeline analyzes real anonymized IAM telemetry to identify identity-related behavioral patterns.

Capabilities include:

- Processing large-scale IAM event datasets.
- Filtering relevant behavioral events.
- Analyzing failed-password threshold events.
- Identifying repeated behavioral activity within a 15-minute window.
- Generating severity-based security alerts.
- Optimized CSV processing for large datasets.
- Comparing optimized processing results against the original implementation.

4. Explainable Security Reporting

The reporting layer converts detection results into structured findings designed for investigation.

Each finding can include:

- User and application identification.
- Risk score and severity classification.
- Authentication event counts.
- Number of active days.
- Supporting behavioral evidence.
- Explicit assumptions and limitations.

The system is designed to make detection decisions understandable rather than presenting unexplained risk scores.

Technical Architecture

The project follows a modular architecture that separates data ingestion, application identification, behavioral detection, risk analysis, and reporting.

Component| Responsibility
Ingestion Layer| Parses, validates, and normalizes authentication events
Event Model| Provides a common representation for different log sources
Application Catalog| Matches known applications, domains, and configured SSO service names
Detection Engine| Identifies authentication behavior patterns
Risk Engine| Calculates explainable risk scores and severity levels
Reporting Layer| Produces structured findings with supporting evidence
IAM Behavioral Engine| Analyzes identity-related behavioral events
Data Processing Pipeline| Processes large IAM CSV datasets efficiently

Engineering Approach

The implementation emphasizes:

- Separation of responsibilities across modules.
- Reusable event normalization.
- Explicit input validation.
- Explainable detection decisions.
- Reproducible experimental datasets.
- Automated regression testing.
- Separation of synthetic evaluation from real-data analysis.

Technology & Skills Demonstrated

Programming & Software Engineering

- Python development.
- Modular software architecture.
- Object-oriented data modeling.
- CSV ingestion and processing.
- Input validation and error handling.
- Automated testing with pytest.
- Reproducible experiment design.
- Performance-oriented data processing.

Cybersecurity & Identity Engineering

- Identity and Access Management (IAM).
- Single Sign-On (SSO).
- User and Entity Behavior Analytics (UEBA).
- Shadow AI risk monitoring.
- Authentication security.
- Identity event analysis.
- Behavioral anomaly detection.
- Application access visibility.

Security Analytics & Research

- Application catalog matching.
- Behavioral pattern classification.
- Explainable risk scoring.
- Severity-based alert generation.
- Large-scale anonymized dataset analysis.
- Synthetic benchmark evaluation.
- Evidence-based security reporting.
- Research methodology and validation discipline.

Data Sources & Experimental Methodology

ShadowSaaS Radar uses two distinct data sources for different evaluation purposes. Their results are intentionally reported separately to avoid confusing synthetic detection performance with real-world behavioral analysis.

1. HENNGE Access Control Adapter

The HENNGE adapter follows publicly available HENNGE Access Control access-log documentation:

https://support.hdeone.com/hc/en-us/articles/11374378879641

The adapter supports documented authentication fields, including:

- "Timestamp"
- "Username"
- "Login successful"
- "SSO Target"

Additional documented fields are preserved as event metadata.

Data validation. The adapter:

- Accepts TRUE and FALSE login-success values case-insensitively.
- Rejects invalid authentication outcome values.
- Preserves optional documented metadata.
- Accepts empty "SSO Target" values where a login type does not identify a connected service.
- Rejects missing usernames.
- Distinguishes authentication outcomes (success or failure) from application usage, which the logs do not show.

Validation status. The HENNGE adapter was evaluated using reproducible synthetic HENNGE-style authentication records.

No real HENNGE customer access logs were available for this research. Compatibility with actual customer exports has therefore not yet been independently validated.

HENNGE synthetic evaluation. A reproducible dataset was generated to evaluate application matching and behavioral classification.

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

These results apply only to the generated dataset and its predefined scenarios. They demonstrate consistency against the synthetic benchmark, not independently established real-world detection accuracy.

2. Real Anonymized IAM-UEBA Dataset

The project also includes an experimental IAM behavioral analysis pipeline evaluated using a real anonymized IAM dataset published on Zenodo.

- Dataset: IAM-UEBA Dataset
- Authors: Mayor Gallego, Vicente Jesús; Estepa Alonso, Rafael María; Estepa Alonso, Antonio José; Diaz-Verdejo, Jesús E.
- Source: Zenodo
- DOI: "10.5281/zenodo.22871318"
- License: Creative Commons Attribution 4.0 International (CC BY 4.0)
- Link: "Access the original dataset on Zenodo" (https://zenodo.org/records/22871318)

The dataset contains 2,184,272 real anonymized IAM events collected from a cloud identity and access management environment. It includes authentication, provisioning, administrative, service, and system events. It is not redistributed with this repository.

Experimental results

Metric| Result
Total dataset events| 2,184,272
Target behavioral events| 18,542
Users analyzed| 8,890
Total alerts| 48
HIGH severity alerts| 8
MEDIUM severity alerts| 40
Reported processing time| 5.85 seconds (varies by environment)

The experiment analyzes "exceed_failed_password_limit" events using a 15-minute behavioral window.

The optimized CSV processing pipeline produced the same 48 alerts as the original implementation.

Interpretation and limitations

- The dataset contains real anonymized IAM telemetry.
- The dataset is not an AI application usage dataset.
- Anonymized application identifiers cannot reliably be mapped to ChatGPT, Claude, Gemini, or other specific AI services.
- "exceed_failed_password_limit" represents a failed-password threshold event, not an individual failed password attempt.
- The dataset does not provide ground-truth labels for calculating detection precision or recall.
- Generated alerts indicate behavior requiring security review; they do not prove an attack or compromised account.

This experiment demonstrates ingestion, IAM behavioral analysis, and processing performance on real public telemetry. It does not validate Shadow AI detection accuracy.

Authentication Patterns

The Shadow AI detection engine classifies authentication behavior into three patterns:

Pattern| Definition
"one_off"| One authentication event
"repeated"| Multiple events on fewer than 3 distinct days
"habitual"| Events across 3 or more distinct days

The detection engine analyzes successful authentication events per user and application according to its implemented event-selection logic.

These patterns represent authentication behavior, not confirmed application usage.

Risk Model

The current risk model uses initial engineering weights. These are configurable design assumptions, not a validated security standard.

Factor| Rule
Active days| +10 per day, up to 5 days
Authentication events| +2 per event, up to 10 events
Free account, when available| +20
Approved application, account not marked free| Score capped at 25
Single authentication event| Score capped at 15
Maximum score| 100

Severity classification

- LOW: 0–29
- MEDIUM: 30–59
- HIGH: 60–100

Risk interpretation. The score is a prioritization aid, not a probability of compromise or proof of a policy violation.

The model follows several important principles:

1. Approved applications are not automatically risk-free.
2. Enterprise accounts are not automatically approved.
3. Free accounts are not evidence of compromise.
4. Unknown account types are not automatically classified as free.
5. A single authentication event should not be interpreted as confirmed misuse.

Risk weights and thresholds require further calibration using independently labeled data.

Input Formats

HENNGE Access Control CSV

Required columns:

Timestamp
Username
Login successful
SSO Target

Additional documented fields are preserved as metadata.

The HENNGE format does not provide account-type information. Free-account status cannot be inferred from these logs.

Generic Authentication CSV

Required columns:

timestamp,user,app_domain,account_type

Expected timestamp format:

%Y-%m-%d %H:%M:%S

The generic ingestion pipeline converts supported CSV records into the common event model.

Reproducibility

Clone the repository

git clone https://github.com/alishoaip111am-arch/ShadowSaaS-Radar.git
cd ShadowSaaS-Radar

Install dependencies

python -m pip install -r requirements.txt

Generate synthetic HENNGE-style logs

python scripts/generate_hennge_logs.py \
  --employees 200 \
  --days 90 \
  --failure-rate 0.05 \
  --seed 42

Run HENNGE analysis

python main.py data/hennge_synthetic.csv --source hennge

Run automated tests

python -m pytest -q

Run IAM behavioral analysis

The IAM-UEBA dataset is not included in this repository. Download it from Zenodo and place the extracted "events.csv" file at:

data/real/events.csv

This path is excluded from version control through ".gitignore". Then run:

python iam_main.py data/real/events.csv

Engineering Principles

1. Explainability: Every finding should have an understandable reason.
2. Evidence over assumptions: Authentication evidence must not be confused with application activity.
3. Responsible risk scoring: A risk score is a prioritization aid, not proof of compromise.
4. Data integrity: Synthetic and real datasets must remain clearly distinguished.
5. Reproducibility: Experiments and tests should be repeatable.
6. Privacy awareness: Anonymized identity data must not be re-identified.
7. Modularity: Ingestion, detection, analysis, and reporting should remain independently maintainable.

Limitations

- Authentication logs do not prove actual application usage.
- They cannot confirm file uploads, sharing, or data transfers.
- Services accessed outside organizational SSO may not appear.
- HENNGE "SSO Target" values are organization-configured service names, not necessarily application domains.
- Generic service names must not be automatically mapped to AI applications.
- HENNGE logs do not provide free-versus-enterprise account information.
- Unknown account type is not treated as free.
- The application catalog covers a limited set of services.
- Risk weights and thresholds require independent validation.
- The HENNGE adapter has not been validated against real customer exports.
- The IAM-UEBA dataset does not identify specific generative AI applications.
- Real-world Shadow AI detection accuracy has not yet been established.

Future Research

- Evaluation using independently labeled enterprise authentication datasets.
- Broader application catalog coverage.
- Improved application and SSO service mapping.
- Configurable account-type information.
- Additional identity, proxy, DNS, OAuth, and DLP integrations.
- Privacy-preserving identity analysis.
- Further large-scale processing optimization.
- Independent validation of risk weights and detection thresholds.

Contributing

To add an application, edit "shadowsaas/catalog/app_catalog.json" (name, domains, category, and optional "sso_names"), add or update a test, and run:

python -m pytest -q

For larger changes, open an issue first.

Project Independence

ShadowSaaS Radar is an independent educational and cybersecurity research project.

The HENNGE adapter is based on publicly available documentation. This project is not affiliated with, sponsored by, or endorsed by HENNGE.

License

This project is distributed under the MIT License, provided that the repository's "LICENSE" file contains the corresponding MIT license text.

The IAM-UEBA dataset is separately distributed under CC BY 4.0. Refer to the original Zenodo record for its attribution and licensing terms.

Disclaimer

ShadowSaaS Radar is a research prototype intended to support security analysis and investigation.

Its findings must not be treated as proof of malicious activity, data leakage, account compromise, or policy violations.

The system identifies potential authentication patterns and behavioral indicators that may warrant further investigation. Final security decisions require additional evidence and human review.

---

ShadowSaaS Radar: Turning Identity Telemetry into Explainable Security Intelligence.
