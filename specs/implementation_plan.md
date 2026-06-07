# MindFull - Complete Backend Implementation Plan

## Executive Summary

Implement the **entire production-grade backend** for MindFull based on the architecture document. The existing codebase has a skeleton: FastAPI entry point, a single `User` model, basic JWT verification, and one Alembic migration. We need to build out **all 11 bounded contexts** with full DDD layering (models → schemas → repositories → services → routers), plus cross-cutting concerns (middleware, tasks, monitoring, deployment).

## Current State

| Component | Status |
|---|---|
| FastAPI entry point (`main.py`) | ✅ Basic |
| Config (`core/config.py`) | ✅ Basic |
| Security (`core/security.py`) | ✅ Basic JWT |
| DB session (`db/session.py`) | ✅ Working |
| User model | ✅ Minimal |
| User schema | ✅ Minimal |
| User router | ✅ 2 endpoints |
| Alembic setup | ✅ 1 migration |
| Docker Compose | ✅ Basic (db, redis, api) |
| **Everything else** | ❌ Not implemented |

---

## Proposed Changes

### Phase 1: Core Infrastructure & Cross-Cutting Concerns

---

#### 1.1 Enhanced Configuration

#### [MODIFY] [config.py](file:///c:/Users/MY%20PC/Documents/Hackathon%20testing/MindFull/backend/app/core/config.py)
- Add all missing settings: JWT secrets, Redis config, Celery broker, rate limiting params, CORS origins, Supabase JWT secret, API key prefix, monitoring, OpenTelemetry, log level, environment name

#### [NEW] `backend/app/core/exceptions.py`
- Custom exception classes: `MindfullException`, `NotFoundError`, `PermissionDeniedError`, `TenantIsolationError`, `RateLimitExceededError`, `ValidationError`
- FastAPI exception handlers registered globally

#### [NEW] `backend/app/core/logger.py`
- Structured JSON logging with `structlog`
- Request ID propagation
- Context-aware log formatting

#### [NEW] `backend/app/core/redis.py`
- Async Redis connection pool (using `redis.asyncio`)
- Cache helper functions (`get_cached`, `set_cached`, `invalidate`)

#### [NEW] `backend/app/core/events.py`
- Application lifecycle events (startup/shutdown hooks for Redis, Celery, OTel)

---

#### 1.2 Security & Middleware Layer

#### [MODIFY] [security.py](file:///c:/Users/MY%20PC/Documents/Hackathon%20testing/MindFull/backend/app/core/security.py)
- Add API key generation & verification (prefix-hashed `mf_live_...`)
- Add HMAC request signing verification
- Add device fingerprint verification
- Add refresh token rotation logic

#### [NEW] `backend/app/middleware/__init__.py`
#### [NEW] `backend/app/middleware/rate_limit.py`
- Redis sliding-window rate limiter
- Per-user and per-IP rate limiting
- Configurable limits per endpoint

#### [NEW] `backend/app/middleware/tenant_context.py`
- Extract `org_id` from JWT claims
- Set tenant context for all downstream queries
- Enforce RLS-like isolation at the application layer

#### [NEW] `backend/app/middleware/audit_log.py`
- Log all mutating requests (POST/PUT/PATCH/DELETE)
- Capture: user_id, action, resource, IP, timestamp, request body hash

#### [NEW] `backend/app/middleware/request_id.py`
- Generate/propagate X-Request-ID headers for distributed tracing

#### [NEW] `backend/app/middleware/device_fingerprint.py`
- Validate device fingerprint from extension/mobile headers
- Track device sessions

---

#### 1.3 Enhanced Database Layer

#### [MODIFY] [base.py](file:///c:/Users/MY%20PC/Documents/Hackathon%20testing/MindFull/backend/app/db/base.py)
- Add `TimestampMixin` (created_at, updated_at)
- Add `TenantMixin` (org_id with index)
- Add `SoftDeleteMixin` (deleted_at)
- Import all models for Alembic discovery

#### [NEW] `backend/app/db/base_repository.py`
- Generic async CRUD repository base class
- Methods: `get_by_id`, `get_all`, `create`, `update`, `delete`, `get_paginated` (cursor-based)
- Tenant-scoped queries by default

---

#### 1.4 Enhanced Auth & Dependencies

