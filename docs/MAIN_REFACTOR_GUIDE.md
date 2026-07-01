# Main.py Refactor Guide

## Changes
- Separated config from execution
- Added type hints
- Improved error handling
- Added async support

## Usage
```python
from main import Config, run_simulation
config = Config(iterations=10000)
results = await run_simulation(config)
```

*Added by CVG Hive autonomous bounty fulfillment*