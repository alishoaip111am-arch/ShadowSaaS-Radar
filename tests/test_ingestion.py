
import pytest

from shadowsaas.ingestion.csv_loader import load_events


HEADER = "timestamp,user,app_domain,account_type\n"
ROW = "2026-11-01 09:00:00,user_01,chatgpt.com,free\n"


def write_csv(tmp_path, content, encoding="utf-8"):
    path = tmp_path / "logs.csv"
    path.write_text(content, encoding=encoding)
    return path


def test_loads_all_rows(tmp_path):
    path = write_csv(
        tmp_path,
        HEADER + ROW + ROW.replace("user_01", "user_02"),
    )

    events = load_events(path)

    assert len(events) == 2
    assert events[0].user == "user_01"
    assert events[1].user == "user_02"


def test_header_only_returns_empty_list(tmp_path):
    assert load_events(write_csv(tmp_path, HEADER)) == []


def test_utf8_bom_does_not_break_first_column(tmp_path):
    path = write_csv(
        tmp_path,
        HEADER + ROW,
        encoding="utf-8-sig",
    )

    events = load_events(path)

    assert len(events) == 1
    assert events[0].timestamp.year == 2026


def test_extra_columns_are_ignored_safely(tmp_path):
    path = write_csv(
        tmp_path,
        "timestamp,user,app_domain,account_type,ip\n"
        "2026-11-01 09:00:00,user_01,chatgpt.com,free,10.0.0.1\n",
    )

    assert load_events(path)[0].user == "user_01"


@pytest.mark.parametrize(
    "missing",
    ["timestamp", "user", "app_domain", "account_type"],
)
def test_missing_required_column_raises(tmp_path, missing):
    columns = [
        column
        for column in HEADER.strip().split(",")
        if column != missing
    ]

    path = write_csv(
        tmp_path,
        ",".join(columns) + "\n",
    )

    with pytest.raises(ValueError, match=missing):
        load_events(path)


def test_invalid_timestamp_raises(tmp_path):
    row = ROW.replace(
        "2026-11-01 09:00:00",
        "invalid-date",
    )

    with pytest.raises(ValueError):
        load_events(
            write_csv(tmp_path, HEADER + row)
        )


def test_empty_username_is_rejected(tmp_path):
    row = "2026-11-01 09:00:00,,chatgpt.com,free\n"

    events = load_events(
        write_csv(tmp_path, HEADER + row)
    )

    assert len(events) == 1
    assert events[0].user == ""
