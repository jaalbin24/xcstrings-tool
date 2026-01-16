"""Tests for parser module."""

from pathlib import Path

import pytest

from xcstrings_tool.core.parser import Parser, ParserError


def test_parse_simple_catalog(simple_catalog: Path) -> None:
    """Test parsing a simple valid catalog."""
    catalog, entries = Parser.parse_file(simple_catalog)

    assert catalog.source_language == "en"
    assert catalog.version == "1.0"
    assert len(entries) == 2
    assert entries[0].key in ["hello", "goodbye"]


def test_parse_missing_translations_catalog(missing_translations_catalog: Path) -> None:
    """Test parsing catalog with missing translations."""
    catalog, entries = Parser.parse_file(missing_translations_catalog)

    assert len(entries) == 3

    # Check that some entries have Spanish, some don't
    entries_with_spanish = sum(1 for e in entries if "es-MX" in e.localizations)
    assert entries_with_spanish == 1  # Only "welcome" has Spanish


def test_parse_invalid_catalog(invalid_catalog: Path) -> None:
    """Test parsing invalid catalog raises error."""
    with pytest.raises(ParserError):
        Parser.parse_file(invalid_catalog)


def test_parse_nonexistent_file() -> None:
    """Test parsing nonexistent file raises error."""
    with pytest.raises(ParserError, match="File not found"):
        Parser.parse_file(Path("does_not_exist.xcstrings"))


def test_parse_wrong_extension(tmp_path: Path) -> None:
    """Test parsing file with wrong extension raises error."""
    wrong_file = tmp_path / "test.json"
    wrong_file.write_text("{}")

    with pytest.raises(ParserError, match="must have .xcstrings extension"):
        Parser.parse_file(wrong_file)


def test_validate_valid_catalog(simple_catalog: Path) -> None:
    """Test validation succeeds for valid catalog."""
    is_valid, error_msg = Parser.validate(simple_catalog)

    assert is_valid is True
    assert error_msg == ""


def test_validate_invalid_catalog(invalid_catalog: Path) -> None:
    """Test validation fails for invalid catalog."""
    is_valid, error_msg = Parser.validate(invalid_catalog)

    assert is_valid is False
    assert error_msg != ""
