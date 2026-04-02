"""
Test cases for URL compression testing.
Each test case is a string of varying length and content type.
All content is plain text that would realistically be shared via URL.
"""

TEST_CASES = {}

# --- TINY (100-500 chars) ---

TEST_CASES["tiny_note"] = "Remember to update the deploy config before Friday. The staging env is using the old API key and it's causing 401s on the /v2/users endpoint."

TEST_CASES["tiny_error"] = """TypeError: Cannot read properties of undefined (reading 'map')
    at UserList (src/components/UserList.tsx:42:18)
    at renderWithHooks (node_modules/react-dom/cjs/react-dom.development.js:14985:18)
    at mountIndeterminateComponent (node_modules/react-dom/cjs/react-dom.development.js:17811:13)"""

TEST_CASES["tiny_config"] = """{
  "database": {
    "host": "db-prod-replica.internal",
    "port": 5432,
    "name": "deck_production",
    "pool_size": 20
  },
  "redis": {
    "host": "redis-cluster.internal",
    "port": 6379
  }
}"""

TEST_CASES["tiny_sql"] = """SELECT t.name, COUNT(s.id) as session_count,
       AVG(s.duration_ms) as avg_duration
FROM teams t
JOIN sessions s ON s.team_id = t.id
WHERE s.created_at > NOW() - INTERVAL '7 days'
  AND s.status = 'completed'
GROUP BY t.name
ORDER BY session_count DESC
LIMIT 20;"""

# --- SMALL (500-1500 chars) ---

TEST_CASES["small_readme"] = """# Quick Start

Install dependencies:
```bash
npm install
```

Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

Run the development server:
```bash
npm run dev
```

The app will be available at http://localhost:3000.

## Project Structure
- `src/api/` - API route handlers
- `src/components/` - React components
- `src/hooks/` - Custom React hooks
- `src/lib/` - Utility functions and shared logic
- `src/types/` - TypeScript type definitions

## Testing
Run the test suite with:
```bash
npm test
```

For watch mode:
```bash
npm run test:watch
```"""

TEST_CASES["small_meeting_notes"] = """Meeting Notes - Sprint Planning 2026-03-28

Attendees: Franco, Sarah, Mike, Priya

## Action Items
1. Franco: Finish the job definition migration by Wednesday
2. Sarah: Review the new scraper architecture PR
3. Mike: Set up monitoring dashboards for the new pipeline
4. Priya: Write integration tests for the billing module

## Decisions
- We're moving forward with the BedrockAgent approach for the new obstacle courses
- The legacy Claude PLAYWRIGHT connections will be deprecated by end of Q2
- We'll use Linear for tracking instead of the spreadsheet

## Blockers
- The staging environment is flaky - DevOps ticket created (INFRA-2341)
- Need access to the client's sandbox API - waiting on their security team
- Memory file updates are not propagating to prod - investigating

## Next Sprint Goals
- Complete the agent memory feature rollout
- Ship the dashboard v2 with the new session viewer
- Reduce average scraping session time by 15%"""

TEST_CASES["small_code_typescript"] = """import { useState, useEffect, useCallback } from 'react';

interface Session {
  id: string;
  teamId: string;
  sourceCode: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  createdAt: string;
  duration?: number;
  error?: string;
}

export function useSessions(teamId: string) {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchSessions = useCallback(async () => {
    try {
      setLoading(true);
      const response = await fetch(`/api/teams/${teamId}/sessions`);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      setSessions(data.sessions);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  }, [teamId]);

  useEffect(() => {
    fetchSessions();
    const interval = setInterval(fetchSessions, 30000);
    return () => clearInterval(interval);
  }, [fetchSessions]);

  return { sessions, loading, error, refresh: fetchSessions };
}"""

TEST_CASES["small_api_response"] = """{
  "data": {
    "connections": [
      {
        "id": "conn_8a4f2b1c",
        "team_id": "fc9eda3b-91ba-481b-c1e6-08ddaf38eeb9",
        "source_code": "APP_RIPPLING_COM",
        "status": "active",
        "last_session": {
          "id": "sess_e7d3a912",
          "status": "completed",
          "started_at": "2026-03-30T14:22:00Z",
          "completed_at": "2026-03-30T14:25:33Z",
          "bills_fetched": 12,
          "accounts_discovered": 3
        },
        "credentials": {
          "username": "admin@company.com",
          "has_mfa": true,
          "last_rotated": "2026-03-15T00:00:00Z"
        }
      },
      {
        "id": "conn_3c7e9d4a",
        "team_id": "fc9eda3b-91ba-481b-c1e6-08ddaf38eeb9",
        "source_code": "WWW_FPL_COM",
        "status": "error",
        "last_session": {
          "id": "sess_b1f4c823",
          "status": "failed",
          "started_at": "2026-03-30T15:00:00Z",
          "error": "MFA challenge timeout - no response within 120s"
        }
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 2
    }
  }
}"""

# --- MEDIUM (1500-5000 chars) ---

TEST_CASES["medium_python_module"] = '''"""
Job Definition Manager - handles CRUD operations for scraping job definitions.
"""
import json
import hashlib
from datetime import datetime, timezone
from typing import Optional
from dataclasses import dataclass, field

@dataclass
class InputSchema:
    required_fields: list[str] = field(default_factory=list)
    optional_fields: list[str] = field(default_factory=list)
    field_types: dict[str, str] = field(default_factory=dict)

    def validate(self, inputs: dict) -> list[str]:
        errors = []
        for f in self.required_fields:
            if f not in inputs:
                errors.append(f"Missing required field: {f}")
            elif f in self.field_types:
                expected = self.field_types[f]
                if expected == "string" and not isinstance(inputs[f], str):
                    errors.append(f"Field {f} must be a string")
                elif expected == "integer" and not isinstance(inputs[f], int):
                    errors.append(f"Field {f} must be an integer")
        return errors


@dataclass
class OutputSchema:
    fields: list[str] = field(default_factory=list)
    format: str = "json"


@dataclass
class JobDefinition:
    name: str
    source_code: str
    prompt: str
    version: int = 1
    input_schema: InputSchema = field(default_factory=InputSchema)
    output_schema: OutputSchema = field(default_factory=OutputSchema)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    checksum: str = ""

    def __post_init__(self):
        if not self.checksum:
            self.checksum = self._compute_checksum()

    def _compute_checksum(self) -> str:
        content = json.dumps({
            "name": self.name,
            "source_code": self.source_code,
            "prompt": self.prompt,
            "version": self.version,
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()[:12]

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "source_code": self.source_code,
            "prompt": self.prompt,
            "version": self.version,
            "input_schema": {
                "required_fields": self.input_schema.required_fields,
                "optional_fields": self.input_schema.optional_fields,
                "field_types": self.input_schema.field_types,
            },
            "output_schema": {
                "fields": self.output_schema.fields,
                "format": self.output_schema.format,
            },
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "checksum": self.checksum,
        }


class JobDefinitionManager:
    def __init__(self, api_client):
        self.api = api_client
        self._cache: dict[str, JobDefinition] = {}

    async def get(self, name: str) -> Optional[JobDefinition]:
        if name in self._cache:
            return self._cache[name]
        response = await self.api.get(f"/job-definitions/{name}")
        if response.status == 404:
            return None
        data = response.json()
        job_def = self._parse(data)
        self._cache[name] = job_def
        return job_def

    async def create(self, job_def: JobDefinition) -> JobDefinition:
        response = await self.api.post("/job-definitions", json=job_def.to_dict())
        response.raise_for_status()
        created = self._parse(response.json())
        self._cache[created.name] = created
        return created

    async def update(self, name: str, prompt: str) -> JobDefinition:
        existing = await self.get(name)
        if not existing:
            raise ValueError(f"Job definition not found: {name}")
        existing.prompt = prompt
        existing.version += 1
        existing.updated_at = datetime.now(timezone.utc)
        existing.checksum = existing._compute_checksum()
        response = await self.api.put(f"/job-definitions/{name}", json=existing.to_dict())
        response.raise_for_status()
        updated = self._parse(response.json())
        self._cache[name] = updated
        return updated

    def _parse(self, data: dict) -> JobDefinition:
        return JobDefinition(
            name=data["name"],
            source_code=data["source_code"],
            prompt=data["prompt"],
            version=data.get("version", 1),
            input_schema=InputSchema(
                required_fields=data.get("input_schema", {}).get("required_fields", []),
                optional_fields=data.get("input_schema", {}).get("optional_fields", []),
                field_types=data.get("input_schema", {}).get("field_types", {}),
            ),
            output_schema=OutputSchema(
                fields=data.get("output_schema", {}).get("fields", []),
                format=data.get("output_schema", {}).get("format", "json"),
            ),
            checksum=data.get("checksum", ""),
        )
'''

