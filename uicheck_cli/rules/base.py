"""
Base rule classes and registry for UICheck-CLI.

Defines the abstract base for all detection rules, the result data class,
severity levels, and the global rule registry.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Type
import re


class RuleSeverity(Enum):
    """Severity levels for rule violations."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class RuleCategory(Enum):
    """Categories of visual quality rules."""

    COLOR = "color"
    TYPOGRAPHY = "typography"
    SPACING = "spacing"
    LAYOUT = "layout"
    ACCESSIBILITY = "accessibility"
    PERFORMANCE = "performance"
    ANTIPATTERN = "antipattern"


@dataclass
class RuleResult:
    """Result of a single rule check.

    Attributes:
        rule_id: Unique identifier for the rule.
        rule_name: Human-readable rule name.
        category: Which category this rule belongs to.
        severity: How severe the violation is.
        message: Description of the issue found.
        line: Line number where the issue was found (0 if unknown).
        column: Column number (0 if unknown).
        snippet: Code snippet showing the issue.
        fix_suggestion: Suggested fix code or description.
        file_path: Path of the file where the issue was found.
    """

    rule_id: str
    rule_name: str
    category: RuleCategory
    severity: RuleSeverity
    message: str
    line: int = 0
    column: int = 0
    snippet: str = ""
    fix_suggestion: str = ""
    file_path: str = ""

    def to_dict(self) -> dict:
        """Serialize the result to a dictionary."""
        return {
            "rule_id": self.rule_id,
            "rule_name": self.rule_name,
            "category": self.category.value,
            "severity": self.severity.value,
            "message": self.message,
            "line": self.line,
            "column": self.column,
            "snippet": self.snippet,
            "fix_suggestion": self.fix_suggestion,
            "file_path": self.file_path,
        }


class Rule:
    """Abstract base class for all detection rules.

    Subclasses must implement:
        - rule_id: Unique string identifier
        - rule_name: Human-readable name
        - category: RuleCategory enum value
        - severity: Default RuleSeverity
        - description: What this rule checks
        - check(content, file_path) -> List[RuleResult]
    """

    rule_id: str = ""
    rule_name: str = ""
    category: RuleCategory = RuleCategory.COLOR
    severity: RuleSeverity = RuleSeverity.WARNING
    description: str = ""

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        """Run the rule check against file content.

        Args:
            content: The file content to analyze.
            file_path: Path of the file being checked.

        Returns:
            List of RuleResult objects for any issues found.
        """
        raise NotImplementedError("Subclasses must implement check()")

    def _make_result(
        self,
        message: str,
        line: int = 0,
        column: int = 0,
        snippet: str = "",
        fix_suggestion: str = "",
        file_path: str = "",
    ) -> RuleResult:
        """Helper to create a RuleResult for this rule."""
        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            category=self.category,
            severity=self.severity,
            message=message,
            line=line,
            column=column,
            snippet=snippet,
            fix_suggestion=fix_suggestion,
            file_path=file_path,
        )

    def info(self) -> dict:
        """Return rule metadata as a dictionary."""
        return {
            "rule_id": self.rule_id,
            "rule_name": self.rule_name,
            "category": self.category.value,
            "severity": self.severity.value,
            "description": self.description,
        }


class RuleRegistry:
    """Global registry for all detection rules.

    Manages registration, lookup, and listing of rules.
    """

    def __init__(self):
        self._rules: Dict[str, Rule] = {}
        self._categories: Dict[RuleCategory, List[str]] = {}

    def register(self, rule: Rule) -> None:
        """Register a rule instance.

        Args:
            rule: A Rule subclass instance.
        """
        self._rules[rule.rule_id] = rule
        if rule.category not in self._categories:
            self._categories[rule.category] = []
        if rule.rule_id not in self._categories[rule.category]:
            self._categories[rule.category].append(rule.rule_id)

    def get(self, rule_id: str) -> Optional[Rule]:
        """Get a rule by its ID.

        Args:
            rule_id: The unique rule identifier.

        Returns:
            The Rule instance, or None if not found.
        """
        return self._rules.get(rule_id)

    def get_by_category(self, category: RuleCategory) -> List[Rule]:
        """Get all rules in a specific category.

        Args:
            category: The RuleCategory to filter by.

        Returns:
            List of Rule instances in that category.
        """
        rule_ids = self._categories.get(category, [])
        return [self._rules[rid] for rid in rule_ids if rid in self._rules]

    def get_all(self) -> List[Rule]:
        """Get all registered rules.

        Returns:
            List of all Rule instances.
        """
        return list(self._rules.values())

    def get_categories(self) -> Dict[str, List[str]]:
        """Get all categories and their rule IDs.

        Returns:
            Dictionary mapping category names to lists of rule IDs.
        """
        return {cat.value: ids for cat, ids in self._categories.items()}

    def count(self) -> int:
        """Get the total number of registered rules."""
        return len(self._rules)

    def filter_by_names(self, names: List[str]) -> List[Rule]:
        """Filter rules by category names (case-insensitive).

        Args:
            names: List of category name strings to include.

        Returns:
            List of Rule instances matching the given categories.
        """
        rules = []
        name_set = {n.lower() for n in names}
        for cat, rule_ids in self._categories.items():
            if cat.value.lower() in name_set:
                for rid in rule_ids:
                    if rid in self._rules:
                        rules.append(self._rules[rid])
        return rules


# Global singleton registry
rule_registry = RuleRegistry()
