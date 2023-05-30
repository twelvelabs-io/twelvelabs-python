# Twelve Labs Python SDK

This SDK provides a convenient way to interact with the Twelve Labs Video Understanding Platform from an application written in the Python language. The SDK equips you with a set of intuitive classes and methods that streamline the process of interacting with the platform, reducing the boilerplate code you have to write.

## Prerequisites

Before using the SDK, ensure that you have the following prerequisites:

-  [Python](https://www.python.org) version TODO or newer.
-  An active API key. If you don't have one, please [sign up](https://api.twelvelabs.io/) for a free account. Then, to retrieve your API key, go to the [Dashboard](https://api.twelvelabs.io/dashboard) page, and select the **Copy** button under the **API** Key section.
-  Your API key is stored in a variable named `API_KEY`.

## Installation

**Question**: Do we want to encourage them to use [virtualenv](https://virtualenv.pypa.io/en/latest/) and  [asyncio](https://docs.python.org/3/library/asyncio.html)?

To install the SDK, follow the steps below:

TODO

## Initialization

You must initialize the SDK using your API key:

```Python
import asyncio
from twelvelabs import APIClient

async def main():
	API_KEY = os.getenv("API_KEY")
	assert API_KEY, "Your API key should be stored in an environment variable named API_KEY."
	async with APIClient(API_KEY) as client:
		#

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

## Usage

The following example code uploads creates an index:

```Python
print("Creating a new index named 'example_index' with default options")
index = await client.create_index("example_index")

print(f"Created an index: {index.name}({index.id})")
```

## Errors