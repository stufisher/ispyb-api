[![Build Status](https://www.travis-ci.org/DiamondLightSource/python-ispyb.svg?branch=master)](https://www.travis-ci.org/DiamondLightSource/python-ispyb)

# ISPyB pypi package
This package provides a python interface to [ISPyB](http://www.esrf.eu/ispyb)
via the official ISPyB webservices API or direct database access.

## Usage example

```python
import ispyb
api = ispyb.driver(ispyb.Backend.DATABASE)
i = api(config_file='credentials.cfg')
rp = i.get_reprocessing_id(rpid)
print(rp['displayName'])
```
