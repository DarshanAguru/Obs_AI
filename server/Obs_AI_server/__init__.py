"""
Obs_AI Server package (case alias for `obs_ai_server`).
"""
import sys
import obs_ai_server
from obs_ai_server import *  # noqa: F401, F403

__path__ = list(obs_ai_server.__path__)
sys.modules["Obs_AI_server"] = obs_ai_server