TEST_CASES["medium_incident_report"] = """# Incident Report: Production Scraping Failures
**Date**: 2026-03-29
**Severity**: P2
**Duration**: 3 hours 42 minutes
**Status**: Resolved

## Summary
Between 02:18 UTC and 05:00 UTC on March 29, approximately 340 scraping sessions failed across 12 different source codes. The root cause was an expired TLS certificate on the proxy rotation service, causing all outbound HTTPS connections through the proxy to fail with SSL_ERROR_HANDSHAKE_FAILURE.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 02:18 | First failed session detected (APP_RIPPLING_COM) |
| 02:25 | Alert fires: "Scraping failure rate > 30% for 5 minutes" |
| 02:28 | On-call engineer (Mike) acknowledges alert |
| 02:35 | Initial investigation begins - sessions failing with connection errors |
| 02:42 | Mike identifies SSL errors in proxy logs |
| 02:55 | Root cause identified: proxy TLS cert expired at 02:15 UTC |
| 03:10 | Emergency cert rotation initiated |
| 03:25 | New cert deployed to proxy fleet (3 instances) |
| 03:30 | First successful session observed post-fix |
| 03:45 | Failure rate drops below 5% |
| 05:00 | All queued sessions reprocessed successfully - incident closed |

## Impact
- **340 sessions failed** across 47 teams
- **12 source codes affected**: APP_RIPPLING_COM, WWW_FPL_COM, PORTAL_CONED_COM, APP_XCEL_ENERGY_COM, WWW_PGE_COM, MYACCOUNT_SRPNET_COM, WWW_DUKE_ENERGY_COM, SECURE_BC_HYDRO_COM, ONLINE_AEP_COM, MYACCOUNT_EVERSOURCE_COM, CUSTOMER_XCELENERGY_COM, SECURE_PEPCO_COM
- **No data loss** - all sessions were automatically retried after recovery
- **3 teams** reported the issue before our alert fired (SLA breach)

## Root Cause
The TLS certificate used by our proxy rotation service (proxy-rotator.internal) expired at 02:15 UTC. This certificate was provisioned manually 1 year ago and was not included in our automated certificate renewal pipeline (cert-manager). When the cert expired, all outbound HTTPS connections through the proxy started failing SSL handshakes.

## Why Detection Was Delayed
Our health checks for the proxy service only verified HTTP connectivity (port 80), not HTTPS (port 443). The service appeared healthy in our monitoring while actually being unable to proxy HTTPS traffic.

## Remediation
1. **Immediate**: Emergency certificate rotation (completed)
2. **Short-term**: Add proxy TLS cert to cert-manager auto-renewal (INFRA-2355)
3. **Short-term**: Update health checks to verify HTTPS connectivity (INFRA-2356)
4. **Medium-term**: Add certificate expiration monitoring with 30-day warning alerts (INFRA-2357)
5. **Long-term**: Audit all manually provisioned certificates across infrastructure (INFRA-2358)

## Lessons Learned
- Manual certificate management is a ticking time bomb
- Health checks must verify the actual protocol being proxied
- Our alert threshold of 30% over 5 minutes was appropriate but we should also alert on absolute failure counts
- The automatic retry mechanism worked perfectly and prevented any customer impact beyond the delay"""

TEST_CASES["medium_log_output"] = """2026-03-30T14:22:01.334Z INFO  [scraper:sess_e7d3a912] Starting session for APP_RIPPLING_COM
2026-03-30T14:22:01.335Z INFO  [scraper:sess_e7d3a912] Loading agent memory from azure://prod/memories/APP_RIPPLING_COM_memory.md
2026-03-30T14:22:01.892Z INFO  [scraper:sess_e7d3a912] Agent memory loaded (2.3KB, last updated 2026-03-28)
2026-03-30T14:22:02.001Z INFO  [scraper:sess_e7d3a912] Launching browser with CDP endpoint ws://browserless:3000
2026-03-30T14:22:03.445Z INFO  [scraper:sess_e7d3a912] Browser connected, navigating to https://app.rippling.com/login
2026-03-30T14:22:05.112Z INFO  [scraper:sess_e7d3a912] Page loaded, executing login flow
2026-03-30T14:22:05.113Z DEBUG [scraper:sess_e7d3a912] Filling username field: admin@company.com
2026-03-30T14:22:05.890Z DEBUG [scraper:sess_e7d3a912] Clicking submit button
2026-03-30T14:22:06.334Z INFO  [scraper:sess_e7d3a912] Waiting for MFA challenge
2026-03-30T14:22:06.335Z INFO  [scraper:sess_e7d3a912] Sending MFA request to user via push notification
2026-03-30T14:22:15.221Z INFO  [scraper:sess_e7d3a912] MFA approved, proceeding to dashboard
2026-03-30T14:22:17.445Z INFO  [scraper:sess_e7d3a912] Dashboard loaded, starting account discovery
2026-03-30T14:22:17.446Z DEBUG [scraper:sess_e7d3a912] Navigating to /payroll/documents
2026-03-30T14:22:19.112Z INFO  [scraper:sess_e7d3a912] Found 3 accounts: [Personal, Business, Contractor]
2026-03-30T14:22:19.113Z INFO  [scraper:sess_e7d3a912] Starting bill fetch for account: Personal
2026-03-30T14:22:20.556Z DEBUG [scraper:sess_e7d3a912] Clicking "View Statements" link
2026-03-30T14:22:22.334Z DEBUG [scraper:sess_e7d3a912] Found 12 statements in date range
2026-03-30T14:22:22.335Z INFO  [scraper:sess_e7d3a912] Downloading statement: March 2026 - $4,521.33
2026-03-30T14:22:23.112Z INFO  [scraper:sess_e7d3a912] Downloading statement: February 2026 - $4,521.33
2026-03-30T14:22:23.890Z INFO  [scraper:sess_e7d3a912] Downloading statement: January 2026 - $4,387.00
2026-03-30T14:22:24.445Z INFO  [scraper:sess_e7d3a912] Downloading statement: December 2025 - $4,387.00
2026-03-30T14:22:25.001Z INFO  [scraper:sess_e7d3a912] Downloading statement: November 2025 - $4,387.00
2026-03-30T14:22:25.556Z INFO  [scraper:sess_e7d3a912] Downloading statement: October 2025 - $4,255.50
2026-03-30T14:22:26.112Z INFO  [scraper:sess_e7d3a912] Downloading statement: September 2025 - $4,255.50
2026-03-30T14:22:26.668Z INFO  [scraper:sess_e7d3a912] Downloading statement: August 2025 - $4,255.50
2026-03-30T14:22:27.224Z INFO  [scraper:sess_e7d3a912] Downloading statement: July 2025 - $4,100.00
2026-03-30T14:22:27.780Z INFO  [scraper:sess_e7d3a912] Downloading statement: June 2025 - $4,100.00
2026-03-30T14:22:28.336Z INFO  [scraper:sess_e7d3a912] Downloading statement: May 2025 - $4,100.00
2026-03-30T14:22:28.892Z INFO  [scraper:sess_e7d3a912] Downloading statement: April 2025 - $3,950.00
2026-03-30T14:22:29.000Z INFO  [scraper:sess_e7d3a912] Account Personal: 12 bills fetched successfully
2026-03-30T14:22:29.001Z INFO  [scraper:sess_e7d3a912] Starting bill fetch for account: Business
2026-03-30T14:22:30.445Z WARN  [scraper:sess_e7d3a912] Account Business has no statements in the requested date range
2026-03-30T14:22:30.446Z INFO  [scraper:sess_e7d3a912] Starting bill fetch for account: Contractor
2026-03-30T14:22:31.890Z WARN  [scraper:sess_e7d3a912] Account Contractor has no statements in the requested date range
2026-03-30T14:22:32.000Z INFO  [scraper:sess_e7d3a912] Session summary: 3 accounts discovered, 12 bills fetched, 0 errors
2026-03-30T14:22:32.001Z INFO  [scraper:sess_e7d3a912] Uploading results to S3: s3://deck-prod-results/sess_e7d3a912/
2026-03-30T14:22:33.445Z INFO  [scraper:sess_e7d3a912] Results uploaded successfully
2026-03-30T14:22:33.446Z INFO  [scraper:sess_e7d3a912] Updating agent memory with session learnings
2026-03-30T14:22:33.890Z INFO  [scraper:sess_e7d3a912] Session completed in 32.556s"""

TEST_CASES["medium_terraform"] = """resource "google_cloud_run_v2_service" "scraper_runtime" {
  name     = "scraper-runtime-prod"
  location = "us-central1"
  project  = var.project_id

  template {
    scaling {
      min_instance_count = 2
      max_instance_count = 50
    }

    containers {
      image = "${var.artifact_registry}/scraper-runtime:${var.image_tag}"

      ports {
        container_port = 8080
      }

      resources {
        limits = {
          cpu    = "4"
          memory = "8Gi"
        }
        cpu_idle          = false
        startup_cpu_boost = true
      }

      env {
        name  = "NODE_ENV"
        value = "production"
      }
      env {
        name  = "RABBITMQ_URL"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.rabbitmq_url.secret_id
            version = "latest"
          }
        }
      }
      env {
        name  = "REDIS_URL"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.redis_url.secret_id
            version = "latest"
          }
        }
      }
      env {
        name  = "DATABASE_URL"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.database_url.secret_id
            version = "latest"
          }
        }
      }
      env {
        name  = "BROWSERLESS_URL"
        value = "ws://browserless.internal:3000"
      }
      env {
        name  = "S3_BUCKET"
        value = google_storage_bucket.results.name
      }
      env {
        name  = "ANTHROPIC_API_KEY"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.anthropic_key.secret_id
            version = "latest"
          }
        }
      }

      startup_probe {
        http_get {
          path = "/health"
          port = 8080
        }
        initial_delay_seconds = 5
        period_seconds        = 3
        failure_threshold     = 10
      }

      liveness_probe {
        http_get {
          path = "/health"
          port = 8080
        }
        period_seconds    = 30
        failure_threshold = 3
      }
    }

    service_account = google_service_account.scraper_runtime.email

    vpc_access {
      connector = google_vpc_access_connector.main.id
      egress    = "ALL_TRAFFIC"
    }

    timeout = "900s"

    labels = {
      environment = "production"
      service     = "scraper-runtime"
      team        = "platform"
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }

  lifecycle {
    ignore_changes = [
      template[0].containers[0].image,
    ]
  }
}

resource "google_cloud_run_v2_service_iam_member" "scraper_invoker" {
  project  = var.project_id
  location = google_cloud_run_v2_service.scraper_runtime.location
  name     = google_cloud_run_v2_service.scraper_runtime.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.scheduler.email}"
}

resource "google_storage_bucket" "results" {
  name          = "${var.project_id}-scraper-results"
  location      = "US"
  force_destroy = false

  lifecycle_rule {
    condition {
      age = 90
    }
    action {
      type = "Delete"
    }
  }

  versioning {
    enabled = true
  }

  encryption {
    default_kms_key_name = google_kms_crypto_key.storage.id
  }
}"""

# --- LARGE (5000-15000 chars) ---

