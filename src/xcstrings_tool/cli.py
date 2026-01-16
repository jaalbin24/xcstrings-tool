"""Command-line interface for xcstrings-tool."""

import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console

from xcstrings_tool import __version__
from xcstrings_tool.core.analyzer import Analyzer
from xcstrings_tool.core.parser import Parser, ParserError
from xcstrings_tool.reporters import (
    ConsoleReporter,
    CSVReporter,
    JSONReporter,
    MarkdownReporter,
)

console = Console()


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    """Audit and analyze Xcode String Catalogs for localization completeness."""
    pass


@main.command()
@click.argument(
    "catalog_path",
    type=click.Path(exists=True, path_type=Path),
)
@click.option(
    "--target",
    "-t",
    "target_language",
    default="es-MX",
    help="Target language code (e.g., es-MX, fr, de)",
    show_default=True,
)
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(path_type=Path),
    default=None,
    help="Directory for output files (default: current directory)",
)
@click.option(
    "--format",
    "-f",
    "formats",
    multiple=True,
    type=click.Choice(["console", "json", "csv", "markdown"], case_sensitive=False),
    default=["console"],
    help="Output format(s). Can specify multiple.",
    show_default=True,
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Show detailed entry lists in console output",
)
@click.option(
    "--threshold",
    type=click.IntRange(0, 100),
    default=None,
    help="Fail with exit code 1 if completion percentage below threshold (for CI)",
)
def audit(
    catalog_path: Path,
    target_language: str,
    output_dir: Optional[Path],
    formats: tuple[str, ...],
    verbose: bool,
    threshold: Optional[int],
) -> None:
    """Audit a String Catalog for localization completeness.

    \b
    Examples:
        xcstrings-tool audit Localizable.xcstrings
        xcstrings-tool audit Localizable.xcstrings --target fr
        xcstrings-tool audit Localizable.xcstrings -f json -f csv -o reports/
        xcstrings-tool audit Localizable.xcstrings --threshold 80
    """
    try:
        # Parse catalog
        catalog, entries = Parser.parse_file(catalog_path)

        # Analyze
        result = Analyzer.analyze(catalog, entries, target_language)

        # Determine output directory
        out_dir = output_dir if output_dir else Path.cwd()
        out_dir.mkdir(parents=True, exist_ok=True)

        # Generate reports
        for fmt in formats:
            if fmt == "console":
                console_reporter = ConsoleReporter(verbose=verbose)
                console_reporter.generate(result)
            elif fmt == "json":
                json_reporter = JSONReporter()
                output_path = out_dir / "localization_report.json"
                json_reporter.generate(result, output_path)
                console.print(f"Generated: [cyan]{output_path}[/cyan]")
            elif fmt == "csv":
                csv_reporter = CSVReporter()
                output_path = out_dir / "localization_report.csv"
                csv_reporter.generate(result, output_path)
                console.print(f"Generated: [cyan]{output_path}[/cyan]")
            elif fmt == "markdown":
                md_reporter = MarkdownReporter()
                output_path = out_dir / "localization_report.md"
                md_reporter.generate(result, output_path)
                console.print(f"Generated: [cyan]{output_path}[/cyan]")

        # Check threshold for CI
        if threshold is not None:
            if result.completion_percentage < threshold:
                console.print(
                    f"\n[red]Completion {result.completion_percentage}% "
                    f"below threshold {threshold}%[/red]"
                )
                sys.exit(1)
            else:
                console.print(
                    f"\n[green]Completion {result.completion_percentage}% "
                    f"meets threshold {threshold}%[/green]"
                )

    except ParserError as e:
        console.print(f"[red]Error:[/red] {e}", style="bold")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}", style="bold")
        sys.exit(1)


@main.command()
@click.argument("catalog_path", type=click.Path(exists=True, path_type=Path))
def validate(catalog_path: Path) -> None:
    """Validate String Catalog JSON structure.

    \b
    Examples:
        xcstrings-tool validate Localizable.xcstrings
    """
    try:
        is_valid, error_msg = Parser.validate(catalog_path)

        if is_valid:
            console.print(
                f"[green]{catalog_path.name} is valid[/green]", style="bold"
            )
        else:
            console.print(
                f"[red]{catalog_path.name} is invalid:[/red]", style="bold"
            )
            console.print(f"  {error_msg}")
            sys.exit(1)

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}", style="bold")
        sys.exit(1)


@main.command()
@click.argument("catalog_path", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--target",
    "-t",
    "target_language",
    required=True,
    help="Target language code (e.g., es-MX, fr)",
)
@click.option(
    "--output",
    "-o",
    "output_path",
    type=click.Path(path_type=Path),
    default=None,
    help="Output CSV file path (default: missing_translations.csv)",
)
def export(
    catalog_path: Path, target_language: str, output_path: Optional[Path]
) -> None:
    """Export missing translations to CSV for translation vendors.

    \b
    Examples:
        xcstrings-tool export Localizable.xcstrings --target es-MX
        xcstrings-tool export Localizable.xcstrings -t fr -o french_todo.csv
    """
    try:
        # Parse and analyze
        catalog, entries = Parser.parse_file(catalog_path)
        result = Analyzer.analyze(catalog, entries, target_language)

        # Generate CSV
        output = output_path if output_path else Path("missing_translations.csv")
        reporter = CSVReporter()
        reporter.generate(result, output)

        console.print(f"[green]Exported to[/green] [cyan]{output}[/cyan]")
        console.print(
            f"  {result.missing_translation} missing translations "
            f"+ {result.needs_review} needing review"
        )

    except ParserError as e:
        console.print(f"[red]Error:[/red] {e}", style="bold")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}", style="bold")
        sys.exit(1)


@main.command()
@click.argument("catalog_path", type=click.Path(exists=True, path_type=Path))
def stats(catalog_path: Path) -> None:
    """Show quick statistics about the catalog.

    \b
    Examples:
        xcstrings-tool stats Localizable.xcstrings
    """
    try:
        catalog, entries = Parser.parse_file(catalog_path)

        console.print("\n[bold]String Catalog Statistics[/bold]")
        console.print(f"File: [cyan]{catalog_path.name}[/cyan]")
        console.print(f"Source Language: [cyan]{catalog.source_language}[/cyan]")
        console.print(f"Total Strings: [cyan]{len(entries)}[/cyan]")

        # Count available languages
        languages: set[str] = set()
        for entry in entries:
            languages.update(entry.localizations.keys())

        console.print(f"Available Languages: [cyan]{', '.join(sorted(languages))}[/cyan]")
        console.print()

    except ParserError as e:
        console.print(f"[red]Error:[/red] {e}", style="bold")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}", style="bold")
        sys.exit(1)


if __name__ == "__main__":
    main()
