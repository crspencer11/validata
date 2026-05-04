import click
import json
import logging
from rich import print
from rich.table import Table

from .engine import DataValidator
from .rules import PriceSpikeRule, MonotonicTimeRule, StatisticalOutlierRule

logging.basicConfig(level=logging.INFO)

@click.command()
@click.option('--input', required=True, help='Input JSON file')
@click.option('--threshold', default=0.10, help='Price spike threshold')
@click.option('--repair', is_flag=True, help='Enable repair mode')
@click.option('--output', type=str, help='Optional output file (JSON)')
def main(input, threshold, repair, output):
    try:
        with open(input, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"[red]Failed to load file:[/red] {e}")
        return

    rules = [
        PriceSpikeRule(threshold, enable_repair=repair),
        MonotonicTimeRule(enable_repair=repair),
        StatisticalOutlierRule(),
    ]

    validator = DataValidator(rules, repair_mode=repair)
    result = validator.run(data)

    # ---- Pretty output ----
    print("\n[bold]Validation Summary[/bold]")
    print(f"Status: {result.status}")
    print(f"Violations: {result.violation_count}")

    if result.violations:
        table = Table(title="Violations")
        table.add_column("Type")
        table.add_column("Timestamp")
        table.add_column("Detail")

        display = result.violations[:20]
        for v in display:
            table.add_row(v.type, str(v.timestamp), v.detail)

        print(table)

        if len(result.violations) > 20:
            print(f"[dim]...and {result.violation_count - 20} more (use --output to see all)[/dim]")

    if repair and result.repaired_data:
        print("\n[green]Repair applied[/green]")

    # ---- Save output ----
    if output:
        with open(output, "w") as f:
            json.dump({
                "status": result.status,
                "violation_count": result.violation_count,
                "violations": [v.__dict__ for v in result.violations],
                "repaired_data": result.repaired_data
            }, f, indent=2)

        print(f"\nSaved report to {output}")

if __name__ == '__main__':
    main()