# SYSTEM ARCHITECT PROMPT

You are a Principal Backend Architect, Senior Security Engineer, Cloud Infrastructure Engineer, and SaaS Systems Designer.

Design a COMPLETE production-grade backend architecture for the following platform:

# PROJECT

Mindfull

A Sustainability, Productivity, and Human-Centered AI Platform.

Mindfull consists of:

1. Browser Extension
2. Web Dashboard (deployed on Vercel)
3. Mobile Application
4. Self-hosted Backend Infrastructure accessible through Tailscale
5. FastAPI Backend
6. Supabase Database
7. REST API Architecture
8. Event-Driven Analytics System

The output should ONLY focus on backend architecture and infrastructure.

Do NOT focus on frontend implementation.

---

# TECH STACK REQUIREMENTS

Backend:

* FastAPI
* Python 3.13+
* Pydantic v2
* SQLAlchemy 2.0
* Alembic

Database:

* Supabase PostgreSQL

Caching:

* Redis

Task Queue:

* Celery or Dramatiq

Authentication:

* Supabase Auth
* JWT
* Refresh Tokens
* Role Based Access Control (RBAC)

Storage:

* Supabase Storage

Monitoring:

* Prometheus
* Grafana

Logging:

* Structured JSON Logging
* OpenTelemetry

Deployment:

* Docker
* Docker Compose
* Self-hosted Server
* Tailscale Network

Reverse Proxy:

* Nginx
  or
* Traefik

Security:

* OWASP API Security Top 10 compliance
* Rate Limiting
* API Keys
* Device Fingerprinting
* Request Signing
* Audit Logs
* Encryption at Rest
* Encryption in Transit
* Secrets Management
* Secure Session Management
* DDoS Protection Strategy

---

# BUSINESS REQUIREMENTS

Design backend support for:

## AI Sustainability Intelligence

* Carbon Footprint Tracking
* Water Usage Estimation
* Electricity Usage Estimation
* Token Usage Tracking
* Cost Tracking
* Sustainability Score
* Personal Dashboard
* Organization Dashboard

## Prompt Coach™

* Prompt Analyzer
* Prompt Efficiency Scoring
* Token Prediction
* Cost Prediction
* Carbon Prediction
* Context Suggestions
* Model Recommendation Engine

## Think-A-Head™

* Reflection Questions
* Delayed Gratification System
* Confidence Tracking
* Learning Retention Tracking
* AI Dependency Score
* Knowledge Retention Quizzes

## AI Wellness

* Daily Prompt Goals
* Usage Limits
* Wellness Reports
* Dependency Analytics

## Gamification

* XP System
* Levels
* Achievements
* Streaks
* Sustainability Leaderboards

## Mindfull Forest™

* Green Points
* Tree Progression System
* Forest Growth Engine
* Community Goals
* Sponsorship Tracking
* Environmental Campaign Tracking

## GreenMap™

* Public Business Profiles
* Sustainability Transparency
* Public Metrics
* Certification Tracking

## Enterprise Suite

* Multi-Tenant Organizations
* Teams
* Departments
* ESG Reporting
* Governance
* Analytics

## Education Features

* Universities
* Schools
* Competitions
* Campus Analytics
* Learning Retention Metrics

## Future Sustainability API

Design backend architecture so that third-party companies can integrate through APIs.

---

# ARCHITECTURE REQUIREMENTS

Create:

## 1. High-Level Architecture Diagram

Show:

Extension
Web Dashboard
Mobile App
API Gateway
FastAPI Services
Redis
Supabase
Analytics Engine
Background Workers
Monitoring Stack

Explain all interactions.

---

## 2. Backend Folder Structure

Generate a complete enterprise-grade folder structure.

Example:

backend/
app/
api/
core/
models/
schemas/
services/
repositories/
tasks/
middleware/
analytics/
gamification/
sustainability/
forest/
organizations/
education/
etc.

Explain the purpose of every folder.

---

## 3. Domain-Driven Design

Separate bounded contexts:

* Users
* Organizations
* Sustainability
* Prompt Coach
* Think-A-Head
* Wellness
* Gamification
* Forest
* GreenMap
* Education
* Reporting

Explain why each context exists.

---

## 4. Database Design

Generate:

* ER Diagram
* Database Tables
* Relationships
* Indexing Strategy
* Partitioning Strategy
* Audit Tables

Include all entities.

Examples:

users
organizations
teams
memberships
prompts
prompt_metrics
sustainability_metrics
ai_sessions
quizzes
quiz_attempts
dependency_scores
achievements
xp_logs
green_points
forests
trees
campaigns
leaderboards
reports
audit_logs

etc.

---

## 5. API Design

Design REST APIs.

Include:

Authentication APIs
User APIs
Organization APIs
Analytics APIs
Prompt APIs
Forest APIs
Gamification APIs
Reporting APIs

For every endpoint provide:

* URL
* Method
* Request Schema
* Response Schema
* Permissions

---

## 6. Security Architecture

Design:

* Authentication Flow
* JWT Strategy
* Refresh Token Rotation
* API Key System
* RBAC
* Tenant Isolation
* Request Validation
* Rate Limiting
* Abuse Prevention
* Audit Logging

Include threat models and mitigations.

---

## 7. Multi-Tenant SaaS Architecture

Design enterprise-ready multi-tenancy.

Support:

* Individual users
* Teams
* Organizations
* Universities

Include:

* Tenant isolation
* Tenant roles
* Organization ownership
* Team permissions

---

## 8. Analytics Architecture

Design an event-driven analytics pipeline.

Track:

* Prompt submissions
* AI usage
* Carbon metrics
* Learning behavior
* Retention scores
* Sustainability metrics

Show event flow.

---

## 9. Background Jobs

Design worker architecture.

Examples:

* Sustainability calculations
* Carbon calculations
* Quiz generation
* Report generation
* Leaderboard updates
* Forest progression updates
* Notification delivery

---

## 10. Scaling Strategy

Explain how to scale:

10K users
100K users
1M users
10M users

Include:

* Horizontal scaling
* Caching strategy
* Read replicas
* Queue scaling
* API optimization

---

## 11. Deployment Architecture

Generate:

Docker Architecture
Docker Compose Structure

Services:

* FastAPI
* Redis
* Workers
* Nginx/Traefik
* Monitoring

Explain deployment on a self-hosted server through Tailscale.

---

## 12. Observability

Design:

* Logging
* Metrics
* Tracing
* Health Checks
* Alerting

---

## 13. API Optimization

Design:

* Pagination
* Cursor Pagination
* Caching
* Query Optimization
* Database Optimization
* Connection Pooling
* Compression
* Async Processing

---

## 14. Sustainability Scoring Engine

Design formulas and architecture for:

* Sustainability Score
* AI Dependency Score
* Prompt Efficiency Score
* Green Points System

Provide backend implementation approach.

---

## 15. Future Expansion

Design architecture so the system can later support:

* AI Sustainability API Marketplace
* Sustainability Credits
* NGO Integrations
* Carbon Offset Integrations
* Tree Planting Providers
* Enterprise White Label Solutions

---

# OUTPUT FORMAT

Provide:

1. Executive Architecture Overview
2. System Diagram
3. Backend Folder Structure
4. Database Design
5. API Design
6. Security Design
7. Multi-Tenant Design
8. Analytics Design
9. Scaling Design
10. Deployment Design
11. Implementation Roadmap

The design must be production-grade, secure, scalable, maintainable, and optimized for a startup that expects enterprise customers in the future.

Assume the platform may eventually serve millions of users.
