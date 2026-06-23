# simulator.py (place at repository root)
# Re-export everything from data_simulator.simulator so tests/patches targeting "simulator" will work.
from data_simulator.simulator import *  # noqa: F401,F403

# Optionally define __all__ to be explicit (non-private names only)
__all__ = [name for name in globals().keys() if not name.startswith("_")]