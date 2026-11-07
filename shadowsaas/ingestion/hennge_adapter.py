
import csv
from datetime import datetime

from shadowsaas.ingestion.event import Event


SOURCE = "hennge_access_log"
EVENT_TYPE = "sso_authentication"

REQUIRED_COLUMNS = {
    "Timestamp",
    "Username",
    "Login successful",
    "SSO Target",
}


def clean(value):
    return (value or "").strip()


def parse_login_successful(value, line):
    normalized = clean(value).casefold()

    if normalized == "true":
        return "success"

    if normalized == "false":
        return "failure"

    raise ValueError(
        f"Line {line}: invalid Login successful value {value!r}. "
        "Expected TRUE or FALSE."
    )


def parse_timestamp(value, line):
    try:
        return datetime.fromisoformat(clean(value))
    except (ValueError, TypeError):
        raise ValueError(
            f"Line {line}: unrecognized timestamp {value!r}"
        ) from None


def load_hennge_events(csv_path):
    with open(
        csv_path,
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:

        reader = csv.DictReader(file)

        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])

        if missing:
            raise ValueError(
                f"Missing columns: {sorted(missing)}"
            )

        events = []

        for row in reader:
            line = reader.line_num

            username = clean(row.get("Username"))
            target = clean(row.get("SSO Target"))

            if not username:
                raise ValueError(
                    f"Line {line}: Username cannot be empty."
                )

            events.append(
                Event(
                    timestamp=parse_timestamp(
                        row.get("Timestamp"), line
                    ),
                    user=username,
                    source=SOURCE,
                    event_type=EVENT_TYPE,
                    target=target,
                    outcome=parse_login_successful(
                        row.get("Login successful"), line
                    ),
                    ip_address=clean(
                        row.get("IP address")
                    ) or None,
                    metadata={
                        "device_type": clean(
                            row.get("Device Type")
                        ),
                        "login_type": clean(
                            row.get("Login Type")
                        ),
                        "reason": clean(
                            row.get("Reason")
                        ),
                        "detail": clean(
                            row.get("Detail")
                        ),
                        "entrance_pass_id": clean(
                            row.get("Entrance Pass ID")
                        ),
                        "certificate_id": clean(
                            row.get("Certificate ID")
                        ),
                    },
                )
            )

    return events
