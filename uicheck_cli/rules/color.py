"""
Color rules for UICheck-CLI.

Detects color-related visual quality issues:
- Too many hardcoded colors
- Low contrast color combinations
- Missing dark mode support
- Pure black/white backgrounds
- Inconsistent brand colors
"""

import re
import math
from typing import List, Optional, Tuple
from .base import Rule, RuleResult, RuleSeverity, RuleCategory, rule_registry
from ..utils import parse_hex_color, color_distance, contrast_ratio, extract_all_colors


class ColorRule001(Rule):
    """Detect too many hardcoded color values (>5 unique colors)."""

    rule_id = "color-001"
    rule_name = "Too Many Hardcoded Colors"
    category = RuleCategory.COLOR
    severity = RuleSeverity.WARNING
    description = "Detects files with more than 5 unique hardcoded color values, suggesting a need for a design token system."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        colors = extract_all_colors(content)
        unique_colors = set(c.lower() for c in colors)

        if len(unique_colors) > 5:
            # Find line numbers for some colors
            color_lines = self._find_color_lines(content, list(unique_colors)[:3])
            snippet_lines = ", ".join(
                f"L{ln}: {c}" for c, ln in color_lines
            )
            results.append(self._make_result(
                message=f"Found {len(unique_colors)} unique hardcoded colors. "
                        f"Consider using CSS custom properties (design tokens).",
                line=color_lines[0][1] if color_lines else 0,
                snippet=snippet_lines,
                fix_suggestion="Define colors as CSS custom properties:\n"
                               ":root {\n"
                               "  --color-primary: #3b82f6;\n"
                               "  --color-secondary: #10b981;\n"
                               "  --color-background: #ffffff;\n"
                               "  --color-text: #1f2937;\n"
                               "}",
                file_path=file_path,
            ))
        return results

    def _find_color_lines(self, content: str, colors: list) -> list:
        """Find line numbers for given color values."""
        results = []
        lines = content.split("\n")
        for color in colors:
            for i, line in enumerate(lines, 1):
                if color in line.lower():
                    results.append((color, i))
                    break
        return results


class ColorRule002(Rule):
    """Detect low contrast color combinations (similar colors used together)."""

    rule_id = "color-002"
    rule_name = "Low Contrast Color Combinations"
    category = RuleCategory.COLOR
    severity = RuleSeverity.ERROR
    description = "Detects color pairs that are too similar, indicating potential contrast issues."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        colors = extract_all_colors(content)
        parsed = []
        for c in colors:
            rgb = parse_hex_color(c)
            if rgb:
                parsed.append((c, rgb))

        # Check pairs for low contrast
        low_contrast_pairs = []
        for i in range(len(parsed)):
            for j in range(i + 1, len(parsed)):
                c1_name, c1_rgb = parsed[i]
                c2_name, c2_rgb = parsed[j]
                ratio = contrast_ratio(c1_rgb, c2_rgb)
                if ratio < 1.5:
                    low_contrast_pairs.append((c1_name, c2_name, ratio))

        if low_contrast_pairs:
            pair_str = "; ".join(
                f"{a} vs {b} (ratio: {r:.2f}:1)" for a, b, r in low_contrast_pairs[:3]
            )
            results.append(self._make_result(
                message=f"Found {len(low_contrast_pairs)} low contrast color pair(s). "
                        f"Pairs: {pair_str}",
                fix_suggestion="Increase contrast between adjacent colors. "
                               "WCAG recommends at least 4.5:1 for normal text "
                               "and 3:1 for large text.",
                file_path=file_path,
            ))
        return results


class ColorRule003(Rule):
    """Detect missing dark mode support."""

    rule_id = "color-003"
    rule_name = "Missing Dark Mode Support"
    category = RuleCategory.COLOR
    severity = RuleSeverity.INFO
    description = "Detects CSS files without dark mode media queries or dark mode class selectors."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        has_dark_mode = bool(
            re.search(r"@media\s.*prefers-color-scheme\s*:\s*dark", content, re.IGNORECASE)
            or re.search(r"\.dark\s", content)
            or re.search(r"data-theme\s*=\s*['\"]dark['\"]", content)
            or re.search(r"\[data-theme.*dark", content)
            or re.search(r"class.*dark", content, re.IGNORECASE)
        )

        if not has_dark_mode and ("background" in content.lower() or "color:" in content.lower()):
            line = self._find_line_with(content, "background")
            results.append(self._make_result(
                message="No dark mode support detected. Consider adding "
                        "'prefers-color-scheme: dark' media query or dark mode class.",
                line=line,
                fix_suggestion="@media (prefers-color-scheme: dark) {\n"
                               "  :root {\n"
                               "    --color-background: #1a1a2e;\n"
                               "    --color-text: #e0e0e0;\n"
                               "  }\n"
                               "}",
                file_path=file_path,
            ))
        return results

    def _find_line_with(self, content: str, keyword: str) -> int:
        for i, line in enumerate(content.split("\n"), 1):
            if keyword in line.lower():
                return i
        return 0


