"""
Obs_AI Python SDK (case-matching namespace alias for `obs_ai`).
Allows `import Obs_AI` as well as `from Obs_AI import trace, span, configure`.
"""
import sys
import importlib
import obs_ai
from obs_ai import *  # noqa: F401, F403
from obs_ai import __all__ as _obs_ai_all
from obs_ai import __version__

__all__ = _obs_ai_all
__path__ = list(obs_ai.__path__)

for mod_name in [
    "exporters",
    "integrations",
    "models",
    "pricing",
    "redaction",
    "sampling",
    "serializer",
    "context",
    "replay",
]:
    try:
        sub = importlib.import_module(f"obs_ai.{mod_name}")
        sys.modules[f"Obs_AI.{mod_name}"] = sub
        setattr(obs_ai, mod_name, sub)
    except Exception:
        pass

try:
    tracer_mod = importlib.import_module("obs_ai.tracer")
    sys.modules["Obs_AI.tracer"] = tracer_mod
except Exception:
    pass

sys.modules["Obs_AI"] = obs_ai
