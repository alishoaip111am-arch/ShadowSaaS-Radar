
import pytest

from shadowsaas.engine.risk_engine import (
    assess,
    score_usage,
    risk_level,
)


def usage(**overrides):
    base = {
        "user": "user_01",
        "app": "ChatGPT",
        "events": 4,
        "days_active": 4,
        "last_seen": None,
        "free_account": True,
        "pattern": "habitual",
    }
    return {**base, **overrides}


def test_habitual_free_account_is_high():
    assert score_usage(usage())["level"] == "high"


def test_single_event_is_low():
    result = score_usage(
        usage(events=1, days_active=1, pattern="one_off")
    )
    assert result["level"] == "low"


def test_unapproved_enterprise_app_is_not_automatically_low():
    assert score_usage(
        usage(free_account=False)
    )["level"] == "medium"


def test_approved_enterprise_app_is_low():
    result = score_usage(
        usage(free_account=False),
        approved_apps={"ChatGPT"},
    )
    assert result["level"] == "low"


def test_approved_app_on_free_account_is_still_high():
    result = score_usage(
        usage(),
        approved_apps={"ChatGPT"},
    )
    assert result["level"] == "high"


def test_missing_field_raises():
    broken = usage()
    del broken["events"]

    with pytest.raises(ValueError, match="events"):
        score_usage(broken)


def test_evidence_explains_the_score():
    result = score_usage(usage())

    assert any(
        "authentication event" in item
        for item in result["evidence"]
    )


def test_free_account_is_recorded_as_assumption():
    result = score_usage(usage())

    assert any(
        "Free-account status" in item
        for item in result["assumptions"]
    )


def test_assess_sorts_highest_risk_first():
    results = assess([
        usage(
            user="user_02",
            events=1,
            days_active=1,
            pattern="one_off",
        ),
        usage(user="user_01"),
    ])

    assert results[0]["user"] == "user_01"


def test_wrong_one_off_label_does_not_cap_repeated_use():
    result = score_usage(
        usage(events=8, days_active=4, pattern="one_off")
    )

    assert result["score"] > 15


def test_approved_app_matching_ignores_case():
    result = score_usage(
        usage(free_account=False),
        approved_apps={"chatgpt"},
    )

    assert result["level"] == "low"


def test_empty_assessment_returns_empty_list():
    assert assess([]) == []


def test_risk_level_boundaries():
    assert risk_level(29) == "low"
    assert risk_level(30) == "medium"
    assert risk_level(59) == "medium"
    assert risk_level(60) == "high"
    assert risk_level(100) == "high"
