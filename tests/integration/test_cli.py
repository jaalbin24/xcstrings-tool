"""Integration tests for CLI."""

from pathlib import Path

from click.testing import CliRunner

from xcstrings_tool.cli import main


def test_audit_command(simple_catalog: Path, tmp_path: Path) -> None:
    """Test audit command execution."""
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "audit",
            str(simple_catalog),
            "--target",
            "es-MX",
            "--output-dir",
            str(tmp_path),
        ],
    )

    assert result.exit_code == 0
    assert "Summary Statistics" in result.output


def test_audit_with_json_export(simple_catalog: Path, tmp_path: Path) -> None:
    """Test audit command with JSON export."""
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "audit",
            str(simple_catalog),
            "--format",
            "json",
            "--output-dir",
            str(tmp_path),
        ],
    )

    assert result.exit_code == 0
    assert (tmp_path / "localization_report.json").exists()


def test_audit_with_multiple_formats(simple_catalog: Path, tmp_path: Path) -> None:
    """Test audit with multiple output formats."""
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "audit",
            str(simple_catalog),
            "-f",
            "json",
            "-f",
            "csv",
            "-f",
            "markdown",
            "-o",
            str(tmp_path),
        ],
    )

    assert result.exit_code == 0
    assert (tmp_path / "localization_report.json").exists()
    assert (tmp_path / "localization_report.csv").exists()
    assert (tmp_path / "localization_report.md").exists()


def test_audit_with_threshold_pass(simple_catalog: Path) -> None:
    """Test audit with threshold that passes."""
    runner = CliRunner()
    result = runner.invoke(
        main,
        ["audit", str(simple_catalog), "--threshold", "90"],
    )

    assert result.exit_code == 0
    assert "meets threshold" in result.output


def test_audit_with_threshold_fail(missing_translations_catalog: Path) -> None:
    """Test audit with threshold that fails."""
    runner = CliRunner()
    result = runner.invoke(
        main,
        ["audit", str(missing_translations_catalog), "--threshold", "90"],
    )

    assert result.exit_code == 1
    assert "below threshold" in result.output


def test_validate_command_valid(simple_catalog: Path) -> None:
    """Test validate command with valid catalog."""
    runner = CliRunner()
    result = runner.invoke(main, ["validate", str(simple_catalog)])

    assert result.exit_code == 0
    assert "is valid" in result.output


def test_validate_command_invalid(invalid_catalog: Path) -> None:
    """Test validate command with invalid catalog."""
    runner = CliRunner()
    result = runner.invoke(main, ["validate", str(invalid_catalog)])

    assert result.exit_code == 1
    assert "is invalid" in result.output


def test_export_command(missing_translations_catalog: Path, tmp_path: Path) -> None:
    """Test export command."""
    output_file = tmp_path / "export.csv"
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "export",
            str(missing_translations_catalog),
            "--target",
            "es-MX",
            "--output",
            str(output_file),
        ],
    )

    assert result.exit_code == 0
    assert output_file.exists()
    assert "Exported to" in result.output


def test_stats_command(simple_catalog: Path) -> None:
    """Test stats command."""
    runner = CliRunner()
    result = runner.invoke(main, ["stats", str(simple_catalog)])

    assert result.exit_code == 0
    assert "String Catalog Statistics" in result.output
    assert "Source Language" in result.output
    assert "Total Strings" in result.output


def test_version_flag() -> None:
    """Test --version flag."""
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])

    assert result.exit_code == 0
    assert "0.1.0" in result.output
