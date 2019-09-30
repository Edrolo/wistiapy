# Wistia Python client

A Python client for the [Wistia Data API](https://wistia.com/support/developers/data-api)

![](https://github.com/Edrolo/wistiapy/workflows/Python%20Tests/badge.svg)
[![PyPI version](https://badge.fury.io/py/wistiapy.svg)](https://badge.fury.io/py/wistiapy)

## Installation
```bash
pip install wistiapy
```

You'll need to create an access token [as documented](https://wistia.com/support/developers/data-api#creating-and-managing-access-tokens).

## Usage

```python
from wistia import WistiaClient
wistia = WistiaClient(api_password='YOUR_API_PASSWORD')
projects = wistia.list_projects()
```

Alternatively, you can set your password in an environment variable, or, if using Django, in a
setting called `WISTIA_API_PASSWORD`. Then use the factory function:
```python
from wistia import get_wistia_client
wistia = get_wistia_client()
```

## Dummy Client
Included is a mock version of the client for testing purposes. It will log any calls made to it,
and attempts to respond in the same manner as the live service. Currently a work-in-progress.
If using Django, including the setting `WISTIA_CLIENT_CLASS = 'WistiaDummyClient'` will make
`get_wistia_client` provide a dummy client.
