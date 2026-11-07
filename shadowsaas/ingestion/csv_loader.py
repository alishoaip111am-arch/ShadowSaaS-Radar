import csv
from datetime import datetime

from shadowsaas.ingestion.event import Event


REQUIRED_COLUMNS = {
    "timestamp",
    "user",
    "app_domain",
    "account_type",
}

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"


def load_events(csv_path):
    events = []

    with open(csv_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing columns: {sorted(missing)}")

        for row in reader:
            event = Event(
                timestamp=datetime.strptime(
                    row["timestamp"], TIMESTAMP_FORMAT
                ),
                user=row["user"].strip(),
                source="synthetic_sso_csv",
                event_type="sso_authentication",
                target=row["app_domain"].strip(),
                outcome="unknown",
                metadata={
                    "account_type": row["account_type"].strip()
                },
            )

            events.append(event)

    return events