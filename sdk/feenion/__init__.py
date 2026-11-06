"""
Backward-compatibility module for `feenion`.
The project has been renamed to `Obs_AI` (package: `obs_ai` / `Obs_AI`).
"""
import sys
import importlib
import warnings
import obs_ai
from obs_ai import *  # noqa: F401, F403
from obs_ai import __all__ as _obs_ai_all
from obs_ai import __version__

warnings.warn(
    "The 'feenion' package has been renamed to 'Obs_AI' / 'obs_ai'. "
    "Please update your imports to 'import obs_ai' or 'import Obs_AI'.",
    DeprecationWarning,
    stacklevel=2,
)

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
        sys.modules[f"feenion.{mod_name}"] = sub
        setattr(obs_ai, mod_name, sub)
    except Exception:
        pass

try:
    tracer_mod = importlib.import_module("obs_ai.tracer")
    sys.modules["feenion.tracer"] = tracer_mod
except Exception:
    pass

sys.modules["feenion"] = obs_ai
