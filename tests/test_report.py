
from shadowsaas.reporting.report_generator import FOOTER, format_report


def result(**overrides):
    base = {
        "user": "user_01",
        "app": "ChatGPT",
        "score": 68,
        "level": "high",
        "evidence": [
            "4 authentication events across 4 active days"
        ],
        "assumptions": [
            "Free-account status comes from metadata, not HENNGE Access Logs."
        ],
    }
    return {**base, **overrides}


def test_report_shows_user_level_and_evidence():
    report = format_report([result()])

    assert "[HIGH] user_01 -> ChatGPT" in report
    assert "4 authentication events" in report


def test_report_shows_assumptions():
    report = format_report([result()])

    assert "Assumptions:" in report
    assert "Free-account status" in report


def test_report_always_ends_with_disclaimer():
    assert format_report([result()]).endswith(FOOTER)
    assert format_report([]).endswith(FOOTER)


def test_empty_results_message():
    assert (
        "No generative AI authentication activity detected"
        in format_report([])
    )


def test_report_shows_multiple_results():
    report = format_report([
        result(user="user_01"),
        result(user="user_02", level="low", score=10),
    ])

    assert "user_01" in report
    assert "user_02" in report


def test_report_displays_exact_risk_score():
    report = format_report([result(score=68)])

    assert "(score 68/100)" in report


def test_empty_assumptions_are_not_displayed():
    report = format_report([result(assumptions=[])])

    assert "Assumptions:" not in report
    assert "Evidence:" in report
