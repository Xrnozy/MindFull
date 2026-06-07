# Mindfull - Enterprise Backend Architecture Design

## 1. Executive Architecture Overview

Mindfull is a sustainability, productivity, and human-centered AI platform designed to track, score, and optimize user interaction with AI tools. The backend infrastructure is architected for high availability, security, and scalability, utilizing **FastAPI** for high-performance async processing, **Supabase** for managed PostgreSQL and Auth, and **Redis/Celery** for asynchronous task execution. 

The architecture relies on **Domain-Driven Design (DDD)** to ensure that the diverse features—Sustainability Tracking, Prompt Coach™, Gamification, and Multi-Tenant Enterprise capabilities—remain decoupled, maintainable, and scalable independently. The deployment leverages a containerized **Docker** ecosystem behind **Nginx/Traefik**, secured via a self-hosted **Tailscale** overlay network.

---

## 2. System Diagram

```mermaid
flowchart TB
    subgraph Clients
        Ext[Browser Extension]
        Web[Web Dashboard - Vercel]
        Mob[Mobile Application]
        3rd[3rd Party APIs]
    end

    subgraph API Gateway / Reverse Proxy
        Traefik[Traefik / Nginx API Gateway]
    end

    subgraph Application Tier
        FastAPI_Core[FastAPI Core Services]
        FastAPI_Worker[FastAPI Background Tasks]
    end

    subgraph Async Processing Tier
        Broker[Redis Message Broker]
        Celery[Celery / Dramatiq Workers]
    end

    subgraph Data Tier
        DB[(Supabase PostgreSQL)]
        Cache[(Redis Cache)]
        Storage[(Supabase Storage)]
    end

    subgraph Security & IAM
        SupabaseAuth[Supabase Auth / JWT]
        Tailscale[Tailscale Secure Network]
    end

    subgraph Observability
        Prometheus[Prometheus]
        Grafana[Grafana]
        OTel[OpenTelemetry Collector]
    end

    Clients -->|HTTPS/WSS| Traefik
    Traefik -->|Rate Limiting/Routing| FastAPI_Core
    
    FastAPI_Core <-->|Verify JWT| SupabaseAuth
    FastAPI_Core <-->|SQLAlchemy/Asyncpg| DB
    FastAPI_Core <-->|Read/Write| Cache
    FastAPI_Core -->|Queue Task| Broker
    
    Broker --> Celery
    Celery <-->|Write Results| DB
    
    FastAPI_Core -.->|Metrics/Traces| OTel
    Celery -.->|Metrics/Traces| OTel
    OTel --> Prometheus
    Prometheus --> Grafana
    
    classDef infra fill:#f9f,stroke:#333,stroke-width:2px;
    class Traefik,Tailscale infra;
```

---

## 3. Backend Folder Structure

The project uses a structured, Domain-Driven standard, keeping features encapsulated.

```text
backend/
├── app/
│   ├── api/                  # API Routers (v1, v2)
│   │   ├── dependencies.py   # Auth & DB dependencies
│   │   └── v1/
│   │       ├── router.py     # Aggregates all v1 routers
│   │       ├── users/
│   │       ├── organizations/
│   │       ├── sustainability/
│   │       ├── prompt_coach/
│   │       ├── wellness/
│   │       ├── gamification/
│   │       ├── forest/
│   │       └── education/
│   ├── core/                 # App-wide settings and configs
│   │   ├── config.py         # Pydantic BaseSettings
│   │   ├── security.py       # JWT, Password hashing
│   │   ├── exceptions.py     # Global exception handlers
│   │   └── logger.py         # JSON structured logging config
│   ├── db/                   # Database connection and migrations
│   │   ├── session.py        # SQLAlchemy async session maker
│   │   └── base.py           # Base declarative class
│   ├── domain/               # Bounded contexts (DDD)
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic models (DTOs)
│   │   ├── repositories/     # Data access layer
│   │   └── services/         # Business logic
│   ├── middleware/           # FastAPI middlewares
│   │   ├── rate_limit.py
│   │   ├── tenant_context.py # Multi-tenant isolation middleware
│   │   └── audit_log.py
│   ├── tasks/                # Background workers
│   │   ├── celery_app.py
│   │   ├── analytics_tasks.py
│   │   └── sustainability_tasks.py
│   └── utils/                # Helper functions (e.g., token calcs)
├── alembic/                  # Database migrations
├── docker/                   # Dockerfiles and entrypoints
├── tests/                    # Pytest suite
├── docker-compose.yml        # Infrastructure orchestration
├── pyproject.toml            # Poetry dependencies
└── main.py                   # FastAPI application entry point
```

