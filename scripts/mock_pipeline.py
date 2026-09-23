import sys
import subprocess
from rich.console import Console

console = Console()

def main():
    console.print("[bold blue]Starting Mock Pipeline...[/bold blue]")
    console.print("[cyan]1. STAGE: Load[/cyan] (simulated)")
    
    console.print("[cyan]2. STAGE: DQ Gate[/cyan]")
    # Run the DQ check on corrupt data
    result = subprocess.run(["dq", "run", "--backend", "duckdb", "--data", "fixtures/data/corrupt"])
    
    if result.returncode != 0:
        console.print("[bold red]PUBLISH SKIPPED (DQ gate failed)[/bold red]")
        sys.exit(1)
        
    console.print("[cyan]3. STAGE: Publish Gold[/cyan]")
    console.print("[bold green]Pipeline finished successfully.[/bold green]")

if __name__ == "__main__":
    main()
