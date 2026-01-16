"""Core functionality for parsing and analyzing XCStrings catalogs."""

from xcstrings_tool.core.analyzer import Analyzer
from xcstrings_tool.core.models import AnalysisResult, StringCatalog, StringEntry
from xcstrings_tool.core.parser import Parser

__all__ = ["Analyzer", "AnalysisResult", "Parser", "StringCatalog", "StringEntry"]