#### [MODIFY] [dependencies.py](file:///c:/Users/MY%20PC/Documents/Hackathon%20testing/MindFull/backend/app/api/dependencies.py)
- Add `get_current_active_user` (checks soft-delete)
- Add `require_role(roles: list)` dependency factory
- Add `get_current_org` tenant extractor
- Add `get_api_key_user` for API key auth
- Add `PaginationParams` dependency

---

### Phase 2: All Domain Models (Database Layer)

Each domain follows the pattern: `app/domain/{context}/models.py`, `schemas.py`, `repository.py`, `service.py`

---

#### 2.1 Users Domain (Enhanced)

#### [MODIFY] [models.py](file:///c:/Users/MY%20PC/Documents/Hackathon%20testing/MindFull/backend/app/domain/users/models.py)
- Add: `full_name`, `avatar_url`, `org_id` FK, `is_active`, `level`, `created_at`, `updated_at`
- Add relationships to Organization, XP logs, Achievements, Forest

#### [NEW] `backend/app/domain/users/repository.py`
#### [NEW] `backend/app/domain/users/service.py`

#### [MODIFY] [schemas.py](file:///c:/Users/MY%20PC/Documents/Hackathon%20testing/MindFull/backend/app/domain/users/schemas.py)
- Add `UserUpdate`, `UserProfile`, `UserStats`

---

#### 2.2 Organizations Domain

#### [NEW] `backend/app/domain/organizations/__init__.py`
#### [NEW] `backend/app/domain/organizations/models.py`
Tables:
- `organizations` — id, name, slug, tier (free/pro/enterprise/education), logo_url, settings (JSONB), is_educational, max_members, created_at, updated_at
- `teams` — id, org_id FK, name, department, created_at
- `memberships` — id, user_id FK, org_id FK, team_id FK (nullable), role (org_admin/team_manager/member), invited_by, joined_at
- `invitations` — id, org_id, email, role, token, expires_at, accepted_at

#### [NEW] `backend/app/domain/organizations/schemas.py`
#### [NEW] `backend/app/domain/organizations/repository.py`
#### [NEW] `backend/app/domain/organizations/service.py`

---

#### 2.3 Sustainability Domain

#### [NEW] `backend/app/domain/sustainability/__init__.py`
#### [NEW] `backend/app/domain/sustainability/models.py`
Tables:
- `ai_sessions` — id, user_id FK, org_id FK, model_provider, model_name, session_start, session_end, total_input_tokens, total_output_tokens, client_source (extension/web/mobile/api)
- `prompts` — id, user_id FK, session_id FK, org_id FK, model_used, input_tokens, output_tokens, duration_ms, client_source, prompt_hash, created_at
- `sustainability_metrics` — id, prompt_id FK, user_id FK, org_id FK, carbon_g, water_ml, electricity_wh, cost_usd, grid_region, pue_factor, created_at
- `sustainability_daily_aggregates` — id, user_id FK, org_id FK, date, total_prompts, total_input_tokens, total_output_tokens, total_carbon_g, total_water_ml, total_electricity_wh, total_cost_usd, sustainability_score
- `token_usage_logs` — id, user_id FK, org_id FK, model_used, input_tokens, output_tokens, cost_usd, created_at

#### [NEW] `backend/app/domain/sustainability/engine.py`
- Carbon footprint formula: `Cf = (T_in × PUE_in + T_out × PUE_out) × CI_grid`
- Water usage estimation
- Electricity estimation
- Sustainability score algorithm
- Model-specific emission factors (GPT-4, Claude, Gemini, etc.)

#### [NEW] `backend/app/domain/sustainability/schemas.py`
#### [NEW] `backend/app/domain/sustainability/repository.py`
#### [NEW] `backend/app/domain/sustainability/service.py`

---

#### 2.4 Prompt Coach Domain

#### [NEW] `backend/app/domain/prompt_coach/__init__.py`
#### [NEW] `backend/app/domain/prompt_coach/models.py`
Tables:
- `prompt_analyses` — id, prompt_id FK, user_id FK, efficiency_score (0–100), clarity_score, specificity_score, context_ratio, repetition_penalty, token_prediction, cost_prediction, carbon_prediction, suggestions (JSONB), recommended_model, created_at
- `model_benchmarks` — id, model_name, provider, avg_tokens_per_watt, cost_per_1k_tokens_in, cost_per_1k_tokens_out, carbon_per_1k_tokens, is_active

