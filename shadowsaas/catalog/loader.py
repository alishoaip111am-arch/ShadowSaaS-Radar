import json
from pathlib import Path

CATALOG_PATH = Path(__file__).parent / "app_catalog.json"


def load_catalog(path=CATALOG_PATH):
    with open(path, encoding="utf-8") as file:
        return json.load(file)["apps"]


def match_app(target, apps):
    target = (target or "").strip().casefold()
    if not target:
        return None

    for app in apps:
        names = [app["name"], *app.get("sso_names", [])]
        if any(target == name.strip().casefold() for name in names):
            return app

        for domain in app["domains"]:
            domain = domain.strip().casefold()
            if target == domain or target.endswith("." + domain):
                return app

    return None