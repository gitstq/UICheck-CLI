"""
Typography rules for UICheck-CLI.

Detects typography-related visual quality issues:
- Too many font size levels
- Missing font fallback stacks
- Missing or too-small line-height
- Heading level skipping
- Using px instead of rem/em
- Too many font weights
"""

import re
from typing import List
from .base import Rule, RuleResult, RuleSeverity, RuleCategory, rule_registry
from ..utils import extract_css_values, extract_font_sizes


class TypographyRule001(Rule):
    """Detect too many font size levels (>6 unique sizes)."""

    rule_id = "typography-001"
    rule_name = "Too Many Font Size Levels"
    category = RuleCategory.TYPOGRAPHY
    severity = RuleSeverity.WARNING
    description = "Detects more than 6 unique font-size values, suggesting inconsistent typography scale."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        sizes = extract_font_sizes(content)
        # Normalize sizes for comparison
        unique_sizes = set()
        for s in sizes:
            normalized = self._normalize_size(s)
            if normalized:
                unique_sizes.add(normalized)

        if len(unique_sizes) > 6:
            size_list = ", ".join(sorted(unique_sizes)[:8])
            line = self._find_font_size_line(content)
            results.append(self._make_result(
                message=f"Found {len(unique_sizes)} unique font sizes: {size_list}. "
                        f"A type scale should have at most 6 levels.",
                line=line,
                snippet=f"font-size values: {size_list}",
                fix_suggestion="Use a consistent type scale (e.g., 0.75rem, 0.875rem, 1rem, "
                               "1.25rem, 1.5rem, 2rem, 2.5rem, 3rem) and define them as tokens:\n"
                               ":root {\n"
                               "  --text-xs: 0.75rem;\n"
                               "  --text-sm: 0.875rem;\n"
                               "  --text-base: 1rem;\n"
                               "  --text-lg: 1.25rem;\n"
                               "  --text-xl: 1.5rem;\n"
                               "  --text-2xl: 2rem;\n"
                               "}",
                file_path=file_path,
            ))
        return results

    def _normalize_size(self, size: str) -> str:
        """Normalize font size to a comparable string."""
        size = size.strip().lower()
        # Remove !important
        size = re.sub(r"!important", "", size).strip()
        # Extract just the value part
        match = re.match(r"([\d.]+)(px|rem|em|pt|%|vh|vw)", size)
        if match:
            return f"{match.group(1)}{match.group(2)}"
        return size

    def _find_font_size_line(self, content: str) -> int:
        match = re.search(r"font-size\s*:", content, re.IGNORECASE)
        if match:
            return content[:match.start()].count("\n") + 1
        return 0


class TypographyRule002(Rule):
    """Detect missing font fallback stacks."""

    rule_id = "typography-002"
    rule_name = "Missing Font Fallback Stack"
    category = RuleCategory.TYPOGRAPHY
    severity = RuleSeverity.ERROR
    description = "Detects font-family declarations with only a single font and no fallback."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        # Find font-family declarations
        pattern = r"font-family\s*:\s*([^;}{]+)"
        matches = list(re.finditer(pattern, content, re.IGNORECASE))

        for match in matches:
            value = match.group(1).strip()
            line_num = content[:match.start()].count("\n") + 1
            # Count number of fonts (split by comma)
            fonts = [f.strip().strip("'\"") for f in value.split(",")]
            fonts = [f for f in fonts if f and not f.startswith("--")]

            if len(fonts) == 1:
                line_content = content.split("\n")[line_num - 1].strip()
                results.append(self._make_result(
                    message=f"Font '{fonts[0]}' has no fallback. "
                            f"Add generic family fallbacks (sans-serif, serif, monospace).",
                    line=line_num,
                    snippet=line_content,
                    fix_suggestion=f"font-family: '{fonts[0]}', -apple-system, BlinkMacSystemFont, "
                                   f"'Segoe UI', Roboto, sans-serif;",
                    file_path=file_path,
                ))
            elif len(fonts) >= 2:
                # Check if last font is a generic family
                last = fonts[-1].lower()
                generic_families = ("sans-serif", "serif", "monospace", "cursive", "fantasy", "system-ui")
                if last not in generic_families:
                    line_content = content.split("\n")[line_num - 1].strip()
                    results.append(self._make_result(
                        message=f"Font stack ends with '{last}', not a generic family. "
                                f"Add a generic fallback (sans-serif, serif, etc.).",
                        line=line_num,
                        snippet=line_content,
                        fix_suggestion=f"Append a generic family: ..., {last}, sans-serif;",
                        file_path=file_path,
                    ))
        return results


