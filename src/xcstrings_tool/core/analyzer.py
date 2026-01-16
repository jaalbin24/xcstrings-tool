"""Analyzer for localization completeness."""


from xcstrings_tool.core.models import (
    AnalysisResult,
    LocalizationState,
    StringCatalog,
    StringEntry,
)


class Analyzer:
    """Analyze string catalog for localization completeness."""

    @staticmethod
    def analyze(
        catalog: StringCatalog,
        entries: list[StringEntry],
        target_language: str,
    ) -> AnalysisResult:
        """Analyze catalog for completeness of target language translations.

        Args:
            catalog: The string catalog metadata
            entries: List of string entries to analyze
            target_language: Language code to check (e.g., 'es-MX', 'fr')

        Returns:
            AnalysisResult with statistics and categorized entries
        """
        total_strings = len(entries)
        translated = 0
        missing_translation = 0
        needs_review = 0
        stale = 0

        missing_entries: list[StringEntry] = []
        needs_review_entries: list[StringEntry] = []
        stale_entries: list[StringEntry] = []

        for entry in entries:
            target_loc = entry.localizations.get(target_language)

            if target_loc is None:
                # No translation exists for target language
                missing_translation += 1
                missing_entries.append(entry)
            else:
                state = target_loc.string_unit.state
                if state == LocalizationState.TRANSLATED:
                    translated += 1
                elif state == LocalizationState.NEEDS_REVIEW:
                    needs_review += 1
                    needs_review_entries.append(entry)
                elif state == LocalizationState.STALE:
                    stale += 1
                    stale_entries.append(entry)
                elif state == LocalizationState.NEW:
                    missing_translation += 1
                    missing_entries.append(entry)

        # Calculate completion percentage
        completion_percentage = (
            (translated / total_strings * 100) if total_strings > 0 else 0.0
        )

        return AnalysisResult(
            total_strings=total_strings,
            source_language=catalog.source_language,
            target_language=target_language,
            translated=translated,
            missing_translation=missing_translation,
            needs_review=needs_review,
            stale=stale,
            completion_percentage=round(completion_percentage, 1),
            missing_entries=missing_entries,
            needs_review_entries=needs_review_entries,
            stale_entries=stale_entries,
        )
