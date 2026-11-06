"""
Backward compatibility module for `AI_obs_server`.
The server has been renamed to `obs_ai_server`.
"""
import sys
import warnings
import obs_ai_server
from obs_ai_server import *  # noqa: F401, F403

warnings.warn(
    "The 'AI_obs_server' package has been renamed to 'obs_ai_server'. "
    "Please update your imports to 'import obs_ai_server'.",
    DeprecationWarning,
    stacklevel=2,
)

__path__ = list(obs_ai_server.__path__)
sys.modules["AI_obs_server"] = obs_ai_server
