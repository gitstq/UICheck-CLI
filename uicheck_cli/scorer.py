"""
Scoring system for UICheck-CLI.

Computes a 0-100 quality score based on rule violations,
with independent scoring per category and an overall score.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

from .rules.base import RuleResult, RuleCategory, RuleSeverity


# Severity weights for score calculation
SEVERITY_WEIGHTS = {
    RuleSeverity.ERROR: 10,
    RuleSeverity.WARNING: 5,
    RuleSeverity.INFO: 1,
}

# Maximum penalty per category before score reaches 0
MAX_PENALTY_PER_CATEGORY = 100


@dataclass
class CategoryScore:
    """Score for a single category.

    Attributes:
        category: The rule category.
        score: Score from 0 to 100.
        issues_count: Number of issues in this category.
        penalty: Total penalty points deducted.
        max_possible: Maximum possible penalty (for reference).
    """

    category: RuleCategory
    score: float = 100.0
    issues_count: int = 0
    penalty: float = 0.0
    max_possible: float = 0.0

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "category": self.category.value,
            "score": round(self.score, 1),
            "issues_count": self.issues_count,
            "penalty": round(self.penalty, 1),
        }


@dataclass
class OverallScore:
    """Overall quality score with per-category breakdown.

    Attributes:
        overall: Overall score from 0 to 100.
        grade: Letter grade (A-F).
        category_scores: Per-category score breakdown.
        total_issues: Total number of issues.
        summary: Human-readable summary string.
    """

    overall: float = 100.0
    grade: str = "A"
    category_scores: Dict[str, CategoryScore] = field(default_factory=dict)
    total_issues: int = 0
    summary: str = ""

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "overall": round(self.overall, 1),
            "grade": self.grade,
            "total_issues": self.total_issues,
            "categories": {
                name: cs.to_dict()
                for name, cs in self.category_scores.items()
            },
            "summary": self.summary,
        }


class Scorer:
    """Computes quality scores from analysis results.

    Usage:
        scorer = Scorer()
        score = scorer.compute(report.results)
        print(score.overall, score.grade)
    """

    def __init__(self):
        """Initialize the scorer with default weights."""
        self.severity_weights = dict(SEVERITY_WEIGHTS)
        self._category_weights = {
            RuleCategory.COLOR: 1.0,
            RuleCategory.TYPOGRAPHY: 1.2,
            RuleCategory.SPACING: 0.8,
            RuleCategory.LAYOUT: 1.2,
            RuleCategory.ACCESSIBILITY: 1.5,  # Higher weight for accessibility
            RuleCategory.PERFORMANCE: 1.0,
            RuleCategory.ANTIPATTERN: 0.8,
        }

    def compute(self, results: List[RuleResult]) -> OverallScore:
        """Compute the overall score from rule results.

        Args:
            results: List of RuleResult objects from analysis.

        Returns:
            OverallScore with per-category breakdown.
        """
        overall_score = OverallScore()
        overall_score.total_issues = len(results)

        if not results:
            overall_score.grade = "A+"
            overall_score.summary = "No issues found. The code looks great!"
            return overall_score

        # Group results by category
        category_results: Dict[RuleCategory, List[RuleResult]] = {}
        for result in results:
            if result.category not in category_results:
                category_results[result.category] = []
            category_results[result.category].append(result)

        # Score each category
        weighted_sum = 0.0
        weight_total = 0.0

        for category in RuleCategory:
            cat_results = category_results.get(category, [])
            cat_score = self._compute_category_score(category, cat_results)
            overall_score.category_scores[category.value] = cat_score

            weight = self._category_weights.get(category, 1.0)
            weighted_sum += cat_score.score * weight
            weight_total += weight

        # Compute weighted overall score
        if weight_total > 0:
            overall_score.overall = weighted_sum / weight_total
        else:
            overall_score.overall = 100.0

        # Clamp to 0-100
        overall_score.overall = max(0.0, min(100.0, overall_score.overall))

        # Determine grade
        overall_score.grade = self._compute_grade(overall_score.overall)

        # Generate summary
        overall_score.summary = self._generate_summary(overall_score)

        return overall_score

    def _compute_category_score(
        self, category: RuleCategory, results: List[RuleResult]
    ) -> CategoryScore:
        """Compute the score for a single category.

        Args:
            category: The rule category being scored.
            results: List of results in this category.

        Returns:
            CategoryScore object.
        """
        cat_score = CategoryScore(category=category, score=100.0)
        cat_score.issues_count = len(results)

        if not results:
            return cat_score

        # Calculate penalty
        penalty = 0.0
        for result in results:
            weight = self.severity_weights.get(result.severity, 1)
            penalty += weight

        cat_score.penalty = penalty
        cat_score.max_possible = MAX_PENALTY_PER_CATEGORY

        # Apply diminishing returns for high penalty counts
        # Using a logarithmic scale to prevent single categories from dominating
        if penalty > 0:
            # Score formula: 100 * e^(-penalty/50)
            import math
            cat_score.score = 100.0 * math.exp(-penalty / 50.0)
            cat_score.score = max(0.0, min(100.0, cat_score.score))

        return cat_score

    def _compute_grade(self, score: float) -> str:
        """Compute a letter grade from a numeric score.

        Args:
            score: Score from 0 to 100.

        Returns:
            Letter grade string (A+ through F).
        """
        if score >= 95:
            return "A+"
        elif score >= 90:
            return "A"
        elif score >= 85:
            return "A-"
        elif score >= 80:
            return "B+"
        elif score >= 75:
            return "B"
        elif score >= 70:
            return "B-"
        elif score >= 65:
            return "C+"
        elif score >= 60:
            return "C"
        elif score >= 55:
            return "C-"
        elif score >= 50:
            return "D"
        elif score >= 40:
            return "D-"
        else:
            return "F"

    def _generate_summary(self, score: OverallScore) -> str:
        """Generate a human-readable summary of the score.

        Args:
            score: The OverallScore object.

        Returns:
            Summary string.
        """
        if score.overall >= 90:
            return f"Excellent! Score: {score.overall:.1f}/100 (Grade {score.grade}). " \
                   f"Very few issues found."
        elif score.overall >= 75:
            return f"Good. Score: {score.overall:.1f}/100 (Grade {score.grade}). " \
                   f"Some improvements recommended."
        elif score.overall >= 60:
            return f"Fair. Score: {score.overall:.1f}/100 (Grade {score.grade}). " \
                   f"Several issues need attention."
        elif score.overall >= 40:
            return f"Needs work. Score: {score.overall:.1f}/100 (Grade {score.grade}). " \
                   f"Many quality issues detected."
        else:
            return f"Poor. Score: {score.overall:.1f}/100 (Grade {score.grade}). " \
                   f"Significant refactoring recommended."
