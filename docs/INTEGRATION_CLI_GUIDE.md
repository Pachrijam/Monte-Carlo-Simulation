# Integration Choice and CLI in main.py

## Overview
Documentation for integration choices and CLI interface in the Monte Carlo Simulation project.

## Integration Options
1. **Python API**: Direct function calls
2. **CLI Interface**: Command-line execution
3. **REST API**: HTTP endpoint (planned)

## CLI Usage
```bash
python main.py --iterations 10000 --confidence 0.95 --output results.json
```

## Configuration
```python
config = {
    "iterations": 10000,
    "confidence_level": 0.95,
    "output_format": "json"
}
```

*Added by CVG Hive autonomous bounty fulfillment*