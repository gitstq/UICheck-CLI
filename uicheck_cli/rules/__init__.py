"""
Rule system for UICheck-CLI.

Base classes and registry for all detection rules.
"""

from .base import Rule, RuleResult, RuleSeverity, RuleCategory, rule_registry
from .color import ColorRules
from .typography import TypographyRules
from .spacing import SpacingRules
from .layout import LayoutRules
from .accessibility import AccessibilityRules
from .performance import PerformanceRules
from .antipattern import AntiPatternRules

__all__ = [
    "Rule", "RuleResult", "RuleSeverity", "RuleCategory", "rule_registry",
    "ColorRules", "TypographyRules", "SpacingRules", "LayoutRules",
    "AccessibilityRules", "PerformanceRules", "AntiPatternRules",
]
