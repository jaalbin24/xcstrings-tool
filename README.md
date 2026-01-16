# xcstrings-tool

Audit and analyze Xcode String Catalogs (`.xcstrings`) for localization completeness.

[![PyPI](https://img.shields.io/pypi/v/xcstrings-tool)](https://pypi.org/project/xcstrings-tool/)
[![Tests](https://github.com/jaalbin24/xcstrings-tool/workflows/Test/badge.svg)](https://github.com/jaalbin24/xcstrings-tool/actions)
[![Python](https://img.shields.io/pypi/pyversions/xcstrings-tool)](https://pypi.org/project/xcstrings-tool/)
[![License](https://img.shields.io/pypi/l/xcstrings-tool)](https://github.com/jaalbin24/xcstrings-tool/blob/main/LICENSE)

## The Problem

You built your iOS app in English. Now you need Spanish, French, and 10 other languages. How do you track:

- Which strings are missing translations?
- Which translations need review?
- Your overall completion percentage?

**xcstrings-tool** answers these questions.

## Installation

```bash
pip install xcstrings-tool
```

Or with pipx (recommended for CLI tools):

```bash
pipx install xcstrings-tool
```

## Quick Start

```bash
# Audit your localization status
xcstrings-tool audit Localizable.xcstrings --target es-MX

# Export missing translations to CSV
xcstrings-tool export Localizable.xcstrings --target fr

# Validate catalog structure
xcstrings-tool validate Localizable.xcstrings

# Show statistics
xcstrings-tool stats Localizable.xcstrings
```

## Features

- Comprehensive localization reports with progress tracking
- Multiple output formats: console, JSON, CSV, Markdown
- CI/CD integration with configurable thresholds
- Fast and reliable (90%+ test coverage)
- Python 3.9+ on macOS and Linux

## Commands

### audit

Analyze localization completeness for a target language.

```bash
xcstrings-tool audit Localizable.xcstrings --target es-MX
```

Options:

- `--target, -t`: Target language code (default: es-MX)
- `--format, -f`: Output format(s): console, json, csv, markdown (can specify multiple)
- `--output-dir, -o`: Directory for output files
- `--verbose, -v`: Show detailed entry lists
- `--threshold`: Fail if completion below percentage (for CI)

Examples:

```bash
# Basic audit
xcstrings-tool audit Localizable.xcstrings

# Multiple formats
xcstrings-tool audit Localizable.xcstrings -f json -f csv -o reports/

# CI integration
xcstrings-tool audit Localizable.xcstrings --threshold 80
```

### export

Export missing translations to CSV for translation vendors.

```bash
xcstrings-tool export Localizable.xcstrings --target fr
```

Options:

- `--target, -t`: Target language code (required)
- `--output, -o`: Output CSV file path

### validate

Validate String Catalog JSON structure.

```bash
xcstrings-tool validate Localizable.xcstrings
```

### stats

Show quick statistics about the catalog.

```bash
xcstrings-tool stats Localizable.xcstrings
```

## CI/CD Integration

Use the `--threshold` flag to fail builds when localization falls below a target:

```yaml
# GitHub Actions example
- name: Check localization
  run: |
    pip install xcstrings-tool
    xcstrings-tool audit Localizable.xcstrings --target es-MX --threshold 80
```

Exit codes:

- `0`: Success (or above threshold)
- `1`: Error or below threshold

## Output Formats

### Console

Beautiful terminal output with progress bars and tables.

### JSON

```json
{
  "summary": {
    "total_strings": 1231,
    "translated": 638,
    "missing_translation": 593,
    "completion_percentage": 51.8
  },
  "missing_translations": [...]
}
```

### CSV

Import into Google Sheets, Excel, or translation management systems.

### Markdown

Generate reports for documentation or GitHub issues.

## Development

```bash
# Clone repo
git clone https://github.com/jaalbin24/xcstrings-tool.git
cd xcstrings-tool

# Install with Poetry
poetry install

# Run tests
poetry run pytest

# Run linting
poetry run ruff check .
poetry run mypy src/

# Install pre-commit hooks
poetry run pre-commit install
```

## Contributing

Contributions welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License. See [LICENSE](LICENSE) for details.

## Author

Morgan Olive
