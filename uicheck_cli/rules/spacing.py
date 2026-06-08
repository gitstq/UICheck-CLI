"""
Spacing rules for UICheck-CLI.

Detects spacing-related visual quality issues:
- Non-standard spacing values (not multiples of 4/8)
- Inconsistent spacing between similar elements
- Missing vertical rhythm
- Negative margin usage
"""

import re
from typing import List, Tuple
from .base import Rule, RuleResult, RuleSeverity, RuleCategory, rule_registry
from ..utils import extract_css_values, extract_spacing_values


class SpacingRule001(Rule):
    """Detect non-standard spacing values (not multiples of 4)."""

    rule_id = "spacing-001"
    rule_name = "Non-Standard Spacing Values"
    category = RuleCategory.SPACING
    severity = RuleSeverity.WARNING
    description = "Detects margin/padding values that are not multiples of 4px (or 0.25rem), breaking visual consistency."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        spacing_values = extract_spacing_values(content)
        non_standard = []

        for prop, val in spacing_values:
            px_val = self._to_px(val)
            if px_val is not None and px_val != 0 and px_val % 4 != 0:
                non_standard.append((prop, val, px_val))

        if len(non_standard) > 2:
            examples = non_standard[:5]
            example_str = "; ".join(
                f"{prop}: {val} ({px_val}px)" for prop, val, px_val in examples
            )
            line = self._find_spacing_line(content)
            results.append(self._make_result(
                message=f"Found {len(non_standard)} non-standard spacing value(s) "
                        f"(not multiples of 4px). Examples: {example_str}",
                line=line,
                fix_suggestion="Use a 4px/8px grid system:\n"
                               "  4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px\n"
                               "Or in rem: 0.25rem, 0.5rem, 0.75rem, 1rem, 1.5rem, 2rem, 3rem, 4rem",
                file_path=file_path,
            ))
        return results

    def _to_px(self, val: str) -> int:
        """Convert a CSS spacing value to approximate px."""
        val = val.strip().lower()
        # Remove !important
        val = re.sub(r"!important", "", val).strip()
        # Handle calc()
        if "calc(" in val:
            return None
        # px
        match = re.match(r"(-?[\d.]+)\s*px", val)
        if match:
            return int(float(match.group(1)))
        # rem (1rem = 16px)
        match = re.match(r"(-?[\d.]+)\s*rem", val)
        if match:
            return int(float(match.group(1)) * 16)
        # em (assume 16px base)
        match = re.match(r"(-?[\d.]+)\s*em", val)
        if match:
            return int(float(match.group(1)) * 16)
        return None

    def _find_spacing_line(self, content: str) -> int:
        match = re.search(r"(margin|padding)\s*:", content, re.IGNORECASE)
        if match:
            return content[:match.start()].count("\n") + 1
        return 0


