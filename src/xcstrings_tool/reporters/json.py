"""JSON reporter for programmatic use."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from xcstrings_tool.core.models import AnalysisResult, StringEntry
from xcstrings_tool.reporters.base import Reporter


class JSONReporter(Reporter):
    """Generate JSON reports."""

    def generate(
        self, result: AnalysisResult, output_path: Optional[Path] = None
    ) -> str:
        """Generate JSON report.

        Args:
            result: Analysis result
            output_path: Optional path to save JSON file

        Returns:
            JSON string
        """
        report = self._build_report(result)
        json_str = json.dumps(report, indent=2, ensure_ascii=False)

        if output_path:
            output_path.write_text(json_str, encoding="utf-8")

        return json_str

    def _build_report(self, result: AnalysisResult) -> dict[str, Any]:
        """Build report dictionary."""
        return {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "source_language": result.source_language,
                "target_language": result.target_language,
            },
            "summary": {
                "total_strings": result.total_strings,
                "translated": result.translated,
                "missing_translation": result.missing_translation,
                "needs_review": result.needs_review,
                "stale": result.stale,
                "completion_percentage": result.completion_percentage,
            },
            "missing_translations": [
                self._entry_to_dict(entry, result)
                for entry in result.missing_entries
            ],
            "needs_review": [
                self._entry_to_dict(entry, result)
                for entry in result.needs_review_entries
            ],
            "stale_entries": [
                self._entry_to_dict(entry, result) for entry in result.stale_entries
            ],
        }

    def _entry_to_dict(
        self, entry: StringEntry, result: AnalysisResult
    ) -> dict[str, Any]:
        """Convert string entry to dictionary."""
        source_loc = entry.localizations.get(result.source_language)
        target_loc = entry.localizations.get(result.target_language)

        return {
            "key": entry.key,
            "comment": entry.comment,
            "extraction_state": (
                entry.extraction_state.value if entry.extraction_state else None
            ),
            "source": {
                "value": source_loc.string_unit.value if source_loc else None,
                "state": source_loc.string_unit.state.value if source_loc else None,
            },
            "target": {
                "value": target_loc.string_unit.value if target_loc else None,
                "state": target_loc.string_unit.state.value if target_loc else None,
            },
        }
