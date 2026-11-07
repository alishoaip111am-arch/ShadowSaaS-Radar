import argparse
from collections import Counter

from shadowsaas.detection.iam_streaming import analyze_iam_csv


def main():
    parser = argparse.ArgumentParser(
        description="IAM Behavioral Detection"
    )

    parser.add_argument("csv_path")
    parser.add_argument("--window", type=int, default=15)

    args = parser.parse_args()

    try:
        print("Scanning IAM-UEBA CSV...")

        result = analyze_iam_csv(
            args.csv_path,
            window_minutes=args.window,
        )

        alerts = result["alerts"]
        counts = Counter(
            alert["severity"] for alert in alerts
        )

        print("\nIAM BEHAVIORAL REPORT")
        print("=" * 45)
        print("Relevant events scanned:", result["events_scanned"])
        print("Users analyzed:", result["users_analyzed"])
        print("Total alerts:", len(alerts))
        print("HIGH:", counts["HIGH"])
        print("MEDIUM:", counts["MEDIUM"])
        print("Processing time:", result["elapsed_seconds"], "seconds")

        for alert in alerts[:30]:
            print("\nUser:", alert["user"])
            print("Severity:", alert["severity"])
            print("Events:", alert["event_count"])
            print("Duration:", alert["duration_minutes"], "minutes")
            print("Unique IPs:", alert["unique_ip_count"])
            print("Reason:", alert["reason"])

        print("\nAnalysis completed.")

    except (OSError, ValueError) as error:
        print("Error:", error)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
