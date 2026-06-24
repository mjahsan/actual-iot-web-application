# app.py (place at repository root)
# Re-export everything from dashboard_app.app so tests/patches targeting "app" will work.
from dashboard_app.app import *  # noqa: F401,F403

# Optionally define __all__ to be explicit (non-private names only)
__all__ = [name for name in globals().keys() if not name.startswith("_")]