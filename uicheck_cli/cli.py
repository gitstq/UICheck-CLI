"""
CLI argument parser and command handler for UICheck-CLI.

Defines all CLI commands and subcommands:
- scan: Analyze files/directories
- rules: List and inspect rules
- version: Show version
"""

import argparse
import sys
from typing import List, Optional

from . import __version__, __description__


def build_parser() -> argparse.ArgumentParser:
    """Build the main CLI argument parser.

    Returns:
        Configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        prog="uicheck_cli",
        description=__description__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m uicheck_cli scan ./src/components
  python -m uicheck_cli scan index.html --format json --output report.json
  python -m uicheck_cli scan ./src --rules color,typography --severity error
  python -m uicheck_cli rules list
  python -m uicheck_cli rules info color-001
  python -m uicheck_cli --version

Supported formats: HTML, CSS, JSX, TSX, Vue SFC
Rule categories: color, typography, spacing, layout, accessibility, performance, antipattern
        """,
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"UICheck-CLI v{__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # ---- scan command ----
    scan_parser = subparsers.add_parser(
        "scan",
        help="Scan files or directories for visual quality issues",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    scan_parser.add_argument(
        "target",
        help="File or directory path to scan",
    )
    scan_parser.add_argument(
        "--format", "-f",
        choices=["terminal", "json", "markdown"],
        default="terminal",
        help="Output format (default: terminal)",
    )
    scan_parser.add_argument(
        "--output", "-o",
        default="",
        help="Output file path (for json/markdown formats)",
    )
    scan_parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        default=False,
        help="Show detailed output with code snippets and fix suggestions",
    )
    scan_parser.add_argument(
        "--rules", "-r",
        default="",
        help="Comma-separated list of rule categories to run "
             "(color,typography,spacing,layout,accessibility,performance,antipattern)",
    )
    scan_parser.add_argument(
        "--severity", "-s",
        choices=["error", "warning", "info"],
        default="",
        help="Filter results by minimum severity level",
    )
    scan_parser.add_argument(
        "--no-color",
        action="store_true",
        default=False,
        help="Disable colored output",
    )

    # ---- rules command ----
    rules_parser = subparsers.add_parser(
        "rules",
        help="List and inspect detection rules",
    )
    rules_subparsers = rules_parser.add_subparsers(dest="rules_command")

    # rules list
    rules_list_parser = rules_subparsers.add_parser(
        "list",
        help="List all detection rules",
    )
    rules_list_parser.add_argument(
        "--category", "-c",
        default="",
        help="Filter by category name",
    )
    rules_list_parser.add_argument(
        "--format", "-f",
        choices=["terminal", "json"],
        default="terminal",
        help="Output format (default: terminal)",
    )
    rules_list_parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        default=False,
        help="Show detailed rule descriptions",
    )

    # rules info
    rules_info_parser = rules_subparsers.add_parser(
        "info",
        help="Show detailed information about a specific rule",
    )
    rules_info_parser.add_argument(
        "rule_id",
        help="Rule ID to inspect (e.g., color-001)",
    )

    return parser


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        argv: Argument list (defaults to sys.argv[1:]).

    Returns:
        Parsed namespace.
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    # Handle --no-color
    if hasattr(args, "no_color") and args.no_color:
        from .utils import Colors
        Colors.disable()

    return args
