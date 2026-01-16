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

## Using with AI Assistants

You can use **xcstrings-tool** with AI assistants like Claude Code to automate localization workflows. Here's a generic prompt template:

```markdown
# Task: Achieve 100% Localization for [TARGET_LANGUAGE]

## Context
You have access to:
- `path/to/Localizable.xcstrings` - The Xcode String Catalog
- `xcstrings-tool` - CLI tool for auditing localization
- Full filesystem access

## Goal
Bring the app from X% to 100% [TARGET_LANGUAGE] localization completion.

## Available Commands
```bash
# Audit current localization state
xcstrings-tool audit path/to/Localizable.xcstrings --target [LANG_CODE]

# Export missing translations to CSV
xcstrings-tool export path/to/Localizable.xcstrings --target [LANG_CODE] -o translations.csv
```

## Workflow

1. **Audit**: Run audit to identify missing translations
2. **Analyze**: Read Localizable.xcstrings to understand structure
3. **Translate**: Work in batches of 50-100 strings
   - Use web search for technical/domain-specific terms if needed
   - Maintain consistency with existing translations
4. **Edit**: Update Localizable.xcstrings directly with new translations
5. **Verify**: Re-run audit after each batch
6. **Repeat**: Continue until 100% complete

## Translation Guidelines
- Target locale: [LANGUAGE] ([LANG_CODE])
- Context: [YOUR_APP_DESCRIPTION]
- Preserve: All placeholder variables (`%@`, `%lld`, `%{variable}`, etc.)
- Match tone: Review existing translations for style consistency
- Technical terms: Research industry-standard terminology

## .xcstrings File Structure
The file is JSON with this format:
```json
{
  "strings": {
    "key_name": {
      "localizations": {
        "en": {"stringUnit": {"state": "translated", "value": "English"}},
        "[LANG_CODE]": {"stringUnit": {"state": "translated", "value": "Translation"}}
      }
    }
  }
}
```

## Success Criteria
Run `xcstrings-tool audit` and confirm:
- Missing translations: 0
- Completion percentage: 100%
- All "needs_review" items addressed

## Important Notes
- Add missing language entries to existing keys
- Preserve JSON structure exactly
- Set "state" to "translated" for completed translations
- Test in-app after major batches to verify context
```

Replace the placeholders:
- `[TARGET_LANGUAGE]` - e.g., "Spanish (Mexico)"
- `[LANG_CODE]` - e.g., "es-MX", "fr", "de"
- `[YOUR_APP_DESCRIPTION]` - Brief app description for translation context

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
