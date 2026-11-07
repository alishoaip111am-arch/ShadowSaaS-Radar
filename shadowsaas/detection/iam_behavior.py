from collections import defaultdict
from datetime import timedelta


ACTION_TO_DETECT = "exceed_failed_password_limit"

DEFAULT_WINDOW_MINUTES = 15
WARNING_THRESHOLD = 5
HIGH_THRESHOLD = 8


def detect_password_limit_events(
    events,
    window_minutes=DEFAULT_WINDOW_MINUTES,
    warning_threshold=WARNING_THRESHOLD,
    high_threshold=HIGH_THRESHOLD,
):
    """
    Detect repeated password-limit-exceeded events.

    This detects concentrated IAM security events.
    It does not prove brute-force attacks or account compromise.
    """

    if window_minutes <= 0:
        raise ValueError("window_minutes must be positive")

    if warning_threshold <= 0:
        raise ValueError("warning_threshold must be positive")

    if high_threshold < warning_threshold:
        raise ValueError(
            "high_threshold must be >= warning_threshold"
        )

    user_events = defaultdict(list)

    # Group relevant events by user.
    for event in events:
        if event.event_type != ACTION_TO_DETECT:
            continue

        user_events[event.user].append(event)

    alerts = []
    window = timedelta(minutes=window_minutes)

    # Analyze each user's events independently.
    for user, user_records in user_events.items():

        user_records.sort(key=lambda event: event.timestamp)

        left = 0
        best_count = 0
        best_start = None
        best_end = None
        best_records = []

        # Sliding-window analysis.
        for right in range(len(user_records)):

            while (
                user_records[right].timestamp
                - user_records[left].timestamp
                > window
            ):
                left += 1

            current_count = right - left + 1

            if current_count > best_count:
                best_count = current_count
                best_start = user_records[left].timestamp
                best_end = user_records[right].timestamp
                best_records = user_records[left:right + 1]

        # Ignore users below the warning threshold.
        if best_count < warning_threshold:
            continue

        # Extract distinct IP tokens.
        unique_ips = set()

        for event in best_records:
            ip = event.ip_address

            if not ip:
                ip = event.metadata.get("geo_ip", "")

            if ip:
                unique_ips.add(ip)

        duration = (
            best_end - best_start
        ).total_seconds() / 60

        if best_count >= high_threshold:
            severity = "HIGH"
        else:
            severity = "MEDIUM"

        alerts.append({
            "user": user,
            "event_type": ACTION_TO_DETECT,
            "event_count": best_count,
            "window_minutes": window_minutes,
            "start_time": best_start.isoformat(),
            "end_time": best_end.isoformat(),
            "duration_minutes": round(duration, 2),
            "unique_ip_count": len(unique_ips),
            "severity": severity,
            "reason": (
                f"{best_count} password-limit-exceeded events "
                f"within {window_minutes} minutes"
            ),
        })

    # Highest priority first.
    alerts.sort(
        key=lambda alert: (
            alert["severity"] == "HIGH",
            alert["event_count"],
        ),
        reverse=True,
    )

    return alerts
