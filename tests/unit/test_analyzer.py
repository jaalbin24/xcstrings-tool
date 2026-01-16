"""Tests for analyzer module."""

from pathlib import Path

from xcstrings_tool.core.analyzer import Analyzer
from xcstrings_tool.core.parser import Parser


def test_analyze_fully_translated(simple_catalog: Path) -> None:
    """Test analysis of fully translated catalog."""
    catalog, entries = Parser.parse_file(simple_catalog)
    result = Analyzer.analyze(catalog, entries, "es-MX")

    assert result.total_strings == 2
    assert result.translated == 2
    assert result.missing_translation == 0
    assert result.needs_review == 0
    assert result.stale == 0
    assert result.completion_percentage == 100.0


def test_analyze_missing_translations(missing_translations_catalog: Path) -> None:
    """Test analysis with missing translations."""
    catalog, entries = Parser.parse_file(missing_translations_catalog)
    result = Analyzer.analyze(catalog, entries, "es-MX")

    assert result.total_strings == 3
    assert result.translated == 1
    assert result.missing_translation == 2
    assert result.completion_percentage == 33.3


def test_analyze_needs_review(needs_review_catalog: Path) -> None:
    """Test analysis with items needing review."""
    catalog, entries = Parser.parse_file(needs_review_catalog)
    result = Analyzer.analyze(catalog, entries, "es-MX")

    assert result.total_strings == 2
    assert result.translated == 0
    assert result.needs_review == 2
    assert len(result.needs_review_entries) == 2


def test_analyze_empty_catalog() -> None:
    """Test analysis of empty catalog."""
    from xcstrings_tool.core.models import StringCatalog

    catalog = StringCatalog(sourceLanguage="en", version="1.0", strings={})
    result = Analyzer.analyze(catalog, [], "es-MX")

    assert result.total_strings == 0
    assert result.completion_percentage == 0.0


def test_analyze_different_target_language(simple_catalog: Path) -> None:
    """Test analysis for different target language."""
    catalog, entries = Parser.parse_file(simple_catalog)
    result = Analyzer.analyze(catalog, entries, "fr")

    # French translations don't exist in simple catalog
    assert result.missing_translation == 2
    assert result.translated == 0
