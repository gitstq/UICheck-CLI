"""
Accessibility rules for UICheck-CLI.

Detects accessibility-related visual quality issues:
- Images missing alt attributes
- Form elements missing labels
- Missing semantic HTML (div soup)
- Missing ARIA attributes on interactive elements
- Insufficient color contrast for text
- Missing skip navigation link
"""

import re
from typing import List, Tuple
from .base import Rule, RuleResult, RuleSeverity, RuleCategory, rule_registry
from ..utils import parse_hex_color, contrast_ratio, extract_all_colors


class AccessibilityRule001(Rule):
    """Detect images missing alt attributes."""

    rule_id = "accessibility-001"
    rule_name = "Images Missing Alt Text"
    category = RuleCategory.ACCESSIBILITY
    severity = RuleSeverity.ERROR
    description = "Detects <img> tags without alt attributes, which are essential for screen readers."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        # Find img tags
        pattern = r"<img\s+([^>]*?)(?:/>|>)"
        matches = list(re.finditer(pattern, content, re.IGNORECASE))

        for match in matches:
            attrs = match.group(1)
            line_num = content[:match.start()].count("\n") + 1
            line_content = content.split("\n")[line_num - 1].strip()

            # Check for alt attribute
            has_alt = bool(re.search(r'alt\s*=\s*["\'][^"\']*["\']', attrs, re.IGNORECASE))
            has_empty_alt = bool(re.search(r'alt\s*=\s*["\']\s*["\']', attrs, re.IGNORECASE))

            if not has_alt:
                results.append(self._make_result(
                    message="Image missing 'alt' attribute. All images must have alt text for accessibility.",
                    line=line_num,
                    snippet=line_content[:80],
                    fix_suggestion='Add alt attribute:\n'
                                   '  <img src="photo.jpg" alt="Description of the image">',
                    file_path=file_path,
                ))
            elif has_empty_alt and "decorative" not in attrs.lower():
                results.append(self._make_result(
                    message="Image has empty alt attribute. Use empty alt only for decorative images.",
                    line=line_num,
                    snippet=line_content[:80],
                    severity=RuleSeverity.INFO,
                    fix_suggestion='If decorative: <img src="deco.png" alt="" role="presentation">\n'
                                   'If meaningful: <img src="photo.jpg" alt="Photo description">',
                    file_path=file_path,
                ))
        return results


class AccessibilityRule002(Rule):
    """Detect form elements missing associated labels."""

    rule_id = "accessibility-002"
    rule_name = "Form Elements Missing Labels"
    category = RuleCategory.ACCESSIBILITY
    severity = RuleSeverity.ERROR
    description = "Detects input/textarea/select elements without associated label elements."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        # Find form inputs
        input_pattern = r'<(input|textarea|select)\s+([^>]*?)(?:/>|>)'
        inputs = list(re.finditer(input_pattern, content, re.IGNORECASE))

        for inp_match in inputs:
            tag = inp_match.group(1).lower()
            attrs = inp_match.group(2)
            line_num = content[:inp_match.start()].count("\n") + 1
            line_content = content.split("\n")[line_num - 1].strip()

            # Skip hidden inputs and submit/button types
            input_type = re.search(r'type\s*=\s*["\'](\w+)["\']', attrs, re.IGNORECASE)
            if input_type and input_type.group(1).lower() in ("hidden", "submit", "button", "reset"):
                continue

            # Check for associated label (by id or wrapping)
            input_id = re.search(r'id\s*=\s*["\']([^"\']+)["\']', attrs, re.IGNORECASE)
            has_aria_label = bool(re.search(r'aria-label\s*=\s*["\'][^"\']+["\']', attrs, re.IGNORECASE))
            has_aria_labelledby = bool(re.search(r'aria-labelledby\s*=', attrs, re.IGNORECASE))
            has_placeholder = bool(re.search(r'placeholder\s*=\s*["\'][^"\']+["\']', attrs, re.IGNORECASE))

            has_label = False
            if input_id:
                label_for = re.search(
                    rf'<label\s+[^>]*for\s*=\s*["\']{re.escape(input_id.group(1))}["\']',
                    content, re.IGNORECASE
                )
                has_label = bool(label_for)

            # Check wrapping label
            # Find the surrounding context
            start = max(0, inp_match.start() - 200)
            surrounding = content[start:inp_match.end() + 200]
            has_wrapping_label = bool(
                re.search(r'<label[^>]*>.*<' + tag, surrounding, re.IGNORECASE | re.DOTALL)
            )

            if not has_label and not has_wrapping_label and not has_aria_label and not has_aria_labelledby:
                results.append(self._make_result(
                    message=f"<{tag}> element has no associated label, aria-label, or aria-labelledby.",
                    line=line_num,
                    snippet=line_content[:80],
                    fix_suggestion=f'Add a label:\n'
                                   f'  <label for="{tag}-id">Label text</label>\n'
                                   f'  <{tag} id="{tag}-id" ...>\n'
                                   f'Or add aria-label:\n'
                                   f'  <{tag} aria-label="Description" ...>',
                    file_path=file_path,
                ))
            elif not has_label and not has_wrapping_label and has_placeholder:
                results.append(self._make_result(
                    message=f"<{tag}> uses placeholder instead of label. "
                            f"Placeholder disappears on input and is not reliable.",
                    line=line_num,
                    snippet=line_content[:80],
                    severity=RuleSeverity.WARNING,
                    fix_suggestion=f'Add a visible label in addition to placeholder:\n'
                                   f'  <label for="{tag}-id">Label</label>\n'
                                   f'  <{tag} id="{tag}-id" placeholder="Hint text">',
                    file_path=file_path,
                ))
        return results


