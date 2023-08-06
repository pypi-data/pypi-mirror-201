# TON Play Public API Connector Python

[![PyPI version](https://img.shields.io/pypi/v/tonplay-connector)](https://pypi.python.org/pypi/tonplay-connector)

## Installation

```bash
pip install tonplay-connector
```

## RESTful APIs

Usage examples:
```python
from tonplay.methods import TonPlayApi

client = TonPlayApi(api_key="YOUR API KEY")

# Get assets on sale
print(client.get_assets_on_sale())