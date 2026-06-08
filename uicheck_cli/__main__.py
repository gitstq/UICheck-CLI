"""
CLI entry point for UICheck-CLI.

Handles command dispatch and orchestrates the analysis pipeline.
"""

import sys
import os
from typing import List, Optional

from .cli import parse_args
from .analyzer import Analyzer
from .scorer import Scorer
from .reporter import Reporter
from .fixer import Fixer
from .rules.base import rule_registry, RuleCategory
from . import __version__


def cmd_scan(args) -> int:
    """Handle the 'scan' command.

    Args:
        args: Parsed CLI arguments.

    Returns:
        Exit code (0 for success, 1 for errors).
    """
    target = args.target

    # Validate target exists
    if not os.path.exists(target):
        print(f"Error: Path not found: {target}", file=sys.stderr)
        return 1

    # Parse category filter
    categories = None
    if args.rules:
        categories = [c.strip() for c in args.rules.split(",")]

    # Parse severity filter
    severity_filter = args.severity if args.severity else None

    # Initialize components
    analyzer = Analyzer()
    scorer = Scorer()
    reporter = Reporter(verbose=args.verbose)

    # Run analysis
    try:
        report = analyzer.analyze(target, categories=categories, severity_filter=severity_filter)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error during analysis: {e}", file=sys.stderr)
        return 1

    # Compute score
    score = scorer.compute(report.results)

    # Output results
    fmt = args.format

    if fmt == "terminal":
        output_path = args.output if args.output else ""
        reporter.print_terminal(report, score, file_path=output_path)
    elif fmt == "json":
        output_path = args.output or "uicheck-report.json"
        reporter.write_json(report, score, output_path)
        print(f"Report written to: {output_path}")
    elif fmt == "markdown":
        output_path = args.output or "uicheck-report.md"
        reporter.write_markdown(report, score, output_path)
        print(f"Report written to: {output_path}")

    # Show fix summary in verbose mode
    if args.verbose and report.results:
        fixer = Fixer()
        patches = fixer.generate_patches(report.results)
        if patches:
            print()
            print(f"  Auto-fix patches available: {len(patches)}")
            for patch in patches[:10]:
                print(f"    {patch.file_path}:{patch.line} - {patch.description}")

    # Return non-zero exit code if errors found
    return 1 if report.errors > 0 else 0


def cmd_rules_list(args) -> int:
    """Handle the 'rules list' command.

    Args:
        args: Parsed CLI arguments.

    Returns:
        Exit code (0 for success).
    """
    # Ensure rules are registered
    analyzer = Analyzer()
    rules = rule_registry.get_all()

    # Filter by category if specified
    if args.category:
        try:
            cat = RuleCategory(args.category.lower())
            rules = rule_registry.get_by_category(cat)
        except ValueError:
            print(f"Error: Unknown category '{args.category}'", file=sys.stderr)
            print(f"Valid categories: {[c.value for c in RuleCategory]}", file=sys.stderr)
            return 1

    if args.format == "json":
        import json
        data = [r.info() for r in rules]
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        # Terminal output
        from .utils import color_bold, color_dim, colored, Colors

        print()
        print(color_bold(f"  UICheck-CLI Rules ({len(rules)} registered)"))
        print(color_dim("  " + "=" * 60))

        # Group by category
        categories = {}
        for rule in rules:
            cat = rule.category.value
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(rule)

        for cat_name in sorted(categories.keys()):
            cat_rules = categories[cat_name]
            print()
            print(color_bold(f"  {cat_name.upper()} ({len(cat_rules)} rules)"))
            print(color_dim(f"  {'-' * 55}"))

            for rule in cat_rules:
                sev_color = {
                    "error": Colors.RED,
                    "warning": Colors.YELLOW,
                    "info": Colors.CYAN,
                }.get(rule.severity.value, Colors.WHITE)

                sev_badge = colored(f" {rule.severity.value.upper():7} ", sev_color + Colors.BOLD)
                print(f"    {sev_badge} {colored(rule.rule_id, Colors.BRIGHT_CYAN)}  "
                      f"{rule.rule_name}")
                if args.verbose:
                    print(f"              {color_dim(rule.description)}")

        print()

    return 0


def cmd_rules_info(args) -> int:
    """Handle the 'rules info' command.

    Args:
        args: Parsed CLI arguments.

    Returns:
        Exit code (0 for success, 1 if rule not found).
    """
    # Ensure rules are registered
    analyzer = Analyzer()
    rule = rule_registry.get(args.rule_id)

    if not rule:
        print(f"Error: Rule '{args.rule_id}' not found.", file=sys.stderr)
        print(f"Use 'python -m uicheck_cli rules list' to see all rules.", file=sys.stderr)
        return 1

    from .utils import color_bold, color_dim, colored, Colors

    info = rule.info()
    print()
    print(color_bold(f"  Rule: {info['rule_id']}"))
    print(color_dim("  " + "=" * 50))
    print(f"  Name:       {info['rule_name']}")
    print(f"  Category:   {info['category']}")
    print(f"  Severity:   {info['severity']}")
    print(f"  Description: {info['description']}")
    print()

    return 0


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI.

    Args:
        argv: Command-line arguments (defaults to sys.argv[1:]).

    Returns:
        Exit code (0 for success, non-zero for errors).
    """
    args = parse_args(argv)

    if args.command == "scan":
        return cmd_scan(args)
    elif args.command == "rules":
        if args.rules_command == "list":
            return cmd_rules_list(args)
        elif args.rules_command == "info":
            return cmd_rules_info(args)
        else:
            # Default to list if no subcommand
            args.rules_command = "list"
            args.category = ""
            args.format = "terminal"
            args.verbose = False
            return cmd_rules_list(args)
    else:
        # No command specified - show help
        from .cli import build_parser
        build_parser().print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
