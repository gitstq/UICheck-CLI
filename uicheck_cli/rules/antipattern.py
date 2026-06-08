"""
Anti-pattern rules for UICheck-CLI.

Detects common AI-generated UI anti-patterns:
- Overly symmetric "AI-flavored" styles
- Cookie-cutter card layouts
- Excessive gradient backgrounds
- Missing micro-interactions/transitions
- Too-uniform button styles
- Missing hover/focus states
- Emoji used as icon replacements
- Missing loading/empty states
"""

import re
from typing import List
from .base import Rule, RuleResult, RuleSeverity, RuleCategory, rule_registry


class AntiPatternRule001(Rule):
    """Detect overly symmetric AI-flavored styles."""

    rule_id = "antipattern-001"
    rule_name = "Overly Symmetric AI Style"
    category = RuleCategory.ANTIPATTERN
    severity = RuleSeverity.INFO
    description = "Detects overly uniform spacing and sizing patterns typical of AI-generated UIs."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        # Check for identical padding on all sides everywhere
        padding_pattern = r"padding\s*:\s*(\d+(?:px|rem|em))"
        paddings = re.findall(padding_pattern, content, re.IGNORECASE)

        if len(paddings) >= 4:
            # Check if all paddings are the same value
            unique_paddings = set(paddings)
            if len(unique_paddings) == 1:
                results.append(self._make_result(
                    message=f"All {len(paddings)} padding declarations use the same value "
                            f"({unique_paddings.pop()}). This creates an overly uniform 'AI look'.",
                    fix_suggestion="Vary spacing to create visual hierarchy:\n"
                                   "  .hero { padding: 4rem 2rem; }      /* More vertical space */\n"
                                   "  .card { padding: 1.5rem; }        /* Standard */\n"
                                   "  .badge { padding: 0.25rem 0.75rem; } /* Compact */",
                    file_path=file_path,
                ))

        # Check for identical border-radius everywhere
        radius_pattern = r"border-radius\s*:\s*(\d+(?:px|rem|em)|\d+%)"
        radii = re.findall(radius_pattern, content, re.IGNORECASE)
        if len(radii) >= 4:
            unique_radii = set(radii)
            if len(unique_radii) == 1:
                results.append(self._make_result(
                    message=f"All {len(radii)} border-radius values are identical "
                            f"({unique_radii.pop()}). Vary corner rounding for visual interest.",
                    fix_suggestion="Use varied border-radius for visual hierarchy:\n"
                                   "  .card { border-radius: 12px; }\n"
                                   "  .button { border-radius: 8px; }\n"
                                   "  .badge { border-radius: 999px; }  /* Pill shape */\n"
                                   "  .avatar { border-radius: 50%; }    /* Circle */",
                    file_path=file_path,
                ))
        return results


class AntiPatternRule002(Rule):
    """Detect cookie-cutter card layouts."""

    rule_id = "antipattern-002"
    rule_name = "Cookie-Cutter Card Layout"
    category = RuleCategory.ANTIPATTERN
    severity = RuleSeverity.WARNING
    description = "Detects repetitive card components with identical structure, a common AI pattern."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        # Count card-like class names
        card_pattern = r"class\s*=\s*['\"][^'\"]*card[^'\"]*['\"]"
        card_matches = re.findall(card_pattern, content, re.IGNORECASE)

        if len(card_matches) >= 4:
            # Check if they have similar inner structure
            card_blocks = re.findall(
                r'class\s*=\s*["\'][^"\']*card[^"\']*["\'][^>]*>(.*?)</div>',
                content, re.IGNORECASE | re.DOTALL
            )
            if len(card_blocks) >= 3:
                # Check for repetitive structure (all have img + h3 + p)
                similar_count = 0
                for block in card_blocks:
                    has_img = bool(re.search(r"<img", block, re.IGNORECASE))
                    has_heading = bool(re.search(r"<h[23]", block, re.IGNORECASE))
                    has_para = bool(re.search(r"<p", block, re.IGNORECASE))
                    if has_img and has_heading and has_para:
                        similar_count += 1

                if similar_count >= 3:
                    results.append(self._make_result(
                        message=f"Found {len(card_matches)} card elements with identical structure "
                                f"(image + heading + paragraph). Add visual variety.",
                        fix_suggestion="Vary card layouts:\n"
                                       "  1. Alternate card sizes (featured vs standard)\n"
                                       "  2. Use different content arrangements\n"
                                       "  3. Add visual accents (borders, shadows, icons)\n"
                                       "  4. Include at least one 'hero' card with different proportions",
                        file_path=file_path,
                    ))
        return results


