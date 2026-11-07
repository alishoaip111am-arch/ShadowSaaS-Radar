DAY_POINTS = 10
EVENT_POINTS = 2
FREE_ACCOUNT_POINTS = 20
APPROVED_CAP = 25
ONE_OFF_CAP = 15
HIGH = 60
MEDIUM = 30
MAX_SCORE = 100

REQUIRED_FIELDS = {"app", "days_active", "events", "free_account"}


def risk_level(score):
    if score >= HIGH:
        return "high"
    if score >= MEDIUM:
        return "medium"
    return "low"


def score_usage(usage, approved_apps=frozenset()):
    missing = REQUIRED_FIELDS - usage.keys()
    if missing:
        raise ValueError(f"Missing usage fields: {sorted(missing)}")

    approved = {name.strip().casefold() for name in approved_apps}
    app_name = usage["app"].strip().casefold()
    days = usage["days_active"]
    events = usage["events"]

    score = min(days, 5) * DAY_POINTS + min(events, 10) * EVENT_POINTS

    evidence = [
        f"{events} authentication event(s) across {days} active day(s)"
    ]
    assumptions = []

    if usage["free_account"]:
        score += FREE_ACCOUNT_POINTS
        assumptions.append(
            "Free-account status comes from metadata, not HENNGE Access Logs."
        )
    elif app_name in approved:
        score = min(score, APPROVED_CAP)
        assumptions.append(
            "Approved-app status was supplied through local configuration."
        )

    if events == 1:
        score = min(score, ONE_OFF_CAP)
        assumptions.append(
            "A single authentication event may be accidental."
        )

    score = min(score, MAX_SCORE)

    return {
        **usage,
        "score": score,
        "level": risk_level(score),
        "evidence": evidence,
        "assumptions": assumptions,
    }


def assess(usages, approved_apps=frozenset()):
    results = [score_usage(usage, approved_apps) for usage in usages]
    return sorted(results, key=lambda result: result["score"], reverse=True)