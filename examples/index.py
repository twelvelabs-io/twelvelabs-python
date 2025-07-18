import os
import uuid

from twelvelabs import TwelveLabs
from twelvelabs.indexes import IndexesCreateRequestModelsItem


API_KEY = os.getenv("API_KEY")
assert (
    API_KEY
), "Your API key should be stored in an environment variable named API_KEY."


with TwelveLabs(api_key=API_KEY) as client:
    index = client.indexes.create(
        index_name=f"idx-{uuid.uuid4()}",
        models=[
            IndexesCreateRequestModelsItem(
                model_name="marengo2.7", model_options=["visual", "audio"]
            ),
            IndexesCreateRequestModelsItem(
                model_name="pegasus1.2", model_options=["visual", "audio"]
            ),
            # or you can provide the dict directly like this:
            # {
            #     "model_name": "marengo2.7",
            #     "model_options": ["visual", "audio"],
            # },
            # {
            #     "model_name": "pegasus1.2",
            #     "model_options": ["visual", "audio"],
            # },
        ],
        addons=["thumbnail"],
    )
    print(f"Created index: id={index.id}")

    index = client.indexes.retrieve(index_id=index.id)
    print(f"Retrieved index: id={index.id} name={index.index_name}")

    updated_name = f"idx-{uuid.uuid4()}"
    client.indexes.update(index_id=index.id, index_name=updated_name)
    updated_index = client.indexes.retrieve(index_id=index.id)
    print(f"Updated index name to {updated_index.index_name}")

    print("All Indexes: ")
    indexes_pager = client.indexes.list()
    for index in indexes_pager:
        print(f"  id={index.id} name={index.index_name} created_at={index.created_at}")