**Purpose of Key Folders:**
* **`app/domain/`**: Enforces DDD. Services contain purely business logic, decoupled from HTTP context. Repositories handle SQLAlchemy queries. Models map to DB tables, and Schemas map to JSON payloads.
* **`app/api/`**: Thin routing layer. Extracts data from requests, calls the respective domain service, and returns serialized responses.
* **`app/tasks/`**: Celery tasks for heavy processing (e.g., carbon calculation aggregations) to ensure API endpoints remain responsive.

---

## 4. Domain-Driven Design (Bounded Contexts)

*   **Users & Identity:** Manages authentication (via Supabase), profiles, API keys, and RBAC.
*   **Organizations (Tenants):** Handles multi-tenancy, teams, billing, enterprise limits, and data isolation via Row Level Security (RLS).
*   **Sustainability Engine:** Tracks electricity, water, and carbon footprints for AI interactions.
*   **Prompt Coach™:** Analyzes prompt efficiency, token predictions, and model recommendations.
*   **Think-A-Head™ & Wellness:** Enforces delayed gratification, usage limits, reflections, and dependency scoring.
*   **Gamification & Forest:** Tracks XP, levels, achievements, green points, and digital tree planting.
*   **GreenMap™:** Public business profiles, certifications, and transparency reporting.
*   **Education:** Campus analytics, student cohorts, and retention metrics.

---

## 5. Database Design

Mindfull uses Supabase PostgreSQL. We utilize Row-Level Security (RLS) for multi-tenant isolation.

### 5.1 ER Diagram

```mermaid
erDiagram
    ORGANIZATIONS ||--o{ USERS : "contains"
    USERS ||--o{ PROMPTS : "submits"
    PROMPTS ||--o| SUSTAINABILITY_METRICS : "generates"
    PROMPTS ||--o| PROMPT_METRICS : "has"
    USERS ||--o{ AI_SESSIONS : "conducts"
    USERS ||--o{ QUIZZES : "takes"
    USERS ||--o{ FORESTS : "owns"
    FORESTS ||--o{ TREES : "grows"
    USERS ||--o{ XP_LOGS : "earns"
    USERS ||--o{ ACHIEVEMENTS : "unlocks"

    ORGANIZATIONS {
        uuid id PK
        string name
        string tier
        boolean is_educational
        timestamp created_at
    }
    USERS {
        uuid id PK
        uuid org_id FK
        string email
        string role
        integer total_xp
        float dependency_score
    }
    PROMPTS {
        uuid id PK
        uuid user_id FK
        string model_used
        integer input_tokens
        integer output_tokens
        timestamp created_at
    }
    SUSTAINABILITY_METRICS {
        uuid id PK
        uuid prompt_id FK
        float carbon_g
        float water_ml
        float electricity_wh
        float cost_usd
    }
    FORESTS {
        uuid id PK
        uuid user_id FK
        integer green_points
        integer total_trees
    }
```

### 5.2 Indexing & Partitioning Strategy
*   **Indexes:** B-Tree indexes on `user_id`, `org_id`, and `created_at` across all metric tables.
*   **Partitioning:** Time-series tables like `prompts`, `sustainability_metrics`, and `xp_logs` will be partitioned by **month** (e.g., `prompts_2026_06`) to ensure high read/write performance at scale.
*   **Audit Tables:** Use triggers to maintain `audit_logs` for any `UPDATE` or `DELETE` on critical tables (Organizations, Users, Permissions).