class AntiPatternRule003(Rule):
    """Detect excessive gradient backgrounds."""

    rule_id = "antipattern-003"
    rule_name = "Excessive Gradient Backgrounds"
    category = RuleCategory.ANTIPATTERN
    severity = RuleSeverity.WARNING
    description = "Detects overuse of gradient backgrounds, a common AI-generated UI pattern."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        gradient_pattern = r"(linear-gradient|radial-gradient|conic-gradient)\s*\("
        gradients = list(re.finditer(gradient_pattern, content, re.IGNORECASE))

        if len(gradients) > 3:
            results.append(self._make_result(
                message=f"Found {len(gradients)} gradient declarations. "
                        f"Excessive gradients can look generic and 'AI-generated'.",
                fix_suggestion="Reduce gradient usage:\n"
                               "  1. Use solid colors for most backgrounds\n"
                               "  2. Reserve gradients for hero sections or accents\n"
                               "  3. Try subtle texture or patterns instead",
                file_path=file_path,
            ))
        return results


class AntiPatternRule004(Rule):
    """Detect missing micro-interactions and transitions."""

    rule_id = "antipattern-004"
    rule_name = "Missing Micro-Interactions"
    category = RuleCategory.ANTIPATTERN
    severity = RuleSeverity.WARNING
    description = "Detects lack of CSS transitions and animations, making the UI feel static."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        has_transitions = bool(re.search(r"transition\s*:", content, re.IGNORECASE))
        has_animations = bool(re.search(r"@keyframes|animation\s*:", content, re.IGNORECASE))
        has_transform = bool(re.search(r"transform\s*:", content, re.IGNORECASE))

        # Check for interactive elements
        has_buttons = bool(re.search(r"<button", content, re.IGNORECASE))
        has_links = bool(re.search(r"<a\s", content, re.IGNORECASE))

        if (has_buttons or has_links) and not has_transitions and not has_animations:
            results.append(self._make_result(
                message="No CSS transitions or animations found. "
                        "Add micro-interactions for a polished feel.",
                fix_suggestion="Add transitions to interactive elements:\n"
                               "  button {\n"
                               "    transition: all 0.2s ease;\n"
                               "  }\n"
                               "  button:hover {\n"
                               "    transform: translateY(-1px);\n"
                               "    box-shadow: 0 4px 12px rgba(0,0,0,0.15);\n"
                               "  }",
                file_path=file_path,
            ))
        return results


class AntiPatternRule005(Rule):
    """Detect overly uniform button styles."""

    rule_id = "antipattern-005"
    rule_name = "Uniform Button Styles"
    category = RuleCategory.ANTIPATTERN
    severity = RuleSeverity.INFO
    description = "Detects all buttons having identical styling without visual hierarchy (primary/secondary)."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        # Count button elements
        buttons = re.findall(r"<button", content, re.IGNORECASE)
        # Check for button class variations
        btn_classes = re.findall(
            r'class\s*=\s*["\']([^"\']*btn[^"\']*)["\']',
            content, re.IGNORECASE
        )

        if len(buttons) >= 3 and len(set(btn_classes)) <= 1:
            results.append(self._make_result(
                message=f"Found {len(buttons)} buttons but no style variations "
                        f"(primary/secondary/outline/ghost). Create button hierarchy.",
                fix_suggestion="Create button variants:\n"
                               "  .btn-primary { background: var(--color-primary); color: white; }\n"
                               "  .btn-secondary { background: var(--color-muted); color: white; }\n"
                               "  .btn-outline { border: 1px solid var(--color-primary); color: var(--color-primary); }\n"
                               "  .btn-ghost { background: transparent; color: var(--color-primary); }",
                file_path=file_path,
            ))
        return results