#### [NEW] `backend/app/domain/prompt_coach/analyzer.py`
- Prompt efficiency scoring engine
- Token prediction
- Cost prediction
- Model recommendation logic

#### [NEW] `backend/app/domain/prompt_coach/schemas.py`
#### [NEW] `backend/app/domain/prompt_coach/repository.py`
#### [NEW] `backend/app/domain/prompt_coach/service.py`

---

#### 2.5 Think-A-Head Domain

#### [NEW] `backend/app/domain/think_ahead/__init__.py`
#### [NEW] `backend/app/domain/think_ahead/models.py`
Tables:
- `reflection_prompts` — id, user_id FK, original_prompt_text_hash, reflection_questions (JSONB), confidence_before, confidence_after, did_proceed, delay_seconds, created_at
- `learning_retention` — id, user_id FK, topic, retention_score, last_tested_at, decay_rate, created_at
- `dependency_scores` — id, user_id FK, score, calculation_data (JSONB), period_start, period_end, created_at

#### [NEW] `backend/app/domain/think_ahead/schemas.py`
#### [NEW] `backend/app/domain/think_ahead/repository.py`
#### [NEW] `backend/app/domain/think_ahead/service.py`

---

#### 2.6 Wellness Domain

#### [NEW] `backend/app/domain/wellness/__init__.py`
#### [NEW] `backend/app/domain/wellness/models.py`
Tables:
- `daily_goals` — id, user_id FK, date, prompt_limit, prompts_used, is_completed, created_at
- `usage_limits` — id, user_id FK, org_id FK, max_daily_prompts, max_daily_tokens, max_daily_cost_usd, cooldown_minutes, created_at, updated_at
- `wellness_reports` — id, user_id FK, period_start, period_end, total_prompts, avg_daily_prompts, dependency_trend, wellness_score, recommendations (JSONB), created_at

#### [NEW] `backend/app/domain/wellness/schemas.py`
#### [NEW] `backend/app/domain/wellness/repository.py`
#### [NEW] `backend/app/domain/wellness/service.py`

---

#### 2.7 Gamification Domain

#### [NEW] `backend/app/domain/gamification/__init__.py`
#### [NEW] `backend/app/domain/gamification/models.py`
Tables:
- `xp_logs` — id, user_id FK, amount, source (prompt_logged/quiz_completed/streak_bonus/reflection_done), reference_id, created_at
- `levels` — id, level_number, xp_required, title, badge_icon, perks (JSONB)
- `achievements` — id, user_id FK, achievement_type, title, description, icon, unlocked_at
- `achievement_definitions` — id, key, title, description, icon, criteria (JSONB), xp_reward, is_active
- `streaks` — id, user_id FK, streak_type (daily_login/daily_prompt/quiz), current_count, longest_count, last_activity_date, created_at
- `leaderboards` — id, user_id FK, org_id FK, period (weekly/monthly/all_time), score_type (sustainability/xp/green_points), score, rank, period_start, period_end

#### [NEW] `backend/app/domain/gamification/schemas.py`
#### [NEW] `backend/app/domain/gamification/repository.py`
#### [NEW] `backend/app/domain/gamification/service.py`

---

#### 2.8 Forest Domain (Mindfull Forest™)

#### [NEW] `backend/app/domain/forest/__init__.py`
#### [NEW] `backend/app/domain/forest/models.py`
Tables:
- `forests` — id, user_id FK, green_points, total_trees, total_carbon_offset_g, created_at, updated_at
- `trees` — id, forest_id FK, species, growth_stage (seed/sapling/young/mature/ancient), health, planted_at, last_watered_at, carbon_absorbed_g
- `green_point_logs` — id, user_id FK, amount, source (sustainability_action/prompt_efficiency/quiz/streak), reference_id, created_at
- `community_goals` — id, title, description, target_trees, current_trees, target_carbon_g, current_carbon_g, starts_at, ends_at, is_completed
- `campaigns` — id, title, description, sponsor_org_id FK, goal_type, target_value, current_value, starts_at, ends_at, is_active
- `sponsorships` — id, campaign_id FK, org_id FK, amount_pledged, amount_fulfilled, created_at

#### [NEW] `backend/app/domain/forest/engine.py`
- Forest growth calculations
- Tree progression logic
- Green points system

