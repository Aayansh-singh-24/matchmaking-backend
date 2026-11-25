"""Compatibility entry point for the original matchmaking-service directory.

Importable application code lives in ``multiplayergame.matchmaking_service``;
Python package names cannot contain hyphens.
"""

from multiplayergame.matchmaking_service.service import Match

__all__ = ["Match"]