TEST_CASES["large_api_docs"] = """# Deck Scraping API Documentation

## Authentication
All API requests require a Bearer token in the Authorization header:
```
Authorization: Bearer <your-api-token>
```

Tokens are scoped to a team and can be generated from the Dashboard settings page.

## Base URL
```
Production: https://api.deck.co/v2
Staging:    https://api-staging.deck.co/v2
```

## Endpoints

### Teams

#### GET /teams
List all teams accessible to the authenticated user.

**Response:**
```json
{
  "data": [
    {
      "id": "fc9eda3b-91ba-481b-c1e6-08ddaf38eeb9",
      "name": "Francoboss-Prod",
      "created_at": "2025-01-15T00:00:00Z",
      "connection_count": 42,
      "active_sources": ["APP_RIPPLING_COM", "WWW_FPL_COM"]
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 1
  }
}
```

#### GET /teams/:id
Get a specific team by ID.

### Connections

#### GET /teams/:team_id/connections
List all connections for a team.

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| source_code | string | Filter by source code |
| status | string | Filter by status: active, paused, error |
| page | integer | Page number (default: 1) |
| per_page | integer | Results per page (default: 20, max: 100) |

**Response:**
```json
{
  "data": [
    {
      "id": "conn_8a4f2b1c",
      "source_code": "APP_RIPPLING_COM",
      "status": "active",
      "created_at": "2025-06-01T00:00:00Z",
      "last_session_at": "2026-03-30T14:22:00Z",
      "credentials_status": "valid",
      "schedule": "daily"
    }
  ]
}
```

#### POST /teams/:team_id/connections
Create a new connection.

**Request Body:**
```json
{
  "source_code": "APP_RIPPLING_COM",
  "credentials": {
    "username": "user@example.com",
    "password": "encrypted_password_here"
  },
  "schedule": "daily",
  "job_definition": "fetch_bills_v2"
}
```

#### DELETE /teams/:team_id/connections/:id
Delete a connection. This will also cancel any pending sessions.

### Sessions

#### GET /connections/:connection_id/sessions
List sessions for a connection.

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| status | string | Filter: pending, running, completed, failed |
| from | datetime | Start of date range (ISO 8601) |
| to | datetime | End of date range (ISO 8601) |

**Response:**
```json
{
  "data": [
    {
      "id": "sess_e7d3a912",
      "connection_id": "conn_8a4f2b1c",
      "status": "completed",
      "started_at": "2026-03-30T14:22:00Z",
      "completed_at": "2026-03-30T14:25:33Z",
      "duration_ms": 213000,
      "results": {
        "accounts_discovered": 3,
        "bills_fetched": 12,
        "errors": 0
      },
      "agent": {
        "model": "claude-sonnet-4-6",
        "steps": 24,
        "tokens_used": 15234
      }
    }
  ]
}
```

#### POST /connections/:connection_id/sessions
Trigger a new scraping session.

**Request Body:**
```json
{
  "priority": "normal",
  "job_override": {
    "date_range": {
      "from": "2025-01-01",
      "to": "2026-03-30"
    }
  }
}
```

#### GET /sessions/:id
Get detailed session information including agent logs.

#### GET /sessions/:id/logs
Stream session logs in real-time (SSE endpoint).

### Job Definitions

#### GET /job-definitions
List all available job definitions.

#### GET /job-definitions/:name
Get a specific job definition.

**Response:**
```json
{
  "name": "fetch_bills_v2",
  "source_code": "APP_RIPPLING_COM",
  "version": 3,
  "prompt": "Navigate to the billing section and download all available statements...",
  "input_schema": {
    "required_fields": ["username", "password"],
    "optional_fields": ["date_range", "account_filter"]
  },
  "output_schema": {
    "fields": ["bills", "accounts", "summary"],
    "format": "json"
  },
  "created_at": "2025-09-01T00:00:00Z",
  "updated_at": "2026-03-15T00:00:00Z"
}
```

#### POST /job-definitions
Create a new job definition.

#### PUT /job-definitions/:name
Update an existing job definition. This creates a new version.

### Sources

#### GET /sources
List all supported source codes.

#### GET /sources/:code
Get details about a specific source including supported job types.

### Webhooks

#### GET /teams/:team_id/webhooks
List configured webhooks.

#### POST /teams/:team_id/webhooks
Register a new webhook.

**Request Body:**
```json
{
  "url": "https://your-app.com/webhooks/deck",
  "events": ["session.completed", "session.failed", "connection.error"],
  "secret": "your_webhook_secret"
}
```

**Webhook Payload:**
```json
{
  "event": "session.completed",
  "timestamp": "2026-03-30T14:25:33Z",
  "data": {
    "session_id": "sess_e7d3a912",
    "connection_id": "conn_8a4f2b1c",
    "team_id": "fc9eda3b-91ba-481b-c1e6-08ddaf38eeb9",
    "results": {
      "bills_fetched": 12,
      "accounts_discovered": 3
    }
  }
}
```

## Error Handling

All errors follow this format:
```json
{
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "The provided credentials are invalid or expired",
    "details": {
      "field": "credentials.password"
    }
  }
}
```

### Common Error Codes
| Code | HTTP Status | Description |
|------|-------------|-------------|
| UNAUTHORIZED | 401 | Invalid or expired API token |
| FORBIDDEN | 403 | Token lacks required permissions |
| NOT_FOUND | 404 | Resource not found |
| RATE_LIMITED | 429 | Too many requests (see Rate Limits) |
| INVALID_CREDENTIALS | 422 | Connection credentials are invalid |
| SESSION_TIMEOUT | 408 | Scraping session exceeded time limit |
| SOURCE_UNAVAILABLE | 503 | Target website is down or blocking |

## Rate Limits
- 100 requests per minute per team
- 1000 requests per hour per team
- Session creation: 10 per minute per connection

Rate limit headers are included in all responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1711809600
```"""

TEST_CASES["large_react_component"] = """import React, { useState, useEffect, useCallback, useMemo, useRef } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { formatDistanceToNow, format } from 'date-fns';
import clsx from 'clsx';

interface Session {
  id: string;
  connectionId: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  startedAt: string;
  completedAt?: string;
  durationMs?: number;
  results?: {
    accountsDiscovered: number;
    billsFetched: number;
    errors: number;
  };
  agent?: {
    model: string;
    steps: number;
    tokensUsed: number;
  };
  error?: string;
}

interface SessionViewerProps {
  connectionId: string;
  onSessionSelect?: (session: Session) => void;
}

const STATUS_COLORS = {
  pending: 'bg-yellow-100 text-yellow-800 border-yellow-200',
  running: 'bg-blue-100 text-blue-800 border-blue-200',
  completed: 'bg-green-100 text-green-800 border-green-200',
  failed: 'bg-red-100 text-red-800 border-red-200',
} as const;

const STATUS_ICONS = {
  pending: '\\u23f3',
  running: '\\u25b6',
  completed: '\\u2713',
  failed: '\\u2717',
} as const;

function SessionCard({ session, isSelected, onClick }: {
  session: Session;
  isSelected: boolean;
  onClick: () => void;
}) {
  return (
    <div
      className={clsx(
        'border rounded-lg p-4 cursor-pointer transition-all duration-150',
        'hover:shadow-md hover:border-blue-300',
        isSelected && 'ring-2 ring-blue-500 border-blue-500',
        !isSelected && 'border-gray-200'
      )}
      onClick={onClick}
      role="button"
      tabIndex={0}
      aria-selected={isSelected}
    >
      <div className="flex items-center justify-between mb-2">
        <code className="text-sm text-gray-600 font-mono">{session.id}</code>
        <span className={clsx(
          'px-2 py-0.5 rounded-full text-xs font-medium border',
          STATUS_COLORS[session.status]
        )}>
          {STATUS_ICONS[session.status]} {session.status}
        </span>
      </div>

      <div className="text-sm text-gray-500 mb-2">
        Started {formatDistanceToNow(new Date(session.startedAt), { addSuffix: true })}
      </div>

      {session.results && (
        <div className="grid grid-cols-3 gap-2 text-center">
          <div className="bg-gray-50 rounded p-2">
            <div className="text-lg font-semibold">{session.results.accountsDiscovered}</div>
            <div className="text-xs text-gray-500">Accounts</div>
          </div>
          <div className="bg-gray-50 rounded p-2">
            <div className="text-lg font-semibold">{session.results.billsFetched}</div>
            <div className="text-xs text-gray-500">Bills</div>
          </div>
          <div className="bg-gray-50 rounded p-2">
            <div className="text-lg font-semibold text-red-600">{session.results.errors}</div>
            <div className="text-xs text-gray-500">Errors</div>
          </div>
        </div>
      )}

      {session.error && (
        <div className="mt-2 p-2 bg-red-50 rounded text-sm text-red-700 font-mono">
          {session.error}
        </div>
      )}

      {session.agent && (
        <div className="mt-2 flex items-center gap-3 text-xs text-gray-400">
          <span>{session.agent.model}</span>
          <span>{session.agent.steps} steps</span>
          <span>{session.agent.tokensUsed.toLocaleString()} tokens</span>
        </div>
      )}

      {session.durationMs && (
        <div className="mt-1 text-xs text-gray-400">
          Duration: {(session.durationMs / 1000).toFixed(1)}s
        </div>
      )}
    </div>
  );
}

function SessionFilters({ filters, onChange }: {
  filters: { status?: string; dateRange?: string };
  onChange: (filters: any) => void;
}) {
  return (
    <div className="flex gap-3 mb-4">
      <select
        value={filters.status || 'all'}
        onChange={(e) => onChange({ ...filters, status: e.target.value === 'all' ? undefined : e.target.value })}
        className="border rounded-md px-3 py-1.5 text-sm bg-white"
      >
        <option value="all">All Statuses</option>
        <option value="pending">Pending</option>
        <option value="running">Running</option>
        <option value="completed">Completed</option>
        <option value="failed">Failed</option>
      </select>

      <select
        value={filters.dateRange || '7d'}
        onChange={(e) => onChange({ ...filters, dateRange: e.target.value })}
        className="border rounded-md px-3 py-1.5 text-sm bg-white"
      >
        <option value="1d">Last 24 hours</option>
        <option value="7d">Last 7 days</option>
        <option value="30d">Last 30 days</option>
        <option value="90d">Last 90 days</option>
      </select>
    </div>
  );
}

export function SessionViewer({ connectionId, onSessionSelect }: SessionViewerProps) {
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [filters, setFilters] = useState<{ status?: string; dateRange?: string }>({ dateRange: '7d' });
  const queryClient = useQueryClient();
  const listRef = useRef<HTMLDivElement>(null);

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['sessions', connectionId, filters],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (filters.status) params.set('status', filters.status);
      if (filters.dateRange) params.set('range', filters.dateRange);
      const res = await fetch(`/api/connections/${connectionId}/sessions?${params}`);
      if (!res.ok) throw new Error(`Failed to fetch sessions: ${res.status}`);
      return res.json() as Promise<{ data: Session[] }>;
    },
    refetchInterval: 15000,
  });

  const triggerSession = useMutation({
    mutationFn: async () => {
      const res = await fetch(`/api/connections/${connectionId}/sessions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ priority: 'normal' }),
      });
      if (!res.ok) throw new Error(`Failed to trigger session: ${res.status}`);
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sessions', connectionId] });
    },
  });

  const sessions = data?.data ?? [];

  const stats = useMemo(() => ({
    total: sessions.length,
    completed: sessions.filter(s => s.status === 'completed').length,
    failed: sessions.filter(s => s.status === 'failed').length,
    avgDuration: sessions
      .filter(s => s.durationMs)
      .reduce((sum, s) => sum + (s.durationMs || 0), 0) /
      Math.max(sessions.filter(s => s.durationMs).length, 1),
  }), [sessions]);

  const handleSelect = useCallback((session: Session) => {
    setSelectedId(session.id);
    onSessionSelect?.(session);
  }, [onSessionSelect]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <h3 className="text-red-800 font-medium">Failed to load sessions</h3>
        <p className="text-red-600 text-sm mt-1">{error.message}</p>
        <button onClick={() => refetch()} className="mt-2 text-sm text-red-700 underline">
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold">Sessions</h2>
        <button
          onClick={() => triggerSession.mutate()}
          disabled={triggerSession.isPending}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 disabled:opacity-50"
        >
          {triggerSession.isPending ? 'Triggering...' : 'Trigger Session'}
        </button>
      </div>

      <div className="grid grid-cols-4 gap-3">
        <div className="bg-gray-50 rounded-lg p-3 text-center">
          <div className="text-2xl font-bold">{stats.total}</div>
          <div className="text-xs text-gray-500">Total</div>
        </div>
        <div className="bg-green-50 rounded-lg p-3 text-center">
          <div className="text-2xl font-bold text-green-700">{stats.completed}</div>
          <div className="text-xs text-gray-500">Completed</div>
        </div>
        <div className="bg-red-50 rounded-lg p-3 text-center">
          <div className="text-2xl font-bold text-red-700">{stats.failed}</div>
          <div className="text-xs text-gray-500">Failed</div>
        </div>
        <div className="bg-blue-50 rounded-lg p-3 text-center">
          <div className="text-2xl font-bold text-blue-700">{(stats.avgDuration / 1000).toFixed(0)}s</div>
          <div className="text-xs text-gray-500">Avg Duration</div>
        </div>
      </div>

      <SessionFilters filters={filters} onChange={setFilters} />

      <div ref={listRef} className="space-y-3 max-h-[600px] overflow-y-auto">
        {sessions.length === 0 ? (
          <div className="text-center py-12 text-gray-400">
            No sessions found for the selected filters.
          </div>
        ) : (
          sessions.map(session => (
            <SessionCard
              key={session.id}
              session={session}
              isSelected={session.id === selectedId}
              onClick={() => handleSelect(session)}
            />
          ))
        )}
      </div>
    </div>
  );
}"""

