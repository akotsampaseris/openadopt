# OpenAdopt

**The open-source animal adoption platform that any shelter can deploy in minutes.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React 18+](https://img.shields.io/badge/react-18+-61dafb.svg)](https://reactjs.org/)
[![Docker](https://img.shields.io/badge/docker-ready-2496ED.svg)](https://www.docker.com/)

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
   docker-compose up -d
   ```

4. **Run database migrations**
   ```bash
   docker-compose exec web alembic upgrade head
   ```

5. **Create your first admin user**
   ```bash
   docker-compose exec web python -m app.scripts.create_admin
   ```

6. **Access the application**
   - Public site: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

That's it! Your shelter's adoption platform is now running.

---

## Documentation

- **[Architecture](ARCHITECTURE.md)**: Technical design and decisions
- **[Roadmap](ROADMAP.md)**: Development phases and timeline
- **[Installation Guide](docs/INSTALLATION.md)**: Detailed deployment instructions *(coming soon)*
- **[Configuration](docs/CONFIGURATION.md)**: All environment variables explained *(coming soon)*
- **[Contributing](CONTRIBUTING.md)**: How to contribute to OpenAdopt *(coming soon)*
- **[API Documentation](http://localhost:8000/docs)**: Interactive API docs (when running)

---

## Technology Stack

### Backend
- **FastAPI**: Modern, fast Python web framework
- **SQLAlchemy**: Powerful ORM with async support
- **PostgreSQL**: Reliable, scalable database
- **Alembic**: Database migration management
- **FastAPI-Users**: Authentication and user management

### Frontend
- **React 18**: Component-based UI library
- **Vite**: Lightning-fast build tool
- **React Router**: Client-side routing
- **React Query**: Server state management
- **Tailwind CSS**: Utility-first styling

### Infrastructure
- **Docker**: Containerization
- **Nginx**: Reverse proxy (optional)
- **Cloudinary/S3**: Image storage (optional)

---

## Plugin System

OpenAdopt uses a flexible plugin architecture for key services:

### Storage Backends
Choose where to store animal photos:
- **Local** (default): Files stored on disk
- **S3**: Amazon S3 buckets
- **Cloudinary**: CDN with image optimization

Configure via `STORAGE_BACKEND` environment variable.

### Email Backends
Choose how to send notifications:
- **Console** (default): Logs emails to console (development)
- **SMTP**: Any SMTP server (Gmail, etc.)
- **SendGrid**: SendGrid API

Configure via `EMAIL_BACKEND` environment variable.

See [Configuration Guide](docs/CONFIGURATION.md) for details.

---

## Deployment Options

OpenAdopt can be deployed anywhere Docker runs:

### Managed Platforms (Easiest)
- **Railway**: One-click deploy, ~$10/month
- **Render**: Simple deployment, free tier available
- **Fly.io**: Global deployment, generous free tier

### Self-Hosted
- **DigitalOcean Droplet**: $6/month for small shelters
- **AWS/GCP/Azure**: Use your existing cloud infrastructure
- **Home Server**: Run on-premise with dynamic DNS

See [Installation Guide](docs/INSTALLATION.md) for detailed instructions.

---

## Use Cases

OpenAdopt is perfect for:

- **Animal Shelters**: Municipal and private shelters of any size
- **Rescue Organizations**: Breed-specific or multi-species rescues
- **Foster Networks**: Manage foster placements and adoptions
- **Wildlife Rehabilitation**: Track and release wildlife
- **Sanctuary Operations**: Manage residents and sponsorships

---

## Contributing

We welcome contributions from everyone! Whether you're:
- Reporting bugs
- Suggesting features
- Improving documentation
- Submitting code
- Translating to other languages

Please read our [Contributing Guide](CONTRIBUTING.md) to get started.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/openadopt.git
cd openadopt

# Start development environment
docker-compose -f docker-compose.dev.yml up

# Backend will be at http://localhost:8000 (with hot reload)
# Frontend will be at http://localhost:5173 (with hot reload)
```

### Running Tests

```bash
# Backend tests
docker-compose exec web pytest

# Frontend tests
cd frontend && npm test
```

---

## Project Status

OpenAdopt is currently in **active development** (Phase 0-1).

- Architecture defined
- Roadmap created
- Core MVP in progress
- Open source launch planned for Q2 2026

See the [Roadmap](ROADMAP.md) for detailed timeline.

---

## Why OpenAdopt?

### vs. Commercial Solutions
- **Free forever**: No per-animal fees, no monthly subscriptions
- **Own your data**: Complete control over your shelter's information
- **Customizable**: Modify it to fit your exact needs
- **Privacy-focused**: No third-party tracking or data selling

### vs. Building Your Own
- **Production-ready**: Secure, tested, and documented
- **Active development**: Regular updates and improvements
- **Community support**: Help from other shelters and developers
- **Best practices**: Architecture designed by experienced developers

### vs. Generic Platforms
- **Purpose-built**: Designed specifically for animal adoptions
- **Workflow optimized**: Features built around shelter operations
- **Mobile-first**: Staff can use it in the field
- **Adopter-focused**: Beautiful public interface to find animals homes

---

## Screenshots

*Coming soon! Screenshots will be added as features are completed.*

---

## Roadmap Highlights

### Phase 1 (Q1 2026) - MVP
- Complete animal management
- Public gallery and interest forms
- Admin authentication and dashboard

### Phase 2 (Q2 2026) - Enhancement
- Multiple photos per animal
- Email notifications
- Advanced search and filtering

### Phase 3 (Q2 2026) - Multi-Admin
- User management
- Activity logging
- Conflict prevention

### Phase 4 (Q2 2026) - Launch
- Complete documentation
- One-click deployment
- Community building

See full [Roadmap](ROADMAP.md) for details.

---

## Acknowledgments

OpenAdopt is built with gratitude for:
- The countless shelter volunteers who inspired this project
- The open source community whose tools made this possible
- Every developer who contributes their time and expertise
- The animals waiting for their forever homes

---

## License

OpenAdopt is released under the [MIT License](LICENSE).

This means you can:
- Use it commercially
- Modify it
- Distribute it
- Use it privately

You must:
- Include the license and copyright notice

See [LICENSE](LICENSE) file for full details.

---

## Support & Community

- **Bug Reports**: [GitHub Issues](https://github.com/yourusername/openadopt/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/openadopt/discussions)
- **Email**: openadopt@example.com *(coming soon)*
- **Discord**: Join our community *(coming soon)*

---

## Support the Project

If OpenAdopt helps your shelter, consider:
- **Starring** the repository
- **Sharing** it with other shelters
- **Reporting** bugs you find
- **Contributing** code or documentation
- **Sponsoring** development *(coming soon)*

Every bit helps make OpenAdopt better for shelters everywhere!

---

## Mission

**To make professional-quality adoption management accessible to every animal shelter, regardless of budget or technical expertise.**

We believe every animal deserves a great chance at finding a home, and every shelter deserves great tools to make that happen.

---

## Made with love for animals everywhere

**OpenAdopt** - *Because every animal deserves a home, and every shelter deserves great software.*

---

### Quick Links

- [Report a Bug](https://github.com/yourusername/openadopt/issues/new?template=bug_report.md)
- [Request a Feature](https://github.com/yourusername/openadopt/issues/new?template=feature_request.md)
- [View Changelog](CHANGELOG.md) *(coming soon)*
- [Live Demo](https://demo.openadopt.org) *(coming soon)*

---

**Star this repository** if you support the mission!