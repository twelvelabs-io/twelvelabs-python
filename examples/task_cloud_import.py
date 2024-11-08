import os

import _context
from twelvelabs import TwelveLabs


API_KEY = os.getenv("API_KEY")
assert (
    API_KEY
), "Your API key should be stored in an environment variable named API_KEY."

with TwelveLabs(API_KEY) as client:
    index_id = "<YOUR_INDEX_ID>"
    integration_id = "<YOUR_INTEGRATION_ID>"

    res = client.task.transfers.import_videos(
        integration_id,
        index_id,
    )
    for video in res.videos:
        print(f"video: {video.video_id} {video.filename}")
    if res.failed_files:
        for failed_file in res.failed_files:
            print(f"failed_file: {failed_file.filename} {failed_file.error_message}")

    status = client.task.transfers.import_status(integration_id, index_id)
    for ready in status.ready:
        print(f"ready: {ready.video_id} {ready.filename} {ready.created_at}")
    for failed in status.failed:
        print(f"failed: {failed.filename} {failed.error_message}")

    logs = client.task.transfers.import_logs(integration_id)
    for log in logs:
        print(
            f"index_id={log.index_id} index_name={log.index_name} created_at={log.created_at} ended_at={log.ended_at} video_status={log.video_status}"
        )
        if log.failed_files:
            for failed_file in log.failed_files:
                print(
                    f"failed_file: {failed_file.filename} {failed_file.error_message}"
                )
