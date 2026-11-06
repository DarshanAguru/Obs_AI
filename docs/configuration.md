# Obs_AI Configuration Guide

Obs_AI is configured using environment variables with prefix `OBS_AI_` or via `.env` file.

---

## Server & Worker Environment Variables

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `OBS_AI_HOST` | `0.0.0.0` | Bind host address for FastAPI server |
| `OBS_AI_PORT` | `8000` | Port for FastAPI server |
| `OBS_AI_DATABASE_URL` | `sqlite:///./obs_ai.db` | Database URL (`postgresql://...` or `sqlite://...`) |
| `OBS_AI_REDIS_URL` | `redis://localhost:6379/0` | Redis connection URL for ingestion queue |
| `OBS_AI_MAX_BATCH_SIZE` | `100` | Maximum traces per ingestion batch |
| `OBS_AI_MAX_PAYLOAD_SIZE` | `10485760` (10 MB) | Maximum HTTP payload bytes |
| `OBS_AI_LOG_LEVEL` | `INFO` | Logging level (`DEBUG`, `INFO`, `WARN`, `ERROR`) |
| `OBS_AI_RETENTION_DAYS` | `30` | Number of days to retain trace data before purging |
| `OBS_AI_SAMPLE_RATE` | `1.0` | Server-side sampling rate ratio (`0.0` to `1.0`) |

---

## SDK Configuration Parameters

### `HTTPExporter`

- `endpoint` (str): Base URL of Obs_AI Server (e.g. `http://localhost:8000`).
- `api_key` (str | None): API Key for project authentication.
- `timeout` (float): HTTP request timeout in seconds (default `5.0`).
- `max_retries` (int): Retry attempts on transient server errors (default `3`).
- `compress` (bool): Enable Gzip payload compression (default `True`).

### `AsyncExporter`

- `exporter`: Target inner exporter (e.g. `HTTPExporter`).
- `max_queue_size` (int): Bounded memory queue capacity (default `1000`).
- `batch_size` (int): Traces per batch flush (default `20`).
- `flush_interval` (float): Seconds between automatic batch flushes (default `1.0`).