class AccessibilityRule003(Rule):
    """Detect missing semantic HTML (overuse of div)."""

    rule_id = "accessibility-003"
    rule_name = "Missing Semantic HTML"
    category = RuleCategory.ACCESSIBILITY
    severity = RuleSeverity.WARNING
    description = "Detects overuse of <div> elements without semantic HTML tags (header, nav, main, etc.)."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        # Count divs vs semantic elements
        div_count = len(re.findall(r"<div[\s>]", content, re.IGNORECASE))
        semantic_tags = [
            "header", "nav", "main", "footer", "article", "section",
            "aside", "figure", "figcaption", "details", "summary",
            "time", "mark", "address",
        ]
        semantic_count = sum(
            len(re.findall(rf"<{tag}[\s>]", content, re.IGNORECASE))
            for tag in semantic_tags
        )

        # If many divs but few/no semantic tags
        if div_count > 5 and semantic_count < 2:
            ratio = div_count / max(semantic_count, 1)
            results.append(self._make_result(
                message=f"Found {div_count} <div> elements but only {semantic_count} semantic tags. "
                        f"Use semantic HTML (header, nav, main, section, article, footer) for accessibility.",
                fix_suggestion="Replace generic divs with semantic elements:\n"
                               "  <div class='header'>  ->  <header>\n"
                               "  <div class='nav'>    ->  <nav>\n"
                               "  <div class='main'>   ->  <main>\n"
                               "  <div class='footer'> ->  <footer>\n"
                               "  <div class='article'> ->  <article>",
                file_path=file_path,
            ))
        return results


class AccessibilityRule004(Rule):
    """Detect missing ARIA attributes on interactive elements."""

    rule_id = "accessibility-004"
    rule_name = "Missing ARIA Attributes"
    category = RuleCategory.ACCESSIBILITY
    severity = RuleSeverity.WARNING
    description = "Detects interactive elements (buttons, links with click handlers) missing ARIA attributes."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        # Check div/span with onclick but no role
        pattern = r'<(div|span)\s+([^>]*?)onclick'
        matches = list(re.finditer(pattern, content, re.IGNORECASE))

        for match in matches:
            tag = match.group(1)
            attrs = match.group(2)
            line_num = content[:match.start()].count("\n") + 1
            line_content = content.split("\n")[line_num - 1].strip()

            has_role = bool(re.search(r'role\s*=', attrs, re.IGNORECASE))
            has_tabindex = bool(re.search(r'tabindex\s*=', attrs, re.IGNORECASE))
            has_aria = bool(re.search(r'aria-', attrs, re.IGNORECASE))

            if not has_role:
                results.append(self._make_result(
                    message=f"<{tag}> with onclick but no 'role' attribute. "
                            f"Interactive elements must have appropriate ARIA roles.",
                    line=line_num,
                    snippet=line_content[:80],
                    fix_suggestion=f'Add role and keyboard support:\n'
                                   f'  <{tag} role="button" tabindex="0" '
                                   f'onKeyDown="if(event.key===\'Enter\')click()" ...>',
                    file_path=file_path,
                ))
            elif not has_tabindex:
                results.append(self._make_result(
                    message=f"<{tag}> with onclick and role but no 'tabindex'. "
                            f"Element won't be keyboard focusable.",
                    line=line_num,
                    snippet=line_content[:80],
                    severity=RuleSeverity.INFO,
                    fix_suggestion=f'Add tabindex="0" to make the element keyboard focusable.',
                    file_path=file_path,
                ))

        # Check for icon-only buttons (no text content)
        btn_pattern = r'<button\s+([^>]*?)>(\s*</button>|[^<]{0,3}</button>)'
        btn_matches = list(re.finditer(btn_pattern, content, re.IGNORECASE))
        for match in btn_matches:
            attrs = match.group(1)
            line_num = content[:match.start()].count("\n") + 1
            has_aria_label = bool(re.search(r'aria-label\s*=', attrs, re.IGNORECASE))
            has_title = bool(re.search(r'title\s*=', attrs, re.IGNORECASE))
            if not has_aria_label and not has_title:
                results.append(self._make_result(
                    message="Button with no visible text and no aria-label or title.",
                    line=line_num,
                    severity=RuleSeverity.ERROR,
                    fix_suggestion='Add aria-label to icon buttons:\n'
                                   '  <button aria-label="Close"><svg>...</svg></button>',
                    file_path=file_path,
                ))
        return results