TEST_CASES["large_db_migration"] = """-- Migration: 20260330_add_job_definitions_and_sessions
-- Description: Add job definitions table, update sessions with agent metadata,
--              and create materialized views for analytics.

BEGIN;

-- ============================================================
-- Job Definitions
-- ============================================================

CREATE TABLE job_definitions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            VARCHAR(255) NOT NULL UNIQUE,
    source_code     VARCHAR(255) NOT NULL,
    prompt          TEXT NOT NULL,
    version         INTEGER NOT NULL DEFAULT 1,
    input_schema    JSONB NOT NULL DEFAULT '{}',
    output_schema   JSONB NOT NULL DEFAULT '{}',
    checksum        VARCHAR(12) NOT NULL,
    is_active       BOOLEAN NOT NULL DEFAULT true,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by      UUID REFERENCES users(id),

    CONSTRAINT job_definitions_version_positive CHECK (version > 0),
    CONSTRAINT job_definitions_name_format CHECK (name ~ '^[a-z][a-z0-9_]*$')
);

CREATE INDEX idx_job_definitions_source_code ON job_definitions(source_code);
CREATE INDEX idx_job_definitions_active ON job_definitions(is_active) WHERE is_active = true;

-- Version history for job definitions
CREATE TABLE job_definition_versions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_definition_id UUID NOT NULL REFERENCES job_definitions(id) ON DELETE CASCADE,
    version         INTEGER NOT NULL,
    prompt          TEXT NOT NULL,
    input_schema    JSONB NOT NULL DEFAULT '{}',
    output_schema   JSONB NOT NULL DEFAULT '{}',
    checksum        VARCHAR(12) NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by      UUID REFERENCES users(id),

    CONSTRAINT unique_job_version UNIQUE (job_definition_id, version)
);

CREATE INDEX idx_job_def_versions_lookup ON job_definition_versions(job_definition_id, version DESC);

-- ============================================================
-- Sessions: Add agent metadata columns
-- ============================================================

ALTER TABLE sessions
    ADD COLUMN job_definition_id UUID REFERENCES job_definitions(id),
    ADD COLUMN agent_model VARCHAR(100),
    ADD COLUMN agent_steps INTEGER,
    ADD COLUMN agent_tokens_used INTEGER,
    ADD COLUMN agent_reasoning_tokens INTEGER,
    ADD COLUMN results JSONB,
    ADD COLUMN error_code VARCHAR(50),
    ADD COLUMN error_details JSONB,
    ADD COLUMN retry_count INTEGER NOT NULL DEFAULT 0,
    ADD COLUMN parent_session_id UUID REFERENCES sessions(id);

CREATE INDEX idx_sessions_job_definition ON sessions(job_definition_id);
CREATE INDEX idx_sessions_error_code ON sessions(error_code) WHERE error_code IS NOT NULL;
CREATE INDEX idx_sessions_parent ON sessions(parent_session_id) WHERE parent_session_id IS NOT NULL;
CREATE INDEX idx_sessions_agent_model ON sessions(agent_model);

-- Partial index for active/recent sessions
CREATE INDEX idx_sessions_recent_by_connection ON sessions(connection_id, created_at DESC)
    WHERE created_at > NOW() - INTERVAL '30 days';

-- ============================================================
-- Analytics: Materialized views
-- ============================================================

-- Daily session stats per source
CREATE MATERIALIZED VIEW mv_daily_source_stats AS
SELECT
    date_trunc('day', s.created_at)::DATE AS day,
    c.source_code,
    COUNT(*) AS total_sessions,
    COUNT(*) FILTER (WHERE s.status = 'completed') AS completed,
    COUNT(*) FILTER (WHERE s.status = 'failed') AS failed,
    AVG(s.duration_ms) FILTER (WHERE s.status = 'completed') AS avg_duration_ms,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY s.duration_ms)
        FILTER (WHERE s.status = 'completed') AS median_duration_ms,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY s.duration_ms)
        FILTER (WHERE s.status = 'completed') AS p95_duration_ms,
    AVG(s.agent_tokens_used) FILTER (WHERE s.status = 'completed') AS avg_tokens,
    AVG(s.agent_steps) FILTER (WHERE s.status = 'completed') AS avg_steps,
    SUM((s.results->>'bills_fetched')::INTEGER) FILTER (WHERE s.status = 'completed') AS total_bills,
    SUM((s.results->>'accounts_discovered')::INTEGER) FILTER (WHERE s.status = 'completed') AS total_accounts
FROM sessions s
JOIN connections c ON c.id = s.connection_id
WHERE s.created_at > NOW() - INTERVAL '90 days'
GROUP BY 1, 2
WITH DATA;

CREATE UNIQUE INDEX idx_mv_daily_source_stats ON mv_daily_source_stats(day, source_code);

-- Error breakdown per source
CREATE MATERIALIZED VIEW mv_error_breakdown AS
SELECT
    date_trunc('week', s.created_at)::DATE AS week,
    c.source_code,
    s.error_code,
    COUNT(*) AS error_count,
    array_agg(DISTINCT s.id ORDER BY s.id) AS sample_session_ids
FROM sessions s
JOIN connections c ON c.id = s.connection_id
WHERE s.status = 'failed'
  AND s.created_at > NOW() - INTERVAL '90 days'
  AND s.error_code IS NOT NULL
GROUP BY 1, 2, 3
WITH DATA;

CREATE UNIQUE INDEX idx_mv_error_breakdown ON mv_error_breakdown(week, source_code, error_code);

-- Team-level aggregates
CREATE MATERIALIZED VIEW mv_team_stats AS
SELECT
    t.id AS team_id,
    t.name AS team_name,
    COUNT(DISTINCT c.id) AS connection_count,
    COUNT(DISTINCT c.source_code) AS source_count,
    COUNT(s.id) FILTER (WHERE s.created_at > NOW() - INTERVAL '7 days') AS sessions_7d,
    COUNT(s.id) FILTER (WHERE s.status = 'completed' AND s.created_at > NOW() - INTERVAL '7 days') AS completed_7d,
    COUNT(s.id) FILTER (WHERE s.status = 'failed' AND s.created_at > NOW() - INTERVAL '7 days') AS failed_7d,
    ROUND(
        COUNT(s.id) FILTER (WHERE s.status = 'completed' AND s.created_at > NOW() - INTERVAL '7 days')::NUMERIC /
        NULLIF(COUNT(s.id) FILTER (WHERE s.created_at > NOW() - INTERVAL '7 days'), 0) * 100,
        1
    ) AS success_rate_7d
FROM teams t
LEFT JOIN connections c ON c.team_id = t.id
LEFT JOIN sessions s ON s.connection_id = c.id
GROUP BY t.id, t.name
WITH DATA;

CREATE UNIQUE INDEX idx_mv_team_stats ON mv_team_stats(team_id);

-- ============================================================
-- Refresh function for materialized views
-- ============================================================

CREATE OR REPLACE FUNCTION refresh_analytics_views()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_daily_source_stats;
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_error_breakdown;
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_team_stats;
END;
$$ LANGUAGE plpgsql;

-- Schedule refresh every 15 minutes (requires pg_cron extension)
-- SELECT cron.schedule('refresh-analytics', '*/15 * * * *', 'SELECT refresh_analytics_views()');

-- ============================================================
-- Trigger: Auto-version job definitions on update
-- ============================================================

CREATE OR REPLACE FUNCTION fn_job_definition_version()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.prompt IS DISTINCT FROM NEW.prompt
       OR OLD.input_schema IS DISTINCT FROM NEW.input_schema
       OR OLD.output_schema IS DISTINCT FROM NEW.output_schema THEN

        -- Archive the old version
        INSERT INTO job_definition_versions (
            job_definition_id, version, prompt,
            input_schema, output_schema, checksum, created_by
        ) VALUES (
            OLD.id, OLD.version, OLD.prompt,
            OLD.input_schema, OLD.output_schema, OLD.checksum, NEW.created_by
        );

        -- Bump version
        NEW.version := OLD.version + 1;
        NEW.updated_at := NOW();
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_job_definition_version
    BEFORE UPDATE ON job_definitions
    FOR EACH ROW
    EXECUTE FUNCTION fn_job_definition_version();

-- ============================================================
-- Seed default job definitions
-- ============================================================

INSERT INTO job_definitions (name, source_code, prompt, input_schema, output_schema, checksum)
VALUES
    ('fetch_bills_generic', '*',
     'Log into the website using the provided credentials. Navigate to the billing or statements section. Download all available bills/statements as PDF files. Return a summary of what was found.',
     '{"required_fields": ["username", "password"], "optional_fields": ["date_range", "account_filter"]}',
     '{"fields": ["bills", "accounts", "summary"], "format": "json"}',
     'a1b2c3d4e5f6'),
    ('discover_accounts', '*',
     'Log into the website and discover all available accounts, sub-accounts, and service points. Do not download any documents. Return the account hierarchy.',
     '{"required_fields": ["username", "password"], "optional_fields": []}',
     '{"fields": ["accounts"], "format": "json"}',
     'f6e5d4c3b2a1'),
    ('fetch_interval_data', '*',
     'Log into the utility website. Navigate to the usage/consumption section. Download interval data (15-min or hourly readings) for all meters. Export as CSV if available.',
     '{"required_fields": ["username", "password"], "optional_fields": ["meter_ids", "date_range"]}',
     '{"fields": ["interval_data", "meters", "summary"], "format": "json"}',
     'c3d4e5f6a1b2');

COMMIT;"""

