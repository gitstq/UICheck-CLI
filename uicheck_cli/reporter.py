"""
Reporter for UICheck-CLI.

Generates analysis reports in three formats:
- Terminal (colored, table-based)
- JSON (machine-readable)
- Markdown (documentation-friendly)
"""

import json
import os
from typing import List, Optional, Dict
from datetime import datetime

from .rules.base import RuleResult, RuleCategory, RuleSeverity
from .analyzer import AnalysisReport
from .scorer import OverallScore
from .utils import (
    Colors, colored, color_error, color_warning, color_info,
    color_success, color_dim, color_bold, severity_badge, severity_icon,
    score_color, score_bar, align_left, align_right, align_center,
    truncate, strip_ansi, visible_length,
)


class Reporter:
    """Generates formatted analysis reports.

    Usage:
        reporter = Reporter()
        reporter.print_terminal(report, score)
        reporter.write_json(report, score, "output.json")
        reporter.write_markdown(report, score, "output.md")
    """

    def __init__(self, verbose: bool = False):
        """Initialize the reporter.

        Args:
            verbose: Whether to show detailed output.
        """
        self.verbose = verbose
        # Disable colors if terminal doesn't support them
        if not Colors.supports_color():
            Colors.disable()

    def print_terminal(
        self,
        report: AnalysisReport,
        score: OverallScore,
        file_path: str = "",
    ) -> None:
        """Print a colored terminal report.

        Args:
            report: The analysis report.
            score: The computed score.
            file_path: Optional path to write output to (if not empty).
        """
        lines = self._build_terminal_output(report, score)
        output = "\n".join(lines)

        if file_path:
            # Write stripped version (no ANSI codes)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(strip_ansi(output))
        else:
            print(output)

    def _build_terminal_output(self, report: AnalysisReport, score: OverallScore) -> List[str]:
        """Build terminal output lines.

        Args:
            report: The analysis report.
            score: The computed score.

        Returns:
            List of output lines.
        """
        lines = []

        # Header
        lines.append("")
        lines.append(color_bold("  UICheck-CLI") + color_dim("  Visual Quality Report"))
        lines.append(color_dim("  " + "=" * 50))
        lines.append("")

        # Score section
        lines.append(f"  Overall Score: {score_color(score.overall)}/100  "
                      f"Grade: {color_bold(self._grade_color(score.grade, score.grade))}")
        lines.append(f"  {score_bar(score.overall)}")
        lines.append(f"  {color_dim(score.summary)}")
        lines.append("")

        # Stats summary
        lines.append(f"  Files scanned: {color_bold(str(report.files_scanned))}  "
                      f"Skipped: {color_dim(str(report.files_skipped))}  "
                      f"Issues: {color_bold(str(report.total_issues))}")
        lines.append(f"  {color_error(str(report.errors))} errors  "
                      f"{color_warning(str(report.warnings))} warnings  "
                      f"{color_info(str(report.infos))} infos")
        lines.append("")

        # Category breakdown table
        lines.append(color_bold("  Category Breakdown"))
        lines.append(color_dim("  " + "-" * 60))
        header = f"  {align_left('Category', 18)} {align_right('Score', 8)} " \
                 f"{align_right('Issues', 8)}  {align_left('Bar', 32)}"
        lines.append(color_dim(header))
        lines.append(color_dim("  " + "-" * 60))

        for cat_name, cat_score in score.category_scores.items():
            cat_label = self._category_label(cat_name)
            score_str = score_color(cat_score.score)
            issues_str = str(cat_score.issues_count)
            bar = score_bar(cat_score.score, 20)
            line = f"  {align_left(cat_label, 18)} {align_right(score_str, 8)} " \
                   f"{align_right(issues_str, 8)}  {bar}"
            lines.append(line)

        lines.append("")

        # Issues list
        if report.results:
            lines.append(color_bold(f"  Issues ({report.total_issues})"))
            lines.append(color_dim("  " + "-" * 70))

            # Group by file
            by_file: Dict[str, List[RuleResult]] = {}
            for result in report.results:
                if result.file_path not in by_file:
                    by_file[result.file_path] = []
                by_file[result.file_path].append(result)

            for file_path, file_results in by_file.items():
                if len(by_file) > 1:
                    lines.append("")
                    lines.append(color_bold(f"  {file_path}"))

                for result in file_results:
                    badge = severity_badge(result.severity.value)
                    cat_label = color_dim(f"[{result.category.value}]")
                    msg = truncate(result.message, 60)
                    loc = ""
                    if result.line > 0:
                        loc = color_dim(f":{result.line}")

                    line = f"  {badge} {cat_label} {msg}{loc}"
                    lines.append(line)

                    # Show snippet in verbose mode
                    if self.verbose and result.snippet:
                        snippet = truncate(result.snippet, 70)
                        lines.append(color_dim(f"         {snippet}"))

                    # Show fix suggestion in verbose mode
                    if self.verbose and result.fix_suggestion:
                        fix_lines = result.fix_suggestion.split("\n")
                        for fl in fix_lines[:3]:
                            lines.append(color_info(f"         > {fl}"))

            lines.append("")

        # Footer
        lines.append(color_dim("  " + "=" * 50))
        lines.append(color_dim(f"  Generated by UICheck-CLI v1.0.0  "
                               f"|  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"))
        lines.append("")

        return lines

    def write_json(
        self,
        report: AnalysisReport,
        score: OverallScore,
        file_path: str,
    ) -> None:
        """Write a JSON report to a file.

        Args:
            report: The analysis report.
            score: The computed score.
            file_path: Output file path.
        """
        data = {
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "scan_root": report.scan_root,
            "score": score.to_dict(),
            "summary": {
                "files_scanned": report.files_scanned,
                "files_skipped": report.files_skipped,
                "total_issues": report.total_issues,
                "errors": report.errors,
                "warnings": report.warnings,
                "infos": report.infos,
            },
            "results": [r.to_dict() for r in report.results],
        }

        os.makedirs(os.path.dirname(file_path) if os.path.dirname(file_path) else ".", exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def write_markdown(
        self,
        report: AnalysisReport,
        score: OverallScore,
        file_path: str,
    ) -> None:
        """Write a Markdown report to a file.

        Args:
            report: The analysis report.
            score: The computed score.
            file_path: Output file path.
        """
        lines = []
        lines.append("# UICheck-CLI Visual Quality Report")
        lines.append("")
        lines.append(f"**Overall Score:** {score.overall:.1f}/100 (Grade: {score.grade})")
        lines.append("")
        lines.append(f"> {score.summary}")
        lines.append("")
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"**Files Scanned:** {report.files_scanned}")
        lines.append(f"**Total Issues:** {report.total_issues} "
                     f"({report.errors} errors, {report.warnings} warnings, {report.infos} infos)")
        lines.append("")

        # Category breakdown
        lines.append("## Category Breakdown")
        lines.append("")
        lines.append("| Category | Score | Issues |")
        lines.append("|----------|-------|--------|")
        for cat_name, cat_score in score.category_scores.items():
            cat_label = cat_name.replace("_", " ").title()
            lines.append(f"| {cat_label} | {cat_score.score:.1f} | {cat_score.issues_count} |")
        lines.append("")

        # Issues
        if report.results:
            lines.append("## Issues")
            lines.append("")

            # Group by severity
            for severity in [RuleSeverity.ERROR, RuleSeverity.WARNING, RuleSeverity.INFO]:
                filtered = [r for r in report.results if r.severity == severity]
                if not filtered:
                    continue
                lines.append(f"### {severity.value.capitalize()} ({len(filtered)})")
                lines.append("")
                for result in filtered:
                    lines.append(f"**[{result.rule_id}]** {result.message}")
                    if result.file_path:
                        loc = f"{result.file_path}"
                        if result.line > 0:
                            loc += f":{result.line}"
                        lines.append(f"- File: `{loc}`")
                    if result.fix_suggestion:
                        lines.append(f"- Fix: {result.fix_suggestion}")
                    lines.append("")

        # Footer
        lines.append("---")
        lines.append("*Generated by [UICheck-CLI](https://github.com/uicheck-cli) v1.0.0*")

        os.makedirs(os.path.dirname(file_path) if os.path.dirname(file_path) else ".", exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    def _grade_color(self, grade: str, text: str) -> str:
        """Apply color to a grade letter."""
        if grade.startswith("A"):
            return color_success(text)
        elif grade.startswith("B"):
            return colored(text, Colors.YELLOW)
        elif grade.startswith("C"):
            return colored(text, Colors.BRIGHT_YELLOW)
        elif grade.startswith("D"):
            return color_error(text)
        else:
            return color_error(text)

    def _category_label(self, cat_name: str) -> str:
        """Format a category name for display."""
        labels = {
            "color": "Color",
            "typography": "Typography",
            "spacing": "Spacing",
            "layout": "Layout",
            "accessibility": "Accessibility",
            "performance": "Performance",
            "antipattern": "Anti-Pattern",
        }
        return labels.get(cat_name, cat_name.title())