#### [NEW] `backend/app/domain/forest/schemas.py`
#### [NEW] `backend/app/domain/forest/repository.py`
#### [NEW] `backend/app/domain/forest/service.py`

---

#### 2.9 GreenMap Domain

#### [NEW] `backend/app/domain/greenmap/__init__.py`
#### [NEW] `backend/app/domain/greenmap/models.py`
Tables:
- `business_profiles` — id, org_id FK, display_name, description, logo_url, website, is_public, verified_at, created_at, updated_at
- `public_metrics` — id, profile_id FK, period, total_carbon_saved_g, total_prompts_optimized, sustainability_score, efficiency_score, updated_at
- `certifications` — id, profile_id FK, certification_name, issuer, issued_at, expires_at, document_url, verified

#### [NEW] `backend/app/domain/greenmap/schemas.py`
#### [NEW] `backend/app/domain/greenmap/repository.py`
#### [NEW] `backend/app/domain/greenmap/service.py`

---

#### 2.10 Education Domain

#### [NEW] `backend/app/domain/education/__init__.py`
#### [NEW] `backend/app/domain/education/models.py`
Tables:
- `institutions` — id, org_id FK, type (university/school), name, campus_code, created_at
- `courses` — id, institution_id FK, name, instructor_user_id FK, code, semester, created_at
- `enrollments` — id, course_id FK, user_id FK, enrolled_at
- `competitions` — id, institution_id FK, title, description, metric_type, starts_at, ends_at, prizes (JSONB)
- `competition_entries` — id, competition_id FK, user_id FK, score, rank, submitted_at
- `quizzes` — id, user_id FK, topic, questions (JSONB), created_at
- `quiz_attempts` — id, quiz_id FK, user_id FK, answers (JSONB), score, completed_at
- `campus_analytics` — id, institution_id FK, period, total_students_active, avg_sustainability_score, avg_retention_score, total_carbon_saved_g, created_at

#### [NEW] `backend/app/domain/education/schemas.py`
#### [NEW] `backend/app/domain/education/repository.py`
#### [NEW] `backend/app/domain/education/service.py`

---

#### 2.11 Reporting Domain

#### [NEW] `backend/app/domain/reporting/__init__.py`
#### [NEW] `backend/app/domain/reporting/models.py`
Tables:
- `reports` — id, org_id FK, report_type (esg/sustainability/wellness/campus), format (pdf/csv/json), parameters (JSONB), status (pending/processing/completed/failed), file_url, generated_by FK, created_at, completed_at
- `audit_logs` — id, user_id FK, org_id FK, action, resource_type, resource_id, ip_address, user_agent, request_body_hash, metadata (JSONB), created_at
- `api_keys` — id, user_id FK, org_id FK, key_prefix, key_hash, name, scopes (JSONB), is_active, last_used_at, expires_at, created_at

#### [NEW] `backend/app/domain/reporting/schemas.py`
#### [NEW] `backend/app/domain/reporting/repository.py`
#### [NEW] `backend/app/domain/reporting/service.py`

---

#### 2.12 Analytics Domain (Events)

#### [NEW] `backend/app/domain/analytics/__init__.py`
#### [NEW] `backend/app/domain/analytics/models.py`
Tables:
- `events` — id, user_id FK, org_id FK, event_type, event_data (JSONB), client_source, session_id, created_at
- `event_aggregates` — id, user_id FK, org_id FK, event_type, period (hourly/daily/weekly), count, sum_value, avg_value, period_start, period_end

#### [NEW] `backend/app/domain/analytics/schemas.py`
#### [NEW] `backend/app/domain/analytics/repository.py`
#### [NEW] `backend/app/domain/analytics/service.py`

---

### Phase 3: API Layer (All Routers)

#### [MODIFY] [router.py](file:///c:/Users/MY%20PC/Documents/Hackathon%20testing/MindFull/backend/app/api/v1/router.py)
- Register ALL domain routers

#### [MODIFY] [users/router.py](file:///c:/Users/MY%20PC/Documents/Hackathon%20testing/MindFull/backend/app/api/v1/users/router.py)
- Full CRUD + stats endpoints

#### [NEW] `backend/app/api/v1/auth/router.py`
- POST `/auth/login` — Supabase auth proxy
- POST `/auth/refresh` — Refresh token rotation
- POST `/auth/api-keys` — Generate API key
- DELETE `/auth/api-keys/{id}` — Revoke API key
- POST `/auth/device-register` — Register device fingerprint

