ShadowSaaS Radar

Explainable Shadow AI Detection and IAM Behavioral Analysis from Authentication Logs

ShadowSaaS Radar is an independent Python security research prototype designed to identify potential access to known generative AI applications through identity and authentication logs.

The system maps authentication events against an application catalog, analyzes user access patterns, and generates explainable risk scores with supporting evidence.

It also includes an experimental IAM behavioral analysis pipeline evaluated using a real, publicly available anonymized IAM dataset.

Important: Authentication events alone do not prove actual application usage, file uploads, data transfers, or data leakage.

«Independent educational and research project. Not affiliated with, sponsored by, or endorsed by HENNGE.»

---

Key Features

- HENNGE Access Control CSV integration.
- Generic authentication CSV ingestion.
- Application catalog covering known generative AI services.
- Explainable Shadow AI risk scoring.
- Detection of one-off, repeated, and habitual authentication patterns.
- Experimental IAM behavioral analysis.
- Synthetic HENNGE-style log generation.
- Evaluation using a real anonymized IAM dataset.
- Reproducible tests and performance experiments.

Quick Start

git clone https://github.com/alishoaip111am-arch/ShadowSaaS-Radar.git

cd ShadowSaaS-Radar

python -m pip install -r requirements.txt

python main.py data/hennge_sample.csv --source hennge

python main.py data/sample_logs.csv --source generic

python -m pytest -q

The application has no external runtime dependencies. Development dependencies, including pytest, are used for testing.

Example Output

Example from the synthetic HENNGE sample:

Loaded 7 events, found 1 AI usage record(s)

[MEDIUM] user_01 -> ChatGPT (score 48/100)

Evidence:
- 4 authentication event(s) across 4 active day(s)

Based on authentication events only;
does not confirm file uploads or data transfers.

The example uses synthetic data and does not represent a real organization.

---

Data Sources and Evidence

ShadowSaaS Radar has been developed and evaluated using two distinct data sources.

1. HENNGE Access Control Integration

The HENNGE adapter follows the publicly documented HENNGE Access Control access-log format.

Documentation:

