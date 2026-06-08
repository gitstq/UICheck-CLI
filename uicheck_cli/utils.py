"""
Utility functions for UICheck-CLI.

Provides ANSI color codes, text helpers, and common utilities
used across the project. Zero external dependencies.
"""

import re
import os
import sys
import math
from typing import Optional


# ---------------------------------------------------------------------------
# ANSI Color Codes (no colorama dependency)
# ---------------------------------------------------------------------------

class Colors:
    """ANSI escape code constants for terminal coloring."""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"

    @staticmethod
    def supports_color() -> bool:
        """Check if the current terminal supports color output."""
        # Check NO_COLOR environment variable
        if os.environ.get("NO_COLOR"):
            return False
        # Check if running in a real terminal
        if not hasattr(sys.stdout, "isatty") or not sys.stdout.isatty():
            return False
        # Check for common terminal emulators on Windows
        if sys.platform == "win32":
            return "ANSICON" in os.environ or "WT_SESSION" in os.environ
        return True

    @staticmethod
    def disable():
        """Disable all color codes by replacing them with empty strings."""
        for attr in dir(Colors):
            if attr.startswith("_") or attr in ("supports_color", "disable"):
                continue
            val = getattr(Colors, attr)
            if isinstance(val, str) and val.startswith("\033"):
                setattr(Colors, attr, "")


# ---------------------------------------------------------------------------
# Color formatting helpers
# ---------------------------------------------------------------------------

def colored(text: str, color: str, bold: bool = False) -> str:
    """Wrap text with ANSI color codes.

    Args:
        text: The text to colorize.
        color: ANSI color code string.
        bold: Whether to also apply bold styling.

    Returns:
        Colorized text string with ANSI codes.
    """
    prefix = Colors.BOLD if bold else ""
    return f"{prefix}{color}{text}{Colors.RESET}"


def color_error(text: str) -> str:
    return colored(text, Colors.RED, bold=True)


def color_warning(text: str) -> str:
    return colored(text, Colors.YELLOW, bold=True)


def color_info(text: str) -> str:
    return colored(text, Colors.CYAN, bold=False)


def color_success(text: str) -> str:
    return colored(text, Colors.GREEN, bold=True)


def color_dim(text: str) -> str:
    return colored(text, Colors.DIM, bold=False)


def color_bold(text: str) -> str:
    return colored(text, Colors.BOLD, bold=True)


# ---------------------------------------------------------------------------
# Severity badge helpers
# ---------------------------------------------------------------------------

def severity_badge(severity: str) -> str:
    """Return a colored badge string for a severity level."""
    badges = {
        "error": colored(" ERROR ", Colors.BG_RED + Colors.WHITE, bold=True),
        "warning": colored(" WARN  ", Colors.BG_YELLOW + Colors.BLACK, bold=True),
        "info": colored(" INFO  ", Colors.BG_BLUE + Colors.WHITE, bold=True),
    }
    return badges.get(severity.lower(), colored(f" {severity.upper()} ", Colors.BG_BLACK + Colors.WHITE))


def severity_icon(severity: str) -> str:
    """Return an icon character for a severity level."""
    icons = {
        "error": color_error("x"),
        "warning": color_warning("!"),
        "info": color_info("i"),
    }
    return icons.get(severity.lower(), "?")


# ---------------------------------------------------------------------------
# Score color helpers
# ---------------------------------------------------------------------------

def score_color(score: float) -> str:
    """Return colored score text based on value."""
    if score >= 80:
        return color_success(f"{score:.1f}")
    elif score >= 60:
        return color_warning(f"{score:.1f}")
    else:
        return color_error(f"{score:.1f}")


def score_bar(score: float, width: int = 30) -> str:
    """Generate a visual progress bar for a score.

    Args:
        score: Score value from 0 to 100.
        width: Character width of the bar.

    Returns:
        A string representing the visual progress bar.
    """
    filled = int(width * score / 100)
    empty = width - filled

    if score >= 80:
        bar_char = colored("#", Colors.GREEN)
    elif score >= 60:
        bar_char = colored("#", Colors.YELLOW)
    else:
        bar_char = colored("#", Colors.RED)

    empty_char = color_dim("-")
    return f"[{bar_char * filled}{empty_char * empty}]"


