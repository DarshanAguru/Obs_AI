# Obs_AI Python SDK (`obs_ai` / `Obs_AI`)

The official, high-performance Python client library for Obs_AI — the self-hosted AI debugging and observability platform.

## Features

- 🌲 **Dual Sync & Async Tracing**: Trace synchronous functions and `asyncio` coroutines using `@trace` and `with span(...)`. Both `import obs_ai` and `import Obs_AI` are supported.
- ⚡ **Non-Blocking Background Export**: Bounded memory queue (`AsyncExporter`) ensures telemetry export never adds latency to production loops.
- 🦜 **First-Class Framework Integrations**:
  - `obs_ai.integrations.azure`: `wrap_azure_openai(client)` and `wrap_azure_ai(client)` for Azure OpenAI & Azure AI Foundry, supporting both LangChain (`AzureChatOpenAI`) and raw SDK clients.
  - `obs_ai.integrations.openai`: `wrap_openai(client)` with automatic token counts and model pricing calculations for OpenAI & LangChain (`ChatOpenAI`).
  - `obs_ai.integrations.anthropic`: `wrap_anthropic(client)` wrapping Claude messages and LangChain (`ChatAnthropic`).
  - `obs_ai.integrations.gemini`: `wrap_gemini(client)` for Google Gemini SDK and LangChain (`ChatGoogleGenerativeAI`).
  - `obs_ai.integrations.langchain`: `ObsAiCallbackHandler` capturing chains, LLMs, tools, and retrievers.
- 💵 **Dynamic & Tunable Pricing Registry**: Built-in default rates for OpenAI, Anthropic, Gemini, Mistral, and DeepSeek, with developer override APIs (`obs_ai.configure(model_pricing={...})`).
- 🛡️ **Sensitive Data Redaction**: Automatic masking of passwords, credit cards, bearer tokens, and API keys.
- 🔁 **Trace Replay Engine**: Mock and replay execution trees for deterministic offline testing.

## Installation

```bash
# Using uv (Recommended)
uv add obs-ai

# Or using pip
pip install obs-ai
```

## Quickstart Examples

### 1. Manual Tracing with Spans & Customization

```python
import obs_ai
from obs_ai import trace, span, configure
from obs_ai.exporters import HTTPExporter, AsyncExporter

configure(exporter=AsyncExporter(HTTPExporter("http://localhost:8000")))

@trace(name="rag_search_agent", span_type="agent", capture_input=True, capture_output=True)
def run_agent(query: str):
    obs_ai.set_user("user_401")
    obs_ai.set_tag("pipeline", "compliance")

    # Vector Search Span
    with span("hybrid_search", span_type="retrieval") as s:
        s.input = {"query": query}
        docs = ["Obs_AI is a self-hosted AI observability platform."]
        s.output = {"documents": docs}
        obs_ai.add_event("docs_retrieved", {"count": len(docs)})

    # LLM Completion Span
    with span("llm_completion", span_type="llm") as s:
        s.input = {"prompt": query, "context": docs}
        response = "Obs_AI runs locally with zero external dependencies."
        s.output = {"response": response}
        s.set_llm_metrics(
            model="gpt-4o",
            prompt_tokens=180,
            completion_tokens=42,
            cost=0.00087,
        )
        return response
```

### 2. LangChain Chat Models & Azure OpenAI Auto-Instrumentation

```python
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from obs_ai.integrations import wrap_azure_openai, wrap_openai

# Azure OpenAI (LangChain AzureChatOpenAI or raw AzureOpenAI)
azure_llm = wrap_azure_openai(
    AzureChatOpenAI(
        azure_endpoint="https://my-resource.openai.azure.com/",
        api_key="AZURE_API_KEY",
        azure_deployment="gpt-4o",
        api_version="2024-02-01",
    )
)

# OpenAI (LangChain ChatOpenAI or raw OpenAI)
openai_llm = wrap_openai(ChatOpenAI(model="gpt-4o"))

# Telemetry, tokens, and errors are captured automatically across .invoke() / .ainvoke()
response = azure_llm.invoke([("user", "Explain quantum computing in 2 sentences")])
```

### 3. Pluggable Telemetry Exporters

```python
import obs_ai
from obs_ai.exporters import (
    AsyncExporter,
    HTTPExporter,
    JSONLExporter,
    ConsoleExporter,
    CompositeExporter,
)

# 1. Non-Blocking Async Exporter (Default for Production)
obs_ai.configure(
    exporter=AsyncExporter(
        HTTPExporter(
            endpoint="http://localhost:8000",
            api_key="your_api_key",
            project_id="prod-workspace",
        )
    )
)

# 2. Local File Exporter (Air-gapped / CI / Offline Replay)
obs_ai.configure(exporter=JSONLExporter("traces.jsonl"))

# 3. Terminal Console Exporter
obs_ai.configure(exporter=ConsoleExporter(verbose=True))

# 4. Multi-Destination Composite Exporter
obs_ai.configure(
    exporter=CompositeExporter([
        AsyncExporter(HTTPExporter("http://localhost:8000")),
        JSONLExporter("audit_traces.jsonl"),
        ConsoleExporter(verbose=False),
    ])
)
```

### 4. Custom Pricing Overrides

```python
import obs_ai

obs_ai.configure(
    model_pricing={
        "gpt-4o": (2.50, 10.00),          # $2.50 prompt / $10.00 completion per 1M tokens
        "custom-llama-3": (0.30, 0.90),
    }
)
```
