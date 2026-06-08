"""
Auto-fix suggestion generator for UICheck-CLI.

Enhances rule results with concrete fix suggestions,
including code patches when possible.
"""

import re
from typing import List, Optional, Dict
from dataclasses import dataclass

from .rules.base import RuleResult, RuleCategory, RuleSeverity


@dataclass
class FixPatch:
    """A suggested code fix patch.

    Attributes:
        file_path: Path to the file.
        line: Line number to apply the fix.
        original: Original code snippet.
        replacement: Replacement code.
        description: Human-readable description of the fix.
    """

    file_path: str
    line: int
    original: str
    replacement: str
    description: str

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "file_path": self.file_path,
            "line": self.line,
            "original": self.original,
            "replacement": self.replacement,
            "description": self.description,
        }


class Fixer:
    """Generates auto-fix suggestions for rule violations.

    Usage:
        fixer = Fixer()
        patches = fixer.generate_patches(report.results)
        for patch in patches:
            print(f"Line {patch.line}: {patch.description}")
    """

    def __init__(self):
        """Initialize the fixer."""
        self._fix_generators: Dict[str, callable] = {
            "typography-005": self._fix_px_to_rem,
            "layout-001": self._fix_fixed_width,
            "accessibility-001": self._fix_missing_alt,
            "accessibility-002": self._fix_missing_label,
            "performance-005": self._fix_important,
        }

    def generate_patches(self, results: List[RuleResult]) -> List[FixPatch]:
        """Generate fix patches from rule results.

        Args:
            results: List of RuleResult objects.

        Returns:
            List of FixPatch objects with concrete fixes.
        """
        patches = []
        for result in results:
            generator = self._fix_generators.get(result.rule_id)
            if generator:
                patch = generator(result)
                if patch:
                    patches.append(patch)

        return patches

    def generate_fix_summary(self, results: List[RuleResult]) -> str:
        """Generate a human-readable summary of fix suggestions.

        Args:
            results: List of RuleResult objects.

        Returns:
            Formatted string with fix suggestions grouped by category.
        """
        if not results:
            return "No issues to fix."

        lines = ["Auto-fix Suggestions:", ""]

        # Group by category
        by_category: Dict[str, List[RuleResult]] = {}
        for result in results:
            cat = result.category.value
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(result)

        for category, cat_results in sorted(by_category.items()):
            lines.append(f"  [{category.upper()}]")
            for result in cat_results:
                if result.fix_suggestion:
                    lines.append(f"    - {result.rule_id}: {result.message}")
                    fix_lines = result.fix_suggestion.split("\n")
                    for fl in fix_lines:
                        lines.append(f"      {fl}")
                    lines.append("")

        return "\n".join(lines)

    def _fix_px_to_rem(self, result: RuleResult) -> Optional[FixPatch]:
        """Generate fix for px to rem conversion."""
        if not result.snippet:
            return None

        # Extract px value from snippet
        match = re.search(r"(\d+(?:\.\d+)?)px", result.snippet)
        if match:
            px_val = float(match.group(1))
            rem_val = px_val / 16.0
            return FixPatch(
                file_path=result.file_path,
                line=result.line,
                original=match.group(0),
                replacement=f"{rem_val:.3f}rem".rstrip("0").rstrip("."),
                description=f"Convert {px_val}px to {rem_val:.2f}rem",
            )
        return None

    def _fix_fixed_width(self, result: RuleResult) -> Optional[FixPatch]:
        """Generate fix for fixed width without max-width."""
        if not result.snippet:
            return None

        match = re.search(r"width\s*:\s*(\d+)px", result.snippet, re.IGNORECASE)
        if match:
            return FixPatch(
                file_path=result.file_path,
                line=result.line,
                original=f"width: {match.group(1)}px",
                replacement=f"max-width: {match.group(1)}px;\n  width: 100%;",
                description="Add max-width and make width responsive",
            )
        return None

    def _fix_missing_alt(self, result: RuleResult) -> Optional[FixPatch]:
        """Generate fix for missing alt attribute."""
        if not result.snippet:
            return None

        match = re.search(r"(<img\s+)([^>]*?)(\s*/?>)", result.snippet, re.IGNORECASE)
        if match:
            attrs = match.group(2)
            if "alt" not in attrs.lower():
                return FixPatch(
                    file_path=result.file_path,
                    line=result.line,
                    original=result.snippet[:60],
                    replacement=f'{match.group(1)}{attrs} alt=""{match.group(3)}',
                    description="Add empty alt attribute (fill with description)",
                )
        return None

    def _fix_missing_label(self, result: RuleResult) -> Optional[FixPatch]:
        """Generate fix for missing form label."""
        if not result.snippet:
            return None

        match = re.search(r"<(input|textarea|select)\s+([^>]*?)(?:/>|>)", result.snippet, re.IGNORECASE)
        if match:
            tag = match.group(1)
            attrs = match.group(2)
            # Try to extract name or id
            name_match = re.search(r'(?:name|id)\s*=\s*["\']([^"\']+)["\']', attrs, re.IGNORECASE)
            label_text = name_match.group(1).replace("-", " ").replace("_", " ").title() if name_match else "Label"
            return FixPatch(
                file_path=result.file_path,
                line=result.line,
                original=result.snippet[:60],
                replacement=f'<label for="{label_text.lower()}">{label_text}</label>\n  <{tag} {attrs}>',
                description=f"Add label element for {tag}",
            )
        return None

    def _fix_important(self, result: RuleResult) -> Optional[FixPatch]:
        """Generate fix for !important removal."""
        if not result.snippet:
            return None

        match = re.search(r"!\s*important", result.snippet, re.IGNORECASE)
        if match:
            return FixPatch(
                file_path=result.file_path,
                line=result.line,
                original="!important",
                replacement="/* Remove !important by increasing specificity */",
                description="Remove !important and use more specific selector",
            )
        return None
