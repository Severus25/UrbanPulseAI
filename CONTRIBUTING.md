# Contributing to UrbanPulse AI

Thank you for your interest in contributing to UrbanPulse AI! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Architecture Guidelines](#architecture-guidelines)

---

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please be respectful, inclusive, and constructive in all interactions.

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+
- Docker & Docker Compose
- Git

### Development Setup

```bash
# 1. Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/UrbanPulse_AI.git
cd UrbanPulse_AI

# 2. Create a feature branch
git checkout -b feature/your-feature-name

# 3. Set up environment
cp .env.example .env

# 4. Install Python dev dependencies
pip install -e ".[dev]"

# 5. Install frontend dependencies
cd frontend && npm install && cd ..

# 6. Install pre-commit hooks
pre-commit install

# 7. Start infrastructure services
docker-compose up -d postgres redis

# 8. Verify setup
pytest tests/unit/ -x
```

---

## Development Workflow

### Branch Naming

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feature/<description>` | `feature/congestion-heatmap` |
| Bug fix | `fix/<description>` | `fix/websocket-reconnect` |
| Documentation | `docs/<description>` | `docs/api-examples` |
| Refactor | `refactor/<description>` | `refactor/feature-store` |
| Performance | `perf/<description>` | `perf/inference-batching` |

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `ci`, `chore`

**Examples:**
```
feat(ml): add temporal fusion transformer for congestion forecasting
fix(gateway): handle missing GPS coordinates gracefully
docs(api): add WebSocket subscription examples
perf(inference): batch YOLO predictions for 3x throughput
test(agents): add integration tests for traffic reasoner
```

---

## Code Standards

### Python

- **Formatter**: [Ruff](https://github.com/astral-sh/ruff) (format)
- **Linter**: [Ruff](https://github.com/astral-sh/ruff) (check)
- **Type checker**: [mypy](https://mypy-lang.org/) (strict mode)
- **Line length**: 100 characters
- **Style**: PEP 8, with Pydantic models for data validation

```bash
# Run all checks
ruff check .
ruff format --check .
mypy services/ ml/ agents/
```

### TypeScript / React

- **Formatter**: Prettier (via ESLint)
- **Linter**: ESLint with Next.js config
- **Style**: Functional components, hooks-based state management

```bash
cd frontend
npm run lint
npm run type-check
```

### General Guidelines

1. **Type everything** — Use type hints in Python, TypeScript types in frontend
2. **Validate at boundaries** — Pydantic models for API input/output
3. **Test what matters** — Focus on behavior, not implementation details
4. **Keep services small** — Each service has a single responsibility
5. **Document decisions** — Add comments for non-obvious logic, ADRs for architecture

---

## Pull Request Process

### Before Submitting

- [ ] All tests pass locally (`pytest` and `npm test`)
- [ ] Linter passes with no warnings (`ruff check .`)
- [ ] Type checker passes (`mypy`)
- [ ] New code has appropriate test coverage
- [ ] Documentation is updated if needed
- [ ] Commit messages follow conventional commits format
- [ ] Branch is up-to-date with `main`

### PR Template

When creating a PR, include:

1. **What**: Brief description of changes
2. **Why**: Problem being solved or feature being added
3. **How**: Technical approach (if non-obvious)
4. **Testing**: How the changes were tested
5. **Screenshots**: For UI changes

### Review Process

1. At least 1 approval required for merge
2. CI pipeline must pass (tests, lint, type check, build)
3. No merge conflicts with `main`
4. Reviewer feedback addressed or discussed

---

## Issue Reporting

### Bug Reports

Include:
- **Description**: Clear description of the bug
- **Steps to reproduce**: Minimal steps to trigger the issue
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Environment**: OS, Python/Node versions, Docker version
- **Logs**: Relevant error messages or stack traces

### Feature Requests

Include:
- **Problem**: What problem does this solve?
- **Proposal**: How should it work?
- **Alternatives**: Other approaches considered
- **Impact**: Who benefits and how?

---

## Architecture Guidelines

### Adding a New Service

1. Create service directory under `services/<name>/`
2. Follow the existing FastAPI service structure
3. Add Dockerfile in `infrastructure/docker/`
4. Add to `docker-compose.yml`
5. Add health check endpoint
6. Add to CI pipeline
7. Update architecture documentation

### Adding a New ML Model

1. Create model module under `ml/<name>/`
2. Implement training script with MLflow logging
3. Add model serving endpoint in inference service
4. Add unit tests for model logic
5. Document model card (architecture, metrics, limitations)

### Adding a New Agent

1. Create agent module under `agents/<name>/`
2. Define agent state schema and tools
3. Register in the LangGraph orchestration graph
4. Add integration tests
5. Document agent capabilities and limitations

---

## Questions?

- Open a [GitHub Discussion](https://github.com/YOUR_USERNAME/UrbanPulse_AI/discussions) for general questions
- Open an [Issue](https://github.com/YOUR_USERNAME/UrbanPulse_AI/issues) for bugs or feature requests
- Check existing documentation in the `docs/` folder
