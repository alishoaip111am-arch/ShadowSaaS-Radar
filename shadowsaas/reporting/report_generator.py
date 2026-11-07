FOOTER = (
    "Based on authentication events only; "
    "does not confirm file uploads or data transfers."
)


def format_report(results):
    lines = []

    if not results:
        lines.append(
            "No generative AI authentication activity detected."
        )

    for result in results:
        lines.append(
            f"[{result['level'].upper()}] "
            f"{result['user']} -> {result['app']} "
            f"(score {result['score']}/100)"
        )

        lines.append("  Evidence:")
        for item in result["evidence"]:
            lines.append(f"    - {item}")

        if result["assumptions"]:
            lines.append("  Assumptions:")
            for item in result["assumptions"]:
                lines.append(f"    - {item}")

        lines.append("")

    lines.append(FOOTER)

    return "\n".join(lines)