"""
Code analysis engine for UICheck-CLI.

Orchestrates the scanning and rule checking process.
Combines AST-like parsing with regex-based pattern matching
to analyze HTML/CSS/JSX/Vue SFC files.
"""

import os
import re
from typing import List, Optional, Dict
from dataclasses import dataclass, field

from .scanner import FileScanner, ScannedFile, FileFormat
from .rules.base import Rule, RuleResult, RuleCategory, RuleSeverity, rule_registry
from .rules import (
    ColorRules, TypographyRules, SpacingRules, LayoutRules,
    AccessibilityRules, PerformanceRules, AntiPatternRules,
)


@dataclass
class AnalysisReport:
    """Complete analysis report for one or more files.

    Attributes:
        results: All rule results from the analysis.
        files_scanned: Number of files scanned.
        files_skipped: Number of files skipped.
        total_issues: Total number of issues found.
        errors: Number of error-level issues.
        warnings: Number of warning-level issues.
        infos: Number of info-level issues.
        scan_root: Root path that was scanned.
    """

    results: List[RuleResult] = field(default_factory=list)
    files_scanned: int = 0
    files_skipped: int = 0
    total_issues: int = 0
    errors: int = 0
    warnings: int = 0
    infos: int = 0
    scan_root: str = ""

    def compute_counts(self) -> None:
        """Recompute issue counts from results."""
        self.total_issues = len(self.results)
        self.errors = sum(1 for r in self.results if r.severity == RuleSeverity.ERROR)
        self.warnings = sum(1 for r in self.results if r.severity == RuleSeverity.WARNING)
        self.infos = sum(1 for r in self.results if r.severity == RuleSeverity.INFO)

    def get_by_severity(self, severity: RuleSeverity) -> List[RuleResult]:
        """Filter results by severity level."""
        return [r for r in self.results if r.severity == severity]

    def get_by_category(self, category: RuleCategory) -> List[RuleResult]:
        """Filter results by category."""
        return [r for r in self.results if r.category == category]

    def get_by_file(self, file_path: str) -> List[RuleResult]:
        """Filter results by file path."""
        return [r for r in self.results if r.file_path == file_path]

    def to_dict(self) -> dict:
        """Serialize the report to a dictionary."""
        self.compute_counts()
        return {
            "scan_root": self.scan_root,
            "files_scanned": self.files_scanned,
            "files_skipped": self.files_skipped,
            "total_issues": self.total_issues,
            "errors": self.errors,
            "warnings": self.warnings,
            "infos": self.infos,
            "results": [r.to_dict() for r in self.results],
        }


class Analyzer:
    """Main analysis engine that orchestrates scanning and rule checking.

    Usage:
        analyzer = Analyzer()
        report = analyzer.analyze("/path/to/project")
        print(report.total_issues)
    """

    def __init__(self):
        """Initialize the analyzer and register all rules."""
        self.scanner = FileScanner()
        self._rules: List[Rule] = []
        self._register_all_rules()

    def _register_all_rules(self) -> None:
        """Register all built-in rules."""
        registrars = [
            ColorRules,
            TypographyRules,
            SpacingRules,
            LayoutRules,
            AccessibilityRules,
            PerformanceRules,
            AntiPatternRules,
        ]
        for registrar in registrars:
            registrar.register_all()
        self._rules = rule_registry.get_all()

    @property
    def rules(self) -> List[Rule]:
        """Get all registered rules."""
        return self._rules

    @property
    def rule_count(self) -> int:
        """Get the total number of registered rules."""
        return len(self._rules)

    def analyze(
        self,
        target: str,
        categories: Optional[List[str]] = None,
        severity_filter: Optional[str] = None,
    ) -> AnalysisReport:
        """Analyze a file or directory.

        Args:
            target: Path to a file or directory to analyze.
            categories: Optional list of category names to filter rules.
            severity_filter: Optional severity level to filter results.

        Returns:
            AnalysisReport with all findings.
        """
        report = AnalysisReport(scan_root=target)

        # Determine which rules to use
        if categories:
            rules = rule_registry.filter_by_names(categories)
        else:
            rules = self._rules

        # Scan files
        try:
            scanned_files = self.scanner.scan(target)
        except FileNotFoundError as e:
            raise FileNotFoundError(str(e))

        report.files_scanned = len(scanned_files)
        report.files_skipped = self.scanner.stats.get("skipped_files", 0)

        # Analyze each file
        for scanned in scanned_files:
            file_results = self._analyze_file(scanned, rules)
            report.results.extend(file_results)

        # Apply severity filter
        if severity_filter:
            sev = RuleSeverity(severity_filter.lower())
            report.results = [r for r in report.results if r.severity == sev]

        report.compute_counts()
        return report

    def _analyze_file(self, scanned: ScannedFile, rules: List[Rule]) -> List[RuleResult]:
        """Analyze a single scanned file with all applicable rules.

        Args:
            scanned: The ScannedFile to analyze.
            rules: List of Rule instances to apply.

        Returns:
            List of RuleResult objects from all rules.
        """
        results = []

        # Extract sections based on file format
        sections = self.scanner.extract_sections(scanned)

        # Determine which content sections to analyze
        content_sections = self._get_content_sections(scanned, sections)

        # Run each rule against appropriate content
        for rule in rules:
            for section_name, section_content in content_sections:
                if section_content.strip():
                    try:
                        rule_results = rule.check(section_content, scanned.relative_path)
                        results.extend(rule_results)
                    except Exception:
                        # Skip rules that throw errors
                        continue

        return results

    def _get_content_sections(
        self, scanned: ScannedFile, sections: Dict[str, str]
    ) -> List[tuple]:
        """Get the relevant content sections for analysis based on file format.

        Args:
            scanned: The ScannedFile being analyzed.
            sections: Extracted content sections.

        Returns:
            List of (section_name, content) tuples to analyze.
        """
        content_sections = []

        if scanned.format == FileFormat.VUE_SFC:
            # Analyze template as HTML, style as CSS
            if sections["html"]:
                content_sections.append(("html", sections["html"]))
            if sections["css"]:
                content_sections.append(("css", sections["css"]))

        elif scanned.format == FileFormat.JSX:
            # Analyze JSX content as HTML-like
            if sections["html"]:
                content_sections.append(("html", sections["html"]))
            # Also analyze full content for CSS-in-JS patterns
            content_sections.append(("css", scanned.content))

        elif scanned.format == FileFormat.HTML:
            # Analyze full HTML (includes inline styles)
            content_sections.append(("html", scanned.content))
            if sections["css"]:
                content_sections.append(("css", sections["css"]))

        elif scanned.format == FileFormat.CSS:
            content_sections.append(("css", scanned.content))

        else:
            # Unknown format: try analyzing as HTML
            content_sections.append(("html", scanned.content))

        return content_sections
