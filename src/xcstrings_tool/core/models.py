"""Data models for XCStrings catalog structure."""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class LocalizationState(str, Enum):
    """Translation state for a specific language."""

    NEW = "new"
    TRANSLATED = "translated"
    NEEDS_REVIEW = "needs_review"
    STALE = "stale"


class ExtractionState(str, Enum):
    """How the string was added to the catalog."""

    AUTOMATIC = "extracted_with_value"
    MANUAL = "manual"
    MIGRATED = "migrated"
    STALE = "stale"


class StringUnit(BaseModel):
    """A single translation unit."""

    state: LocalizationState
    value: str


class Localization(BaseModel):
    """Translation data for a specific language."""

    model_config = ConfigDict(populate_by_name=True)

    string_unit: StringUnit = Field(alias="stringUnit")


class StringEntry(BaseModel):
    """A single string in the catalog."""

    model_config = ConfigDict(populate_by_name=True)

    key: str
    extraction_state: Optional[ExtractionState] = Field(None, alias="extractionState")
    localizations: Dict[str, Localization] = Field(default_factory=dict)
    comment: Optional[str] = None


class StringCatalog(BaseModel):
    """Root catalog structure."""

    model_config = ConfigDict(populate_by_name=True)

    source_language: str = Field(alias="sourceLanguage")
    version: str = "1.0"
    strings: Dict[str, Dict[str, Any]]


class AnalysisResult(BaseModel):
    """Result of analyzing a catalog."""

    total_strings: int
    source_language: str
    target_language: str

    # Counts
    translated: int
    missing_translation: int
    needs_review: int
    stale: int

    # Percentage
    completion_percentage: float

    # Details
    missing_entries: List[StringEntry]
    needs_review_entries: List[StringEntry]
    stale_entries: List[StringEntry]