class ColorRule004(Rule):
    """Detect pure black (#000) or pure white (#fff) used as background."""

    rule_id = "color-004"
    rule_name = "Pure Black/White Background"
    category = RuleCategory.COLOR
    severity = RuleSeverity.WARNING
    description = "Detects use of pure black (#000000) or pure white (#ffffff) as background colors, which can cause eye strain."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        # Find background-color or background with pure black/white
        pattern = r"(background-color|background)\s*:\s*(#[0fF]{3,6}|#[fF]{3,6}|rgb\s*\(\s*0\s*,\s*0\s*,\s*0\s*\)|rgb\s*\(\s*255\s*,\s*255\s*,\s*255\s*\)|white|black)\s*"
        matches = list(re.finditer(pattern, content, re.IGNORECASE))

        for match in matches:
            line_num = content[:match.start()].count("\n") + 1
            line_content = content.split("\n")[line_num - 1].strip()
            val = match.group(2)
            if val.lower() in ("#000", "#000000", "black", "rgb(0, 0, 0)", "rgb(0,0,0)"):
                results.append(self._make_result(
                    message=f"Pure black background detected. Use off-black (#1a1a2e) for better readability.",
                    line=line_num,
                    snippet=line_content,
                    fix_suggestion="Replace #000 or black with an off-black:\n"
                                   "  background-color: #1a1a2e;  /* or #121212, #0f0f0f */",
                    file_path=file_path,
                ))
            elif val.lower() in ("#fff", "#ffffff", "white", "rgb(255, 255, 255)", "rgb(255,255,255)"):
                results.append(self._make_result(
                    message=f"Pure white background detected. Use off-white (#fafafa) for reduced eye strain.",
                    line=line_num,
                    snippet=line_content,
                    fix_suggestion="Replace #fff or white with an off-white:\n"
                                   "  background-color: #fafafa;  /* or #f5f5f5, #f8f9fa */",
                    file_path=file_path,
                ))
        return results


class ColorRule005(Rule):
    """Detect inconsistent brand color usage."""

    rule_id = "color-005"
    rule_name = "Inconsistent Brand Colors"
    category = RuleCategory.COLOR
    severity = RuleSeverity.WARNING
    description = "Detects similar but not identical color values that may represent inconsistent brand color usage."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        colors = extract_all_colors(content)
        parsed = []
        for c in colors:
            rgb = parse_hex_color(c)
            if rgb:
                parsed.append((c, rgb))

        # Find groups of similar colors (distance < 30)
        similar_groups = []
        used = set()
        for i in range(len(parsed)):
            if i in used:
                continue
            group = [parsed[i]]
            for j in range(i + 1, len(parsed)):
                if j in used:
                    continue
                dist = color_distance(parsed[i][1], parsed[j][1])
                if dist < 30:
                    group.append(parsed[j])
                    used.add(j)
            if len(group) > 1:
                similar_groups.append(group)

        for group in similar_groups:
            names = [g[0] for g in group]
            results.append(self._make_result(
                message=f"Inconsistent similar colors detected: {', '.join(names[:5])}. "
                        f"These may be variations of the same brand color.",
                fix_suggestion="Standardize brand colors using CSS custom properties:\n"
                               ":root {\n"
                               "  --brand-primary: #3b82f6;  /* Use this consistently */\n"
                               "}",
                file_path=file_path,
            ))
        return results


class ColorRule006(Rule):
    """Detect missing CSS custom properties for colors."""

    rule_id = "color-006"
    rule_name = "No CSS Custom Properties for Colors"
    category = RuleCategory.COLOR
    severity = RuleSeverity.INFO
    description = "Detects files with hardcoded colors but no CSS custom properties (design tokens)."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        colors = extract_all_colors(content)
        has_custom_props = bool(re.search(r"--[\w-]+\s*:", content))

        if len(colors) >= 3 and not has_custom_props:
            line = self._find_first_color_line(content)
            results.append(self._make_result(
                message=f"Found {len(colors)} hardcoded colors but no CSS custom properties. "
                        f"Consider extracting colors into design tokens.",
                line=line,
                fix_suggestion=":root {\n"
                               "  --color-primary: #3b82f6;\n"
                               "  --color-secondary: #10b981;\n"
                               "  --color-accent: #f59e0b;\n"
                               "  --color-bg: #ffffff;\n"
                               "  --color-text: #1f2937;\n"
                               "  --color-muted: #6b7280;\n"
                               "}",
                file_path=file_path,
            ))
        return results

    def _find_first_color_line(self, content: str) -> int:
        pattern = r"#[0-9a-fA-F]{3,8}\b"
        match = re.search(pattern, content)
        if match:
            return content[:match.start()].count("\n") + 1
        return 0


class ColorRules:
    """Container class that registers all color rules."""

    @staticmethod
    def register_all():
        """Register all color rules with the global registry."""
        rules = [
            ColorRule001(),
            ColorRule002(),
            ColorRule003(),
            ColorRule004(),
            ColorRule005(),
            ColorRule006(),
        ]
        for rule in rules:
            rule_registry.register(rule)
        return rules
