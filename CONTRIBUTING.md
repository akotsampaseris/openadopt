# Contributing to OpenAdopt

Thank you for your interest in contributing to OpenAdopt! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful, inclusive, and considerate. We're all here to help animals find homes.

## How to Contribute

### Reporting Bugs

Found a bug? Please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, browser, Docker version)
- Screenshots if applicable

### Suggesting Features

Have an idea? Open an issue with:
- Clear description of the feature
- Use case: why would this help shelters?
- Proposed implementation (if you have ideas)

### Contributing Code

1. **Fork the repository**
2. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Test your changes** (see Testing section below)
5. **Commit with clear messages**:
   ```bash
   git commit -m "Add feature: brief description"
   ```
6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Open a Pull Request**

## Development Setup

### Prerequisites
- Docker and Docker Compose
- OR: Python 3.11+, Node.js 18+, PostgreSQL 15+
- **pnpm** (this project uses pnpm, not npm)

### Installing pnpm

We use pnpm for JavaScript package management:

```bash
# Node 16.13+ has corepack built-in
corepack enable
corepack prepare pnpm@latest --activate

# Or install globally
npm install -g pnpm
```

### Quick Start

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/openadopt.git
cd openadopt

# Copy environment file
cp .env.example .env

# Start development environment
docker-compose -f docker-compose.dev.yml up -d

# Run migrations
docker-compose -f docker-compose.dev.yml exec api alembic upgrade head

# Create admin user
docker-compose -f docker-compose.dev.yml exec api python -m app.scripts.create_admin
```

### Running Locally (Without Docker)

#### Backend
```bash
cd api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd web
pnpm install
pnpm run dev
```

## Project Structure

```
openadopt/
├── api/              # Backend (FastAPI)
│   ├── app/
│   │   ├── api/      # API routes
│   │   ├── core/     # Config, database, plugins
│   │   ├── models/   # SQLAlchemy models
│   │   ├── schemas/  # Pydantic schemas
│   │   └── services/ # Business logic
│   ├── alembic/      # Database migrations
│   └── tests/        # Backend tests
├── web/              # Frontend (React)
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── lib/
│   └── tests/        # Frontend tests
└── docs/             # Documentation
```

## Coding Standards

### Python (Backend)
- **Style**: Follow PEP 8
- **Formatter**: Black (line length 100)
- **Linter**: Ruff
- **Type hints**: Use them everywhere
- **Docstrings**: Google style

```python
def create_animal(name: str, species: str) -> Animal:
    """
    Create a new animal in the database.
    
    Args:
        name: The animal's name
        species: The animal's species (dog, cat, etc.)
        
    Returns:
        Created Animal object
        
    Raises:
        ValueError: If species is invalid
    """
    pass
```

### JavaScript/React (Frontend)
- **Style**: Airbnb style guide
- **Formatter**: Prettier
- **Linter**: ESLint
- **Components**: Functional components with hooks
- **Naming**: PascalCase for components, camelCase for functions/variables

```jsx
function AnimalCard({ animal }) {
  const { name, species, age } = animal
  
  return (
    <div className="animal-card">
      <h3>{name}</h3>
      <p>{species}, {age} years old</p>
    </div>
  )
}
```

### Commit Messages

Use conventional commits:
```
type(scope): brief description

Longer description if needed

Fixes #123
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
- `feat(api): add animal search endpoint`
- `fix(web): resolve photo upload bug`
- `docs: update installation guide`

## Testing

### Backend Tests
```bash
# Run all tests
docker-compose -f docker-compose.dev.yml exec api pytest

# Run with coverage
docker-compose -f docker-compose.dev.yml exec api pytest --cov=app

# Run specific test
docker-compose -f docker-compose.dev.yml exec api pytest tests/test_animals.py
```

### Frontend Tests
```bash
cd web
pnpm test
```

### Writing Tests

**Backend** - Use pytest with async support:
```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_animals(client: AsyncClient):
    response = await client.get("/api/animals")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

**Frontend** - Use React Testing Library:
```jsx
import { render, screen } from '@testing-library/react'
import AnimalCard from './AnimalCard'

test('renders animal name', () => {
  const animal = { name: 'Buddy', species: 'dog', age: 3 }
  render(<AnimalCard animal={animal} />)
  expect(screen.getByText('Buddy')).toBeInTheDocument()
})
```

## Database Migrations

When changing models, create a migration:

```bash
# Auto-generate migration
docker-compose -f docker-compose.dev.yml exec api alembic revision --autogenerate -m "description"

# Review the generated migration in api/alembic/versions/

# Apply migration
docker-compose -f docker-compose.dev.yml exec api alembic upgrade head
```

Always review auto-generated migrations before committing!

## Pull Request Guidelines

### Before Submitting
- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Added tests for new features
- [ ] Updated documentation if needed
- [ ] Rebased on latest `main`

### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How did you test this?

## Screenshots (if applicable)

## Related Issues
Fixes #123
```

### Review Process
1. Automated tests must pass (GitHub Actions)
2. At least one maintainer approval required
3. No unresolved conversations
4. Up-to-date with `main` branch

## Plugin Development

Adding a new storage or email backend:

1. Create class inheriting from base (e.g., `StorageBackend`)
2. Implement required methods
3. Add to registry dictionary
4. Update configuration in `config.py`
5. Document in `.env.example`
6. Add tests

See `api/app/core/plugins/` for examples.

## Documentation

When adding features:
- Update relevant `.md` files
- Add docstrings to code
- Update API documentation (FastAPI auto-generates from docstrings)
- Consider adding to FAQ if it's a common question

## Questions?

- Open a [Discussion](https://github.com/yourusername/openadopt/discussions)
- Ask in [Discord](https://discord.gg/openadopt) (coming soon)
- Email: contributors@openadopt.org (coming soon)

## Recognition

Contributors are listed in:
- GitHub contributors page
- Release notes for their contributions
- Special thanks in README for significant contributions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Thank You!

Every contribution, no matter how small, helps animals find homes. Thank you for being part of OpenAdopt!