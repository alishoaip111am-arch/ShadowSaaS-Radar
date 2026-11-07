from shadowsaas.catalog.loader import load_catalog, match_app


def test_catalog_loads_apps():
    assert len(load_catalog()) > 0


def test_exact_domain_matches():
    assert match_app("chatgpt.com", load_catalog())["name"] == "ChatGPT"


def test_subdomain_matches():
    assert match_app("chat.openai.com", load_catalog())["name"] == "ChatGPT"


def test_matching_is_case_insensitive():
    assert match_app("Claude.AI", load_catalog())["name"] == "Claude"


def test_lookalike_domain_does_not_match():
    assert match_app("notchatgpt.com", load_catalog()) is None


def test_unknown_domain_returns_none():
    assert match_app("google.com", load_catalog()) is None


def test_every_catalog_entry_has_required_fields():
    for app in load_catalog():
        assert app["name"]
        assert app["domains"]
        assert app["category"]


def test_catalog_app_names_are_unique():
    names = [app["name"].casefold() for app in load_catalog()]
    assert len(names) == len(set(names))
