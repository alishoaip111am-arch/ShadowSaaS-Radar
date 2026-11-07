from datetime import datetime, timedelta

from shadowsaas.ingestion.event import Event
from shadowsaas.detection.iam_behavior import (
    detect_password_limit_events,
)


def make_event(user, timestamp, ip="<ip:1>"):
    return Event(
        timestamp=timestamp,
        user=user,
        source="login_portal",
        event_type="exceed_failed_password_limit",
        target="",
        outcome="unknown",
        ip_address=ip,
        metadata={"geo_ip": ip},
    )


def test_detects_medium_alert():
    start = datetime(2024, 1, 1, 10, 0)

    events = [
        make_event(
            "user1",
            start + timedelta(minutes=i),
        )
        for i in range(5)
    ]

    alerts = detect_password_limit_events(events)

    assert len(alerts) == 1
    assert alerts[0]["severity"] == "MEDIUM"
    assert alerts[0]["event_count"] == 5


def test_detects_high_alert():
    start = datetime(2024, 1, 1, 10, 0)

    events = [
        make_event(
            "user1",
            start + timedelta(minutes=i),
        )
        for i in range(8)
    ]

    alerts = detect_password_limit_events(events)

    assert len(alerts) == 1
    assert alerts[0]["severity"] == "HIGH"
    assert alerts[0]["event_count"] == 8


def test_ignores_events_below_threshold():
    start = datetime(2024, 1, 1, 10, 0)

    events = [
        make_event(
            "user1",
            start + timedelta(minutes=i),
        )
        for i in range(4)
    ]

    alerts = detect_password_limit_events(events)

    assert alerts == []


def test_ignores_events_outside_window():
    start = datetime(2024, 1, 1, 10, 0)

    events = [
        make_event("user1", start),
        make_event("user1", start + timedelta(minutes=20)),
        make_event("user1", start + timedelta(minutes=40)),
        make_event("user1", start + timedelta(minutes=60)),
        make_event("user1", start + timedelta(minutes=80)),
    ]

    alerts = detect_password_limit_events(events)

    assert alerts == []


def test_counts_unique_ips():
    start = datetime(2024, 1, 1, 10, 0)

    events = [
        make_event(
            "user1",
            start + timedelta(minutes=i),
            ip="<ip:1>" if i < 4 else "<ip:2>",
        )
        for i in range(5)
    ]

    alerts = detect_password_limit_events(events)

    assert alerts[0]["unique_ip_count"] == 2


def test_separates_users():
    start = datetime(2024, 1, 1, 10, 0)

    events = []

    for user in ("user1", "user2"):
        for i in range(5):
            events.append(
                make_event(
                    user,
                    start + timedelta(minutes=i),
                )
            )

    alerts = detect_password_limit_events(events)

    assert len(alerts) == 2
    assert {alert["user"] for alert in alerts} == {
        "user1",
        "user2",
    }


def test_ignores_other_event_types():
    start = datetime(2024, 1, 1, 10, 0)

    events = [
        Event(
            timestamp=start + timedelta(minutes=i),
            user="user1",
            source="login_portal",
            event_type="log_in",
            target="",
            outcome="unknown",
        )
        for i in range(10)
    ]

    alerts = detect_password_limit_events(events)

    assert alerts == []


def test_rejects_invalid_window():
    try:
        detect_password_limit_events([], window_minutes=0)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError")


def test_rejects_invalid_thresholds():
    try:
        detect_password_limit_events(
            [],
            warning_threshold=8,
            high_threshold=5,
        )
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError")
