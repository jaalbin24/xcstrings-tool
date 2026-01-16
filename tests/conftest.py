"""Pytest configuration and fixtures."""

from pathlib import Path

import pytest


@pytest.fixture
def fixtures_dir() -> Path:
    """Return path to test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def simple_catalog(fixtures_dir: Path) -> Path:
    """Path to simple test catalog."""
    return fixtures_dir / "simple.xcstrings"


@pytest.fixture
def missing_translations_catalog(fixtures_dir: Path) -> Path:
    """Path to catalog with missing translations."""
    return fixtures_dir / "missing_translations.xcstrings"


@pytest.fixture
def needs_review_catalog(fixtures_dir: Path) -> Path:
    """Path to catalog with items needing review."""
    return fixtures_dir / "needs_review.xcstrings"


@pytest.fixture
def invalid_catalog(fixtures_dir: Path) -> Path:
    """Path to invalid catalog."""
    return fixtures_dir / "invalid.xcstrings"