# --- EXTRA LARGE (15000-50000 chars) ---

TEST_CASES["xlarge_full_codebase"] = """// ============================================================
// scraper-runtime/src/index.ts - Main entry point
// ============================================================

import { createServer } from 'http';
import { config } from './config';
import { RabbitMQConsumer } from './messaging/consumer';
import { SessionManager } from './sessions/manager';
import { AgentFactory } from './agents/factory';
import { BrowserPool } from './browser/pool';
import { MetricsCollector } from './monitoring/metrics';
import { logger } from './utils/logger';

async function main() {
  logger.info('Starting scraper runtime', {
    version: config.version,
    environment: config.env,
    nodeVersion: process.version,
  });

  const metrics = new MetricsCollector(config.metrics);
  const browserPool = new BrowserPool({
    endpoint: config.browserless.url,
    maxConcurrent: config.browserless.maxConcurrent,
    launchTimeout: config.browserless.launchTimeout,
  });
  const agentFactory = new AgentFactory({
    anthropicApiKey: config.anthropic.apiKey,
    defaultModel: config.anthropic.defaultModel,
    maxTokens: config.anthropic.maxTokens,
  });
  const sessionManager = new SessionManager({
    browserPool,
    agentFactory,
    metrics,
    resultsBucket: config.s3.bucket,
    memoryStorage: config.azure.memoryContainer,
    maxSessionDuration: config.sessions.maxDuration,
  });

  const consumer = new RabbitMQConsumer({
    url: config.rabbitmq.url,
    queue: config.rabbitmq.queue,
    prefetch: config.rabbitmq.prefetch,
    handler: async (message) => {
      const { connectionId, teamId, sourceCode, credentials, jobDefinition } = message;

      metrics.increment('sessions.started', { sourceCode });
      const startTime = Date.now();

      try {
        const result = await sessionManager.execute({
          connectionId,
          teamId,
          sourceCode,
          credentials,
          jobDefinition,
        });

        const duration = Date.now() - startTime;
        metrics.timing('sessions.duration', duration, { sourceCode, status: 'completed' });
        metrics.increment('sessions.completed', { sourceCode });

        logger.info('Session completed', {
          connectionId,
          sourceCode,
          duration,
          billsFetched: result.billsFetched,
          accountsDiscovered: result.accountsDiscovered,
        });

        return result;
      } catch (error) {
        const duration = Date.now() - startTime;
        metrics.timing('sessions.duration', duration, { sourceCode, status: 'failed' });
        metrics.increment('sessions.failed', { sourceCode, errorCode: error.code || 'UNKNOWN' });

        logger.error('Session failed', {
          connectionId,
          sourceCode,
          duration,
          error: error.message,
          errorCode: error.code,
        });

        throw error;
      }
    },
  });

  // Health check server
  const healthServer = createServer((req, res) => {
    if (req.url === '/health') {
      const healthy = consumer.isConnected() && browserPool.isHealthy();
      res.writeHead(healthy ? 200 : 503);
      res.end(JSON.stringify({
        status: healthy ? 'ok' : 'degraded',
        uptime: process.uptime(),
        activeSessions: sessionManager.activeCount(),
        browserPoolSize: browserPool.size(),
        rabbitMQ: consumer.isConnected() ? 'connected' : 'disconnected',
      }));
    } else if (req.url === '/metrics') {
      res.writeHead(200, { 'Content-Type': 'text/plain' });
      res.end(metrics.toPrometheus());
    } else {
      res.writeHead(404);
      res.end();
    }
  });

  healthServer.listen(config.port, () => {
    logger.info(`Health server listening on port ${config.port}`);
  });

  await consumer.start();
  logger.info('Consumer started, waiting for messages');

  // Graceful shutdown
  const shutdown = async (signal: string) => {
    logger.info(`Received ${signal}, starting graceful shutdown`);
    consumer.stop();
    await sessionManager.drainActive(30000);
    await browserPool.closeAll();
    healthServer.close();
    process.exit(0);
  };

  process.on('SIGTERM', () => shutdown('SIGTERM'));
  process.on('SIGINT', () => shutdown('SIGINT'));
}

main().catch((err) => {
  logger.fatal('Failed to start runtime', { error: err.message });
  process.exit(1);
});


// ============================================================
// scraper-runtime/src/sessions/manager.ts
// ============================================================

import { BrowserPool, BrowserContext } from '../browser/pool';
import { AgentFactory, Agent } from '../agents/factory';
import { MetricsCollector } from '../monitoring/metrics';
import { MemoryStore } from '../memory/store';
import { ResultUploader } from '../results/uploader';
import { logger } from '../utils/logger';

interface SessionConfig {
  browserPool: BrowserPool;
  agentFactory: AgentFactory;
  metrics: MetricsCollector;
  resultsBucket: string;
  memoryStorage: string;
  maxSessionDuration: number;
}

interface SessionRequest {
  connectionId: string;
  teamId: string;
  sourceCode: string;
  credentials: {
    username: string;
    password: string;
    mfaSecret?: string;
  };
  jobDefinition: {
    name: string;
    prompt: string;
    inputSchema: Record<string, any>;
    outputSchema: Record<string, any>;
  };
}

interface SessionResult {
  sessionId: string;
  status: 'completed' | 'failed';
  accountsDiscovered: number;
  billsFetched: number;
  errors: ErrorDetail[];
  agentSteps: number;
  tokensUsed: number;
  artifacts: string[];
}

interface ErrorDetail {
  code: string;
  message: string;
  step?: number;
  recoverable: boolean;
}

export class SessionManager {
  private config: SessionConfig;
  private activeSessions: Map<string, AbortController> = new Map();
  private memoryStore: MemoryStore;
  private resultUploader: ResultUploader;

  constructor(config: SessionConfig) {
    this.config = config;
    this.memoryStore = new MemoryStore(config.memoryStorage);
    this.resultUploader = new ResultUploader(config.resultsBucket);
  }

  activeCount(): number {
    return this.activeSessions.size;
  }

  async execute(request: SessionRequest): Promise<SessionResult> {
    const sessionId = `sess_${crypto.randomUUID().slice(0, 8)}`;
    const abortController = new AbortController();
    this.activeSessions.set(sessionId, abortController);

    // Set session timeout
    const timeout = setTimeout(() => {
      abortController.abort(new Error('Session timeout exceeded'));
    }, this.config.maxSessionDuration);

    let browser: BrowserContext | null = null;
    let agent: Agent | null = null;

    try {
      // Load agent memory for this source
      const memory = await this.memoryStore.load(request.sourceCode);

      // Acquire browser from pool
      browser = await this.config.browserPool.acquire();

      // Create agent with tools
      agent = this.config.agentFactory.create({
        model: 'claude-sonnet-4-6',
        systemPrompt: this.buildSystemPrompt(request, memory),
        tools: this.buildTools(browser, request),
        maxSteps: 100,
        signal: abortController.signal,
      });

      // Execute the agent
      const agentResult = await agent.run(request.jobDefinition.prompt);

      // Parse and validate results
      const parsed = this.parseResults(agentResult, request.jobDefinition.outputSchema);

      // Upload artifacts (PDFs, CSVs, etc.)
      const artifacts = await this.resultUploader.upload(sessionId, parsed.files);

      // Update agent memory with learnings
      if (agentResult.learnings) {
        await this.memoryStore.update(request.sourceCode, agentResult.learnings);
      }

      const result: SessionResult = {
        sessionId,
        status: 'completed',
        accountsDiscovered: parsed.accounts.length,
        billsFetched: parsed.bills.length,
        errors: [],
        agentSteps: agentResult.steps,
        tokensUsed: agentResult.tokensUsed,
        artifacts,
      };

      return result;
    } catch (error) {
      const errorDetail: ErrorDetail = {
        code: error.code || 'UNKNOWN_ERROR',
        message: error.message,
        step: agent?.currentStep,
        recoverable: this.isRecoverable(error),
      };

      return {
        sessionId,
        status: 'failed',
        accountsDiscovered: 0,
        billsFetched: 0,
        errors: [errorDetail],
        agentSteps: agent?.currentStep || 0,
        tokensUsed: agent?.tokensUsed || 0,
        artifacts: [],
      };
    } finally {
      clearTimeout(timeout);
      this.activeSessions.delete(sessionId);
      if (browser) {
        await this.config.browserPool.release(browser);
      }
    }
  }

  async drainActive(timeoutMs: number): Promise<void> {
    if (this.activeSessions.size === 0) return;

    logger.info(`Draining ${this.activeSessions.size} active sessions`);

    const deadline = Date.now() + timeoutMs;
    while (this.activeSessions.size > 0 && Date.now() < deadline) {
      await new Promise(resolve => setTimeout(resolve, 1000));
    }

    if (this.activeSessions.size > 0) {
      logger.warn(`Force-aborting ${this.activeSessions.size} sessions after drain timeout`);
      for (const [id, controller] of this.activeSessions) {
        controller.abort(new Error('Shutdown drain timeout'));
      }
    }
  }

  private buildSystemPrompt(request: SessionRequest, memory: string | null): string {
    let prompt = `You are a web scraping agent for ${request.sourceCode}.\\n`;
    prompt += `Connection ID: ${request.connectionId}\\n`;
    prompt += `Team ID: ${request.teamId}\\n\\n`;

    if (memory) {
      prompt += `## Agent Memory\\nHere is what you learned from previous sessions:\\n${memory}\\n\\n`;
    }

    prompt += `## Credentials\\nUsername: ${request.credentials.username}\\n`;
    if (request.credentials.mfaSecret) {
      prompt += `MFA is configured and will be handled automatically.\\n`;
    }

    return prompt;
  }

  private buildTools(browser: BrowserContext, request: SessionRequest): any[] {
    return [
      {
        name: 'navigate',
        description: 'Navigate to a URL',
        execute: async (url: string) => browser.goto(url),
      },
      {
        name: 'click',
        description: 'Click an element by selector',
        execute: async (selector: string) => browser.click(selector),
      },
      {
        name: 'fill',
        description: 'Fill a form field',
        execute: async (selector: string, value: string) => browser.fill(selector, value),
      },
      {
        name: 'screenshot',
        description: 'Take a screenshot of the current page',
        execute: async () => browser.screenshot(),
      },
      {
        name: 'download',
        description: 'Download a file from the current page',
        execute: async (selector: string) => browser.downloadFile(selector),
      },
      {
        name: 'get_text',
        description: 'Get visible text content of the page',
        execute: async () => browser.getVisibleText(),
      },
      {
        name: 'wait_for',
        description: 'Wait for a selector to appear',
        execute: async (selector: string, timeout: number = 10000) =>
          browser.waitForSelector(selector, { timeout }),
      },
    ];
  }

  private parseResults(agentResult: any, outputSchema: Record<string, any>): any {
    // Validate against output schema
    const results = agentResult.output;

    return {
      accounts: results.accounts || [],
      bills: results.bills || [],
      files: results.files || [],
      summary: results.summary || '',
    };
  }

  private isRecoverable(error: any): boolean {
    const recoverableCodes = [
      'TIMEOUT', 'NETWORK_ERROR', 'MFA_TIMEOUT',
      'RATE_LIMITED', 'TEMPORARY_BLOCK',
    ];
    return recoverableCodes.includes(error.code);
  }
}


// ============================================================
// scraper-runtime/src/agents/factory.ts
// ============================================================

import Anthropic from '@anthropic-ai/sdk';
import { logger } from '../utils/logger';

interface AgentConfig {
  anthropicApiKey: string;
  defaultModel: string;
  maxTokens: number;
}

interface CreateAgentOptions {
  model?: string;
  systemPrompt: string;
  tools: any[];
  maxSteps: number;
  signal?: AbortSignal;
}

export interface Agent {
  run(prompt: string): Promise<AgentResult>;
  currentStep: number;
  tokensUsed: number;
}

interface AgentResult {
  output: any;
  steps: number;
  tokensUsed: number;
  learnings?: string;
}

export class AgentFactory {
  private client: Anthropic;
  private config: AgentConfig;

  constructor(config: AgentConfig) {
    this.config = config;
    this.client = new Anthropic({ apiKey: config.anthropicApiKey });
  }

  create(options: CreateAgentOptions): Agent {
    const model = options.model || this.config.defaultModel;
    let currentStep = 0;
    let tokensUsed = 0;
    const messages: any[] = [];

    const agent: Agent = {
      currentStep: 0,
      tokensUsed: 0,

      run: async (prompt: string): Promise<AgentResult> => {
        messages.push({ role: 'user', content: prompt });

        for (let step = 0; step < options.maxSteps; step++) {
          if (options.signal?.aborted) {
            throw Object.assign(new Error('Session aborted'), { code: 'ABORTED' });
          }

          currentStep = step + 1;
          agent.currentStep = currentStep;

          const response = await this.client.messages.create({
            model,
            max_tokens: this.config.maxTokens,
            system: options.systemPrompt,
            messages,
            tools: options.tools.map(t => ({
              name: t.name,
              description: t.description,
              input_schema: t.inputSchema || { type: 'object', properties: {} },
            })),
          });

          tokensUsed += (response.usage?.input_tokens || 0) + (response.usage?.output_tokens || 0);
          agent.tokensUsed = tokensUsed;

          // Check for tool use
          const toolUse = response.content.find((c: any) => c.type === 'tool_use');

          if (!toolUse) {
            // Agent is done - extract final response
            const textContent = response.content.find((c: any) => c.type === 'text');

            let output;
            try {
              output = JSON.parse(textContent?.text || '{}');
            } catch {
              output = { raw: textContent?.text };
            }

            return {
              output,
              steps: currentStep,
              tokensUsed,
              learnings: output.learnings,
            };
          }

          // Execute tool
          const tool = options.tools.find(t => t.name === toolUse.name);
          if (!tool) {
            throw Object.assign(
              new Error(`Unknown tool: ${toolUse.name}`),
              { code: 'INVALID_TOOL' }
            );
          }

          logger.debug('Executing tool', {
            step: currentStep,
            tool: toolUse.name,
            input: toolUse.input,
          });

          let toolResult;
          try {
            toolResult = await tool.execute(...Object.values(toolUse.input));
          } catch (error) {
            toolResult = { error: error.message };
          }

          messages.push({ role: 'assistant', content: response.content });
          messages.push({
            role: 'user',
            content: [{
              type: 'tool_result',
              tool_use_id: toolUse.id,
              content: typeof toolResult === 'string'
                ? toolResult
                : JSON.stringify(toolResult),
            }],
          });
        }

        throw Object.assign(
          new Error(`Agent exceeded maximum steps (${options.maxSteps})`),
          { code: 'MAX_STEPS_EXCEEDED' }
        );
      },
    };

    return agent;
  }
}"""

