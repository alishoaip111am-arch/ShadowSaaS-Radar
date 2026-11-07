ShadowSaaS Radar

Explainable Shadow AI Detection from SSO Authentication Logs

ShadowSaaS Radar is an independent cybersecurity tool designed to identify potential Shadow AI access patterns through the analysis of Single Sign-On (SSO) authentication logs.

It processes authentication events, matches application targets against a catalog of known generative AI services, analyzes sign-in frequency, and produces explainable risk assessments to support security investigations.

The goal is to prioritize activity for review — not to claim that an application was used, that data was exposed, or that a security incident occurred.

«An independent educational project. Not affiliated with, sponsored by, or endorsed by HENNGE.»

---

Quick Start

Installation

git clone https://github.com/<your-username>/shadowsaas-radar.git
cd shadowsaas-radar
pip install -r requirements.txt

Replace "<your-username>" with your actual GitHub username before publishing.

The application has no runtime dependencies. "pytest" is used for development and testing.

Run the application

HENNGE Access Control logs:

python main.py data/hennge_sample.csv --source hennge

Generic CSV logs:

python main.py data/sample_logs.csv --source generic

Specify approved applications:

python main.py data/sample_logs.csv --approved "Gemini,Microsoft Copilot"

Run automated tests:

python -m pytest -q

Example Output

The following output was observed when running the implementation against the synthetic HENNGE sample:

Loaded 7 events, found 1 AI usage record(s)

[MEDIUM] user_01 -> ChatGPT (score 48/100)
  Evidence:
    - 4 authentication event(s) across 4 active day(s)

The sample data is synthetic and does not represent activity from a real organization.

---

Design Principles

The detection and risk assessment logic follows five principles:

1. Approved does not mean safe. Approved applications may still exhibit activity worth reviewing.
2. Enterprise does not mean approved. An enterprise subscription does not establish organizational authorization.
3. Free does not mean compromised. A free account alone is not evidence of data leakage.
4. Authentication does not prove usage. Sign-in events do not reveal what happened inside an application.
5. Every score needs an explanation. Observed evidence and assumptions must remain distinguishable.

These principles help prevent incomplete authentication data from becoming unsupported security conclusions.

---

How It Works

The application uses a modular processing pipeline:

1. Ingestion: Converts input records into a common "Event" model. Currently supports generic CSV and HENNGE Access Control logs.
2. Application catalog: Matches event targets against known application names, domains, and optional SSO aliases.
3. Detection: Groups eligible authentication events by user and AI application, then analyzes up to the latest 20 events per group.
4. Risk engine: Calculates a transparent score using activity frequency and available account metadata.
5. Reporting: Produces findings with severity levels, supporting evidence, and relevant assumptions.

Activity Classification

Pattern| Definition
One-off| One authentication event
Repeated| Multiple events across fewer than three distinct days
Habitual| Activity across at least three distinct days

---

Risk Assessment Model

The risk engine uses an explainable weighted scoring model.

The initial weights are engineering choices, not a validated security standard. They should be evaluated and calibrated against labeled data before operational use.

Factor| Scoring rule
Active days| +10 per day, maximum 5 days
Authentication events| +2 per event, maximum 10 events
Free-account metadata| +20 when available
Approved application, account not marked free| Score capped at 25
Single authentication event| Score capped at 15
Maximum score| 100

Severity levels

Score| Severity
0–29| Low
30–59| Medium
60–100| High

The approved-application cap applies when the account is not marked as free, including when account type is unknown. Free-account metadata follows a separate scoring branch.

The score is a prioritization mechanism, not a probability of compromise, a compliance verdict, or proof of a policy violation.

---

Supported Input Formats

HENNGE Access Control CSV

The HENNGE adapter follows the publicly documented Access Control access-log structure.