#### [NEW] `backend/app/api/v1/organizations/router.py`
- Full CRUD for orgs, teams, memberships, invitations

#### [NEW] `backend/app/api/v1/sustainability/router.py`
- POST `/sustainability/log` — Log prompt + calculate metrics
- GET `/sustainability/score` — Get sustainability score
- GET `/sustainability/history` — Daily/weekly/monthly trends
- GET `/sustainability/leaderboard` — Org-level rankings

#### [NEW] `backend/app/api/v1/prompt_coach/router.py`
- POST `/prompt-coach/analyze` — Analyze prompt efficiency
- GET `/prompt-coach/history` — Past analyses
- GET `/prompt-coach/models` — Model recommendations

#### [NEW] `backend/app/api/v1/think_ahead/router.py`
- POST `/think-ahead/reflect` — Generate reflection questions
- POST `/think-ahead/confidence` — Log confidence tracking
- GET `/think-ahead/retention` — Learning retention data
- GET `/think-ahead/dependency-score` — AI dependency score

#### [NEW] `backend/app/api/v1/wellness/router.py`
- GET/PUT `/wellness/goals` — Daily goals
- GET/PUT `/wellness/limits` — Usage limits
- GET `/wellness/reports` — Wellness reports

#### [NEW] `backend/app/api/v1/gamification/router.py`
- GET `/gamification/xp` — XP history
- GET `/gamification/achievements` — Achievements
- GET `/gamification/streaks` — Streaks
- GET `/gamification/leaderboard` — Leaderboards
- GET `/gamification/levels` — Level definitions

#### [NEW] `backend/app/api/v1/forest/router.py`
- GET `/forest` — User's forest state
- POST `/forest/plant` — Plant a tree
- GET `/forest/trees` — List trees
- GET `/forest/community-goals` — Community goals
- GET `/forest/campaigns` — Active campaigns

#### [NEW] `backend/app/api/v1/greenmap/router.py`
- GET `/greenmap/profiles` — Public business profiles
- GET `/greenmap/profiles/{id}` — Profile detail
- PUT `/greenmap/profiles/{id}` — Update profile
- GET `/greenmap/certifications` — Certifications

#### [NEW] `backend/app/api/v1/education/router.py`
- CRUD for institutions, courses, enrollments
- GET `/education/quizzes` — List quizzes
- POST `/education/quizzes/{id}/attempt` — Submit quiz attempt
- GET `/education/competitions` — Competitions
- GET `/education/campus-analytics` — Campus metrics

#### [NEW] `backend/app/api/v1/reporting/router.py`
- POST `/reports/generate` — Queue report generation
- GET `/reports` — List reports
- GET `/reports/{id}` — Report detail/download
- GET `/audit-logs` — Audit log search

#### [NEW] `backend/app/api/v1/analytics/router.py`
- POST `/analytics/events` — Batch event ingestion
- GET `/analytics/dashboard` — Dashboard metrics
- GET `/analytics/trends` — Time-series trends

#### [NEW] `backend/app/api/v1/health/router.py`
- GET `/health/liveness` — Basic health check
- GET `/health/readiness` — Deep health check (DB, Redis, Workers)

---

### Phase 4: Background Workers

#### [NEW] `backend/app/tasks/__init__.py`
#### [NEW] `backend/app/tasks/celery_app.py`
- Celery application configuration with Redis broker
- Task routing (high/default/low priority queues)
- Beat schedule for periodic tasks

#### [NEW] `backend/app/tasks/sustainability_tasks.py`
- `calculate_sustainability_metrics` — Per-prompt carbon/water/electricity
- `aggregate_daily_sustainability` — Daily rollups
- `calculate_sustainability_scores` — Weekly score calculation

#### [NEW] `backend/app/tasks/gamification_tasks.py`
- `update_leaderboards` — Periodic leaderboard recalculation
- `check_achievements` — Achievement unlock checker
- `update_streaks` — Daily streak update

#### [NEW] `backend/app/tasks/forest_tasks.py`
- `progress_forest` — Tree growth progression
- `process_community_goals` — Community goal progress updates

#### [NEW] `backend/app/tasks/reporting_tasks.py`
- `generate_report` — Async report generation (ESG, sustainability, wellness)
- `generate_campus_analytics` — Campus analytics aggregation