# --- HUGE (50000-100000 chars) - Generated repetitive but realistic content ---

def _generate_large_json_dataset(n_records: int) -> str:
    """Generate a large JSON dataset simulating API response data."""
    import json
    import hashlib

    sources = [
        "APP_RIPPLING_COM", "WWW_FPL_COM", "PORTAL_CONED_COM",
        "APP_XCEL_ENERGY_COM", "WWW_PGE_COM", "MYACCOUNT_SRPNET_COM",
        "WWW_DUKE_ENERGY_COM", "SECURE_BC_HYDRO_COM", "ONLINE_AEP_COM",
        "MYACCOUNT_EVERSOURCE_COM", "CUSTOMER_XCELENERGY_COM",
    ]
    statuses = ["completed", "completed", "completed", "completed", "failed", "completed"]
    errors = [
        None, None, None, None,
        "MFA challenge timeout - no response within 120s",
        "Navigation failed: page not found (404)",
        "Login failed: invalid credentials",
        "Session timeout after 900s",
        None, None,
    ]
    models = ["claude-sonnet-4-6", "claude-haiku-4-5-20251001", "claude-opus-4-6"]

    records = []
    for i in range(n_records):
        source = sources[i % len(sources)]
        status = statuses[i % len(statuses)]
        error = errors[i % len(errors)] if status == "failed" else None
        session_hash = hashlib.md5(f"session_{i}".encode()).hexdigest()[:8]
        conn_hash = hashlib.md5(f"conn_{i % 50}".encode()).hexdigest()[:8]
        team_hash = hashlib.md5(f"team_{i % 10}".encode()).hexdigest()

        record = {
            "session_id": f"sess_{session_hash}",
            "connection_id": f"conn_{conn_hash}",
            "team_id": f"{team_hash[:8]}-{team_hash[8:12]}-{team_hash[12:16]}-{team_hash[16:20]}-{team_hash[20:32]}",
            "source_code": source,
            "status": status,
            "started_at": f"2026-03-{(i % 28) + 1:02d}T{(i % 24):02d}:{(i * 7) % 60:02d}:00Z",
            "duration_ms": (i * 1337 + 15000) % 120000 + 10000 if status == "completed" else None,
            "agent": {
                "model": models[i % len(models)],
                "steps": (i * 3 + 10) % 80 + 5,
                "tokens_used": (i * 571 + 5000) % 50000 + 3000,
                "reasoning_tokens": (i * 200 + 1000) % 15000,
            },
            "results": {
                "accounts_discovered": (i % 5) + 1,
                "bills_fetched": (i * 3 + 2) % 24,
                "errors": 1 if error else 0,
            } if status == "completed" else None,
            "error": error,
        }
        records.append(record)

    return json.dumps({"data": records, "total": n_records}, indent=2)