class AccessibilityRule005(Rule):
    """Detect insufficient color contrast for text."""

    rule_id = "accessibility-005"
    rule_name = "Insufficient Text Color Contrast"
    category = RuleCategory.ACCESSIBILITY
    severity = RuleSeverity.ERROR
    description = "Detects text/background color combinations that fail WCAG contrast requirements."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        # Extract color and background-color pairs
        color_vals = re.findall(r"(?:^|[^-\w])color\s*:\s*([^;}{]+)", content, re.IGNORECASE)
        bg_vals = re.findall(r"background(?:-color)?\s*:\s*([^;}{]+)", content, re.IGNORECASE)

        if not color_vals:
            return results

        # Parse colors
        text_colors = []
        bg_colors = []
        for c in color_vals:
            parsed = parse_hex_color(c.strip())
            if parsed:
                text_colors.append((c.strip(), parsed))
        for c in bg_vals:
            parsed = parse_hex_color(c.strip())
            if parsed:
                bg_colors.append((c.strip(), parsed))

        # Check contrast between text and background colors
        for text_name, text_rgb in text_colors:
            for bg_name, bg_rgb in bg_colors:
                ratio = contrast_ratio(text_rgb, bg_rgb)
                if ratio < 4.5:
                    results.append(self._make_result(
                        message=f"Low contrast ratio: {text_name} on {bg_name} = {ratio:.2f}:1. "
                                f"WCAG requires 4.5:1 for normal text.",
                        severity=RuleSeverity.ERROR,
                        fix_suggestion=f"Increase contrast. Current ratio: {ratio:.2f}:1 (need >= 4.5:1).\n"
                                       f"Try darkening the text or lightening the background.",
                        file_path=file_path,
                    ))
                elif ratio < 7:
                    results.append(self._make_result(
                        message=f"Borderline contrast ratio: {text_name} on {bg_name} = {ratio:.2f}:1. "
                                f"WCAG AAA requires 7:1 for normal text.",
                        severity=RuleSeverity.INFO,
                        fix_suggestion=f"Consider increasing contrast to meet AAA standard (7:1).",
                        file_path=file_path,
                    ))
        return results


class AccessibilityRule006(Rule):
    """Detect missing skip navigation link."""

    rule_id = "accessibility-006"
    rule_name = "Missing Skip Navigation Link"
    category = RuleCategory.ACCESSIBILITY
    severity = RuleSeverity.INFO
    description = "Detects HTML pages without a skip navigation link for keyboard users."

    def check(self, content: str, file_path: str = "") -> List[RuleResult]:
        results = []
        # Only check full HTML documents
        if "<html" not in content.lower() and "<!doctype" not in content.lower():
            return results

        has_skip = bool(
            re.search(r'skip[-\s]?navigation|skip[-\s]?to[-\s]?content|skip[-\s]?link', content, re.IGNORECASE)
        )
        if not has_skip:
            head_match = re.search(r"<body", content, re.IGNORECASE)
            line_num = content[:head_match.start()].count("\n") + 1 if head_match else 1
            results.append(self._make_result(
                message="No skip navigation link found. Add one as the first focusable element "
                        "in the page for keyboard accessibility.",
                line=line_num,
                fix_suggestion='Add as first element inside <body>:\n'
                               '  <a href="#main-content" class="skip-link">'
                               'Skip to main content</a>\n'
                               'And add id="main-content" to your <main> element.',
                file_path=file_path,
            ))
        return results


class AccessibilityRules:
    """Container class that registers all accessibility rules."""

    @staticmethod
    def register_all():
        """Register all accessibility rules with the global registry."""
        rules = [
            AccessibilityRule001(),
            AccessibilityRule002(),
            AccessibilityRule003(),
            AccessibilityRule004(),
            AccessibilityRule005(),
            AccessibilityRule006(),
        ]
        for rule in rules:
            rule_registry.register(rule)
        return rules
