# Development Roadmap

## Project Vision

Create the **best open-source animal adoption platform** that any shelter can deploy in minutes, regardless of technical expertise or budget.

## Guiding Principles

1. **MVP First**: Get a working system deployed before adding bells and whistles
2. **Progressive Enhancement**: Each phase builds on the previous, nothing breaks
3. **Community Input**: Major features guided by actual shelter needs
4. **Documentation Driven**: Every feature documented before implementation
5. **Test Coverage**: Maintain >80% backend coverage, >60% frontend coverage

---

## Phase 0: Foundation (Week 1-2) - PLANNING

**Goal**: Establish project structure, tooling, and core architecture

### Deliverables
- [x] Architecture documentation
- [x] Development roadmap
- [x] Repository setup (GitHub)
- [ ] Project structure scaffolding
- [ ] Docker development environment
- [ ] Database schema design
- [ ] CI/CD pipeline (GitHub Actions)

### Technical Tasks

#### Repository Structure
```
openadopt/
├── .github/
│   └── workflows/
│       ├── backend-tests.yml
│       ├── frontend-tests.yml
│       └── docker-build.yml
├── api/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── plugins/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── api/
│   │   └── services/
│   ├── alembic/
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── web/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── pages/
│   │   ├── components/
│   │   └── lib/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml
├── docker-compose.dev.yml
├── .env.example
├── ARCHITECTURE.md
├── ROADMAP.md
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

#### Development Environment
- Docker Compose with hot reload for both backend and frontend
- PostgreSQL container with persistent volume
- Adminer for database management
- Pre-commit hooks for linting

#### Initial Database Schema
- Create Alembic migration structure
- Design all tables (users, animals, interests, activity_log)
- Add indexes for performance
- Seed data script for development

### Success Criteria
- [ ] `docker-compose up` runs entire stack
- [ ] Backend at `http://localhost:8000`, frontend at `http://localhost:5173`
- [ ] Database migrations work: `alembic upgrade head`
- [ ] Tests run: `pytest` (backend), `npm test` (frontend)
- [ ] CI pipeline passes on push

**Estimated Time**: 12-16 hours  
**Blocker Risk**: Low

---

## Phase 1: Core MVP (Week 3-5) - PRIORITY

**Goal**: Minimally viable product - admins can add animals, public can view and express interest

### Features

#### Backend
- FastAPI setup with basic routes
- SQLAlchemy models (User, Animal, Interest)
- Alembic migrations
- Authentication system (FastAPI-Users + JWT)
- Plugin system foundation (storage, email)
- CRUD endpoints for animals
- Interest submission endpoint (public)
- Activity logging

#### Frontend - Public
- Animal gallery page (grid view)
- Individual animal detail page
- Interest form submission
- Basic filters (species, size, age range)
- Responsive design (mobile-first)

#### Frontend - Admin
- Login page
- Admin dashboard (stats overview)
- Animal management (CRUD)
- Photo upload (single primary photo)
- Interest management (view, update status)
- Basic search

### Technical Implementation

#### Authentication Flow
```
1. Admin navigates to /admin
2. Redirected to /admin/login if not authenticated
3. Submit credentials → POST /api/auth/login
4. Receive JWT token, store in localStorage
5. All API requests include Authorization header
6. Token validated via FastAPI dependency injection
```

#### File Upload Flow (Phase 1 - Local Storage Only)
```
1. Admin uploads photo via form
2. POST /api/animals/{id}/photos (multipart/form-data)
3. LocalStorage plugin saves to /app/uploads
4. Return URL: http://localhost:8000/uploads/animals/{id}/{filename}
5. URL saved to animal.primary_photo_url
```

#### API Endpoints (MVP)

**Public Endpoints**:
```
GET  /api/animals              # List animals (paginated, filtered)
GET  /api/animals/{id}         # Animal details
POST /api/interests            # Submit interest
```

**Admin Endpoints** (require authentication):
```
POST   /api/auth/login         # Login
POST   /api/auth/logout        # Logout
GET    /api/auth/me            # Current user

GET    /api/admin/animals      # List all animals (more fields)
POST   /api/admin/animals      # Create animal
GET    /api/admin/animals/{id} # Animal details
PUT    /api/admin/animals/{id} # Update animal
DELETE /api/admin/animals/{id} # Delete animal
POST   /api/admin/animals/{id}/photos  # Upload photo

GET    /api/admin/interests    # List interests (paginated, filtered)
GET    /api/admin/interests/{id}       # Interest details
PUT    /api/admin/interests/{id}       # Update status, add notes
DELETE /api/admin/interests/{id}       # Delete interest

GET    /api/admin/dashboard    # Dashboard stats
```

