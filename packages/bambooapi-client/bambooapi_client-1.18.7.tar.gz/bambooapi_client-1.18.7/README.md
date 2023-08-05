# Python client for Bamboo REST API

[![PyPI Version](https://img.shields.io/pypi/v/bambooapi-client.svg)](https://pypi.org/project/bambooapi-client/)
[![Python Versions](https://img.shields.io/pypi/pyversions/bambooapi-client.svg)](https://pypi.org/project/bambooapi-client/)


The Bamboo REST API provides access to flexibility assets managed by Bamboo 
Energy:

- Create and list flexibility sites & assets
- Post and get measurements for specific assets
- Obtain activations for specific assets

The sandboxed version of the API to be used for development & testing is 
available at: https://dev-sandbox.bambooenergy.tech/v1/docs

## Installation & Usage

You can install the package directly using:

```sh
pip install bambooapi-client
```

Then import the package:

```python
import bambooapi_client
```

## Getting Started

First, import the `BambooAPIClient` class and initialize it with the API URL 
and the API bearer token that was assigned to you.

```python
from bambooapi_client import BambooAPIClient

bambooapi_url = 'https://dev-sandbox.bambooenergy.tech/v1'
bambooapi_token = 'your_token'

client = BambooAPIClient(url=bambooapi_url, token=bambooapi_token)
```

You can now access the **Sites API** and its methods

```python
sites_api = client.sites_api()
```

### Retrieving Site Metadata

You can then list all the sites related to your API user with the 
`list_sites` command.

```python
sites_api.list_sites()
```

Given a site name, you can obtain a site ID and retrieve the site's detailed 
description

```python
site_id = sites_api.get_site_id('dummy_building_1')
sites_api.get_site(site_id)
```

Given a site ID, you can now retrieve information about a particular zone or 
device

```python
sites_api.get_thermal_zone(site_id, 'zone1')
sites_api.get_device(site_id, 'hvac1')
```

### Retrieving and pushing Site Measurements

Given a site ID you can retrieve measurements for a specific period.

```python
from datetime import datetime, timezone
sites_api.read_device_measurements(
    site_id=site_id,
    device_name='meter',
    start=datetime(2021, 6, 3, 8, tzinfo=timezone.utc),
    stop=datetime(2021, 6, 3, 20, tzinfo=timezone.utc),
)
```

On the other hand, you can also upload new measurements (or update existing 
measurements). For that, new measurements must first be converted to a `pandas`
DataFrame. **1 or more data points can be uploaded at once**.

```python
import pandas as pd

data_points = [
    {
        'time': '2021-06-03T07:00:00+00:00',
        'power': 12.0,
        'quality': 1
    },
    {
        'time': '2021-06-03T07:15:00+00:00',
        'power': 15.0,
        'quality': 1
    }
]

new_data_points = pd.DataFrame.from_records(data_points, index='time')
sites_api.update_device_measurements(site_id, 'meter', new_data_points)
```

### Retrieving Activations (BETA)

You can test how activations would be retrieved with the following command.

```python
sites_api.read_device_activations(site_id, 'hvac1')
```

This feature is not fully operational yet, and the endpoint currently returns mock data only. However, the response format should remain the same.