Documentation: "HENNGE Help Center – Access Control access logs" (https://support.hdeone.com/hc/en-us/articles/11374378879641)

The referenced specification is dated December 2025 and may change.

Required columns:

- "Timestamp"
- "Username"
- "Login successful"
- "SSO Target"

Additional documented fields are preserved as event metadata.

Validation and processing:

- "Login successful" accepts "TRUE" or "FALSE", case-insensitively.
- Invalid values are rejected with their corresponding line number.
- Failed HENNGE authentication events are excluded from AI detection.
- An empty "SSO Target" is accepted because some login types do not identify a connected SSO service.
- "Timestamp" is parsed using Python's "datetime.fromisoformat()".

Generic CSV

Expected columns:

timestamp,user,app_domain,account_type

Timestamps must follow this format:

%Y-%m-%d %H:%M:%S

---

Technical Limitations

Understanding the available telemetry is essential when interpreting findings.

- Authentication visibility: SSO logs show authentication events, not actual application usage, uploads, sharing, or data transfers.
- SSO coverage: Applications accessed outside the configured SSO environment may not appear in the available logs.
- HENNGE validation: The adapter is based on public documentation and has been tested using synthetic records. Compatibility with real customer exports has not yet been validated.
- Service identification: "SSO Target" is a service name configured by each organization's administrator. It is not necessarily a domain name.
- Application matching: Generic names such as Office 365 or Gmail must not automatically be interpreted as AI applications.
- Account metadata: The HENNGE fields currently used do not provide account subscription type. Unknown account type is therefore not treated as free, which may lower the calculated score.
- Timestamp handling: Timestamps are parsed in their supplied format. No timezone normalization or conversion is currently performed.
- Catalog coverage: The application catalog covers a limited set of known services and requires further expansion and validation.

These limitations mean that findings should be treated as investigation signals rather than definitive security conclusions.

---

Project Structure

ShadowSaaS-Radar/
├── main.py
├── README.md
├── requirements.txt
├── LICENSE
├── data/
│   ├── hennge_sample.csv
│   └── sample_logs.csv
├── shadowsaas/
│   ├── __init__.py
│   ├── catalog/
│   │   ├── __init__.py
│   │   ├── app_catalog.json
│   │   └── loader.py
│   ├── detection/
│   │   ├── __init__.py
│   │   └── shadow_ai.py
│   ├── engine/
│   │   ├── __init__.py
│   │   └── risk_engine.py
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── event.py
│   │   ├── csv_loader.py
│   │   └── hennge_adapter.py
│   └── reporting/
│       ├── __init__.py
│       └── report_generator.py
└── tests/
    ├── test_catalog.py
    ├── test_detection.py
    ├── test_hennge_adapter.py
    ├── test_ingestion.py
    ├── test_main.py
    ├── test_report.py
    └── test_risk_engine.py

---

Testing

The automated test suite covers:

- Generic CSV ingestion and validation.
- HENNGE log parsing and field validation.
- Application catalog matching.
- Failed authentication filtering.
- AI activity detection and pattern classification.
- Risk scoring and severity boundaries.
- Report generation.
- Command-line argument handling and source selection.

Run the complete test suite:

python -m pytest -q

---

Roadmap

- Detection evaluation: Build labeled synthetic scenarios and measure Precision, Recall, and F1-score.
- Account context: Add configurable account-type rules for individual services.
- Privacy: Support anonymized user identifiers in reports.
- Catalog expansion: Increase application coverage and validate matching behavior.
- Additional telemetry: Develop separate adapters for Proxy, DNS, OAuth, and DLP sources, each with documented input formats and dedicated tests.

Additional sources will only be considered supported after their ingestion and validation logic has been implemented and tested.

---

Contributing

To add an application:

1. Edit "shadowsaas/catalog/app_catalog.json".
2. Add its canonical name, domains, category, and optional "sso_names".
3. Add or update relevant tests.
4. Run the complete test suite.

For larger changes, open an issue describing the proposed functionality.

License

This project is licensed under the MIT License. See "LICENSE" (LICENSE) for details.