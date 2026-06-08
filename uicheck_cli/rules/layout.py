"""
Layout rules for UICheck-CLI.

Detects layout-related visual quality issues:
- Fixed width layouts without max-width
- Missing viewport meta tag
- Absolute positioning for layout
- Missing responsive breakpoints
- Unhandled overflow
- Float-based layouts
"""

import re
from typing import List
from .base import Rule, RuleResult, RuleSeverity, RuleCategory, rule_registry


class LayoutRule001(Rule):
    """Detect fixed width layouts without max-width."""

    rule_id = "layout-001"
    rule_name = "Fixed Width Without max-width"
    category = RuleCategory.LAYOUT
    severity = RuleSeverity.ERROR
    description = "Detects width set to fixed pixel values without max-width, causing layout issues on small screens."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        # Find width: Npx without max-width in same block
        blocks = re.finditer(r"([^{}]+)\{([^{}]+)\}", content)
        for block in blocks:
            selector = block.group(1).strip()
            body = block.group(2)
            # Check for fixed width in px
            width_match = re.search(r"width\s*:\s*(\d+)px", body, re.IGNORECASE)
            if width_match:
                # Check if max-width is also set
                has_max_width = bool(re.search(r"max-width\s*:", body, re.IGNORECASE))
                if not has_max_width:
                    line_num = content[:block.start()].count("\n") + 1
                    width_val = width_match.group(1)
                    results.append(self._make_result(
                        message=f"'{selector}' has fixed width ({width_val}px) without max-width. "
                                f"This will break on smaller screens.",
                        line=line_num,
                        fix_suggestion=f"Replace width: {width_val}px with:\n"
                                       f"  max-width: {width_val}px;\n"
                                       f"  width: 100%;",
                        file_path=file_path,
                    ))
        return results


class LayoutRule002(Rule):
    """Detect missing viewport meta tag."""

    rule_id = "layout-002"
    rule_name = "Missing Viewport Meta Tag"
    category = RuleCategory.LAYOUT
    severity = RuleSeverity.ERROR
    description = "Detects HTML files without the viewport meta tag, essential for responsive design."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        # Only check HTML-like files
        if "<html" not in content.lower() and "<!doctype" not in content.lower():
            return results

        has_viewport = bool(
            re.search(r'<meta\s+[^>]*name\s*=\s*["\']viewport["\']', content, re.IGNORECASE)
        )
        if not has_viewport:
            # Find the <head> tag line
            head_match = re.search(r"<head", content, re.IGNORECASE)
            line_num = content[:head_match.start()].count("\n") + 1 if head_match else 1
            results.append(self._make_result(
                message="Missing viewport meta tag. Required for responsive design on mobile devices.",
                line=line_num,
                fix_suggestion='Add inside <head>:\n'
                               '  <meta name="viewport" content="width=device-width, initial-scale=1.0">',
                file_path=file_path,
            ))
        return results


class LayoutRule003(Rule):
    """Detect absolute positioning used for main layout."""

    rule_id = "layout-003"
    rule_name = "Absolute Positioning for Layout"
    category = RuleCategory.LAYOUT
    severity = RuleSeverity.WARNING
    description = "Detects use of position: absolute for layout purposes instead of flexbox/grid."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        pattern = r"position\s*:\s*absolute"
        matches = list(re.finditer(pattern, content, re.IGNORECASE))

        for match in matches:
            line_num = content[:match.start()].count("\n") + 1
            line_content = content.split("\n")[line_num - 1].strip()
            # Check context - if it's in a container with relative, it might be OK
            block_start = content.rfind("{", 0, match.start())
            block_body = content[block_start:match.start()] if block_start > 0 else ""
            has_relative_parent = bool(re.search(r"position\s*:\s*relative", block_body, re.IGNORECASE))

            if not has_relative_parent:
                results.append(self._make_result(
                    message="position: absolute used without a relative parent. "
                            "Consider using flexbox or CSS grid for layout.",
                    line=line_num,
                    snippet=line_content,
                    fix_suggestion="Use flexbox or grid instead:\n"
                                   "  display: flex;\n"
                                   "  justify-content: space-between;\n"
                                   "  align-items: center;",
                    file_path=file_path,
                ))
        return results


