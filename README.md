# OpenAdopt

**Open source animal adoption platform for shelters and rescues**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![pnpm](https://img.shields.io/badge/pnpm-10.22+-orange.svg)](https://pnpm.io/)

OpenAdopt is a free, self-hosted platform designed to help animal shelters and rescue organizations manage their animals and connect them with loving homes. Built with modern technologies and a focus on ease of use, OpenAdopt can be deployed by anyone—no technical expertise required.

---

## Features

### For Shelter Staff
- **Animal Management**: Complete CRUD operations for managing your animals
- **Photo Galleries**: Upload and manage multiple photos per animal
- **Interest Tracking**: Receive and manage adoption interest from visitors
- **Multi-Admin Support**: Multiple staff members can work simultaneously
- **Dashboard & Analytics**: Track adoptions, pending interests, and key metrics
- **Email Notifications**: Get notified when someone expresses interest
- **Advanced Search & Filtering**: Find animals quickly by species, status, age, and more
- **Activity Logging**: Full audit trail of who did what and when

### For Adopters
- **Browse Animals**: Beautiful gallery of available animals
- **Filter & Search**: Find your perfect companion by species, size, age, etc.
- **Detailed Profiles**: Learn about each animal's personality and needs
- **Express Interest**: Simple form to declare interest in adoption
- **Mobile Friendly**: Works perfectly on phones, tablets, and desktops

### For Everyone
- **Completely Free**: No subscription fees, no hidden costs
- **Open Source**: Audit the code, customize it, contribute back
- **Easy Deployment**: One Docker command to run everything
- **Pluggable Architecture**: Swap storage and email providers easily
- **Self-Hosted**: Your data stays on your servers
- **Lightweight**: Runs on minimal hardware, costs ~$10/month to host

---

## Quick Start

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- That's it!

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/openadopt.git
   cd openadopt
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings (or use the defaults)
   ```

3. **Start the application**
   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```

4. **Run database migrations**
   ```bash
   docker-compose -f docker-compose.dev.yml exec api alembic upgrade head
   ```

5. **Create your first admin user**
   ```bash
   docker-compose -f docker-compose.dev.yml exec api python -m app.scripts.create_admin
   ```

6. **Access the application**
   - Application: http://localhost:5173 (dev server)
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Database Admin: http://localhost:8080

That's it! Your shelter's adoption platform is now running.

---

## Technology Stack

### Backend
- **FastAPI**: Modern, fast Python web framework
- **SQLAlchemy**: Powerful ORM with async support
- **PostgreSQL**: Reliable, scalable database
- **Alembic**: Database migration management
- **uv**: Fast Python package manager

### Frontend
- **React 19**: Component-based UI library
- **Vite**: Lightning-fast build tool
- **pnpm**: Fast, disk space efficient package manager
- **Tailwind CSS**: Utility-first styling

### Infrastructure
- **Docker**: Containerization for easy deployment
- **PostgreSQL**: Production-ready database

---

## Development

### Prerequisites for Local Development
- Python 3.14+
- Node.js 22+
- pnpm (install with: `corepack enable`)
- uv (install with: `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- PostgreSQL 18+

### Using pnpm

This project uses **pnpm** for JavaScript package management. pnpm is faster and more efficient than npm.

**Installing pnpm:**
```bash
# Node 16.13+ has corepack built-in
corepack enable
corepack prepare pnpm@latest --activate

# Or install globally
npm install -g pnpm
```

**Basic pnpm commands:**
```bash
pnpm install          # Install dependencies
pnpm run dev          # Run dev server
pnpm run build        # Build for production
pnpm run lint         # Run linter
pnpm test             # Run tests
```

### Development with Docker (Recommended)

Everything runs in containers with hot reload:

```bash
# Start all services
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop services
docker-compose -f docker-compose.dev.yml down
```

Your changes to `api/` and `web/` are automatically reflected.

### Development without Docker

#### Backend
```bash
cd api

# Install dependencies with uv
uv sync

# Run migrations
uv run alembic upgrade head

# Start backend
uv run uvicorn app.main:app --reload
```

Backend will be at http://localhost:8000

#### Frontend
```bash
cd web

# Install dependencies
pnpm install

# Start development server
pnpm run dev
```

Frontend will be at http://localhost:5173

---

## Documentation

- [Architecture](ARCHITECTURE.md): Technical design and decisions
- [Roadmap](ROADMAP.md): Development phases and timeline
- [Contributing](CONTRIBUTING.md): How to contribute to OpenAdopt
- [API Documentation](http://localhost:8000/docs): Interactive API docs (when running)

---

## Plugin System

OpenAdopt uses a flexible plugin architecture for key services:

### Storage Backends
Choose where to store animal photos:
- **local** (default): Files stored on disk
- **s3**: Amazon S3 buckets
- **cloudinary**: Cloudinary CDN with image optimization

Configure via `STORAGE_BACKEND` environment variable.

### Email Backends
Choose how to send notifications:
- **console** (default): Logs emails to console (development)
- **smtp**: Any SMTP server (Gmail, etc.)
- **sendgrid**: SendGrid API

Configure via `EMAIL_BACKEND` environment variable.

See [ARCHITECTURE.md](ARCHITECTURE.md) for details.

---

## Deployment

### Production with Docker

```bash
# Configure production environment
cp .env.example .env
# Edit .env with production settings

# Start production stack
docker-compose up -d

# Run migrations
docker-compose exec app alembic upgrade head

# Create admin user
docker-compose exec app python -m app.scripts.create_admin
```

### Deploy to Cloud Platforms

**Railway / Render / Fly.io:**
1. Connect your repository
2. Set environment variables
3. Deploy!

See deployment guides in [docs/](docs/) for platform-specific instructions.

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Quick start for contributors:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

---

## Project Status

OpenAdopt is currently in **active development** (Phase 0-1).

- Architecture defined
- Roadmap created  
- Foundation complete
- Core features in progress

See [ROADMAP.md](ROADMAP.md) for detailed timeline.

---

## Support & Community

- **Bug Reports**: [GitHub Issues](https://github.com/yourusername/openadopt/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/openadopt/discussions)

---

## License

OpenAdopt is released under the [MIT License](LICENSE).

---

## Mission

**To make professional-quality adoption management accessible to every animal shelter, regardless of budget or technical expertise.**

We believe every animal deserves a great chance at finding a home, and every shelter deserves great tools to make that happen.

---

## Acknowledgments

OpenAdopt is built with gratitude for:
- The countless shelter volunteers who inspired this project
- The open source community whose tools made this possible
- Every developer who contributes their time and expertise
- The animals waiting for their forever homes

---

**OpenAdopt** - *Because every animal deserves a home, and every shelter deserves great software.*

---

**Star this repository** if you support the mission!