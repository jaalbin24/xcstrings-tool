"""Parser for XCStrings catalog files."""

import json
from pathlib import Path
from typing import Any

from xcstrings_tool.core.models import (
    ExtractionState,
    Localization,
    StringCatalog,
    StringEntry,
)


class ParserError(Exception):
    """Raised when parsing fails."""

    pass


class Parser:
    """Parse XCStrings catalog JSON files."""

    @staticmethod
    def parse_file(path: Path) -> tuple[StringCatalog, list[StringEntry]]:
        """Parse an XCStrings file and return catalog metadata and string entries.

        Args:
            path: Path to the .xcstrings file

        Returns:
            Tuple of (StringCatalog, List[StringEntry])

        Raises:
            ParserError: If file cannot be parsed
        """
        if not path.exists():
            raise ParserError(f"File not found: {path}")

        if not path.suffix == ".xcstrings":
            raise ParserError(f"File must have .xcstrings extension: {path}")

        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ParserError(f"Invalid JSON: {e}")
        except Exception as e:
            raise ParserError(f"Failed to read file: {e}")

        return Parser._parse_data(data)

    @staticmethod
    def _parse_data(data: dict[str, Any]) -> tuple[StringCatalog, list[StringEntry]]:
        """Parse catalog data dictionary.

        Args:
            data: Parsed JSON dictionary

        Returns:
            Tuple of (StringCatalog, List[StringEntry])

        Raises:
            ParserError: If data structure is invalid
        """
        try:
            catalog = StringCatalog(**data)
        except Exception as e:
            raise ParserError(f"Invalid catalog structure: {e}")

        # Parse individual string entries
        entries = []
        for key, value in catalog.strings.items():
            try:
                # Parse localizations
                localizations = {}
                for lang, loc_data in value.get("localizations", {}).items():
                    localizations[lang] = Localization(**loc_data)

                # Parse extraction state
                extraction_state_str = value.get("extractionState")
                extraction_state = None
                if extraction_state_str:
                    try:
                        extraction_state = ExtractionState(extraction_state_str)
                    except ValueError:
                        # Unknown extraction state, leave as None
                        pass

                entry = StringEntry(
                    key=key,
                    extractionState=extraction_state,
                    localizations=localizations,
                    comment=value.get("comment"),
                )
                entries.append(entry)
            except Exception:
                # Skip malformed entries but continue parsing
                continue

        return catalog, entries

    @staticmethod
    def validate(path: Path) -> tuple[bool, str]:
        """Validate an XCStrings file structure.

        Args:
            path: Path to the .xcstrings file

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            Parser.parse_file(path)
            return True, ""
        except ParserError as e:
            return False, str(e)
