import os
import asyncio

from twelvelabs import AsyncTwelveLabs


API_KEY = os.getenv("API_KEY")
assert (
    API_KEY
), "Your API key should be stored in an environment variable named API_KEY."


async def list_indexes():
    async with AsyncTwelveLabs(api_key=API_KEY) as client:
        indexes_pager = await client.indexes.list()
        print("All Indexes: ")
        async for index in indexes_pager:
            print(
                f"  id={index.id} name={index.index_name} created_at={index.created_at}"
            )


async def search():
    index_id = "<YOUR_INDEX_ID>"
    async with AsyncTwelveLabs(api_key=API_KEY) as client:
        search_pager = await client.search.query(
            index_id=index_id,
            search_options=["visual", "audio"],
            query_text="A man talking",
        )
        async for item in search_pager:
            print(f"  Video ID: {item.video_id}")
            print(
                f"  score={item.score} start={item.start} end={item.end} confidence={item.confidence}"
            )


async def generate_text():
    video_id = "<YOUR_VIDEO_ID>"
    async with AsyncTwelveLabs(api_key=API_KEY) as client:
        res = client.analyze_stream(
            video_id=video_id,
            prompt="What happened?",
        )
        async for chunk in res:
            if chunk.event_type == "text_generation":
                print(chunk.text)


async def main():
    await list_indexes()
    await search()
    await generate_text()


if __name__ == "__main__":
    asyncio.run(main())
