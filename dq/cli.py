import typer
from typing import Optional
from pathlib import Path
import sys
from rich.console import Console
from rich.table import Table

from dq.discovery import discover_checks
from dq.engine import run_checks
from dq.runner import apply_policy, PipelineHaltError
from dq.guards import generate_guards
from dq.report import write_json_report, write_markdown_report

app = typer.Typer()
console = Console()

@app.command()
def generate():
    """Generates the multi-tenancy guard suite."""
    generate_guards("fixtures/catalog.yml", "checks/_generated/")
    console.print("[green]Guards generated successfully in checks/_generated/[/green]")

@app.command()
def validate(checks_dir: str):
    """Validates check declarations."""
    try:
        checks = discover_checks(checks_dir)
        console.print(f"[green]Successfully validated {len(checks)} table declarations.[/green]")
    except Exception as e:
        console.print(f"[red]Validation failed: {e}[/red]")
        sys.exit(2)

@app.command()
def run(
    backend: str = "duckdb",
    data: str = "fixtures/data/corrupt",
    checks: str = "checks/",
    fail_fast: bool = False,
    fail_on_warning: bool = False,
    report_dir: str = "reports/"
):
    """Runs data quality checks."""
    
    if backend == "duckdb":
        from dq.adapters.duckdb_adapter import DuckDBAdapter
        try:
            adapter = DuckDBAdapter(data)
        except Exception as e:
            console.print(f"[red]Failed to connect to DuckDB: {e}[/red]")
            sys.exit(3)
    elif backend == "clickhouse":
        from dq.adapters.clickhouse_adapter import ClickHouseAdapter
        try:
            adapter = ClickHouseAdapter()
        except Exception as e:
            console.print(f"[red]Failed to connect to ClickHouse: {e}[/red]")
            sys.exit(3)
    else:
        console.print(f"[red]Unknown backend: {backend}[/red]")
        sys.exit(3)

    try:
        declarations = discover_checks(checks)
    except Exception as e:
        console.print(f"[red]Invalid config: {e}[/red]")
        sys.exit(2)

    report = run_checks(declarations, adapter)
    adapter.close()

    write_json_report(report, report_dir)
    write_markdown_report(report, report_dir)

    # Print to console
    table = Table(title="DQ Run Results")
    table.add_column("ID")
    table.add_column("Table")
    table.add_column("Type")
    table.add_column("Severity")
    table.add_column("Status")
    table.add_column("Violations")
    table.add_column("Duration (ms)")

    for r in report.results:
        color = "green" if r.status == "PASS" else ("red" if r.severity == "error" else "yellow")
        table.add_row(
            r.check_id, r.table, r.type, r.severity, 
            f"[{color}]{r.status}[/{color}]", 
            str(r.violations), str(r.duration_ms)
        )

    console.print(table)
    
    verdict = f"PIPELINE HALTED: {report.errors} errors, {report.warnings} warnings" if report.errors > 0 or (fail_on_warning and report.warnings > 0) else f"PIPELINE SUCCESS: {report.passed} passed, {report.warnings} warnings"
    color = "red" if report.errors > 0 or (fail_on_warning and report.warnings > 0) else "green"
    console.print(f"[{color}]{verdict}[/{color}]")

    try:
        apply_policy(report, fail_fast, fail_on_warning)
    except PipelineHaltError:
        sys.exit(1)
        
    sys.exit(0)

@app.command()
def demo(backend: str = "duckdb"):
    """Runs a live demo."""
    console.print(f"--- Running CLEAN data on {backend} ---")
    generate() # Ensure checks are present
    run(backend=backend, data="fixtures/data/clean", checks="checks/", report_dir="reports/clean")
    
if __name__ == "__main__":
    app()