---

## 6. API Design

The API follows strict RESTful conventions using JSON.

**Base URL:** `https://api.mindfull.com/v1/`

| Endpoint | Method | Purpose | Auth / Role |
| :--- | :---: | :--- | :--- |
| `/auth/login` | POST | Authenticate via Supabase Auth | Public |
| `/auth/api-keys` | POST | Generate API Key for Extension | User |
| `/prompts/analyze` | POST | Analyze prompt efficiency & token prediction | User |
| `/prompts/log` | POST | Log an executed prompt & calculate metrics | User/Ext |
| `/sustainability/score` | GET | Retrieve user/org sustainability score | User/Admin |
| `/gamification/forest` | GET | Get user's forest state and green points | User |
| `/organizations/{id}/metrics`| GET | Aggregate ESG report for Enterprise | Org Admin |

**Example Request: `/prompts/log`**
```json
{
  "model": "gpt-4o",
  "input_tokens": 150,
  "output_tokens": 300,
  "duration_ms": 1200,
  "client_source": "browser_extension"
}
```

**Example Response:**
```json
{
  "id": "uuid-1234",
  "sustainability": {
    "carbon_g": 0.45,
    "water_ml": 2.1,
    "electricity_wh": 1.2,
    "cost_usd": 0.0045
  },
  "gamification": {
    "xp_gained": 10,
    "green_points_gained": 2
  }
}
```

---

## 7. Security Architecture

Mindfull adheres to OWASP API Security Top 10:

1.  **Authentication:** Leverages Supabase Auth for identity management. API uses short-lived JWTs (15 min) and Refresh Tokens (7 days).
2.  **API Keys:** For the browser extension and external APIs, we use prefix-hashed API keys (e.g., `mf_live_...`) stored securely in the database as SHA-256 hashes.
3.  **RBAC & Multi-Tenancy:**
    *   Roles: `super_admin`, `org_admin`, `team_manager`, `user`.
    *   Tenant Isolation enforced via **PostgreSQL Row Level Security (RLS)** using `current_setting('request.jwt.claims')::json->>'org_id'`.
4.  **Rate Limiting:** Redis-based sliding window rate limiter applied via FastAPI middleware.
5.  **Device Fingerprinting & Request Signing:** Extension requests include a signature (`HMAC-SHA256`) utilizing a device-specific secret to prevent replay attacks and spoofing.
6.  **Encryption:** TLS 1.3 in transit. At rest, Supabase handles AES-256 encryption. Environment secrets managed via Doppler or AWS Secrets Manager injected at runtime.
7.  **DDoS Protection:** Cloudflare / Traefik IP filtering, active connection limits, and geographically distributed failovers.

---

## 8. Analytics Architecture (Event-Driven)

High-volume events (e.g., keystrokes, prompt drafts, focus time) require non-blocking ingestion.

1.  **Ingestion:** Client sends events to `/events/batch`.
2.  **Processing:** FastAPI publishes the event to **Redis Streams**.
3.  **Workers:** Celery workers consume events, aggregate them (e.g., roll up token usage per 5 minutes), and insert them in bulk into PostgreSQL.
4.  **OLAP Sink (Future):** For analytics queries beyond standard limits, events are mirrored to an analytical DB (ClickHouse or Snowflake).

---

## 9. Background Jobs

Celery (or Dramatiq) handles all asynchronous workloads.
*   **High Priority Queue:** Prompt analysis logic, immediate gamification feedback.
*   **Default Queue:** Forest progression updates, webhook deliveries to integrations.
*   **Low Priority / Cron:** Nightly report generation, calculating weekly Sustainability/Dependency Scores, database cleanup, syncing tree-planting APIs (e.g., Ecologi).

---

## 10. Scaling Strategy

