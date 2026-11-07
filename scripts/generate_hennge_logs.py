import argparse
import csv
import json
import random
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path


HEADER = [
    "Timestamp",
    "Username",
    "Login successful",
    "IP address",
    "Device Type",
    "Detail",
    "Reason",
    "Entrance Pass ID",
    "Certificate ID",
    "Login Type",
    "SSO Target",
]

AI_APPS = [
    "ChatGPT",
    "Claude",
    "Gemini",
    "Perplexity",
    "DeepSeek",
    "Microsoft Copilot",
]

NORMAL_APPS = [
    "Office 365",
    "Gmail",
    "Slack",
    "Zoom",
    "Salesforce",
    "Dropbox",
]

UNKNOWN_APPS = [
    "Unknown AI Assistant",
    "New Productivity Assistant",
    "Unlisted AI Service",
]

DEVICES = [
    "PC browser",
    "mobile browser",
    "HENNGE Secure Browser",
]

PROFILES = [
    "habitual",
    "repeated",
    "one_off",
    "none",
]

PROFILE_WEIGHTS = [10, 15, 20, 55]

START = datetime(2026, 1, 1, 8, 0, 0)


def make_row(rng, user, target, device, when, success):
    return [
        when.strftime("%Y-%m-%d %H:%M:%S"),
        user,
        "TRUE" if success else "FALSE",
        f"10.0.{rng.randint(0, 255)}.{rng.randint(1, 254)}",
        device,
        "",
        "" if success else "invalid-password",
        "",
        "",
        "saml",
        target,
    ]


def generate(employees, days, failure_rate, seed):
    rng = random.Random(seed)

    rows = []
    expected = []
    profile_counts = Counter()

    def event_time(day):
        return START + timedelta(
            days=day,
            hours=rng.randint(0, 9),
            minutes=rng.randint(0, 59),
        )

    for number in range(1, employees + 1):
        user = f"employee_{number:04d}"
        device = rng.choice(DEVICES)

        profile = rng.choices(
            PROFILES,
            weights=PROFILE_WEIGHTS,
            k=1,
        )[0]

        profile_counts[profile] += 1

        # Keep account type consistent for this employee.
        account_type = rng.choice([
            "free",
            "enterprise",
            "unknown",
        ])

        # Guarantee at least one successful ordinary event.
        rows.append(
            make_row(
                rng,
                user,
                rng.choice(NORMAL_APPS),
                device,
                event_time(rng.randrange(days)),
                True,
            )
        )

        # Additional ordinary application activity.
        for _ in range(rng.randint(2, 8)):
            success = rng.random() >= failure_rate

            rows.append(
                make_row(
                    rng,
                    user,
                    rng.choice(NORMAL_APPS),
                    device,
                    event_time(rng.randrange(days)),
                    success,
                )
            )

        # HENNGE web login with an empty SSO Target.
        rows.append([
            event_time(rng.randrange(days)).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            user,
            "TRUE",
            f"10.0.{rng.randint(0, 255)}.{rng.randint(1, 254)}",
            device,
            "",
            "",
            "",
            "",
            "web",
            "",
        ])

        # Each employee is assigned one AI application.
        app = rng.choice(AI_APPS)

        if profile == "habitual":
            active_days = rng.randint(3, min(8, days))
            used_days = sorted(
                rng.sample(range(days), active_days)
            )

        elif profile == "repeated":
            first_day = rng.randrange(days - 1)
            used_days = [first_day, first_day]

            if rng.random() < 0.5:
                used_days.append(first_day + 1)

        elif profile == "one_off":
            used_days = [rng.randrange(days)]

        else:
            used_days = []

        # Successful AI events.
        for day in used_days:
            rows.append(
                make_row(
                    rng,
                    user,
                    app,
                    device,
                    event_time(day),
                    True,
                )
            )

        # Independent ground-truth labels.
        if used_days:
            expected.append({
                "user": user,
                "app": app,
                "events": len(used_days),
                "days_active": len(set(used_days)),
                "pattern": profile,
                "account_type": account_type,
            })

        # Failed AI authentication attempts.
        if rng.random() < failure_rate:
            for _ in range(rng.randint(1, 2)):
                failed_app = rng.choice(AI_APPS)

                rows.append(
                    make_row(
                        rng,
                        user,
                        failed_app,
                        device,
                        event_time(rng.randrange(days)),
                        False,
                    )
                )

        # Unknown applications are separate from AI ground truth.
        if rng.random() < 0.15:
            rows.append(
                make_row(
                    rng,
                    user,
                    rng.choice(UNKNOWN_APPS),
                    device,
                    event_time(rng.randrange(days)),
                    True,
                )
            )

    rows.sort(key=lambda row: row[0])

    return rows, expected, profile_counts


def write_outputs(rows, expected, output):
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as file:
        writer = csv.writer(file)
        writer.writerow(HEADER)
        writer.writerows(rows)

    labels_path = path.with_suffix(".expected.json")

    labels_path.write_text(
        json.dumps(expected, indent=2),
        encoding="utf-8",
    )

    return path, labels_path


def main():
    parser = argparse.ArgumentParser(
        description="Generate synthetic HENNGE-style SSO logs"
    )

    parser.add_argument(
        "--employees",
        type=int,
        default=200,
    )

    parser.add_argument(
        "--days",
        type=int,
        default=90,
    )

    parser.add_argument(
        "--failure-rate",
        type=float,
        default=0.05,
    )

    parser.add_argument(
        "--output",
        default="data/hennge_synthetic.csv",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
    )

    args = parser.parse_args()

    if args.employees < 1:
        parser.error("--employees must be at least 1")

    if args.days < 8:
        parser.error("--days must be at least 8")

    if not 0 <= args.failure_rate <= 1:
        parser.error(
            "--failure-rate must be between 0 and 1"
        )

    rows, expected, profile_counts = generate(
        args.employees,
        args.days,
        args.failure_rate,
        args.seed,
    )

    csv_path, labels_path = write_outputs(
        rows,
        expected,
        args.output,
    )

    print("\nDataset generated successfully")
    print("-------------------------------")
    print(f"Employees: {args.employees}")
    print(f"Total events: {len(rows)}")
    print(f"Expected AI usage pairs: {len(expected)}")
    print(f"CSV file: {csv_path}")
    print(f"Ground truth: {labels_path}")

    print("\nEmployee behavior profiles:")
    for profile in PROFILES:
        print(f"{profile}: {profile_counts[profile]}")


if __name__ == "__main__":
    main()