class SpacingRule002(Rule):
    """Detect inconsistent spacing between similar elements."""

    rule_id = "spacing-002"
    rule_name = "Inconsistent Spacing"
    category = RuleCategory.SPACING
    severity = RuleSeverity.WARNING
    description = "Detects similar CSS selectors with different spacing values, indicating inconsistency."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        # Extract selector -> spacing mappings
        selector_spacing = {}
        # Simple pattern: selector { ... margin/padding: value ... }
        blocks = re.finditer(r"([^{}]+)\{([^{}]+)\}", content)
        for block in blocks:
            selector = block.group(1).strip()
            body = block.group(2)
            margins = re.findall(r"margin\s*:\s*([^;]+)", body, re.IGNORECASE)
            paddings = re.findall(r"padding\s*:\s*([^;]+)", body, re.IGNORECASE)
            if margins or paddings:
                selector_spacing[selector] = {
                    "margin": margins,
                    "padding": paddings,
                    "line": content[:block.start()].count("\n") + 1,
                }

        # Check for similar selectors with different spacing
        checked = set()
        for sel1, spacing1 in selector_spacing.items():
            for sel2, spacing2 in selector_spacing.items():
                if sel1 >= sel2 or (sel1, sel2) in checked:
                    continue
                checked.add((sel1, sel2))
                # Check if selectors are similar (e.g., .card and .card-hover)
                if self._are_similar_selectors(sel1, sel2):
                    if spacing1 != spacing2:
                        results.append(self._make_result(
                            message=f"Similar selectors '{sel1}' and '{sel2}' have different spacing values.",
                            line=spacing1["line"],
                            fix_suggestion=f"Align spacing between '{sel1}' and '{sel2}' for consistency.",
                            file_path=file_path,
                        ))
        return results

    def _are_similar_selectors(self, s1: str, s2: str) -> bool:
        """Check if two selectors are likely related (similar base)."""
        # Remove pseudo-classes and modifiers
        base1 = re.sub(r"[:\[].*", "", s1).strip().lower()
        base2 = re.sub(r"[:\[].*", "", s2).strip().lower()
        if base1 == base2:
            return False  # Same selector, not interesting
        # Check if one is a prefix of the other
        if base1.startswith(base2[:len(base2)//2 + 1]) or base2.startswith(base1[:len(base1)//2 + 1]):
            return True
        return False


class SpacingRule003(Rule):
    """Detect missing vertical rhythm."""

    rule_id = "spacing-003"
    rule_name = "Missing Vertical Rhythm"
    category = RuleCategory.SPACING
    severity = RuleSeverity.INFO
    description = "Detects lack of consistent vertical spacing rhythm in the layout."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        # Look for margin-top/margin-bottom on block elements
        block_props = re.findall(
            r"(margin-top|margin-bottom)\s*:\s*([^;]+)",
            content, re.IGNORECASE
        )
        if not block_props:
            return results

        # Extract unique values
        values = set()
        for prop, val in block_props:
            val = val.strip().lower()
            val = re.sub(r"!important", "", val).strip()
            if val:
                values.add(val)

        # If too many unique values, rhythm is likely missing
        if len(values) > 5:
            results.append(self._make_result(
                message=f"Found {len(values)} unique vertical margin values. "
                        f"Consider establishing a consistent vertical rhythm.",
                fix_suggestion="Establish vertical rhythm with a baseline unit:\n"
                               ":root {\n"
                               "  --space-1: 0.25rem;  /* 4px */\n"
                               "  --space-2: 0.5rem;   /* 8px */\n"
                               "  --space-3: 0.75rem;  /* 12px */\n"
                               "  --space-4: 1rem;     /* 16px */\n"
                               "  --space-6: 1.5rem;   /* 24px */\n"
                               "  --space-8: 2rem;     /* 32px */\n"
                               "}",
                file_path=file_path,
            ))
        return results


class SpacingRule004(Rule):
    """Detect negative margin usage."""

    rule_id = "spacing-004"
    rule_name = "Negative Margin Usage"
    category = RuleCategory.SPACING
    severity = RuleSeverity.WARNING
    description = "Detects use of negative margins, which can cause layout issues."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        pattern = r"margin(-top|-bottom|-left|-right)?\s*:\s*-\s*([\d.]+)"
        matches = list(re.finditer(pattern, content, re.IGNORECASE))

        for match in matches:
            line_num = content[:match.start()].count("\n") + 1
            line_content = content.split("\n")[line_num - 1].strip()
            results.append(self._make_result(
                message=f"Negative margin detected: margin{match.group(1) or ''}: -{match.group(2)}. "
                        f"Consider using flexbox/grid gap or transform instead.",
                line=line_num,
                snippet=line_content,
                fix_suggestion="Replace negative margin with:\n"
                               "  /* Use gap in flexbox/grid */\n"
                               "  display: flex;\n"
                               "  gap: -8px;  /* Not valid, use negative margin only as last resort */\n"
                               "  /* Or use transform: translateY(-8px) */",
                file_path=file_path,
            ))
        return results


class SpacingRules:
    """Container class that registers all spacing rules."""

    @staticmethod
    def register_all():
        """Register all spacing rules with the global registry."""
        rules = [
            SpacingRule001(),
            SpacingRule002(),
            SpacingRule003(),
            SpacingRule004(),
        ]
        for rule in rules:
            rule_registry.register(rule)
        return rules
