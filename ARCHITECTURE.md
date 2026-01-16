# Architecture Documentation

## Overview

OpenAdopt is an open-source platform for animal shelters and rescue organizations to manage their animals and facilitate adoptions. The system is designed to be deployed as a single Docker container with minimal configuration, while maintaining extensibility for future growth.

## Design Principles

1. **Single Deployment Artifact**: One Docker image contains everything needed to run the system
2. **Zero-Config Default**: Works out of the box with sensible defaults (local storage, console logging)
3. **Plugin Architecture**: Core features use pluggable backends that can be swapped via environment variables
4. **Multi-Admin Ready**: Built from day one to handle multiple concurrent administrators
5. **Open Source First**: Architecture decisions favor forkability and community contributions
6. **Progressive Enhancement**: Start simple, scale up as needed

## Technology Stack

### Backend
- **Framework**: FastAPI 0.109+
  - Modern async Python framework
  - Built-in OpenAPI/Swagger documentation
  - Excellent performance characteristics
  - Strong typing with Pydantic
  
- **ORM**: SQLAlchemy 2.0+
  - Industry standard Python ORM
  - Async support
  - Migration support via Alembic
  
- **Database**: PostgreSQL 15+
  - Primary database for production
  - SQLite fallback for development/small deployments
  - JSON field support for flexible data
  
- **Authentication**: FastAPI-Users
  - Battle-tested auth library
  - JWT token support
  - Role-based access control
  - Password reset flows

### Frontend
- **Framework**: React 18+ with Vite
  - Component-based architecture
  - Large ecosystem and contributor pool
  - Excellent TypeScript support
  - Fast development experience with Vite
  
- **Routing**: React Router v6
  - Client-side routing
  - Nested routes for complex admin UI
  
- **State Management**: React Query + Context API
  - Server state managed by React Query
  - Local UI state via Context/useState
  - Optimistic updates for better UX
  
- **Styling**: Tailwind CSS
  - Utility-first CSS framework
  - Rapid UI development
  - Easy theming support

### Infrastructure
- **Containerization**: Docker + Docker Compose
  - Multi-stage builds for optimized images
  - Development and production configurations
  - Volume management for persistent data
  
