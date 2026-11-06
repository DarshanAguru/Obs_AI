# Obs_AI System Architecture

Obs_AI separates runtime instrumentation from backend processing for zero impact on application latency.

```text
 Developer AI Application
          │
          ▼
   Obs_AI Python SDK
          │
  (Async Bounded Queue)
          │
          ▼ (HTTP / Gzip / Retries)
   Obs_AI Server API
          │
          ▼
     Redis Queue
          │
          ▼
   Ingestion Worker
          │
          ▼
   PostgreSQL Database
          │
    ┌─────┴─────┐
    ▼           ▼
Query API    Web UI Dashboard
```

## Core Components

1. **Obs_AI SDK**: Zero-overhead Python library supporting `@trace` decorator, `with span(...)` context managers, automatic `contextvars` propagation, sensitive data redaction, and `AsyncExporter` bounded batching.
2. **FastAPI Ingestion Server**: Accepts telemetry payload batches, validates API keys and schemas, and pushes batches to Redis queue with low-latency acknowledgment (`< 5ms`).
3. **Redis & Background Worker**: Asynchronous queue and multi-threaded worker handling database transactions, retry strategies, dead-letter fallbacks, and schema upserts.
4. **PostgreSQL Storage**: Relational store indexed on `project_id`, `trace_id`, `span_id`, `parent_span_id`, `status`, and `start_time` for fast timeline querying.
5. **Web UI Dashboard**: React + HTML5 dashboard for visual debugging of trace trees, Gantt chart timelines, LLM prompts, token costs, and error fingerprints.

