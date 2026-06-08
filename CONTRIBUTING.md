# Contributing to UICheck-CLI

Thank you for your interest in contributing to UICheck-CLI!

## Development Setup

1. Clone the repository
2. Ensure Python 3.8+ is installed
3. No additional dependencies required (zero-dependency project)

```bash
# Run directly without installation
python -m uicheck_cli --help
python -m uicheck_cli scan ./test_files

# Or install in development mode
pip install -e .
uicheck-cli --help
```

## Project Structure

```
uicheck_cli/
├── __init__.py          # Package metadata
├── __main__.py          # CLI entry point
├── cli.py               # Argument parsing
├── scanner.py           # File scanning and format detection
├── analyzer.py          # Analysis engine
├── scorer.py            # Scoring system
├── reporter.py          # Report generation
├── fixer.py             # Auto-fix suggestions
├── utils.py             # Utility functions
└── rules/
    ├── base.py          # Rule base classes
    ├── color.py         # Color rules
    ├── typography.py     # Typography rules
    ├── spacing.py       # Spacing rules
    ├── layout.py        # Layout rules
    ├── accessibility.py # Accessibility rules
    ├── performance.py   # Performance rules
    └── antipattern.py   # Anti-pattern rules
```

## Adding a New Rule

1. Create a new rule class in the appropriate `rules/*.py` file
2. Extend the `Rule` base class from `rules/base.py`
3. Implement the `check(content, file_path)` method
4. Register the rule in the corresponding `register_all()` method

Example:

```python
from .base import Rule, RuleResult, RuleSeverity, RuleCategory, rule_registry

class MyNewRule(Rule):
    rule_id = "category-NNN"
    rule_name = "My New Rule"
    category = RuleCategory.COLOR
    severity = RuleSeverity.WARNING
    description = "What this rule checks."

    def check(self, content: str, file_path: str = "") -> list:
        results = []
        # Your detection logic here
        if some_condition:
            results.append(self._make_result(
                message="Issue description",
                line=1,
                fix_suggestion="How to fix it",
                file_path=file_path,
            ))
        return results
```

## Code Style

- Use type hints for all function signatures
- Write docstrings for all public classes and methods
- Keep comments in English
- Follow PEP 8 conventions
- Zero external dependencies (stdlib only)

## Testing

```bash
python -m pytest tests/
```

## Reporting Issues

When reporting issues, please include:
- Python version
- OS and version
- The file or code that triggered the issue
- Expected vs actual behavior
