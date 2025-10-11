"""timelapse_lib package - lightweight helpers for capturing photos and sending Discord messages.

Import paths:
  from timelapse_lib import capture, config, discord_webhook, cli

This package is intentionally small and dependency-light so tests and other
tools can import `capture` without loading network code.
"""

__all__ = ["config", "capture", "discord_webhook", "cli"]
