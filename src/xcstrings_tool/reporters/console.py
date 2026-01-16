"""Console reporter with Rich formatting."""

from datetime import datetime
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn
from rich.table import Table

from xcstrings_tool.core.models import AnalysisResult
from xcstrings_tool.reporters.base import Reporter


class ConsoleReporter(Reporter):
    """Generate beautiful console output with Rich."""

    def __init__(self, verbose: bool = False) -> None:
        """Initialize console reporter.

        Args:
            verbose: Show detailed entries (not just summary)
        """
        self.verbose = verbose
        self.console = Console()

    def generate(
        self, result: AnalysisResult, output_path: Optional[Path] = None
    ) -> str:
        """Generate console report.

        Args:
            result: Analysis result
            output_path: Ignored for console output

        Returns:
            Empty string (output is printed directly)
        """
        self._print_header(result)
        self._print_progress(result)
        self._print_summary_table(result)

        if self.verbose:
            self._print_detailed_entries(result)

        self._print_next_steps(result)

        return ""

    def _print_header(self, result: AnalysisResult) -> None:
        """Print report header."""
        title = f"[bold cyan]Localization Analysis[/bold cyan]\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        self.console.print(Panel(title, expand=False))
        self.console.print()

    def _print_progress(self, result: AnalysisResult) -> None:
        """Print progress bars."""
        progress = Progress(
            TextColumn("[bold]{task.description}"),
            BarColumn(bar_width=40),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("({task.completed}/{task.total})"),
        )

        with progress:
            progress.add_task(
                f"[green]{result.target_language} Translation Progress",
                total=result.total_strings,
                completed=result.translated,
            )

        self.console.print()

    def _print_summary_table(self, result: AnalysisResult) -> None:
        """Print summary statistics table."""
        table = Table(title="Summary Statistics", show_header=True)
        table.add_column("Metric", style="cyan")
        table.add_column("Count", justify="right", style="yellow")
        table.add_column("Percentage", justify="right")

        table.add_row(
            "Total Strings",
            str(result.total_strings),
            "100.0%",
        )
        table.add_row(
            "Translated",
            str(result.translated),
            f"{result.completion_percentage}%",
            style="green",
        )
        table.add_row(
            "Missing Translation",
            str(result.missing_translation),
            f"{result.missing_translation / result.total_strings * 100:.1f}%"
            if result.total_strings > 0
            else "0.0%",
            style="red",
        )
        table.add_row(
            "Needs Review",
            str(result.needs_review),
            f"{result.needs_review / result.total_strings * 100:.1f}%"
            if result.total_strings > 0
            else "0.0%",
            style="yellow",
        )
        table.add_row(
            "Stale",
            str(result.stale),
            f"{result.stale / result.total_strings * 100:.1f}%"
            if result.total_strings > 0
            else "0.0%",
            style="dim",
        )

        self.console.print(table)
        self.console.print()

    def _print_detailed_entries(self, result: AnalysisResult) -> None:
        """Print detailed entry lists."""
        if result.missing_translation > 0:
            self.console.print("[bold red]Missing Translations[/bold red]")
            for entry in result.missing_entries[:10]:  # Show first 10
                source_loc = entry.localizations.get(result.source_language)
                source_value = (
                    source_loc.string_unit.value if source_loc else entry.key
                )
                self.console.print(f"  • {entry.key}: [dim]{source_value}[/dim]")
            if result.missing_translation > 10:
                self.console.print(
                    f"  [dim]... and {result.missing_translation - 10} more[/dim]"
                )
            self.console.print()

        if result.needs_review > 0:
            self.console.print("[bold yellow]Needs Review[/bold yellow]")
            for entry in result.needs_review_entries[:10]:
                self.console.print(f"  • {entry.key}")
            if result.needs_review > 10:
                self.console.print(
                    f"  [dim]... and {result.needs_review - 10} more[/dim]"
                )
            self.console.print()

    def _print_next_steps(self, result: AnalysisResult) -> None:
        """Print actionable next steps."""
        next_steps = []

        if result.missing_translation > 0:
            next_steps.append(
                f"Translate {result.missing_translation} missing {result.target_language} strings"
            )

        if result.needs_review > 0:
            next_steps.append(
                f"Review {result.needs_review} strings marked for review"
            )

        if result.stale > 0:
            next_steps.append(f"Remove {result.stale} stale entries from catalog")

        if next_steps:
            self.console.print("[bold]Next Steps:[/bold]")
            for i, step in enumerate(next_steps, 1):
                self.console.print(f"  {i}. {step}")
            self.console.print()