#### [NEW] `backend/app/tasks/analytics_tasks.py`
- `process_event_batch` — Bulk event processing
- `aggregate_events` — Hourly/daily aggregation

#### [NEW] `backend/app/tasks/wellness_tasks.py`
- `calculate_dependency_scores` — Weekly dependency score calculation
- `generate_wellness_reports` — Periodic wellness reports
- `reset_daily_goals` — Reset daily goal counters

#### [NEW] `backend/app/tasks/quiz_tasks.py`
- `generate_retention_quiz` — Auto-generate knowledge retention quizzes

---

### Phase 5: Infrastructure & Deployment

#### [MODIFY] [docker-compose.yml](file:///c:/Users/MY%20PC/Documents/Hackathon%20testing/MindFull/docker-compose.yml)
- Add Traefik reverse proxy with TLS
- Add Celery worker service
- Add Celery beat service
- Add Prometheus service
- Add Grafana service
- Add Tailscale network configuration
- Add health checks for all services
- Add proper volume management

#### [MODIFY] [Dockerfile](file:///c:/Users/MY%20PC/Documents/Hackathon%20testing/MindFull/backend/Dockerfile)
- Upgrade to Python 3.13
- Multi-stage build
- Non-root user
- Health check instruction

#### [NEW] `backend/docker/celery.Dockerfile`
- Celery worker image

#### [NEW] `traefik/traefik.yml`
- Traefik static configuration

#### [NEW] `traefik/dynamic.yml`
- Traefik dynamic routing rules

#### [NEW] `prometheus/prometheus.yml`
- Prometheus scrape targets

#### [NEW] `grafana/provisioning/datasources/prometheus.yml`
- Grafana auto-provisioning

#### [NEW] `backend/.env.example`
- All environment variables documented

---

### Phase 6: Alembic Migration

#### [NEW] `backend/alembic/versions/0002_full_schema.py`
- Single comprehensive migration creating ALL tables for all 11 domains
- All indexes, foreign keys, and constraints
- Replaces the minimal initial migration chain

---

### Phase 7: Application Entry Point Updates

#### [MODIFY] [main.py](file:///c:/Users/MY%20PC/Documents/Hackathon%20testing/MindFull/backend/main.py)
- Add all middleware (rate limit, audit, tenant, request ID)
- Add Prometheus instrumentation
- Add OpenTelemetry tracing
- Add Redis lifecycle management
- Enhanced CORS configuration
- API metadata and documentation

#### [MODIFY] [alembic/env.py](file:///c:/Users/MY%20PC/Documents/Hackathon%20testing/MindFull/backend/alembic/env.py)
- Import ALL domain models for autogenerate support

#### [MODIFY] [pyproject.toml](file:///c:/Users/MY%20PC/Documents/Hackathon%20testing/MindFull/backend/pyproject.toml)
- Add all required dependencies: structlog, prometheus-fastapi-instrumentator, opentelemetry-*, httpx, passlib, python-multipart, email-validator

#### [MODIFY] [requirements.txt](file:///c:/Users/MY%20PC/Documents/Hackathon%20testing/MindFull/backend/requirements.txt)
- Sync with pyproject.toml additions

---

## Open Questions

> [!IMPORTANT]
> **Supabase vs Self-hosted PostgreSQL**: The current docker-compose runs a local Postgres. The architecture doc mentions Supabase PostgreSQL. Should we keep the local Postgres for development and design for Supabase in production, or remove the local Postgres entirely?

> [!IMPORTANT]
> **Celery vs Dramatiq**: The architecture doc mentions both. I'll implement with **Celery** (already in dependencies) as it's more mature. Confirm if you prefer Dramatiq instead.

> [!NOTE]
> **Scope**: This will create approximately **120+ files**. The implementation will be complete, production-grade code — not stubs. Every model has full columns, every schema has proper Pydantic validation, every service has real business logic, every repository has actual queries.

---

## Verification Plan

### Automated Tests
- Run `python -c "from app.domain.users.models import User; print('Import OK')"` for each domain to verify all imports resolve
- Verify the FastAPI app starts: `uvicorn main:app --host 0.0.0.0 --port 8000`
- Verify Docker Compose validates: `docker compose config`

### Manual Verification
- Confirm all OpenAPI docs render at `/api/v1/openapi.json`
- Verify Alembic migration generates valid SQL: `alembic upgrade head --sql`