def _generate_large_log_output(n_lines: int) -> str:
    """Generate realistic scraper log output."""
    import hashlib

    actions = [
        ("INFO", "Navigating to {url}"),
        ("DEBUG", "Waiting for selector: {selector}"),
        ("INFO", "Page loaded, title: {title}"),
        ("DEBUG", "Clicking element: {selector}"),
        ("INFO", "Form submitted, waiting for response"),
        ("DEBUG", "Response received: HTTP {status}"),
        ("INFO", "Found {count} elements matching criteria"),
        ("WARN", "Slow page load: {duration}ms"),
        ("DEBUG", "Taking screenshot: step_{step}.png"),
        ("INFO", "Downloading file: {filename}"),
        ("DEBUG", "File downloaded: {size}KB"),
        ("INFO", "Account discovered: {account}"),
        ("INFO", "Bill found: {month} - ${amount}"),
        ("DEBUG", "Extracting text from element: {selector}"),
        ("INFO", "MFA challenge detected, sending push notification"),
        ("INFO", "MFA approved, proceeding"),
        ("WARN", "Element not found, retrying with fallback selector"),
        ("ERROR", "Network timeout on {url}, retrying (attempt {attempt}/3)"),
        ("INFO", "Retry successful"),
        ("DEBUG", "Cookie set: session_id={value}"),
    ]

    urls = ["https://app.rippling.com/login", "https://app.rippling.com/dashboard",
            "https://app.rippling.com/payroll", "https://app.rippling.com/documents",
            "https://app.rippling.com/billing/statements"]
    selectors = ["#login-form", ".submit-btn", "[data-testid='nav-menu']",
                 ".statement-row", "#download-btn", ".account-card", "table.bills tbody tr"]
    accounts = ["Personal Checking", "Business Premium", "Savings", "Contractor Payments"]
    months = ["January 2026", "February 2026", "March 2026", "December 2025",
              "November 2025", "October 2025"]

    lines = []
    base_hour = 14
    base_min = 22

    for i in range(n_lines):
        sec = (i * 2) % 60
        ms = (i * 137) % 1000
        level, template = actions[i % len(actions)]
        session_hash = hashlib.md5(b"main_session").hexdigest()[:8]

        msg = template.format(
            url=urls[i % len(urls)],
            selector=selectors[i % len(selectors)],
            title=f"Rippling - {['Login', 'Dashboard', 'Payroll', 'Documents', 'Billing'][i % 5]}",
            status=[200, 200, 200, 302, 200, 200, 404, 200][i % 8],
            count=(i * 3 + 1) % 25,
            duration=(i * 47 + 200) % 5000 + 100,
            step=i + 1,
            filename=f"statement_{months[i % len(months)].replace(' ', '_').lower()}.pdf",
            size=(i * 89 + 50) % 2000 + 50,
            account=accounts[i % len(accounts)],
            month=months[i % len(months)],
            amount=f"{(i * 437 + 1000) % 10000 + 500:.2f}",
            attempt=(i % 3) + 1,
            value=hashlib.md5(f"cookie_{i}".encode()).hexdigest()[:16],
        )

        lines.append(
            f"2026-03-30T{base_hour}:{base_min:02d}:{sec:02d}.{ms:03d}Z "
            f"{level:<5} [scraper:sess_{session_hash}] {msg}"
        )

    return "\n".join(lines)


