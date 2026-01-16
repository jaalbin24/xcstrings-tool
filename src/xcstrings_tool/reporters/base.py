"""Base reporter interface."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from xcstrings_tool.core.models import AnalysisResult


class Reporter(ABC):
    """Abstract base class for reporters."""

    @abstractmethod
    def generate(
        self, result: AnalysisResult, output_path: Optional[Path] = None
    ) -> str:
        """Generate report from analysis result.

        Args:
            result: Analysis result to report
            output_path: Optional path to save output file

        Returns:
            Report content as string
        """
        pass
