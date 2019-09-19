# Wistia Python client

A Python client for the [Wistia Data API](https://wistia.com/support/developers/data-api)

![](https://github.com/Edrolo/wistiapy/workflows/python-test/badge.svg)

## Installation
```bash
pip install wistiapy
```

You'll need to create an access token [as documented](https://wistia.com/support/developers/data-api#creating-and-managing-access-tokens).

## Usage

```python
from wistia.api import WistiaClient
wistia = WistiaClient(api_password='YOUR_API_PASSWORD')
projects = wistia.list_projects()
```
