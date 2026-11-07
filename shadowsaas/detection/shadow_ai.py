
from collections import defaultdict

from shadowsaas.catalog.loader import match_app


WINDOW = 20
HABITUAL_DAYS = 3


def classify(events, days_active):
    if events == 1:
        return "one_off"

    if days_active >= HABITUAL_DAYS:
        return "habitual"

    return "repeated"


def find_ai_usage(events, apps, window=WINDOW):
    grouped = defaultdict(list)

    for event in events:

        # Ignore failed HENNGE authentication attempts
        if (
            event.source == "hennge_access_log"
            and event.outcome != "success"
        ):
            continue

        app = match_app(event.target, apps)

        if app is None or app["category"] != "generative_ai":
            continue

        grouped[(event.user, app["name"])].append(event)

    usage = []

    for (user, app_name), items in grouped.items():
        items.sort(key=lambda event: event.timestamp)
        recent = items[-window:]

        days_active = len({
            event.timestamp.date()
            for event in recent
        })

        usage.append({
            "user": user,
            "app": app_name,
            "events": len(recent),
            "days_active": days_active,
            "last_seen": recent[-1].timestamp,
            "free_account": any(
                event.metadata.get("account_type", "").strip().lower() == "free"
                for event in recent
            ),
            "pattern": classify(len(recent), days_active),
        })

    return usage
