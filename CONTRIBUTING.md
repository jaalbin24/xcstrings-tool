# Contributing to xcstrings-tool

Thank you for considering contributing to xcstrings-tool!

## Development Setup

1. **Clone the repository:**

```bash
git clone https://github.com/jaalbin24/xcstrings-tool.git
cd xcstrings-tool
```

2. **Install Poetry** (if not already installed):

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. **Install dependencies:**

```bash
poetry install
```

4. **Install pre-commit hooks:**

```bash
poetry run pre-commit install
```

## Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov

# Run specific test file
poetry run pytest tests/unit/test_parser.py

# Run with verbose output
poetry run pytest -v
```

## Code Quality

We use several tools to maintain code quality:

- **ruff**: Fast linter and formatter
- **mypy**: Static type checking
- **pytest**: Testing framework

Run checks locally:

```bash
# Linting
poetry run ruff check src/ tests/

# Type checking
poetry run mypy src/

# Format code
poetry run ruff format src/ tests/
```

## Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for public functions
- Keep functions focused and small
- No emojis in code or output

## Submitting Changes

1. **Fork the repository**

2. **Create a feature branch:**

```bash
git checkout -b feature/your-feature-name
```

3. **Make your changes** with clear commit messages

4. **Add tests** for new functionality

5. **Run tests and linting:**

```bash
poetry run pytest
poetry run ruff check .
poetry run mypy src/
```

6. **Submit a pull request** with a clear description

## Pull Request Guidelines

- Keep PRs focused on a single feature or fix
- Include tests for new functionality
- Update documentation if needed
- Ensure all CI checks pass
- Write clear commit messages

## Adding New Features

When adding new features:

1. **Discuss first**: Open an issue to discuss major changes
2. **Add tests**: New code should have test coverage
3. **Update docs**: Update README and docstrings
4. **Follow patterns**: Match existing code structure

## Reporting Bugs

When reporting bugs, include:

- Python version
- Operating system
- xcstrings-tool version
- Minimal reproduction example
- Expected vs actual behavior

## Questions?

Open an issue for questions or discussion.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
