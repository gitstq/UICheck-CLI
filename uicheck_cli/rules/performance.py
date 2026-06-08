"""
Performance rules for UICheck-CLI.

Detects performance-related visual quality issues:
- Too many inline styles
- Duplicate CSS selectors
- Uncompressed CSS (extra whitespace)
- Deep DOM nesting (>10 levels)
- Use of !important
"""

import re
from typing import List
from .base import Rule, RuleResult, RuleSeverity, RuleCategory, rule_registry
from ..utils import extract_inline_styles, extract_selectors, count_dom_depth


class PerformanceRule001(Rule):
    """Detect excessive inline styles."""

    rule_id = "performance-001"
    rule_name = "Excessive Inline Styles"
    category = RuleCategory.PERFORMANCE
    severity = RuleSeverity.WARNING
    description = "Detects too many inline style attributes, which reduce maintainability and performance."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        inline_styles = extract_inline_styles(content)

        if len(inline_styles) > 5:
            results.append(self._make_result(
                message=f"Found {len(inline_styles)} inline style attributes. "
                        f"Move repeated styles to CSS classes for better maintainability.",
                fix_suggestion="Extract inline styles to CSS classes:\n"
                               "  /* Instead of: */\n"
                               "  <div style=\"color: red; padding: 16px;\">\n\n"
                               "  /* Use: */\n"
                               "  .highlight-box {\n"
                               "    color: red;\n"
                               "    padding: 16px;\n"
                               "  }\n"
                               "  <div class=\"highlight-box\">",
                file_path=file_path,
            ))
        return results


class PerformanceRule002(Rule):
    """Detect duplicate CSS selectors."""

    rule_id = "performance-002"
    rule_name = "Duplicate CSS Selectors"
    category = RuleCategory.PERFORMANCE
    severity = RuleSeverity.WARNING
    description = "Detects CSS selectors that appear more than once, indicating potential redundancy."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        selectors = extract_selectors(content)

        # Count occurrences
        selector_counts = {}
        for sel in selectors:
            normalized = sel.strip()
            if normalized:
                selector_counts[normalized] = selector_counts.get(normalized, 0) + 1

        duplicates = {sel: count for sel, count in selector_counts.items() if count > 1}
        if duplicates:
            dup_list = ", ".join(f"'{s}' ({c}x)" for s, c in list(duplicates.items())[:5])
            results.append(self._make_result(
                message=f"Found {len(duplicates)} duplicate CSS selector(s): {dup_list}. "
                        f"Consolidate to reduce file size and avoid specificity conflicts.",
                fix_suggestion="Merge duplicate selectors:\n"
                               "  /* Instead of: */\n"
                               "  .card { color: blue; }\n"
                               "  .card { padding: 16px; }\n\n"
                               "  /* Use: */\n"
                               "  .card {\n"
                               "    color: blue;\n"
                               "    padding: 16px;\n"
                               "  }",
                file_path=file_path,
            ))
        return results


class PerformanceRule003(Rule):
    """Detect uncompressed CSS (excessive whitespace)."""

    rule_id = "performance-003"
    rule_name = "Uncompressed CSS"
    category = RuleCategory.PERFORMANCE
    severity = RuleSeverity.INFO
    description = "Detects CSS with excessive whitespace, newlines, and comments that could be minified."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        # Count whitespace
        whitespace_lines = sum(1 for line in content.split("\n") if not line.strip())
        total_lines = len(content.split("\n"))
        css_comments = len(re.findall(r"/\*.*?\*/", content, re.DOTALL))

        if total_lines > 0:
            whitespace_ratio = whitespace_lines / total_lines
            if whitespace_ratio > 0.3 and total_lines > 20:
                results.append(self._make_result(
                    message=f"CSS has {whitespace_ratio:.0%} empty lines ({whitespace_lines}/{total_lines}) "
                            f"and {css_comments} comments. Consider minifying for production.",
                    fix_suggestion="Use a CSS minifier for production:\n"
                                   "  /* Development: readable CSS with comments */\n"
                                   "  /* Production: minified CSS */\n"
                                   "  Tools: cssnano, clean-css, or online minifiers",
                    file_path=file_path,
                ))
        return results