- **Reverse Proxy**: Nginx (optional)
  - Can serve static files
  - SSL termination
  - Rate limiting

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Docker Container                     │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │              FastAPI Application                    │ │
│  │                                                     │ │
│  │  ┌─────────────┐  ┌──────────────┐  ┌──────────┐ │ │
│  │  │   API       │  │   Static     │  │  Admin   │ │ │
│  │  │   Routes    │  │   Files      │  │  Auth    │ │ │
│  │  │  /api/*     │  │  (React)     │  │          │ │ │
│  │  └─────────────┘  └──────────────┘  └──────────┘ │ │
│  │                                                     │ │
│  │  ┌─────────────────────────────────────────────┐  │ │
│  │  │         Plugin System                        │  │ │
│  │  │  • Storage (Local/S3/Cloudinary)            │  │ │
│  │  │  • Email (Console/SMTP/SendGrid)            │  │ │
│  │  └─────────────────────────────────────────────┘  │ │
│  │                                                     │ │
│  │  ┌─────────────────────────────────────────────┐  │ │
│  │  │         SQLAlchemy ORM                       │  │ │
│  │  └─────────────────────────────────────────────┘  │ │
│  └─────────────────┬───────────────────────────────┘ │
│                    │                                   │
│  ┌─────────────────▼───────────────────────────────┐ │
│  │         PostgreSQL Database                      │ │
│  │  • Animals  • Users  • Interests  • Activity    │ │
│  └──────────────────────────────────────────────────┘ │
│                                                          │
│  ┌──────────────────────────────────────────────────┐ │
│  │         File Storage                              │ │
│  │  • Local: /app/uploads (volume mounted)          │ │
│  │  • Remote: S3/Cloudinary (optional)              │ │
│  └──────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Request Flow

#### Public User Flow
1. Browser requests `/animals` → FastAPI serves React's index.html
2. React loads, requests `/api/animals` → FastAPI returns JSON
3. User clicks animal → React Router handles navigation client-side
4. User submits interest form → POST to `/api/interests`
5. FastAPI validates, saves to DB, triggers email plugin

#### Admin User Flow
1. Browser requests `/admin/login` → React renders login form
2. User submits credentials → POST to `/api/auth/login`
3. FastAPI validates, returns JWT token
4. React stores token, redirects to dashboard
5. All subsequent API calls include `Authorization: Bearer <token>`
6. FastAPI validates token, checks permissions, returns data

#### File Upload Flow
1. Admin uploads animal photo via React form
2. POST to `/api/animals/{id}/photos` with multipart form data
3. FastAPI receives file, calls storage plugin
4. Storage plugin uploads to configured backend (local/S3/Cloudinary)
5. Plugin returns public URL
6. FastAPI saves URL to database
7. React displays uploaded image

## Data Model

### Core Entities

#### User (Admin)
```python
- id: UUID (primary key)
- email: String (unique, indexed)
- password_hash: String
- role: Enum (super_admin, admin, viewer)
- first_name: String
- last_name: String
- is_active: Boolean
- created_at: DateTime
- last_login: DateTime
```

**Roles**:
- `super_admin`: Full access, can manage other users
- `admin`: Can manage animals and interests, no user management
- `viewer`: Read-only access to admin panel

#### Animal
```python
- id: Integer (primary key)
- name: String (required)
- species: Enum (dog, cat, rabbit, bird, other)
- breed: String
- age_years: Integer
- age_months: Integer
- sex: Enum (male, female, unknown)
- size: Enum (small, medium, large, extra_large)
- color: String

# Intake information
- intake_date: Date
- source: Enum (stray, owner_surrender, transfer, born_in_care)
- intake_notes: Text

# Medical information
- medical_notes: Text
- vaccination_status: Enum (unknown, partial, complete, overdue)
- spay_neuter_status: Enum (unknown, intact, neutered, scheduled)
- special_needs: Boolean
- special_needs_description: Text

# Behavioral information
- temperament_notes: Text
- good_with_kids: Enum (unknown, yes, no, older_kids_only)
- good_with_dogs: Enum (unknown, yes, no)
- good_with_cats: Enum (unknown, yes, no)
- energy_level: Enum (low, moderate, high, very_high)

# Media
- primary_photo_url: String
- additional_photos: JSON Array[String]

# Status
- status: Enum (available, pending, adopted, fostered, medical_hold, not_available)
- featured: Boolean (for homepage highlighting)
- adoption_fee: Decimal (nullable)

# Metadata
- created_by: UUID (foreign key to User)
- created_at: DateTime
- updated_at: DateTime
- adopted_at: DateTime (nullable)
```

#### InterestDeclaration
```python
- id: Integer (primary key)
- animal_id: Integer (foreign key to Animal)

# Contact information
- name: String (required)
- email: String (required, indexed)
- phone: String

# Application details
- experience_text: Text (previous pet experience)
- living_situation: Enum (house, apartment, farm, other)
- has_yard: Boolean
- has_other_pets: Boolean
- message: Text

# Status tracking
- status: Enum (pending, contacted, visit_scheduled, approved, declined, withdrawn)
- assigned_to: UUID (foreign key to User, nullable)
- admin_notes: Text (visible only to admins)
-
# Metadata
- created_at: DateTime
- updated_at: DateTime
- contacted_at: DateTime (nullable)
```

#### ActivityLog
```python
- id: Integer (primary key)
- user_id: UUID (foreign key to User)
- action: String (created, updated, deleted, status_changed, etc.)
- entity_type: Enum (animal, interest, user)
- entity_id: String (polymorphic reference)
- details: JSON (free-form details about the action)
- ip_address: String (for security auditing)
- timestamp: DateTime
```

### Database Indexes

Critical indexes for performance with hundreds of animals:

```sql
-- Animals
CREATE INDEX idx_animals_status ON animals(status);
CREATE INDEX idx_animals_species ON animals(species);
CREATE INDEX idx_animals_featured ON animals(featured) WHERE featured = true;
CREATE INDEX idx_animals_created_at ON animals(created_at DESC);

-- Interests
CREATE INDEX idx_interests_animal_id ON interests(animal_id);
CREATE INDEX idx_interests_status ON interests(status);
CREATE INDEX idx_interests_email ON interests(email);
CREATE INDEX idx_interests_created_at ON interests(created_at DESC);

-- Activity logs
CREATE INDEX idx_activity_user_id ON activity_log(user_id);
CREATE INDEX idx_activity_entity ON activity_log(entity_type, entity_id);
CREATE INDEX idx_activity_timestamp ON activity_log(timestamp DESC);
```

## Plugin System

### Design Philosophy

The plugin system allows swapping implementations without code changes. Each plugin category has:

1. **Abstract base class** defining the interface
2. **Multiple implementations** of that interface
3. **Registry** mapping config values to implementations
4. **Factory function** that reads config and returns configured instance

### Storage Plugin

**Implementations**:
- `LocalStorage`: Files stored in container volume (default)
- `S3Storage`: AWS S3 bucket (requires boto3)
- `CloudinaryStorage`: Cloudinary CDN (requires cloudinary)

**Interface**:
```python
class StorageBackend(ABC):
    async def upload(file: BinaryIO, path: str) -> str
    async def delete(path: str) -> bool
    async def get_url(path: str) -> str
```

**Configuration**:
```bash
STORAGE_BACKEND=local  # or 's3' or 'cloudinary'
```

### Email Plugin

**Implementations**:
- `ConsoleEmail`: Prints to logs (default, dev mode)
- `SMTPEmail`: Standard SMTP (Gmail, etc.)
- `SendGridEmail`: SendGrid API (requires sendgrid)

**Interface**:
```python
class EmailBackend(ABC):
    async def send(to: List[str], subject: str, body: str, html: str = None)
```

**Configuration**:
```bash
EMAIL_BACKEND=console  # or 'smtp' or 'sendgrid'
```

### Adding New Plugins

To add a new storage backend:

1. Create class inheriting from `StorageBackend`
2. Implement required methods
3. Add to `STORAGE_BACKENDS` registry
4. Document configuration in `.env.example`
5. (Optional) Add to Dockerfile dependencies

Future plugin categories (not implemented yet):
- Payment processors (Stripe, PayPal)
- SMS providers (Twilio)
- Analytics (Google Analytics, Plausible)
- External integrations (PetFinder API, shelter management software)

## Security

### Authentication
- JWT tokens with configurable expiration
- Refresh token support
- Password hashing with bcrypt
- Rate limiting on auth endpoints

### Authorization
- Role-based access control (RBAC)
- Route-level permission checking
- Row-level permissions for sensitive data

### API Security
- CORS configuration
- Input validation with Pydantic
- SQL injection prevention via SQLAlchemy ORM
- XSS prevention (React escapes by default)
- File upload validation (type, size, content)

### Deployment Security
- Secrets via environment variables (never in code)
- HTTPS only in production (via reverse proxy)
- Security headers (CSP, HSTS, etc.)
- Regular dependency updates

## Deployment

### Development

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

### Production (Docker)

```bash
# Build and run
docker-compose up -d

# Migrations
docker-compose exec web alembic upgrade head

# Create first admin user
docker-compose exec web python -m app.scripts.create_admin
```

### Hosting Options

**Free Tier Options** (for small shelters):
- Railway (PostgreSQL + app hosting)
- Render (PostgreSQL + app hosting)
- Fly.io (app hosting, bring your own PostgreSQL)

**Paid Options** (for scaling):
- DigitalOcean App Platform ($12/month+)
- AWS ECS/Fargate
- Any VPS with Docker support

**Recommended for Production**:
- Railway: $5/month for PostgreSQL, $5/month for app = $10/month total
- Cloudinary free tier for images (25GB storage, 25GB bandwidth)
- SendGrid free tier for emails (100/day)

**Total cost for typical shelter**: ~$10/month

## Performance Considerations

### Current Scale (Hundreds of Animals)
- Database queries optimized with proper indexes
- Pagination on all list endpoints (default 50 items)
- Image thumbnails generated on upload
- Lazy loading for image galleries

### Future Optimizations (Thousands of Animals)
- Redis caching layer for frequently accessed data
- ElasticSearch for advanced search/filtering
- CDN for static assets (Cloudflare)
- Database read replicas
- Background job queue (Celery/RQ) for async tasks

## Testing Strategy

### Backend
- Unit tests: Models, services, utilities
- Integration tests: API endpoints with test database
- Plugin tests: Each storage/email backend

### Frontend
- Component tests: React Testing Library
- Integration tests: User flows with Mock Service Worker
- E2E tests: Playwright (critical paths only)

### CI/CD
- GitHub Actions for automated testing
- Automated Docker builds on merge to main
- Deployment via Railway/Render webhooks

## Extensibility Points

### Easy to Extend
1. **Add new animal species**: Add enum value, no code changes
2. **Add custom fields**: Use JSON columns for flexibility
3. **Add new plugins**: Follow plugin interface pattern
4. **Customize email templates**: Template files with variables
5. **Add reports**: New API endpoint + React page

### Requires Code Changes
1. **Change data model**: Alembic migration required
2. **Add new entity types**: Models + API + UI
3. **Complex workflows**: May need state machine library
4. **Multi-organization support**: Significant refactor (tenant isolation)

## Future Architecture Considerations

### Multi-Tenancy (Multiple Shelters on One Instance)
- Add `organization_id` to all tables
- Row-level security in database
- Organization-specific domains/subdomains
- Isolated file storage per organization

### Mobile App Support
- API already mobile-ready (RESTful JSON)
- Consider React Native app sharing business logic
- Push notifications for admins (Firebase Cloud Messaging)

### Advanced Matching
- ML-based adopter-animal matching
- Personality questionnaires
- Recommendation engine

### Public API
- OAuth2 for third-party integrations
- Rate limiting and API keys
- Webhooks for external systems
- OpenAPI documentation already included

## Migration Strategy

### For Existing Shelters
- CSV import tool for bulk animal data
- Image migration script (local → S3/Cloudinary)
- User account creation via CLI
- No downtime migration plan

### From Other Systems
- PetPoint export format supported
- ShelterLuv CSV compatibility
- Custom import scripts as needed

## Monitoring and Observability

### Application Metrics
- Request/response times
- Error rates and types
- Database query performance
- Storage usage

### Business Metrics
- Animals added/adopted per day
- Average time to adoption
- Interest conversion rates
- User activity levels

### Logging
- Structured JSON logs
- Log levels: DEBUG, INFO, WARNING, ERROR
- Centralized logging (optional: Papertrail, Logtail)

### Alerting
- Email on critical errors
- Slack/Discord webhook integration
- Uptime monitoring (UptimeRobot, Pingdom)

## License and Contributions

- **License**: MIT (to be confirmed)
- **Contributions**: Welcome via GitHub PRs
- **Code Style**: Black (Python), Prettier (JavaScript)
- **Commit Convention**: Conventional Commits

## Technical Debt and Known Limitations

### Current Limitations
- No real-time updates (requires polling)
- No offline support
- Single-language only (English)
- Basic search (no full-text search)

### Planned Improvements
- WebSocket support for real-time updates
- PWA for offline capabilities
- i18n/l10n support
- ElasticSearch integration

## Decision Log

### Why FastAPI over Flask/Django?
- Modern async support
- Automatic OpenAPI docs
- Type safety with Pydantic
- Better performance
- Growing ecosystem

### Why React over Vue/Svelte?
- Largest contributor pool
- Most mature ecosystem
- Better for complex admin UIs
- Mobile path via React Native

### Why PostgreSQL over MySQL?
- Better JSON support
- More advanced features (CTEs, window functions)
- Superior full-text search
- Better for open source (less Oracle influence)

### Why JWT over sessions?
- Stateless (easier to scale)
- Works across multiple instances
- Mobile-friendly
- Standard approach for SPAs

### Why not use a CMS (WordPress, Strapi)?
- Custom data model requirements
- Performance for hundreds of animals
- Full control over features
- Cleaner architecture for contributors

---

**Document Version**: 1.0  
**Last Updated**: January 2026  
**Maintainer**: Antony  
**Status**: Initial Draft