
import argparse

from shadowsaas.catalog.loader import load_catalog
from shadowsaas.detection.shadow_ai import find_ai_usage
from shadowsaas.engine.risk_engine import assess
from shadowsaas.ingestion.csv_loader import load_events
from shadowsaas.ingestion.hennge_adapter import load_hennge_events
from shadowsaas.reporting.report_generator import format_report


BANNER = """\
================================
       ShadowSaaS Radar
   Shadow AI detection from SSO logs
================================"""


def parse_args():
    parser = argparse.ArgumentParser(
        description="Detect risky Shadow AI usage from SSO log exports."
    )

    parser.add_argument(
        "csv_path",
        help="path to the SSO log CSV file"
    )

    parser.add_argument(
        "--source",
        choices=["generic", "hennge"],
        default="generic",
        help="log source format (default: generic)"
    )

    parser.add_argument(
        "--approved",
        default="",
        help='comma-separated approved apps, e.g. "Microsoft Copilot,Gemini"'
    )

    return parser.parse_args()


def main():
    args = parse_args()

    approved = {
        name.strip()
        for name in args.approved.split(",")
        if name.strip()
    }

    print(BANNER)

    try:
        if args.source == "hennge":
            events = load_hennge_events(args.csv_path)
        else:
            events = load_events(args.csv_path)

        catalog = load_catalog()

        usages = find_ai_usage(events, catalog)
        results = assess(usages, approved)

        print(
            f"Loaded {len(events)} events, "
            f"found {len(results)} AI usage record(s)\n"
        )

        print(format_report(results))

    except (OSError, ValueError) as error:
        print(f"Error: {error}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
