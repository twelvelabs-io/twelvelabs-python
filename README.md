# TwelveLabs Python SDK

The TwelveLabs SDK has been developed to be compatible with the v1.2 API. The most significant change is the ability to use the multi-engine option when creating an index; please refer to the API Docs for more information.

## For Internal Test

Since it's before uploading to PyPI, you will install the package in editable mode after cloning the git repository.

```sh
git clone https://github.com/twelvelabs-io/twelvelabs-python
cd twelvelabs-python
pip install -e .
```

Afterward, you can import and use the package from your repository.

```python
from twelvelabs import TwelveLabs
client = TwelveLabs("<YOUR_API_KEY>")

engines = client.engine.list()
```

If you want to use development environment, set `TWELVELABS_BASE_URL` to enviroment variables. It'll automatically applied to your client.

## Installation

> Not supported yet

```sh
pip install twelvelabs
```

## Usage

All APIs of this library can be found in the `API.md` file. Additionally, the `examples` folder contains sample files categorized by their functionality.

```python
import os

from twelvelabs import TwelveLabs

client = TwelveLabs(os.getenv("TWELVELABS_API_KEY"))
client.index.create(
        f"my_index",
        [
            {
                "name": "pegasus1",
                "options": ["visual", "conversation"],
            },
        ],
        addons=["thumbnail"],
    )
```

When initializing the client, you must provide the API Key issued from the TwelveLabs Dashboard. Be cautious not to store the API Key in source control when using it. Currently, only synchronous usage is supported, and API communications are handled through httpx. (Support for an Async Client is planned for the future.)

## Error Handling

All errors are included in the twelvelabs package. If there is an issue connecting to the API, a twelvelabs.APIConnectionError will be raised. Errors like 4xx and 5xx status codes can be imported and handled according to the specific status code that occurs.

```python
import os

from twelvelabs import TwelveLabs

client = TwelveLabs(os.getenv("TWELVELABS_API_KEY"))
try:
    engines = client.engines.list()
    print(engines)
except twelvelabs.APIConnectionError as e:
    print("Cannot connect to API server")
except twelvelabs.BadRequestError as e:
    print("Bad request, please refer to api docs")
except twelvelabs.APIStatusError as e:
    print(f"Status code {e.status_code} received")
    print(e.response)
```

## TODO

- cli
- validate video before upload
