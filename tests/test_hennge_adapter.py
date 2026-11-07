
import pytest

from shadowsaas.ingestion.hennge_adapter import load_hennge_events


HEADER = (
    "Timestamp,Username,Login successful,IP address,"
    "Device Type,Detail,Reason,Login Type,SSO Target\n"
)

OK_ROW = (
    "2026-11-01 09:12:00,user_01,TRUE,10.0.0.1,"
    "PC browser,,,saml,ChatGPT\n"
)

FAIL_ROW = (
    "2026-11-01 09:15:00,user_02,FALSE,10.0.0.2,"
    "mobile browser,,invalid-password,saml,ChatGPT\n"
)


def write_csv(tmp_path, content):
    path = tmp_path / "hennge_test.csv"
    path.write_text(content, encoding="utf-8")
    return path


def test_parses_successful_login(tmp_path):
    event = load_hennge_events(
        write_csv(tmp_path, HEADER + OK_ROW)
    )[0]

    assert event.user == "user_01"
    assert event.target == "ChatGPT"
    assert event.outcome == "success"
    assert event.source == "hennge_access_log"


def test_parses_failed_login(tmp_path):
    event = load_hennge_events(
        write_csv(tmp_path, HEADER + FAIL_ROW)
    )[0]

    assert event.outcome == "failure"
    assert event.metadata["reason"] == "invalid-password"


def test_login_successful_is_case_insensitive(tmp_path):
    row = OK_ROW.replace("TRUE", "true")

    event = load_hennge_events(
        write_csv(tmp_path, HEADER + row)
    )[0]

    assert event.outcome == "success"


def test_unexpected_login_value_raises_with_line_number(tmp_path):
    row = OK_ROW.replace("TRUE", "maybe")

    with pytest.raises(ValueError, match="Line 2"):
        load_hennge_events(
            write_csv(tmp_path, HEADER + row)
        )


def test_missing_required_column_raises(tmp_path):
    header = HEADER.replace(",SSO Target", "")

    with pytest.raises(ValueError, match="SSO Target"):
        load_hennge_events(
            write_csv(tmp_path, header)
        )


def test_unrecognized_timestamp_raises(tmp_path):
    row = OK_ROW.replace(
        "2026-11-01 09:12:00",
        "01/11/2026 9am"
    )

    with pytest.raises(ValueError, match="timestamp"):
        load_hennge_events(
            write_csv(tmp_path, HEADER + row)
        )


def test_optional_columns_are_stored(tmp_path):
    event = load_hennge_events(
        write_csv(tmp_path, HEADER + OK_ROW)
    )[0]

    assert event.ip_address == "10.0.0.1"
    assert event.metadata["login_type"] == "saml"
    assert event.metadata["device_type"] == "PC browser"


def test_only_required_columns_are_enough(tmp_path):
    content = (
        "Timestamp,Username,Login successful,SSO Target\n"
        "2026-11-01 09:12:00,user_01,TRUE,ChatGPT\n"
    )

    event = load_hennge_events(
        write_csv(tmp_path, content)
    )[0]

    assert event.ip_address is None
    assert event.metadata["login_type"] == ""
    assert event.target == "ChatGPT"


def test_empty_sso_target_is_accepted(tmp_path):
    content = (
        HEADER
        + "2026-11-01 09:12:00,user_01,TRUE,10.0.0.1,"
        "PC browser,,,web,\n"
    )

    events = load_hennge_events(
        write_csv(tmp_path, content)
    )

    assert len(events) == 1
    assert events[0].target == ""
    assert events[0].metadata["login_type"] == "web"


def test_missing_sso_target_column_is_rejected(tmp_path):
    header = "Timestamp,Username,Login successful\n"

    content = (
        header
        + "2026-11-01 09:12:00,user_01,TRUE\n"
    )

    with pytest.raises(ValueError, match="SSO Target"):
        load_hennge_events(
            write_csv(tmp_path, content)
        )