class TypographyRule003(Rule):
    """Detect missing or too-small line-height."""

    rule_id = "typography-003"
    rule_name = "Missing or Small Line-Height"
    category = RuleCategory.TYPOGRAPHY
    severity = RuleSeverity.WARNING
    description = "Detects text elements without line-height or with line-height less than 1.4."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        # Check for line-height values
        pattern = r"line-height\s*:\s*([\d.]+)"
        matches = list(re.finditer(pattern, content, re.IGNORECASE))

        for match in matches:
            value = float(match.group(1))
            line_num = content[:match.start()].count("\n") + 1
            if value < 1.4:
                line_content = content.split("\n")[line_num - 1].strip()
                results.append(self._make_result(
                    message=f"Line-height {value} is too small. "
                            f"Recommended minimum is 1.4 for body text, 1.2 for headings.",
                    line=line_num,
                    snippet=line_content,
                    fix_suggestion="line-height: 1.5;  /* or 1.6 for body text */",
                    file_path=file_path,
                ))

        # Check if there are font-size declarations but no line-height at all
        has_font_size = bool(re.search(r"font-size\s*:", content, re.IGNORECASE))
        has_line_height = bool(re.search(r"line-height\s*:", content, re.IGNORECASE))
        if has_font_size and not has_line_height:
            line = self._find_font_size_line(content)
            results.append(self._make_result(
                message="Font sizes are set but no line-height is defined anywhere. "
                        "Add line-height for better readability.",
                line=line,
                fix_suggestion="body {\n  line-height: 1.5;\n}\n\nh1, h2, h3 {\n  line-height: 1.2;\n}",
                file_path=file_path,
            ))
        return results

    def _find_font_size_line(self, content: str) -> int:
        match = re.search(r"font-size\s*:", content, re.IGNORECASE)
        if match:
            return content[:match.start()].count("\n") + 1
        return 0


class TypographyRule004(Rule):
    """Detect heading level skipping (e.g., h1 directly to h3)."""

    rule_id = "typography-004"
    rule_name = "Heading Level Skipping"
    category = RuleCategory.TYPOGRAPHY
    severity = RuleSeverity.WARNING
    description = "Detects improper heading hierarchy where levels are skipped (e.g., h1 -> h3)."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        # Find all heading tags
        headings = re.finditer(r"<(h[1-6])[\s>]", content, re.IGNORECASE)
        prev_level = 0
        for match in headings:
            tag = match.group(1).lower()
            level = int(tag[1])
            line_num = content[:match.start()].count("\n") + 1

            if prev_level > 0 and level > prev_level + 1:
                line_content = content.split("\n")[line_num - 1].strip()
                results.append(self._make_result(
                    message=f"Heading level skip: h{prev_level} -> {tag}. "
                            f"Headings should not skip levels for accessibility.",
                    line=line_num,
                    snippet=line_content,
                    fix_suggestion=f"Change <{tag}> to <h{prev_level + 1}> to maintain proper hierarchy.",
                    file_path=file_path,
                ))
            prev_level = level
        return results


class TypographyRule005(Rule):
    """Detect using px instead of rem/em for font sizes."""

    rule_id = "typography-005"
    rule_name = "Using px Instead of rem/em"
    category = RuleCategory.TYPOGRAPHY
    severity = RuleSeverity.INFO
    description = "Detects font-size values using px units instead of rem/em, which are better for accessibility."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        pattern = r"font-size\s*:\s*([\d.]+)\s*px"
        matches = list(re.finditer(pattern, content, re.IGNORECASE))

        px_count = len(matches)
        if px_count > 0:
            examples = []
            for match in matches[:3]:
                px_val = match.group(1)
                line_num = content[:match.start()].count("\n") + 1
                rem_val = float(px_val) / 16.0
                examples.append(f"L{line_num}: {px_val}px -> {rem_val:.2f}rem")

            line_num = content[:matches[0].start()].count("\n") + 1
            results.append(self._make_result(
                message=f"Found {px_count} font-size value(s) using px. "
                        f"Use rem/em for better accessibility and scalability.",
                line=line_num,
                snippet="; ".join(examples),
                fix_suggestion="Convert px to rem (1rem = 16px):\n"
                               "  font-size: 16px;  ->  font-size: 1rem;\n"
                               "  font-size: 24px;  ->  font-size: 1.5rem;\n"
                               "  font-size: 14px;  ->  font-size: 0.875rem;",
                file_path=file_path,
            ))
        return results


class TypographyRule006(Rule):
    """Detect too many font-weight values."""

    rule_id = "typography-006"
    rule_name = "Too Many Font Weights"
    category = RuleCategory.TYPOGRAPHY
    severity = RuleSeverity.WARNING
    description = "Detects more than 4 unique font-weight values, suggesting inconsistent typography."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        pattern = r"font-weight\s*:\s*([\w]+)"
        matches = re.findall(pattern, content, re.IGNORECASE)

        unique_weights = set(w.lower() for w in matches)
        if len(unique_weights) > 4:
            weight_list = ", ".join(sorted(unique_weights))
            line = self._find_font_weight_line(content)
            results.append(self._make_result(
                message=f"Found {len(unique_weights)} unique font weights: {weight_list}. "
                        f"Limit to 3-4 weights for consistency.",
                line=line,
                fix_suggestion="Stick to a consistent weight scale:\n"
                               "  --font-normal: 400;\n"
                               "  --font-medium: 500;\n"
                               "  --font-semibold: 600;\n"
                               "  --font-bold: 700;",
                file_path=file_path,
            ))
        return results

    def _find_font_weight_line(self, content: str) -> int:
        match = re.search(r"font-weight\s*:", content, re.IGNORECASE)
        if match:
            return content[:match.start()].count("\n") + 1
        return 0


class TypographyRules:
    """Container class that registers all typography rules."""

    @staticmethod
    def register_all():
        """Register all typography rules with the global registry."""
        rules = [
            TypographyRule001(),
            TypographyRule002(),
            TypographyRule003(),
            TypographyRule004(),
            TypographyRule005(),
            TypographyRule006(),
        ]
        for rule in rules:
            rule_registry.register(rule)
        return rules
