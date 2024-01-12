import os

from twelvelabs import TwelveLabs
import uuid


def main():
    API_KEY = os.getenv("API_KEY")
    assert (
        API_KEY
    ), "Your API key should be stored in an environment variable named API_KEY."

    with TwelveLabs(API_KEY) as client:
        print("Available engines:")
        engines = client.engine.list()

        for engine in engines:
            print(
                f"id={engine.id} allowed_index_options={engine.allowed_index_options}"
            )

        index = client.index.create(
            f"idx-{uuid.uuid4()}",
            [
                {
                    "name": "marengo2.5",
                    "options": ["visual", "conversation", "text_in_video", "logo"],
                }
            ],
        )
        client.index.update(index.id, f"idx-{uuid.uuid4()}")

        print("Indexes: ")
        indexes = client.index.list()
        for index in indexes:
            print(
                f"id={index.id} name={index.name} engines={index.engines} created_at={index.created_at}"
            )


if __name__ == "__main__":
    main()