class LayoutRule004(Rule):
    """Detect missing responsive breakpoints (media queries)."""

    rule_id = "layout-004"
    rule_name = "Missing Responsive Breakpoints"
    category = RuleCategory.LAYOUT
    severity = RuleSeverity.WARNING
    description = "Detects CSS files without any media queries for responsive design."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        has_media_queries = bool(re.search(r"@media", content, re.IGNORECASE))

        # Only flag if there's substantial CSS (more than 10 rules)
        rule_count = len(re.findall(r"\{", content))
        if not has_media_queries and rule_count > 10:
            results.append(self._make_result(
                message=f"No responsive breakpoints found ({rule_count} CSS rules). "
                        f"Add media queries for different screen sizes.",
                fix_suggestion="Add responsive breakpoints:\n"
                               "/* Tablet */\n"
                               "@media (max-width: 768px) {\n"
                               "  .container { padding: 0 1rem; }\n"
                               "}\n\n"
                               "/* Mobile */\n"
                               "@media (max-width: 480px) {\n"
                               "  .container { padding: 0 0.5rem; }\n"
                               "}",
                file_path=file_path,
            ))
        return results


class LayoutRule005(Rule):
    """Detect unhandled overflow."""

    rule_id = "layout-005"
    rule_name = "Unhandled Overflow"
    category = RuleCategory.LAYOUT
    severity = RuleSeverity.WARNING
    description = "Detects containers that may have overflow issues (long text, images, etc.)."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        # Check for common overflow-prone patterns
        # 1. Fixed height containers without overflow handling
        pattern = r"([^{}]+)\{([^{}]*height\s*:\s*[^a][^}]*?)\}"
        matches = list(re.finditer(pattern, content, re.IGNORECASE))

        for match in matches:
            selector = match.group(1).strip()
            body = match.group(2)
            has_overflow = bool(re.search(r"overflow\s*:", body, re.IGNORECASE))
            if not has_overflow:
                height_match = re.search(r"height\s*:\s*([^;]+)", body, re.IGNORECASE)
                if height_match:
                    line_num = content[:match.start()].count("\n") + 1
                    results.append(self._make_result(
                        message=f"'{selector}' has fixed height but no overflow handling. "
                                f"Content may overflow the container.",
                        line=line_num,
                        fix_suggestion="Add overflow handling:\n"
                                       "  overflow: auto;  /* or overflow: hidden; */",
                        file_path=file_path,
                    ))
        return results


class LayoutRule006(Rule):
    """Detect float-based layouts."""

    rule_id = "layout-006"
    rule_name = "Float-Based Layout"
    category = RuleCategory.LAYOUT
    severity = RuleSeverity.WARNING
    description = "Detects use of float for layout purposes instead of modern flexbox/grid."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        pattern = r"float\s*:\s*(left|right)"
        matches = list(re.finditer(pattern, content, re.IGNORECASE))

        for match in matches:
            line_num = content[:match.start()].count("\n") + 1
            line_content = content.split("\n")[line_num - 1].strip()
            results.append(self._make_result(
                message=f"float: {match.group(1)} detected. Consider using flexbox or grid for layout.",
                line=line_num,
                snippet=line_content,
                fix_suggestion="Replace float with flexbox:\n"
                               "  display: flex;\n"
                               "  justify-content: space-between;\n"
                               "  /* or use justify-content: flex-end for float:right */",
                file_path=file_path,
            ))
        return results


class LayoutRules:
    """Container class that registers all layout rules."""

    @staticmethod
    def register_all():
        """Register all layout rules with the global registry."""
        rules = [
            LayoutRule001(),
            LayoutRule002(),
            LayoutRule003(),
            LayoutRule004(),
            LayoutRule005(),
            LayoutRule006(),
        ]
        for rule in rules:
            rule_registry.register(rule)
        return rules