*   **10K Users:** Single API server, managed Supabase DB, single Redis instance.
*   **100K Users:** Horizontal scaling of FastAPI behind Nginx load balancer. Increase Celery workers. Read-replica for Supabase to offload dashboard analytical queries.
*   **1M Users:** Implement Redis caching layer for user profiles and leaderboards. Partition SQL tables by month. Move event ingestion to Kafka or AWS Kinesis.
*   **10M Users:** Microservice extraction (split Gamification/Sustainability from Core). Shard databases based on regions (EU vs US). Implement ClickHouse for real-time analytics.

---

## 11. Deployment Architecture (Tailscale Self-Hosted)

Deployment utilizes Docker Swarm or Docker Compose over a Tailscale private network mesh, ensuring the database and worker nodes are never exposed to the public internet.

```yaml
# docker-compose.yml
version: '3.8'
services:
  traefik:
    image: traefik:v2.10
    ports:
      - "80:80"
      - "443:443"
    networks:
      - public_net
      - tailscale_net

  api:
    build: ./backend
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
    depends_on:
      - redis
    networks:
      - tailscale_net
    environment:
      - DATABASE_URL=postgresql://user:pass@supabase_host/db

  celery_worker:
    build: ./backend
    command: celery -A app.tasks.celery_app worker -l info -c 4
    networks:
      - tailscale_net

  redis:
    image: redis:7-alpine
    networks:
      - tailscale_net

  prometheus:
    image: prom/prometheus
    networks:
      - tailscale_net

  grafana:
    image: grafana/grafana
    networks:
      - tailscale_net

networks:
  public_net:
  tailscale_net:
    driver: bridge # Managed via Tailscale Subnet Router natively on the host OS
```

---

## 12. Observability

*   **Logging:** Structured JSON logging utilizing the `structlog` library. Ingested into Loki or Datadog.
*   **Metrics:** FastAPI instrumented with `prometheus-fastapi-instrumentator`. Tracks `http_request_duration_seconds`, `db_query_time`, and custom business metrics (`total_carbon_saved`).
*   **Tracing:** OpenTelemetry (OTel) configured in FastAPI to trace requests across the API, Redis, and Celery workers.
*   **Health Checks:** `/health/liveness` and `/health/readiness` endpoints monitored by Docker and Traefik.

---

## 13. API Optimization

*   **Pagination:** Cursor-based pagination (`?cursor=xyz&limit=50`) utilized for fast traversal of large datasets (prompts, logs) without the performance hit of SQL `OFFSET`.
*   **Caching:** Redis caching for static/slow-changing endpoints (e.g., `/users/{id}/stats` cached for 5 mins). Caches invalidated via Celery hooks upon data mutation.
*   **Database Pooling:** Utilizing `PgBouncer` (native to Supabase) + SQLAlchemy async engine (`asyncpg`) to handle thousands of concurrent connections.
*   **Payload Compression:** GZIP/Brotli compression handled natively by Traefik/Nginx.

---

## 14. Sustainability Scoring Engine

The Core calculation engine resides in `app/domain/sustainability/engine.py`.

*   **Prompt Efficiency Score:** Based on Context-to-Output ratio, repetition penalties, and clarity heuristics using a localized lightweight NLP model (spaCy) or standard text heuristics before sending.
*   **Carbon Footprint ($C_f$):** 
    $C_f = (T_{in} \times PUE_{in} + T_{out} \times PUE_{out}) \times CI_{grid}$
    *(Tokens mapped to energy estimates, multiplied by the Carbon Intensity of the assumed data center grid).*
*   **Green Points System:** Points awarded = `Base_Points * Efficiency_Multiplier * Streak_Bonus`. Points map to internal thresholds that trigger external API calls to NGO partners to plant real-world trees.

---

## 15. Future Expansion

The architecture is decoupled to support the **Future Sustainability API**. By maintaining versioned routing (`/api/v1/`), issuing robust API Keys, and using an API Gateway (Traefik) for rate-limiting, third-party companies can securely send token logs to Mindfull for automated carbon calculation and ESG reporting without altering internal logic. Integrations with verified Carbon Offset platforms (e.g., Patch, Ecologi) are abstracted into isolated Service Interfaces, allowing easy swapping of providers as the marketplace grows.
