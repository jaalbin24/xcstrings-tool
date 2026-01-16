"""CSV reporter for translation vendors."""

from pathlib import Path
from typing import Optional

from xcstrings_tool.core.models import AnalysisResult
from xcstrings_tool.reporters.base import Reporter


class CSVReporter(Reporter):
    """Generate CSV reports for translation tools."""

    def generate(
        self, result: AnalysisResult, output_path: Optional[Path] = None
    ) -> str:
        """Generate CSV report.

        Args:
            result: Analysis result
            output_path: Optional path to save CSV file

        Returns:
            CSV string
        """
        rows = self._build_rows(result)
        csv_lines = []

        # Write header
        header = [
            "Key",
            "Source Language",
            "Source Value",
            "Source State",
            "Target Language",
            "Target Value",
            "Target State",
            "Extraction State",
            "Comment",
        ]
        csv_lines.append(",".join(f'"{col}"' for col in header))

        # Write data rows
        for row in rows:
            csv_lines.append(
                ",".join(f'"{str(val).replace(chr(34), chr(34)+chr(34))}"' for val in row)
            )

        csv_str = "\n".join(csv_lines)

        if output_path:
            output_path.write_text(csv_str, encoding="utf-8")

        return csv_str

    def _build_rows(self, result: AnalysisResult) -> list[list[str]]:
        """Build CSV rows from result."""
        rows = []

        # Include all entries (missing, needs review, and stale)
        all_entries = (
            result.missing_entries
            + result.needs_review_entries
            + result.stale_entries
        )

        for entry in all_entries:
            source_loc = entry.localizations.get(result.source_language)
            target_loc = entry.localizations.get(result.target_language)

            row = [
                entry.key,
                result.source_language,
                source_loc.string_unit.value if source_loc else "",
                source_loc.string_unit.state.value if source_loc else "",
                result.target_language,
                target_loc.string_unit.value if target_loc else "",
                target_loc.string_unit.state.value if target_loc else "",
                entry.extraction_state.value if entry.extraction_state else "",
                entry.comment or "",
            ]
            rows.append(row)

        return rows
