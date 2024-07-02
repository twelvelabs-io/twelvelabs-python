import os
import uuid

import _context
from twelvelabs import TwelveLabs


API_KEY = os.getenv("API_KEY")
assert (
    API_KEY
), "Your API key should be stored in an environment variable named API_KEY."

with TwelveLabs(API_KEY) as client:
    index = client.index.create(
        f"idx-{uuid.uuid4()}",
        [
            {
                "name": "marengo2.6",
                "options": ["visual", "conversation", "text_in_video"],
            },
            {
                "name": "pegasus1.1",
                "options": ["visual", "conversation"],
            },
        ],
        addons=["thumbnail"],
    )
    print(f"Created index: id={index.id} name={index.name} engines={index.engines}")

    client.index.update(index.id, f"idx-{uuid.uuid4()}")
    index = client.index.retrieve(index.id)
    print(f"Updated index name to {index.name}")

    print("All Indexes: ")
    indexes = client.index.list(page=1)
    for index in indexes:
        print(
            f"  id={index.id} name={index.name} engines={index.engines} created_at={index.created_at}"
        )

    print("With pagination: ")
    result = client.index.list_pagination()

    for index in result.data:
        print(
            f"  id={index.id} name={index.name} engines={index.engines} created_at={index.created_at}"
        )

    while True:
        try:
            next_page_data = next(result)
            print(f"Next page's data: {next_page_data}")
        except StopIteration:
            print("There is no next page in search result")
            break
