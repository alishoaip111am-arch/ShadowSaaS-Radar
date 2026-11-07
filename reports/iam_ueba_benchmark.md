# IAM-UEBA Real-World Benchmark

## Dataset
- Dataset: IAM-UEBA
- Source: Zenodo
- Records: 2,184,272
- Data type: Real anonymized IAM events
- License: CC BY 4.0

## Detection Experiment
- Target event: exceed_failed_password_limit
- Detection window: 15 minutes
- MEDIUM threshold: 5 events
- HIGH threshold: 8 events

## Results
- Relevant events scanned: 18,542
- Users analyzed: 8,890
- Total alerts: 48
- HIGH alerts: 8
- MEDIUM alerts: 40
- Processing time: 5.85 seconds

## Interpretation
The detector processed the IAM-UEBA CSV and identified
concentrated password-limit-exceeded events using a
sliding-window approach.

The results demonstrate execution and behavioral detection
on real anonymized IAM data.

The alerts do not independently prove brute-force attacks,
account compromise, or malicious activity.

The dataset does not establish AI application usage.
No precision, recall, or F1 score is claimed because
independent ground-truth labels are unavailable.

## Reproducibility
Command:
python iam_main.py data/real/events.csv

Thresholds:
15-minute window, 5-event MEDIUM threshold,
8-event HIGH threshold.
