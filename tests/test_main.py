
import pytest
import main as app


def prepare_pipeline(monkeypatch):
    monkeypatch.setattr(app, "load_catalog", lambda: [])
    monkeypatch.setattr(app, "find_ai_usage", lambda events, catalog: [])
    monkeypatch.setattr(app, "format_report", lambda results: "TEST REPORT")


def test_hennge_source_uses_hennge_adapter(monkeypatch):
    prepare_pipeline(monkeypatch)

    called = {}

    def fake_hennge_loader(path):
        called["path"] = path
        return [object()]

    monkeypatch.setattr(app, "load_hennge_events", fake_hennge_loader)

    def unexpected_generic_loader(path):
        raise AssertionError("Generic loader should not be called")

    monkeypatch.setattr(app, "load_events", unexpected_generic_loader)

    monkeypatch.setattr(
        app,
        "assess",
        lambda usages, approved: [],
    )

    monkeypatch.setattr(
        "sys.argv",
        ["main.py", "logs.csv", "--source", "hennge"],
    )

    app.main()

    assert called["path"] == "logs.csv"


def test_generic_source_is_default(monkeypatch):
    prepare_pipeline(monkeypatch)

    called = {}

    def fake_generic_loader(path):
        called["path"] = path
        return [object()]

    monkeypatch.setattr(app, "load_events", fake_generic_loader)

    def unexpected_hennge_loader(path):
        raise AssertionError("HENNGE loader should not be called")

    monkeypatch.setattr(
        app,
        "load_hennge_events",
        unexpected_hennge_loader,
    )

    monkeypatch.setattr(
        app,
        "assess",
        lambda usages, approved: [],
    )

    monkeypatch.setattr(
        "sys.argv",
        ["main.py", "logs.csv"],
    )

    app.main()

    assert called["path"] == "logs.csv"


def test_approved_apps_are_passed_to_assess(monkeypatch):
    prepare_pipeline(monkeypatch)

    captured = {}

    monkeypatch.setattr(
        app,
        "load_events",
        lambda path: [],
    )

    def fake_assess(usages, approved):
        captured["approved"] = approved
        return []

    monkeypatch.setattr(app, "assess", fake_assess)

    monkeypatch.setattr(
        "sys.argv",
        [
            "main.py",
            "logs.csv",
            "--approved",
            "ChatGPT,Gemini",
        ],
    )

    app.main()

    assert captured["approved"] == {"ChatGPT", "Gemini"}


def test_invalid_source_is_rejected(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        ["main.py", "logs.csv", "--source", "unknown"],
    )

    with pytest.raises(SystemExit):
        app.parse_args()
