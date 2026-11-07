import csv
from datetime import datetime
from pathlib import Path

from shadowsaas.ingestion.event import Event


TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"

REQUIRED_COLUMNS = {
    "timestamp",
    "event_source",
    "actor",
    "action",
    "action_target",
    "action_data",
}


def load_iam_ueba_events(csv_path):
    """
    Load IAM-UEBA authentication and authorization events.

    Original dataset fields are preserved in Event.metadata.
    Anonymous application tokens are never interpreted as real app names.
    """

    events = []

    with open(csv_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file, skipinitialspace=True)

        if not reader.fieldnames:
            raise ValueError("CSV file has no header")

        reader.fieldnames = [
            name.strip() for name in reader.fieldnames
        ]

        missing = REQUIRED_COLUMNS - set(reader.fieldnames)

        if missing:
            raise ValueError(
                f"Missing required columns: {sorted(missing)}"
            )

        for line_number, row in enumerate(reader, start=2):
            row = {
                key.strip(): value.strip() if value else ""
                for key, value in row.items()
                if key is not None
            }

            try:
                timestamp = datetime.strptime(
                    row["timestamp"],
                    TIMESTAMP_FORMAT,
                )
            except ValueError as exc:
                raise ValueError(
                    f"Invalid timestamp at line {line_number}: "
                    f"{row.get('timestamp')}"
                ) from exc

            actor = row["actor"]

            if not actor:
                raise ValueError(
                    f"Missing actor at line {line_number}"
                )

            action = row["action"]
            source = row["event_source"]

            metadata = {
                "event_id": row.get("event_id", ""),
                "session": row.get("session", ""),
                "action_target": row.get("action_target", ""),
                "action_data": row.get("action_data", ""),
                "os_family": row.get("os_family", ""),
                "os_variant": row.get("os_variant", ""),
                "os_version": row.get("os_version", ""),
                "browser_family": row.get("browser_family", ""),
                "browser_version": row.get("browser_version", ""),
                "is_mobile": row.get("is_mobile", ""),
                "geo_ip": row.get("geo_ip", ""),
                "geo_country": row.get("geo_country", ""),
                "geo_city": row.get("geo_city", ""),
            }

            target = row.get("action_target", "")

            events.append(
                Event(
                    timestamp=timestamp,
                    user=actor,
                    source=source,
                    event_type=action,
                    target=target,
                    outcome="unknown",
                    device_id="",
                    ip_address=row.get("geo_ip", ""),
                    metadata=metadata,
                )
            )

    return events