class PerformanceRule004(Rule):
    """Detect deep DOM nesting (>10 levels)."""

    rule_id = "performance-004"
    rule_name = "Deep DOM Nesting"
    category = RuleCategory.PERFORMANCE
    severity = RuleSeverity.WARNING
    description = "Detects DOM nesting deeper than 10 levels, which hurts performance and readability."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        max_depth = count_dom_depth(content)

        if max_depth > 10:
            results.append(self._make_result(
                message=f"DOM nesting depth is {max_depth} levels (max recommended: 10). "
                        f"Deep nesting hurts rendering performance and code readability.",
                fix_suggestion="Flatten the DOM structure:\n"
                               "  1. Use CSS Grid/Flexbox instead of nested divs\n"
                               "  2. Break components into smaller pieces\n"
                               "  3. Remove unnecessary wrapper elements",
                file_path=file_path,
            ))
        return results


class PerformanceRule005(Rule):
    """Detect use of !important."""

    rule_id = "performance-005"
    rule_name = "Use of !important"
    category = RuleCategory.PERFORMANCE
    severity = RuleSeverity.WARNING
    description = "Detects use of !important in CSS, which makes maintenance difficult."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        pattern = r"!\s*important"
        matches = list(re.finditer(pattern, content, re.IGNORECASE))

        if len(matches) > 3:
            examples = []
            for match in matches[:5]:
                line_num = content[:match.start()].count("\n") + 1
                line_content = content.split("\n")[line_num - 1].strip()
                examples.append(f"L{line_num}: {line_content[:50]}")

            results.append(self._make_result(
                message=f"Found {len(matches)} uses of !important. "
                        f"Excessive use indicates specificity management issues.",
                snippet="; ".join(examples),
                fix_suggestion="Avoid !important by:\n"
                               "  1. Using more specific selectors\n"
                               "  2. Organizing CSS with BEM or similar methodology\n"
                               "  3. Using CSS custom properties for overrides",
                file_path=file_path,
            ))
        elif len(matches) > 0:
            for match in matches:
                line_num = content[:match.start()].count("\n") + 1
                line_content = content.split("\n")[line_num - 1].strip()
                results.append(self._make_result(
                    message=f"!important found at line {line_num}. "
                            f"Consider refactoring selector specificity instead.",
                    line=line_num,
                    snippet=line_content[:60],
                    severity=RuleSeverity.INFO,
                    fix_suggestion="Refactor to avoid !important:\n"
                                   "  /* Instead of: */\n"
                                   "  .button { color: blue !important; }\n\n"
                                   "  /* Use more specific selector: */\n"
                                   "  .container .button { color: blue; }",
                    file_path=file_path,
                ))
        return results


class PerformanceRule006(Rule):
    """Detect universal selector (*) usage."""

    rule_id = "performance-006"
    rule_name = "Universal Selector Usage"
    category = RuleCategory.PERFORMANCE
    severity = RuleSeverity.INFO
    description = "Detects use of the universal selector (*) which can impact performance."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        pattern = r"(^|[^.\w#])\*\s*\{"
        matches = list(re.finditer(pattern, content, re.MULTILINE))

        for match in matches:
            line_num = content[:match.start()].count("\n") + 1
            line_content = content.split("\n")[line_num - 1].strip()
            results.append(self._make_result(
                message=f"Universal selector (*) found. It matches every element and can slow rendering.",
                line=line_num,
                snippet=line_content[:60],
                fix_suggestion="Replace * with specific selectors:\n"
                               "  /* Instead of: * { box-sizing: border-box; } */\n"
                               "  /* This is acceptable for box-sizing reset, but avoid for other properties */",
                file_path=file_path,
            ))
        return results


class PerformanceRules:
    """Container class that registers all performance rules."""

    @staticmethod
    def register_all():
        """Register all performance rules with the global registry."""
        rules = [
            PerformanceRule001(),
            PerformanceRule002(),
            PerformanceRule003(),
            PerformanceRule004(),
            PerformanceRule005(),
            PerformanceRule006(),
        ]
        for rule in rules:
            rule_registry.register(rule)
        return rules
