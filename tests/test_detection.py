

from datetime import datetime

from shadowsaas.catalog.loader import load_catalog
from shadowsaas.detection.shadow_ai import find_ai_usage
from shadowsaas.ingestion.event import Event


def event(
    day,
    user="user_01",
    domain="chatgpt.com",
    kind="free",
    source="synthetic_sso_csv",
    outcome="unknown",
):
    return Event(
        timestamp=datetime(2026, 11, day, 9, 0, 0),
        user=user,
        source=source,
        event_type="sso_authentication",
        target=domain,
        outcome=outcome,
        metadata={"account_type": kind},
    )


def usage_for(events):
    return find_ai_usage(events, load_catalog())


def test_single_visit_is_one_off():
    result = usage_for([event(1)])
    assert result[0]["pattern"] == "one_off"


def test_repeated_days_is_habitual():
    result = usage_for([event(d) for d in (1, 2, 3, 4)])
    assert result[0]["pattern"] == "habitual"
    assert result[0]["days_active"] == 4


def test_non_ai_apps_are_ignored():
    events = [
        event(1, domain="dropbox.com"),
        event(2, domain="google.com"),
    ]
    assert usage_for(events) == []


def test_only_last_20_events_are_counted():
    result = usage_for([event(d) for d in range(1, 29)])
    assert result[0]["events"] == 20


def test_enterprise_account_is_not_flagged_free():
    result = usage_for([event(1, kind="enterprise")])
    assert result[0]["free_account"] is False


def test_usage_record_has_expected_types():
    record = usage_for([event(1), event(2)])[0]
    assert isinstance(record["free_account"], bool)
    assert record["events"] == 2
    assert record["days_active"] == 2


def test_account_type_ignores_case_and_spaces():
    record = usage_for([event(1, kind=" Free ")])[0]
    assert record["free_account"] is True


def test_successful_hennge_login_is_counted():
    login = event(
        1,
        domain="ChatGPT",
        source="hennge_access_log",
        outcome="success",
    )

    result = usage_for([login])

    assert len(result) == 1
    assert result[0]["app"] == "ChatGPT"
    assert result[0]["events"] == 1


def test_failed_hennge_login_is_not_counted():
    login = event(
        1,
        domain="ChatGPT",
        source="hennge_access_log",
        outcome="failure",
    )

    assert usage_for([login]) == []


def test_empty_hennge_sso_target_is_ignored():
    login = event(
        1,
        domain="",
        source="hennge_access_log",
        outcome="success",
    )

    assert usage_for([login]) == []


def test_empty_sso_target_does_not_hide_other_ai_events():
    events = [
        event(
            1,
            domain="",
            source="hennge_access_log",
            outcome="success",
        ),
        event(
            2,
            domain="ChatGPT",
            source="hennge_access_log",
            outcome="success",
        ),
    ]

    result = usage_for(events)

    assert len(result) == 1
    assert result[0]["app"] == "ChatGPT"
    assert result[0]["events"] == 1