def _generate_mixed_content(target_chars: int) -> str:
    """Generate mixed content (markdown doc with code, tables, and prose)."""
    sections = []

    sections.append("""# Architecture Decision Record: Agent Runtime V2

## Status: Accepted
## Date: 2026-03-15
## Authors: Franco Dominguez, Sarah Chen

## Context

The current scraper runtime (V1) has served us well for the past year, but we're hitting several limitations:

1. **Single-threaded agent execution**: Each container can only run one scraping session at a time, leading to poor resource utilization
2. **No memory persistence**: Agents start fresh every session, repeating the same discovery work
3. **Rigid tool set**: Adding new browser capabilities requires a full deployment
4. **No sub-agent support**: Complex multi-account scenarios can't be parallelized

We need to design V2 to address these limitations while maintaining backward compatibility with existing job definitions.

## Decision

We will rebuild the agent runtime with the following architecture:

### Core Components

```
+------------------+     +------------------+     +------------------+
|   RabbitMQ       |---->|   Orchestrator   |---->|   Agent Pool     |
|   Consumer       |     |   (per-container)|     |   (concurrent)   |
+------------------+     +------------------+     +------------------+
                               |                        |
                               v                        v
                         +------------------+     +------------------+
                         |   Memory Store   |     |   Browser Pool   |
                         |   (Azure Blob)   |     |   (Browserless)  |
                         +------------------+     +------------------+
```

### Agent Memory System

Each source code gets a persistent memory file stored in Azure Blob Storage:

```
azure://prod/memories/
  APP_RIPPLING_COM_memory.md
  WWW_FPL_COM_memory.md
  PORTAL_CONED_COM_memory.md
  ...
```

Memory files contain:
- Login flow specifics (e.g., "Rippling uses email-first login, password on second page")
- Navigation patterns (e.g., "Bills are under Payroll > Documents > Pay Statements")
- Known gotchas (e.g., "FPL requires clicking 'View All' before statements appear")
- Error recovery strategies learned from past failures

### Concurrent Session Support

The Orchestrator manages a pool of agents, each with its own browser context:

```typescript
interface OrchestratorConfig {
  maxConcurrentSessions: number;  // default: 4
  sessionTimeout: number;          // default: 900s
  memoryRefreshInterval: number;   // default: 300s
}
```

Resource allocation per session:
| Resource | Allocation |
|----------|-----------|
| CPU | 1 core |
| Memory | 2GB |
| Browser tab | 1 (isolated context) |
| Agent model | configurable per job |

### Sub-Agent Architecture

For complex scenarios (multi-account, parallel downloads), the primary agent can spawn sub-agents:

```typescript
interface SubAgentRequest {
  task: string;
  tools: string[];         // subset of parent's tools
  maxSteps: number;        // lower than parent
  browserContext: 'shared' | 'isolated';
  timeout: number;
}
```

Sub-agents share the parent's browser context by default but can request isolation. They report results back to the parent agent, which aggregates them.

### Tool Plugin System

Instead of hardcoded tools, V2 uses a plugin architecture:

```typescript
interface ToolPlugin {
  name: string;
  version: string;
  description: string;
  inputSchema: JSONSchema;
  execute(input: any, context: ToolContext): Promise<any>;
  healthCheck?(): Promise<boolean>;
}

// Core plugins (always available)
const corePlugins = [
  'navigate', 'click', 'fill', 'screenshot',
  'get_text', 'wait_for', 'download',
];

// Extended plugins (opt-in per job definition)
const extendedPlugins = [
  'pdf_extract',     // Extract text from downloaded PDFs
  'table_parse',     // Parse HTML tables into structured data
  'captcha_solve',   // Integration with captcha solving service
  'email_read',      // Read verification emails via IMAP
  'totp_generate',   // Generate TOTP codes for MFA
];
```

## Technical Details

### Container Sizing

| Tier | vCPU | Memory | Max Sessions | Use Case |
|------|------|--------|-------------|----------|
| Small | 2 | 4GB | 2 | Low-volume sources |
| Medium | 4 | 8GB | 4 | Standard sources |
| Large | 8 | 16GB | 8 | High-volume sources |

Auto-scaling rules:
- Scale up when queue depth > 10 messages for > 2 minutes
- Scale down when no active sessions for > 10 minutes
- Minimum 2 instances always running (for latency)
- Maximum 50 instances (cost cap)

### Error Handling Strategy

```
Session Error
  |
  +-- Recoverable?
  |     |
  |     +-- Yes: Retry with exponential backoff
  |     |     |
  |     |     +-- Max retries exceeded?
  |     |           |
  |     |           +-- Yes: Mark failed, alert team
  |     |           +-- No: Retry (delay: 2^attempt * 5s)
  |     |
  |     +-- No: Mark failed immediately
  |           |
  |           +-- Credential error? -> Notify team, pause connection
  |           +-- Site blocked? -> Add to cooldown queue
  |           +-- Unknown? -> Log for manual review
```

Recoverable errors:
- Network timeouts
- MFA challenge timeouts (user didn't respond)
- Rate limiting (429 responses)
- Temporary page load failures

Non-recoverable errors:
- Invalid credentials (wrong password)
- Account locked/suspended
- Site structure changed (selectors broken)
- Job definition error (invalid prompt)

### Migration Plan

Phase 1 (Week 1-2): Deploy V2 runtime alongside V1
- V2 handles 10% of traffic (canary)
- Both write to same results bucket
- Memory system populated from scratch

Phase 2 (Week 3-4): Ramp up V2 traffic
- 50% traffic to V2
- Monitor success rates, latency, cost
- Build up memory files from real sessions

Phase 3 (Week 5-6): Full migration
- 100% traffic to V2
- V1 kept as fallback for 2 weeks
- V1 decommissioned after validation

### Monitoring & Observability

New Grafana dashboards:
1. **Agent Performance**: Steps per session, tokens per session, success rate by model
2. **Memory Effectiveness**: Sessions with memory vs without, time savings
3. **Browser Pool Health**: Utilization, launch times, crash rate
4. **Cost Tracking**: Token spend per source, per team, per day

Alert rules:
- Success rate drops below 80% for any source (P2)
- Average session duration increases by 50% (P3)
- Browser pool exhaustion (P1)
- Memory store write failures (P2)
- Token spend exceeds daily budget (P3)

## Consequences

### Positive
- 4x throughput per container (concurrent sessions)
- Faster sessions via memory (skip discovery on repeat visits)
- Easier to add new capabilities via plugins
- Complex scenarios handled by sub-agents
- Better cost efficiency through right-sized containers

### Negative
- More complex deployment and debugging
- Memory files need ongoing curation
- Sub-agent coordination adds latency for simple cases
- Higher per-container memory footprint
- Need to maintain backward compatibility with V1 job definitions

### Risks
- Memory poisoning: bad session writes incorrect learnings
  - Mitigation: memory validation before write, human review of new entries
- Browser pool contention under load
  - Mitigation: circuit breaker, graceful degradation to single-session mode
- Cost overrun from sub-agent token usage
  - Mitigation: per-session token budget, sub-agent step limits

## References
- [V1 Architecture Doc](https://notion.so/deck/v1-architecture)
- [Anthropic Agent SDK Docs](https://docs.anthropic.com/agent-sdk)
- [Browserless Documentation](https://docs.browserless.io)
- [Azure Blob Storage Best Practices](https://learn.microsoft.com/azure/storage/blobs/best-practices)
""")

    current = "".join(sections)

    # Pad with additional realistic content if needed
    padding_sections = [
        "\n\n## Appendix A: Source Code Registry\n\n" + "\n".join(
            f"| {i+1} | {src} | {'Active' if i % 5 != 0 else 'Paused'} | {(i*7+3) % 50 + 1} connections | {['daily', 'weekly', 'hourly'][i % 3]} |"
            for i, src in enumerate([
                "APP_RIPPLING_COM", "WWW_FPL_COM", "PORTAL_CONED_COM", "APP_XCEL_ENERGY_COM",
                "WWW_PGE_COM", "MYACCOUNT_SRPNET_COM", "WWW_DUKE_ENERGY_COM", "SECURE_BC_HYDRO_COM",
                "ONLINE_AEP_COM", "MYACCOUNT_EVERSOURCE_COM", "CUSTOMER_XCELENERGY_COM",
                "SECURE_PEPCO_COM", "WWW_NATIONALGRIDUS_COM", "MYACCOUNT_CENTERPOINTENERGY_COM",
                "WWW_CONSUMERSENERGY_COM", "ACCOUNT_ENTERGY_COM", "WWW_FIRSTENERGYCORP_COM",
                "MYACCOUNT_AMEREN_COM", "WWW_WE_ENERGIES_COM", "MYACCOUNT_ALLIANTENERGY_COM",
            ])
        ),
        "\n\n## Appendix B: Error Code Reference\n\n" + "\n".join(
            f"- `{code}`: {desc}"
            for code, desc in [
                ("AUTH_FAILED", "Login credentials rejected by the target site"),
                ("AUTH_LOCKED", "Account has been locked due to too many failed attempts"),
                ("MFA_TIMEOUT", "MFA challenge was not responded to within the timeout period"),
                ("MFA_REJECTED", "MFA challenge was explicitly rejected by the user"),
                ("NAV_FAILED", "Navigation to expected page failed - URL may have changed"),
                ("NAV_BLOCKED", "Access blocked by the target site (WAF, CAPTCHA, IP block)"),
                ("SELECTOR_MISSING", "Expected page element not found - site layout may have changed"),
                ("DOWNLOAD_FAILED", "File download failed or was blocked"),
                ("PARSE_ERROR", "Failed to parse page content into expected format"),
                ("SESSION_TIMEOUT", "Session exceeded maximum allowed duration"),
                ("MAX_STEPS", "Agent exceeded maximum step count without completing"),
                ("NETWORK_ERROR", "Network connectivity issue during session"),
                ("RATE_LIMITED", "Target site returned 429 Too Many Requests"),
                ("MAINTENANCE", "Target site is in maintenance mode"),
                ("UNKNOWN", "Unclassified error - requires manual investigation"),
            ]
        ),
    ]

    for section in padding_sections:
        current += section

    # If still under target, generate additional prose to fill
    filler_paragraphs = [
        "The deployment pipeline consists of several stages that ensure code quality and reliability before reaching production. First, the CI system runs unit tests and linting checks against the pull request. If all checks pass, the code is merged into the main branch, which triggers the build pipeline. The build pipeline creates a Docker image, tags it with the commit SHA, and pushes it to the artifact registry. From there, the staging deployment is triggered automatically.\n\n",
        "Monitoring and observability are critical components of the system architecture. We use a combination of Prometheus metrics, Grafana dashboards, and structured logging to maintain visibility into system health. Each scraping session emits detailed metrics including duration, step count, token usage, and error codes. These metrics are aggregated into materialized views that power our analytics dashboards.\n\n",
        "The credential management system follows strict security practices. All credentials are encrypted at rest using AES-256-GCM and in transit using TLS 1.3. Credential rotation is supported through the API, allowing teams to update their stored credentials without recreating connections. Access to credentials is audited, and the encryption keys are stored in Google Cloud KMS with automatic rotation every 90 days.\n\n",
        "Error recovery is handled through a combination of automatic retries and manual intervention workflows. When a session fails with a recoverable error, the system automatically schedules a retry with exponential backoff. The maximum retry count is configurable per source code, with a default of 3 attempts. Non-recoverable errors trigger notifications to the team and pause the connection to prevent further failed attempts.\n\n",
        "The browser pool management system ensures efficient resource utilization across concurrent sessions. Each browser instance is allocated from a shared pool managed by the Browserless service. Instances are health-checked between sessions and recycled after a configurable number of uses to prevent memory leaks. The pool supports both Chrome and Firefox engines, with Chrome being the default for most sources.\n\n",
        "Rate limiting is implemented at multiple levels to protect both our infrastructure and the target websites. At the application level, we enforce per-source rate limits that respect each website's robots.txt and terms of service. At the infrastructure level, we use token bucket algorithms to smooth out request patterns and prevent burst traffic that might trigger WAF rules on target sites.\n\n",
        "The job definition system provides a flexible framework for defining scraping tasks. Each job definition includes a natural language prompt that instructs the AI agent on what to do, along with structured input and output schemas that ensure consistency. Job definitions are versioned, allowing teams to iterate on their prompts while maintaining a history of changes.\n\n",
        "Data validation occurs at multiple points in the pipeline. Input credentials are validated for format before being stored. Session results are validated against the output schema defined in the job definition. Downloaded files are checked for integrity using checksums. Financial data is cross-referenced when possible to detect inconsistencies.\n\n",
        "The team management system supports hierarchical access control. Each team has an owner who can manage connections, credentials, and job definitions. Team members can view session results and trigger new sessions but cannot modify credentials. API tokens are scoped to specific teams and can be configured with fine-grained permissions.\n\n",
        "Performance optimization is an ongoing effort driven by data from our analytics pipeline. We track key metrics like average session duration, steps per session, and tokens per session across all sources. Sources that consistently show degraded performance are flagged for review, and their job definitions are optimized. Common optimizations include refining navigation paths, adding memory entries for known page structures, and adjusting timeout values.\n\n",
        "The webhook notification system provides real-time updates to client applications. When a session completes or fails, the system sends a signed webhook payload to configured endpoints. Webhooks include retry logic with exponential backoff for failed deliveries. Clients can verify webhook authenticity using HMAC signatures. The system supports configurable event filters so clients only receive notifications for events they care about.\n\n",
        "Infrastructure as code is managed through Terraform modules organized by service. Each service has its own module that defines compute resources, networking, IAM permissions, and monitoring. Changes to infrastructure go through the same pull request review process as application code. The Terraform state is stored in a GCS backend with state locking to prevent concurrent modifications.\n\n",
        "Disaster recovery procedures are documented and tested quarterly. The system is designed with redundancy at every layer: multi-zone compute instances, replicated databases, and cross-region storage for critical data. Recovery time objectives vary by component, with the scraping pipeline targeting a 15-minute RTO and the dashboard targeting a 5-minute RTO. Backup verification is automated and runs nightly.\n\n",
        "The development workflow follows a trunk-based development model with short-lived feature branches. Pull requests require at least one approval and must pass all CI checks before merging. We use conventional commits for consistent changelog generation. Deployments to staging happen automatically on merge to main, while production deployments require manual approval through the CI pipeline.\n\n",
        "Cost management is tracked through custom Grafana dashboards that break down spend by service, team, and source code. The largest cost components are AI model tokens (approximately 60% of total cost), compute instances (25%), and browser service (15%). We optimize token usage by using smaller models for simple tasks and reserving larger models for complex scenarios that require advanced reasoning.\n\n",
    ]

    i = 0
    while len(current) < target_chars:
        current += filler_paragraphs[i % len(filler_paragraphs)]
        i += 1

    return current[:target_chars] if len(current) > target_chars else current


# Generate the computed test cases
TEST_CASES["huge_json_dataset"] = _generate_large_json_dataset(200)
TEST_CASES["huge_log_output"] = _generate_large_log_output(500)
TEST_CASES["huge_architecture_doc"] = _generate_mixed_content(50000)

# --- MASSIVE (100000-250000 chars) ---
TEST_CASES["massive_json_dataset"] = _generate_large_json_dataset(800)
TEST_CASES["massive_log_output"] = _generate_large_log_output(2000)
TEST_CASES["massive_mixed_content"] = _generate_mixed_content(100000)


def get_test_summary():
    """Print a summary of all test cases."""
    print(f"{'Name':<30} {'Length':>10} {'Words':>8}")
    print("-" * 52)
    total = 0
    for name, content in sorted(TEST_CASES.items(), key=lambda x: len(x[1])):
        if callable(content):
            continue
        length = len(content)
        words = len(content.split())
        total += 1
        print(f"{name:<30} {length:>10,} {words:>8,}")
    print("-" * 52)
    print(f"Total test cases: {total}")


if __name__ == "__main__":
    get_test_summary()
