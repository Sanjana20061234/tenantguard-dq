from pathlib import Path

from dq.models import RunReport


def write_json_report(report: RunReport, out_dir: str | Path):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "dq_report.json", "w") as f:
        f.write(report.model_dump_json(indent=2))

def write_markdown_report(report: RunReport, out_dir: str | Path):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        "# DQ Run Report",
        f"- **Backend**: {report.backend}",
        f"- **Total Checks**: {report.total_checks}",
        f"- **Passed**: {report.passed}",
        f"- **Errors**: {report.errors}",
        f"- **Warnings**: {report.warnings}",
        "",
        "## Results",
        "| ID | Table | Type | Severity | Status | Violations | Duration (ms) | Message |",
        "|---|---|---|---|---|---|---|---|"
    ]
    
    for r in report.results:
        msg = r.message or ""
        msg = msg.replace("|", "/")
        lines.append(f"| {r.check_id} | {r.table} | {r.type} | {r.severity} | {r.status} | {r.violations} | {r.duration_ms} | {msg} |")
        
    with open(out_dir / "dq_report.md", "w") as f:
        f.write("\n".join(lines))
