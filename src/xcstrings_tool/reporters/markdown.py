"""Markdown reporter for documentation."""

from datetime import datetime
from pathlib import Path
from typing import Optional

from xcstrings_tool.core.models import AnalysisResult
from xcstrings_tool.reporters.base import Reporter


class MarkdownReporter(Reporter):
    """Generate Markdown reports."""

    def generate(
        self, result: AnalysisResult, output_path: Optional[Path] = None
    ) -> str:
        """Generate Markdown report.

        Args:
            result: Analysis result
            output_path: Optional path to save Markdown file

        Returns:
            Markdown string
        """
        sections = [
            self._header(result),
            self._summary(result),
            self._missing_translations(result),
            self._needs_review(result),
            self._stale_entries(result),
            self._next_steps(result),
        ]

        markdown = "\n\n".join(sections)

        if output_path:
            output_path.write_text(markdown, encoding="utf-8")

        return markdown

    def _header(self, result: AnalysisResult) -> str:
        """Generate header section."""
        return f"""# Localization Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Source Language:** {result.source_language}
**Target Language:** {result.target_language}"""

    def _summary(self, result: AnalysisResult) -> str:
        """Generate summary section."""
        missing_pct = (
            result.missing_translation / result.total_strings * 100
            if result.total_strings > 0
            else 0
        )
        needs_review_pct = (
            result.needs_review / result.total_strings * 100
            if result.total_strings > 0
            else 0
        )
        stale_pct = (
            result.stale / result.total_strings * 100
            if result.total_strings > 0
            else 0
        )

        return f"""## Summary

| Metric | Count | Percentage |
|--------|-------|------------|
| Total Strings | {result.total_strings} | 100.0% |
| Translated | {result.translated} | {result.completion_percentage}% |
| Missing Translation | {result.missing_translation} | {missing_pct:.1f}% |
| Needs Review | {result.needs_review} | {needs_review_pct:.1f}% |
| Stale | {result.stale} | {stale_pct:.1f}% |"""

    def _missing_translations(self, result: AnalysisResult) -> str:
        """Generate missing translations section."""
        if not result.missing_entries:
            return "## Missing Translations\n\nNone."

        lines = ["## Missing Translations", ""]
        for entry in result.missing_entries[:20]:  # Limit to first 20
            source_loc = entry.localizations.get(result.source_language)
            source_value = source_loc.string_unit.value if source_loc else entry.key
            lines.append(f"- `{entry.key}`: _{source_value}_")

        if len(result.missing_entries) > 20:
            lines.append(f"\n_...and {len(result.missing_entries) - 20} more_")

        return "\n".join(lines)

    def _needs_review(self, result: AnalysisResult) -> str:
        """Generate needs review section."""
        if not result.needs_review_entries:
            return "## Needs Review\n\nNone."

        lines = ["## Needs Review", ""]
        for entry in result.needs_review_entries[:20]:
            lines.append(f"- `{entry.key}`")

        if len(result.needs_review_entries) > 20:
            lines.append(f"\n_...and {len(result.needs_review_entries) - 20} more_")

        return "\n".join(lines)

    def _stale_entries(self, result: AnalysisResult) -> str:
        """Generate stale entries section."""
        if not result.stale_entries:
            return "## Stale Entries\n\nNone."

        lines = ["## Stale Entries", ""]
        for entry in result.stale_entries[:20]:
            lines.append(f"- `{entry.key}`")

        if len(result.stale_entries) > 20:
            lines.append(f"\n_...and {len(result.stale_entries) - 20} more_")

        return "\n".join(lines)

    def _next_steps(self, result: AnalysisResult) -> str:
        """Generate next steps section."""
        steps = []

        if result.missing_translation > 0:
            steps.append(
                f"1. Translate {result.missing_translation} missing strings"
            )

        if result.needs_review > 0:
            steps.append(f"2. Review {result.needs_review} strings")

        if result.stale > 0:
            steps.append(f"3. Remove {result.stale} stale entries")

        if not steps:
            return "## Next Steps\n\nYou're all set!"

        return "## Next Steps\n\n" + "\n".join(steps)
