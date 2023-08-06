# SHT Rest Interface

It is made by two modules to interact with the Juice Core Uplink 
API.

## Install

The module is now contributed to PyPI, just call

```bash
pip install juice_core_uplink_api_client
```

to install the module. If you use poetry to build your package and you want to add it as a dependency use:

```bash
poetry add juice_core_uplink_api_client
```

if you need to test development version (the main branch in this repository):

```bash
pip install "git+https://www.ict.inaf.it/gitlab/juice-janus/sht_rest_interface.git#egg=juice-core-uplink-api-client&subdirectory=juice-core-uplink-api-client"
```

## juice-core-uplink-api-client

This module is automatically generated using the command below. It must not be 
modified manually.

```bash 
 openapi-python-client update --path openapi.json 
```

or just using the makefile `make` shortcut. The command is expected to be runt 
from the root of the repository (where the makefile is located) and requires 
`openapi-python-client` to be installed in the host system.

The module is generated from the openapi definition available at 
https://juicesoc.esac.esa.int/docs/, but **notice** that the openapi.json definition is a modified version of the one 
available at that link. The file was modified by:

- updating the file to openapi 3.1
- making several changes to fix inconsistencies in the definition

The original files are mantained here for simplicity:

1. `openapi_source.json` -> as downloaded from [swagger](https://juicesoc.esac.esa.int/docs/)
2. `openapi_converted.json` -> updated to version 3.x using [https://converter.swagger.io/#/Converter/convertByUrl](swagger converter service)
3. `openapi.json` -> used to generate the module with openapi-python-client

Also note that only some issues were corrected in the openapi.json file,
hence the generated module is not complete, and it is not granted to work.
If you find any additional inconsistency, please report it to the repo issue 
tracker.


## juice_core 

this module is a wrapper around the automatically generated module. It is made 
by a class with several methods to interact with the API. It is just a stub to 
start disucssing the API interface. It is not complete and it is not guaranteed 
to work.

## Usage example

First, create a client:

```python
from juice_core import SHTRestInterface
i = SHTRestInterface()
```

and access the list of available plans on the server:

```python
i.plans()
```

will output a pandas dataframe with the list of plans (just some here):

|    | trajectory   | name                       | mnemonic                   | is_public   | created                    |   id | author   | description                                                                                                                                                           | refine_log   | ptr_file                                                                |
|---:|:-------------|:---------------------------|:---------------------------|:------------|:---------------------------|-----:|:---------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-------------|:------------------------------------------------------------------------|
|  0 | CREMA_3_0    | CASE4                      | CASE4                      | True        | 2021-03-04 13:29:58.835199 |   17 | rlorente | Demonstration Case 4                                                                                                                                                  |              |                                                                         |
|  1 | CREMA_5_0    | CREMA_5_0_OPPORTUNITIES_v0 | CREMA_5_0_OPPORTUNITIES_v0 | True        | 2021-08-26 09:12:06.767139 |   31 | cvallat  | 1st run opf opportunities generation (UC22), based on existing definitions of oppportunities (inherited from crema 3_0)                                               |              | https://juicesoc.esac.esa.int/rest_api/file/trajectory%23CREMA_5_0.ptx/ |
|  2 | CREMA_5_0    | CREMA_5_0_OPPORTUNITIES_v1 | CREMA_5_0_OPPORTUNITIES_v1 | True        | 2021-10-04 13:49:49.262682 |   36 | cvallat  | Added two opportunities for JMAG_CALROL for the last 2 perijoves before JOI (PJ69 not considered since too clsoe to GoI for observations to take place --> MPAD rule) |              | https://juicesoc.esac.esa.int/rest_api/file/trajectory%23CREMA_5_0.ptx/ |
|  3 | CREMA_5_0    | CREMA_5_0_OPPORTUNITIES_v2 | CREMA_5_0_OPPORTUNITIES_v2 | True        | 2021-10-05 07:24:07.742653 |   37 | cvallat  | Modified GANYMEDE_GM opportunity around 3G3 for WG3 prime allocation (1 hour centered at CA)                                                                          |              | https://juicesoc.esac.esa.int/rest_api/file/trajectory%23CREMA_5_0.ptx/ |


You can also directly interact with the underalying `juice-core-uplink-api-client` module:


### juice-core-uplink-api-client

A client library for accessing Juice Core Uplink API

docs at https://juicesoc.esac.esa.int/docs/

browsable at https://juicesoc.esac.esa.int/readonly_admin/core/

## Usage

First, create a client:

```python
from juice_core_uplink_api_client import Client

client = Client(base_url="https://api.example.com")
```

If the endpoints you're going to hit require authentication, use `AuthenticatedClient` instead:

```python
from juice_core_uplink_api_client import AuthenticatedClient

client = AuthenticatedClient(base_url="https://api.example.com", token="SuperSecretToken")
```

Now call your endpoint and use your models:

```python
from juice_core_uplink_api_client.models import MyDataModel
from juice_core_uplink_api_client.api.my_tag import get_my_data_model
from juice_core_uplink_api_client.types import Response

my_data: MyDataModel = get_my_data_model.sync(client=client)
# or if you need more info (e.g. status_code)
response: Response[MyDataModel] = get_my_data_model.sync_detailed(client=client)
```

Or do the same thing with an async version:

```python
from juice_core_uplink_api_client.models import MyDataModel
from juice_core_uplink_api_client.api.my_tag import get_my_data_model
from juice_core_uplink_api_client.types import Response

my_data: MyDataModel = await get_my_data_model.asyncio(client=client)
response: Response[MyDataModel] = await get_my_data_model.asyncio_detailed(client=client)
```

By default, when you're calling an HTTPS API it will attempt to verify that SSL is working correctly. Using certificate verification is highly recommended most of the time, but sometimes you may need to authenticate to a server (especially an internal server) using a custom certificate bundle.

```python
client = AuthenticatedClient(
    base_url="https://internal_api.example.com", 
    token="SuperSecretToken",
    verify_ssl="/path/to/certificate_bundle.pem",
)
```

You can also disable certificate validation altogether, but beware that **this is a security risk**.

```python
client = AuthenticatedClient(
    base_url="https://internal_api.example.com", 
    token="SuperSecretToken", 
    verify_ssl=False
)
```

Things to know:
1. Every path/method combo becomes a Python module with four functions:

    1. `sync`: Blocking request that returns parsed data (if successful) or `None`
    1. `sync_detailed`: Blocking request that always returns a `Request`, optionally with `parsed` set if the request was successful.
    1. `asyncio`: Like `sync` but async instead of blocking
    1. `asyncio_detailed`: Like `sync_detailed` but async instead of blocking

1. All path/query params, and bodies become method arguments.
1. If your endpoint had any tags on it, the first tag will be used as a module name for the function (my_tag above)
1. Any endpoint which did not have a tag will be in `juice_core_uplink_api_client.api.default`

## Building / publishing this Client

This project uses [Poetry](https://python-poetry.org/) to manage dependencies  and packaging.  Here are the basics:

1. Update the metadata in pyproject.toml (e.g. authors, version)
1. If you're using a private repository, configure it with Poetry
    1. `poetry config repositories.<your-repository-name> <url-to-your-repository>`
    1. `poetry config http-basic.<your-repository-name> <username> <password>`
1. Publish the client with `poetry publish --build -r <your-repository-name>` or, if for public PyPI, just `poetry publish --build`

If you want to install this client into another project without publishing it (e.g. for development) then:

1. If that project **is using Poetry**, you can simply do `poetry add <path-to-this-client>` from that project
1. If that project is not using Poetry:
    1. Build a wheel with `poetry build -f wheel`
    1. Install that wheel from the other project `pip install <path-to-wheel>`
