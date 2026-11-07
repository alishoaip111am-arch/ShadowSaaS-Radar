import csv
from collections import defaultdict
from datetime import datetime, timedelta
from time import perf_counter


ACTION = "exceed_failed_password_limit"
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"


def analyze_iam_csv(
    csv_path,
    window_minutes=15,
    warning_threshold=5,
    high_threshold=8,
):
    if window_minutes <= 0:
        raise ValueError("window_minutes must be positive")

    if warning_threshold <= 0:
        raise ValueError("warning_threshold must be positive")

    if high_threshold < warning_threshold:
        raise ValueError("high_threshold must be >= warning_threshold")

    started = perf_counter()
    user_events = defaultdict(list)
    events_scanned = 0

    with open(csv_path, encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file, skipinitialspace=True)

        if not reader.fieldnames:
            raise ValueError("CSV file has no header")

        reader.fieldnames = [
            name.strip() for name in reader.fieldnames
        ]

        required = {"timestamp", "actor", "action", "geo_ip"}
        missing = required - set(reader.fieldnames)

        if missing:
            raise ValueError(
                f"Missing required columns: {sorted(missing)}"
            )

        for line_number, row in enumerate(reader, start=2):
            action = (row.get("action") or "").strip()

            if action != ACTION:
                continue

            user = (row.get("actor") or "").strip()

            if not user:
                raise ValueError(
                    f"Missing actor at line {line_number}"
                )

            try:
                timestamp = datetime.strptime(
                    (row.get("timestamp") or "").strip(),
                    TIMESTAMP_FORMAT,
                )
            except ValueError as exc:
                raise ValueError(
                    f"Invalid timestamp at line {line_number}"
                ) from exc

            ip = (row.get("geo_ip") or "").strip()

            user_events[user].append((timestamp, ip))
            events_scanned += 1

    alerts = []
    window = timedelta(minutes=window_minutes)

    for user, records in user_events.items():
        records.sort(key=lambda item: item[0])

        left = 0
        best_count = 0
        best_start = None
        best_end = None
        best_ips = set()

        for right in range(len(records)):
            while (
                records[right][0] - records[left][0] > window
            ):
                left += 1

            count = right - left + 1

            if count > best_count:
                best_count = count
                best_start = records[left][0]
                best_end = records[right][0]
                best_ips = {
                    ip
                    for _, ip in records[left:right + 1]
                    if ip
                }

        if best_count < warning_threshold:
            continue

        severity = (
            "HIGH"
            if best_count >= high_threshold
            else "MEDIUM"
        )

        duration = (
            best_end - best_start
        ).total_seconds() / 60

        alerts.append({
            "user": user,
            "event_type": ACTION,
            "event_count": best_count,
            "window_minutes": window_minutes,
            "start_time": best_start.isoformat(),
            "end_time": best_end.isoformat(),
            "duration_minutes": round(duration, 2),
            "unique_ip_count": len(best_ips),
            "severity": severity,
            "reason": (
                f"{best_count} password-limit-exceeded events "
                f"within {window_minutes} minutes"
            ),
        })

    alerts.sort(
        key=lambda alert: (
            alert["severity"] == "HIGH",
            alert["event_count"],
        ),
        reverse=True,
    )

    return {
        "alerts": alerts,
        "events_scanned": events_scanned,
        "users_analyzed": len(user_events),
        "elapsed_seconds": round(perf_counter() - started, 2),
    }