# ---------------------------------------------------------------------------
# Text alignment and table helpers
# ---------------------------------------------------------------------------

def align_left(text: str, width: int) -> str:
    """Left-align text within a given width."""
    if len(text) >= width:
        return text[:width]
    return text + " " * (width - len(text))


def align_right(text: str, width: int) -> str:
    """Right-align text within a given width."""
    if len(text) >= width:
        return text[:width]
    return " " * (width - len(text)) + text


def align_center(text: str, width: int) -> str:
    """Center-align text within a given width."""
    if len(text) >= width:
        return text[:width]
    left = (width - len(text)) // 2
    right = width - len(text) - left
    return " " * left + text + " " * right


def truncate(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to a maximum length with a suffix."""
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def strip_ansi(text: str) -> str:
    """Remove ANSI escape codes from a string."""
    return re.sub(r"\033\[[0-9;]*m", "", text)


def visible_length(text: str) -> int:
    """Get the visible length of text (excluding ANSI codes)."""
    return len(strip_ansi(text))


# ---------------------------------------------------------------------------
# Color parsing utilities
# ---------------------------------------------------------------------------

def parse_hex_color(color_str: str) -> Optional[tuple]:
    """Parse a hex color string to (r, g, b) tuple.

    Args:
        color_str: Hex color string like '#fff', '#ffffff', 'rgb(255,0,0)'.

    Returns:
        Tuple of (r, g, b) integers, or None if parsing fails.
    """
    color_str = color_str.strip()

    # Handle hex formats
    hex_match = re.match(r"#([0-9a-fA-F]{3,8})", color_str)
    if hex_match:
        hex_val = hex_match.group(1)
        if len(hex_val) == 3:
            r = int(hex_val[0] * 2, 16)
            g = int(hex_val[1] * 2, 16)
            b = int(hex_val[2] * 2, 16)
        elif len(hex_val) == 6:
            r = int(hex_val[0:2], 16)
            g = int(hex_val[2:4], 16)
            b = int(hex_val[4:6], 16)
        elif len(hex_val) == 8:
            r = int(hex_val[0:2], 16)
            g = int(hex_val[2:4], 16)
            b = int(hex_val[4:6], 16)
            # Alpha ignored
        else:
            return None
        return (r, g, b)

    # Handle rgb() format
    rgb_match = re.match(r"rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)", color_str)
    if rgb_match:
        return (int(rgb_match.group(1)), int(rgb_match.group(2)), int(rgb_match.group(3)))

    return None


def color_distance(c1: tuple, c2: tuple) -> float:
    """Calculate Euclidean distance between two RGB colors.

    Args:
        c1: First color as (r, g, b) tuple.
        c2: Second color as (r, g, b) tuple.

    Returns:
        Euclidean distance as float (0-441.67).
    """
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))


def relative_luminance(c: tuple) -> float:
    """Calculate relative luminance of an RGB color per WCAG 2.0.

    Args:
        c: Color as (r, g, b) tuple with values 0-255.

    Returns:
        Relative luminance value between 0 and 1.
    """
    def linearize(channel: float) -> float:
        srgb = channel / 255.0
        if srgb <= 0.03928:
            return srgb / 12.92
        return ((srgb + 0.055) / 1.055) ** 2.4

    r, g, b = c
    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)


def contrast_ratio(c1: tuple, c2: tuple) -> float:
    """Calculate contrast ratio between two colors per WCAG 2.0.

    Args:
        c1: First color as (r, g, b).
        c2: Second color as (r, g, b).

    Returns:
        Contrast ratio (1:1 to 21:1).
    """
    l1 = relative_luminance(c1)
    l2 = relative_luminance(c2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    if darker == 0:
        return 21.0
    return (lighter + 0.05) / (darker + 0.05)


# ---------------------------------------------------------------------------
# File and path utilities
# ---------------------------------------------------------------------------

def get_file_extension(path: str) -> str:
    """Get the lowercase file extension without the dot."""
    return os.path.splitext(path)[1].lower()


def read_file_safe(path: str, encoding: str = "utf-8") -> Optional[str]:
    """Safely read a file with error handling.

    Args:
        path: File path to read.
        encoding: File encoding to use.

    Returns:
        File content as string, or None on error.
    """
    try:
        with open(path, "r", encoding=encoding) as f:
            return f.read()
    except (OSError, IOError, UnicodeDecodeError):
        return None


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ("B", "KB", "MB", "GB"):
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


# ---------------------------------------------------------------------------
# CSS value extraction utilities
# ---------------------------------------------------------------------------

def extract_css_values(css_text: str, property_name: str) -> list:
    """Extract all values for a given CSS property from CSS text.

    Args:
        css_text: Raw CSS text.
        property_name: CSS property name to search for.

    Returns:
        List of value strings found.
    """
    pattern = rf"{re.escape(property_name)}\s*:\s*([^;}}]+)"
    matches = re.findall(pattern, css_text, re.IGNORECASE)
    values = []
    for match in matches:
        val = match.strip().rstrip(";").strip()
        values.append(val)
    return values


def extract_all_colors(css_text: str) -> list:
    """Extract all color values from CSS text.

    Returns:
        List of color value strings found.
    """
    colors = []
    # Hex colors
    colors.extend(re.findall(r"#[0-9a-fA-F]{3,8}\b", css_text))
    # rgb/rgba colors
    colors.extend(re.findall(r"rgba?\s*\([^)]+\)", css_text))
    # Named colors (common ones)
    named_colors = [
        "red", "blue", "green", "yellow", "orange", "purple", "pink",
        "black", "white", "gray", "grey", "cyan", "magenta", "navy",
        "teal", "maroon", "olive", "lime", "aqua", "silver", "coral",
        "salmon", "tomato", "gold", "khaki", "violet", "indigo",
        "crimson", "chocolate", "tan", "peru", "sienna",
    ]
    for color in named_colors:
        # Match as whole word in CSS value context
        if re.search(rf"(?<!\w){color}(?!\w)", css_text, re.IGNORECASE):
            colors.append(color)
    return colors


def extract_font_sizes(css_text: str) -> list:
    """Extract all font-size values from CSS text.

    Returns:
        List of font-size value strings.
    """
    return extract_css_values(css_text, "font-size")


def extract_spacing_values(css_text: str) -> list:
    """Extract all margin and padding values from CSS text.

    Returns:
        List of (property, value) tuples.
    """
    results = []
    for prop in ("margin", "padding", "margin-top", "margin-bottom",
                 "margin-left", "margin-right", "padding-top", "padding-bottom",
                 "padding-left", "padding-right", "gap"):
        values = extract_css_values(css_text, prop)
        for val in values:
            results.append((prop, val))
    return results


def extract_selectors(css_text: str) -> list:
    """Extract CSS selectors from CSS text (simple extraction).

    Returns:
        List of selector strings.
    """
    # Simple approach: find text before {
    selectors = re.findall(r"([^{}]+)\{", css_text)
    return [s.strip() for s in selectors if s.strip()]


def extract_html_tags(html_text: str) -> list:
    """Extract all HTML tag names from text.

    Returns:
        List of tag name strings (lowercase).
    """
    return re.findall(r"<(/?)([a-zA-Z][a-zA-Z0-9]*)", html_text)


def count_dom_depth(html_text: str) -> int:
    """Estimate maximum DOM nesting depth from HTML text.

    Returns:
        Maximum nesting depth as integer.
    """
    max_depth = 0
    current_depth = 0
    # Simple tag counting (ignores self-closing and void elements)
    void_elements = {
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr",
    }
    tags = re.findall(r"<(/?)([a-zA-Z][a-zA-Z0-9]*)", html_text)
    for is_closing, tag_name in tags:
        tag_name = tag_name.lower()
        if is_closing:
            current_depth = max(0, current_depth - 1)
        elif tag_name not in void_elements:
            current_depth += 1
            max_depth = max(max_depth, current_depth)
    return max_depth


def extract_inline_styles(html_text: str) -> list:
    """Extract all inline style attribute values from HTML.

    Returns:
        List of inline style strings.
    """
    return re.findall(r'style\s*=\s*["\']([^"\']+)["\']', html_text)