### Database Schema (Phase 1)

#### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    role VARCHAR(20) NOT NULL,  -- 'super_admin', 'admin', 'viewer'
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);
```

#### Animals Table (Simplified for MVP)
```sql
CREATE TABLE animals (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    species VARCHAR(20) NOT NULL,
    breed VARCHAR(100),
    age_years INTEGER,
    age_months INTEGER,
    sex VARCHAR(10),
    size VARCHAR(20),
    description TEXT,
    primary_photo_url VARCHAR(500),
    status VARCHAR(20) DEFAULT 'available',
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### Interests Table
```sql
CREATE TABLE interests (
    id SERIAL PRIMARY KEY,
    animal_id INTEGER REFERENCES animals(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    message TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Testing Requirements

#### Backend
- [ ] User authentication tests
- [ ] Animal CRUD tests
- [ ] Interest submission tests
- [ ] Authorization tests (role-based access)
- [ ] Storage plugin tests (local)

#### Frontend
- [ ] Animal gallery renders correctly
- [ ] Interest form validation
- [ ] Admin login flow
- [ ] Protected routes redirect when not authenticated

### Deployment (Phase 1)

- [ ] Docker image builds successfully
- [ ] Deployed to Railway/Render
- [ ] Database migrations run on deploy
- [ ] Initial admin user created via CLI script
- [ ] Environment variables configured

### Success Criteria
- [ ] Public user can browse animals and submit interest
- [ ] Admin can login, add animals, view interests
- [ ] System deployed and accessible online
- [ ] Basic documentation (README with setup instructions)

**Estimated Time**: 25-35 hours  
**Blocker Risk**: Medium (auth complexity)

---

## Phase 2: Enhanced MVP (Week 6-7) - REFINEMENT

**Goal**: Make the system production-ready for a single shelter

### Features

#### Enhanced Animal Management
- [ ] Multiple photo support (gallery)
- [ ] Drag-and-drop photo reordering
- [ ] All animal fields (medical, behavioral, intake info)
- [ ] Bulk status updates
- [ ] Featured animals flag

#### Enhanced Interest Management
- [ ] Assign interests to admins
- [ ] Admin notes on interests
- [ ] Email notifications (via email plugin)
- [ ] Status workflow tracking

#### Search and Filtering
- [ ] Advanced filters (age range, intake date, medical status)
- [ ] Sort options (newest, oldest, name)
- [ ] Search by name/breed

#### Admin Dashboard
- [ ] Stats: total animals, by status, by species
- [ ] Recent activity feed
- [ ] Pending interests counter

#### Email System
- [ ] Console email (logs only) - default
- [ ] SMTP support
- [ ] Email templates for notifications
- [ ] Interest notification to assigned admin

### Technical Implementation

#### Photo Gallery
```
animals.additional_photos: JSONB column
[
  "https://example.com/photo1.jpg",
  "https://example.com/photo2.jpg"
]

Frontend: React Beautiful DnD for reordering
API: PUT /api/admin/animals/{id}/photos/reorder
```

#### Email Notification Flow
```
1. Interest submitted
2. Trigger email plugin: get_email_backend()
3. Send notification to admin(s)
4. Log in activity_log
```

#### Activity Log
```sql
CREATE TABLE activity_log (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    action VARCHAR(50) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id VARCHAR(50) NOT NULL,
    details JSONB,
    ip_address VARCHAR(45),
    timestamp TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_activity_timestamp ON activity_log(timestamp DESC);
CREATE INDEX idx_activity_user ON activity_log(user_id);
```

### New API Endpoints

```
PUT    /api/admin/animals/{id}/photos/reorder
DELETE /api/admin/animals/{id}/photos/{index}

PUT    /api/admin/interests/{id}/assign    # Assign to admin
POST   /api/admin/interests/{id}/notify    # Send email

GET    /api/admin/activity-log              # Recent activity
GET    /api/admin/dashboard/stats           # Dashboard metrics
```

### Success Criteria
- [ ] Admin can manage multiple photos per animal
- [ ] Interests can be assigned and tracked
- [ ] Email notifications work (SMTP configured)
- [ ] Dashboard shows useful metrics
- [ ] Activity log captures all important actions

**Estimated Time**: 15-20 hours  
**Blocker Risk**: Low

---

## Phase 3: Multi-Admin & Polish (Week 8-9) - COLLABORATION

**Goal**: Support multiple simultaneous administrators efficiently

### Features

#### User Management
- [ ] Super admin can create/edit/delete admin users
- [ ] User list page
- [ ] Role management (super_admin, admin, viewer)
- [ ] Password reset flow
- [ ] Last login tracking

#### Concurrent Admin Support
- [ ] "Claimed" interest system (prevent duplicate contact)
- [ ] Activity feed shows who did what
- [ ] Conflict detection (two admins editing same animal)
- [ ] Optional: real-time updates via polling

#### Data Export
- [ ] Export animals to CSV
- [ ] Export interests to CSV
- [ ] Adoption reports (date range)

#### UI Polish
- [ ] Loading states everywhere
- [ ] Error handling and user feedback
- [ ] Confirmation dialogs for destructive actions
- [ ] Keyboard shortcuts for power users
- [ ] Print-friendly animal pages

### Technical Implementation

#### User Management API
```
GET    /api/admin/users          # List users (super_admin only)
POST   /api/admin/users          # Create user (super_admin only)
PUT    /api/admin/users/{id}     # Update user
DELETE /api/admin/users/{id}     # Deactivate user
POST   /api/admin/users/{id}/reset-password
```

#### Conflict Detection
```python
# Optimistic locking pattern
animals.version: Integer field
GET /api/admin/animals/{id} returns {data, version: 5}
PUT /api/admin/animals/{id} includes version: 5
If current version != 5, return 409 Conflict
```

#### Export Endpoints
```
GET /api/admin/animals/export?format=csv&status=available
GET /api/admin/interests/export?format=csv&from=2024-01-01&to=2024-12-31
```

### Success Criteria
- [ ] Multiple admins can work simultaneously without conflicts
- [ ] Super admin can manage user accounts
- [ ] Data can be exported for record-keeping
- [ ] UI feels polished and professional

**Estimated Time**: 15-20 hours  
**Blocker Risk**: Low

---

## Phase 4: Open Source Release (Week 10-11) - LAUNCH

**Goal**: Prepare for public release and community contributions

### Documentation

- [ ] **README.md**: Quick start, features overview
- [ ] **INSTALLATION.md**: Detailed deployment guide
- [ ] **CONFIGURATION.md**: All env vars explained
- [ ] **DEVELOPMENT.md**: Contributing guide, setup instructions
- [ ] **API.md**: API documentation (OpenAPI exported)
- [ ] **PLUGINS.md**: Plugin system guide
- [ ] **TROUBLESHOOTING.md**: Common issues and solutions

### Deployment Options

- [ ] One-click Railway deployment
- [ ] Render blueprint
- [ ] DigitalOcean droplet guide
- [ ] Self-hosted VPS guide
- [ ] Docker Hub image published

### Marketing/Community

- [ ] Project website (GitHub Pages)
- [ ] Demo instance deployed
- [ ] Screenshots and video walkthrough
- [ ] Submit to Product Hunt, Hacker News, Reddit (r/opensource)
- [ ] Reach out to shelters for beta testing
- [ ] Create Discord/Slack for community

### Code Quality

- [ ] Code review of all components
- [ ] Refactor any messy parts
- [ ] Consistent error handling
- [ ] Security audit (dependency check, OWASP basics)
- [ ] Performance testing (100s of animals, concurrent users)

### Pre-Release Checklist

- [ ] All tests passing
- [ ] No critical security vulnerabilities
- [ ] Docker image < 500MB
- [ ] Startup time < 30 seconds
- [ ] Load test: 10 concurrent users, no errors
- [ ] Mobile-responsive on all pages
- [ ] Accessibility audit (WCAG 2.1 AA compliance)
- [ ] GDPR compliance (data export/deletion)

### Success Criteria
- [ ] Project is installable in < 5 minutes
- [ ] Documentation is comprehensive
- [ ] First external contributor merges PR
- [ ] At least one shelter adopts the system

**Estimated Time**: 20-25 hours  
**Blocker Risk**: Low

---

## Phase 5: Community Features (Week 12+) - GROWTH

**Goal**: Features requested by actual users

### Potential Features (Prioritized by Demand)

#### High Priority
- [ ] **i18n/l10n**: Multi-language support (Spanish, French priority)
- [ ] **Advanced search**: Full-text search with ElasticSearch
- [ ] **Mobile app**: React Native app for field use
- [ ] **Fostering module**: Track foster placements separately
- [ ] **Public favorites**: Anonymous users can save favorites (localStorage)
- [ ] **Success stories page**: Showcase adopted animals

#### Medium Priority
- [ ] **Automated matching**: Score adopters based on preferences
- [ ] **Waiting list**: People can join waitlist for specific animal types
- [ ] **Volunteer management**: Track volunteers and tasks
- [ ] **Medical records**: Detailed vet visit tracking
- [ ] **Donation integration**: Stripe/PayPal for adoption fees
- [ ] **Social media integration**: Auto-post new animals to Facebook/Instagram

#### Lower Priority
- [ ] **SMS notifications**: Twilio integration
- [ ] **QR codes**: Generate codes for animal cages
- [ ] **Analytics dashboard**: Adoption trends, popular breeds
- [ ] **Multi-organization**: Single instance, multiple shelters
- [ ] **Public API**: Third-party integrations
- [ ] **Calendar integration**: Schedule meet-and-greets

### Implementation Strategy

Each feature goes through:
1. **Discovery**: User interviews, requirements gathering
2. **Design**: Technical spec, UI mockups
3. **Implementation**: Development in feature branch
4. **Testing**: Full test coverage
5. **Documentation**: User guide, API docs if applicable
6. **Release**: Merge to main, deploy, announce

### Success Criteria
- Active community of contributors
- 10+ shelters using the system
- Regular releases (every 2-4 weeks)
- Responsive to bug reports and feature requests

---

## Long-Term Vision (6-12 months)

### Scale Goals
- 100+ shelters using the system
- Facilitate 1,000+ adoptions
- 50+ active contributors
- Translated into 5+ languages

### Technical Evolution
- Microservices architecture (if needed at scale)
- Real-time collaboration (WebSockets)
- Mobile apps (iOS and Android)
- Advanced ML features (image recognition, matching algorithms)
- Integration marketplace (plugins from community)

### Community Goals
- Annual survey of shelter needs
- Virtual/in-person meetup for adopters
- Case studies and success stories
- Partnership with national animal welfare orgs

---

## Risk Management

### Technical Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Database performance with 1000s of animals | High | Proper indexing, pagination, caching |
| Storage costs (if using S3/Cloudinary) | Medium | Local storage default, document optimization |
| Security vulnerabilities | High | Regular dependency updates, security audits |
| Docker image size | Low | Multi-stage builds, minimal base images |

### Product Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Low adoption by shelters | High | Beta test with real shelters, incorporate feedback |
| Complex for non-technical users | Medium | Excellent documentation, video tutorials |
| Competing with established (paid) solutions | Medium | Focus on open source benefits, customization |
| Feature creep | Medium | Strict prioritization, MVP first |

### Community Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Lack of contributors | Medium | Good documentation, "good first issue" labels |
| Burnout (maintainer) | High | Find co-maintainers early |
| Low-quality PRs | Low | Clear contributing guide, code review standards |
| Fragmentation (too many forks) | Low | Extensibility via plugins reduces need to fork |

---

## Success Metrics

### Phase 1 (MVP)
- System deployed and publicly accessible
- 1-2 beta test shelters using it
- Core features working reliably

### Phase 4 (Open Source Launch)
- 50+ GitHub stars
- 3+ contributors
- 5+ shelters interested/using
- Listed on awesome-opensource lists

### Phase 5+ (Growth)
- 200+ GitHub stars
- 10+ regular contributors
- 20+ shelters in production
- 500+ animals managed
- 100+ successful adoptions

---

## Open Questions

These will be answered as we go:

1. **Payment Processing**: Do shelters need this in v1, or is it a v2 feature?
2. **Multi-tenancy**: Single shelter focus first, or build for multiple from day one?
3. **Licensing**: MIT vs GPL vs Apache 2.0?
4. **Governance**: Solo maintainer vs steering committee?
5. **Funding**: Pure volunteer vs Open Collective vs GitHub Sponsors?
6. **Feature voting**: How do we prioritize community requests?

---

## Timeline Summary

| Phase | Duration | Key Deliverable |
|-------|----------|-----------------|
| Phase 0 | 1-2 weeks | Project structure, foundation |
| Phase 1 | 2-3 weeks | Working MVP, deployed |
| Phase 2 | 1-2 weeks | Production-ready features |
| Phase 3 | 1-2 weeks | Multi-admin support |
| Phase 4 | 1-2 weeks | Open source release |
| Phase 5+ | Ongoing | Community-driven features |

**Total to Open Source Launch**: ~10 weeks (part-time)  
**Total to Mature Product**: 6-12 months

---

## How to Contribute to This Roadmap

This roadmap is a living document. As the project evolves:

1. **Suggest changes**: Open an issue with "Roadmap" label
2. **Propose features**: Explain the use case and user story
3. **Update timeline**: Reality will differ from plan - that's OK!
4. **Prioritize differently**: If real shelters need X before Y, we adjust

The roadmap serves us, not the other way around.

---

**Document Version**: 1.0  
**Last Updated**: January 2026  
**Maintainer**: Antony  
**Status**: Initial Draft