class AntiPatternRule006(Rule):
    """Detect missing hover/focus states."""

    rule_id = "antipattern-006"
    rule_name = "Missing Hover/Focus States"
    category = RuleCategory.ANTIPATTERN
    severity = RuleSeverity.ERROR
    description = "Detects interactive elements without :hover or :focus CSS states."""

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        has_hover = bool(re.search(r":hover", content))
        has_focus = bool(re.search(r":focus", content))
        has_active = bool(re.search(r":active", content))

        has_interactive = bool(
            re.search(r"<button|<a\s|role\s*=\s*[\"']button[\"']|role\s*=\s*[\"']link[\"']",
                      content, re.IGNORECASE)
        )

        if has_interactive and not has_hover and not has_focus:
            results.append(self._make_result(
                message="No :hover or :focus states defined for interactive elements. "
                        "Essential for usability and accessibility.",
                fix_suggestion="Add hover and focus states:\n"
                               "  a:hover, button:hover {\n"
                               "    opacity: 0.85;\n"
                               "  }\n"
                               "  a:focus-visible, button:focus-visible {\n"
                               "    outline: 2px solid var(--color-primary);\n"
                               "    outline-offset: 2px;\n"
                               "  }",
                file_path=file_path,
            ))
        elif has_interactive and not has_focus:
            results.append(self._make_result(
                message="No :focus states defined. Focus states are essential for keyboard navigation.",
                fix_suggestion="Add focus-visible states:\n"
                               "  :focus-visible {\n"
                               "    outline: 2px solid var(--color-primary);\n"
                               "    outline-offset: 2px;\n"
                               "  }",
                file_path=file_path,
            ))
        return results


class AntiPatternRule007(Rule):
    """Detect emoji used as icon replacements."""

    rule_id = "antipattern-007"
    rule_name = "Emoji as Icon Replacement"
    category = RuleCategory.ANTIPATTERN
    severity = RuleSeverity.WARNING
    description = "Detects emoji characters used in place of proper icons, which look unprofessional."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        # Common emoji ranges in HTML content (not in comments or strings)
        # Check for emoji in visible UI text (buttons, headings, spans)
        emoji_pattern = re.compile(
            r'[\U0001F300-\U0001F9FF\U00002702-\U000027B0\U0001FA00-\U0001FA6F'
            r'\U0001FA70-\U0001FAFF\U00002600-\U000026FF\U0000FE00-\U0000FE0F'
            r'\U0001F900-\U0001F9FF]'
        )

        # Find emoji in HTML tags (not in script/style)
        html_content = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', content, flags=re.IGNORECASE | re.DOTALL)
        matches = list(emoji_pattern.finditer(html_content))

        if len(matches) > 3:
            results.append(self._make_result(
                message=f"Found {len(matches)} emoji characters in the UI. "
                        f"Replace with proper SVG icons for a professional look.",
                fix_suggestion="Replace emoji with SVG icons:\n"
                               "  <!-- Instead of: <span>📧 Contact</span> -->\n"
                               "  <!-- Use: -->\n"
                               "  <svg class='icon' viewBox='0 0 24 24'>\n"
                               "    <path d='...'/>\n"
                               "  </svg> Contact\n\n"
                               "  Consider: Lucide, Heroicons, or Feather Icons",
                file_path=file_path,
            ))
        return results


class AntiPatternRule008(Rule):
    """Detect missing loading/empty states."""

    rule_id = "antipattern-008"
    rule_name = "Missing Loading/Empty States"
    category = RuleCategory.ANTIPATTERN
    severity = RuleSeverity.WARNING
    description = "Detects dynamic content areas without loading or empty state placeholders."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        # Check for patterns suggesting dynamic content
        has_data_fetch = bool(
            re.search(r"(fetch|axios|useEffect|useState|v-for|v-if|map\s*\(|\.map\s*\(|loading|isLoading)",
                      content, re.IGNORECASE)
        )
        has_loading_state = bool(
            re.search(r"(loading|spinner|skeleton|placeholder|empty|no-data|no-results)",
                      content, re.IGNORECASE)
        )

        if has_data_fetch and not has_loading_state:
            results.append(self._make_result(
                message="Dynamic content detected but no loading/empty states found. "
                        "Users need feedback during data loading.",
                fix_suggestion="Add loading and empty states:\n"
                               "  {isLoading && <Spinner />}\n"
                               "  {error && <ErrorMessage />}\n"
                               "  {data.length === 0 && <EmptyState />}\n"
                               "  {data.map(item => <Card key={item.id} />)}",
                file_path=file_path,
            ))
        return results


class AntiPatternRules:
    """Container class that registers all anti-pattern rules."""

    @staticmethod
    def register_all():
        """Register all anti-pattern rules with the global registry."""
        rules = [
            AntiPatternRule001(),
            AntiPatternRule002(),
            AntiPatternRule003(),
            AntiPatternRule004(),
            AntiPatternRule005(),
            AntiPatternRule006(),
            AntiPatternRule007(),
            AntiPatternRule008(),
        ]
        for rule in rules:
            rule_registry.register(rule)
        return rules