"HENNGE Access Control – Access Logs" (https://support.hdeone.com/hc/en-us/articles/11374378879641)

The integration supports:

- Timestamp
- Username
- Login successful
- SSO Target
- Additional documented fields preserved as event metadata

The adapter accepts TRUE and FALSE values case-insensitively, rejects invalid login-success values, and excludes failed sign-ins from successful application access detection.

Empty SSO Target values are accepted where a login type does not identify a connected service.

Validation status:

The HENNGE integration was tested using reproducible synthetic HENNGE-style authentication records.

No real HENNGE customer access logs were available for this research. Compatibility with actual customer exports has therefore not yet been independently validated.

HENNGE Synthetic Evaluation

A reproducible dataset was generated to evaluate application matching and behavioral classification.

Metric| Result
Employees| 200
Authentication events| 1,688
Expected AI usage pairs| 90
Detected pairs| 90
True positives| 90
False positives| 0
False negatives| 0
Precision| 100%
Recall| 100%
F1-score| 100%

These results apply only to the generated dataset and its predefined scenarios. They do not establish real-world detection accuracy.

---

2. Real Anonymized IAM-UEBA Dataset

The project was also evaluated using a real anonymized IAM dataset published on Zenodo.

Dataset: IAM-UEBA Dataset

Source: Zenodo

DOI: "10.5281/zenodo.22871318"

License: Creative Commons Attribution 4.0 International (CC BY 4.0).

"Access the original dataset on Zenodo" (https://zenodo.org/records/22871318)

The dataset contains 2,184,272 real anonymized IAM events collected from a cloud identity and access management environment.

It includes authentication, provisioning, administrative, service, and system events.

Experimental Results

Metric| Result
Total dataset events| 2,184,272
Target behavioral events| 18,542
Users analyzed| 8,890
Total alerts| 48
HIGH alerts| 8
MEDIUM alerts| 40
Processing time| 5.85 seconds

The experiment analyzes "exceed_failed_password_limit" events using a 15-minute behavioral window.

The optimized CSV processing pipeline produced the same 48 alerts as the original implementation.

Interpretation and Limitations

- The dataset contains real anonymized IAM telemetry.
- The dataset is not an AI application usage dataset.
- Anonymized application identifiers cannot reliably be mapped to ChatGPT, Claude, Gemini, or other specific AI services.
- "exceed_failed_password_limit" represents a failed-password threshold event, not an individual failed password attempt.
- The dataset does not provide ground-truth labels for calculating detection precision or recall.
- Generated alerts indicate behavior requiring security review; they do not prove an attack or compromised account.

This experiment demonstrates ingestion, IAM behavioral analysis, and processing performance on real public telemetry. It does not validate Shadow AI detection accuracy.

---

Design Principles

1. Approved does not mean safe. Approved applications can still exhibit activity worth reviewing.
2. Enterprise does not mean approved. An enterprise account is not automatically authorized.
3. Free does not mean compromised. A free account alone is not evidence of data leakage.
4. Authentication does not prove usage. Sign-in events do not reveal what happened inside an application.
5. Every score needs an explanation. Findings include evidence and assumptions separately.

Architecture

1. Ingestion: Converts source logs into a common "Event" model.
2. Application Catalog: Matches event targets against application names, domains, and optional SSO service names.
3. Detection: Analyzes successful authentication frequency and user activity patterns.
4. Risk Engine: Calculates a risk score and severity level.
5. Reporting: Produces findings with supporting evidence and assumptions.
6. IAM Behavioral Analysis: Provides a separate experimental pipeline for analyzing IAM events.

Authentication Patterns

Pattern| Definition
one_off| One authentication event
repeated| Multiple events on fewer than 3 distinct days
habitual| Events across 3 or more distinct days

The detection engine analyzes a limited number of recent successful authentication events per user and application.

Risk Model

The current risk model uses initial engineering weights. These are not a validated security standard.

Factor| Rule
Active days| +10 per day, up to 5 days
Authentication events| +2 per event, up to 10 events
Free account, when available| +20
Approved application, account not marked free| Score capped at 25
Single authentication event| Score capped at 15
Maximum score| 100

Severity levels:

- LOW: 0–29
- MEDIUM: 30–59
- HIGH: 60–100

The score is a prioritization aid, not a probability of compromise or proof of a policy violation.

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

Generic CSV

Required columns:

timestamp,user,app_domain,account_type

Expected timestamp format:

%Y-%m-%d %H:%M:%S

Reproducibility

Generate Synthetic HENNGE-Style Logs

python scripts/generate_hennge_logs.py \
  --employees 200 \
  --days 90 \
  --failure-rate 0.05 \
  --seed 42

Run HENNGE Analysis

python main.py data/hennge_synthetic.csv --source hennge

Run IAM Behavioral Analysis

The IAM-UEBA dataset is not included in this repository. Download the dataset from Zenodo and place the extracted "events.csv" file at:

data/real/events.csv

Then run:

python iam_main.py data/real/events.csv

Limitations

- Authentication logs do not establish actual application usage.
- They do not confirm uploads, sharing, or data transfers.
- Services accessed outside the organization's SSO may not appear.
- HENNGE SSO Target values are organization-configured service names, not necessarily application domains.
- Generic service names must not be automatically mapped to AI applications.
- HENNGE access logs do not provide account-type information.
- Unknown account type is not treated as free.
- The application catalog covers a limited set of services.
- Risk weights and thresholds require independent validation.
- The HENNGE adapter has not been validated against real customer exports.
- The IAM-UEBA dataset does not identify specific generative AI application usage.

Roadmap

- Evaluation using independently labeled datasets.
- Improved application catalog and SSO service mapping.
- Configurable account-type information.
- Privacy-preserving user identifiers in reports.
- Additional identity, proxy, DNS, OAuth, and DLP adapters.
- Further optimization for large-scale log processing.
- Independent validation of risk scores and detection thresholds.

Contributing

Contributions are welcome.

To add an application:

1. Update "shadowsaas/catalog/app_catalog.json".
2. Add its name, domains, category, and optional SSO service names.
3. Add or update relevant tests.
4. Run:

python -m pytest -q

For larger changes, open an issue first.

License

See the "LICENSE" file in the repository for licensing terms.

Disclaimer

ShadowSaaS Radar is an educational and research prototype. Its findings are intended to support security review and must not be treated as proof of malicious activity, data leakage, account compromise, or policy violations.

This project is independent and is not affiliated with, sponsored by, or endorsed by HENNGE.
EOF