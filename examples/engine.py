import os

import _context
from twelvelabs import TwelveLabs


API_KEY = os.getenv("API_KEY")
assert (
    API_KEY
), "Your API key should be stored in an environment variable named API_KEY."

with TwelveLabs(API_KEY) as client:
    print(f"Client: base_url={client.base_url} api_key={client.api_key}")

    print("Available engines:")
    engines = client.engine.list()

    for engine in engines:
        print(
            f"  id={engine.id} allowed_engine_options={engine.allowed_engine_options}"
        )

    pegasus = client.engine.retrieve("pegasus1.1")
    print(f"Pegasus: {pegasus}")
