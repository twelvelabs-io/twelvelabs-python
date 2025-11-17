"""
Example: Using the MultipartUploadClientWrapper for easy multipart uploads

This example demonstrates how to use the high-level upload functionality
provided by the MultipartUploadClientWrapper, which abstracts away the complexity
of multipart uploads with robust error handling, retry logic, and progress tracking.

Features demonstrated:
- Simple synchronous uploads
- Asynchronous uploads with concurrency
- Progress tracking with callbacks
- Error handling and retry mechanisms
- Batch uploads and monitoring
- Timeout handling
"""

import asyncio
import logging
import os
import typing
import urllib.request
from pathlib import Path
from twelvelabs import TwelveLabs, AsyncTwelveLabs
from twelvelabs.wrapper.multipart_upload_client_wrapper import UploadError, UploadProgress, UploadResult

API_KEY = os.getenv("API_KEY")
assert (
    API_KEY
), "Your API key should be stored in an environment variable named API_KEY."

# Configure logging to see detailed progress
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def sync_upload_example():
    """Example of synchronous file upload with progress tracking and error handling."""
    print("=== Synchronous Upload Example ===")
    
    # Initialize client
    client = TwelveLabs(
        api_key=API_KEY,
    )
    
    # Progress callback function with enhanced reporting
    def progress_callback(progress: UploadProgress):
        bar_length = 30
        filled_length = int(bar_length * progress.percentage / 100)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        print(f"\r[{bar}] {progress.percentage:.1f}% "
              f"({progress.completed_chunks}/{progress.total_chunks} chunks) "
              f"Status: {progress.status}", end='', flush=True)
        if progress.percentage == 100:
            print()  # New line when complete
    
    try:
        # Upload with custom parameters and progress tracking
        file_path = "downloads/example_video.mp4"  # Downloaded video file
        print(f"\nStarting upload of {file_path}...")
        
        result = client.multipart_upload.upload_file(
            file_path=file_path,
            filename="my-uploaded-video.mp4",
            file_type="video",
            batch_size=5,  # Process chunks in smaller batches
            max_workers=3,  # Use fewer concurrent workers for stability
            max_retries=3,  # Retry failed chunks up to 3 times
            retry_delay=1.0,  # Wait 1 second between retries (exponential backoff)
            progress_callback=progress_callback
        )
        print(f"✅ Upload completed! Asset ID: {result.asset_id}")
        if result.asset_url:
            print(f"📁 Asset URL: {result.asset_url}")
        
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
    except UploadError as e:
        print(f"❌ Upload failed: {e.message}")
        if e.chunk_index:
            print(f"   Failed at chunk: {e.chunk_index}")
        if e.original_error:
            print(f"   Original error: {e.original_error}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


async def async_upload_example():
    """Example of asynchronous file upload with progress tracking and error handling."""
    print("\n=== Asynchronous Upload Example ===")
    
    # Initialize async client
    client = AsyncTwelveLabs(
        api_key=API_KEY,
    )
    
    # Async progress callback function with enhanced reporting
    async def progress_callback(progress: UploadProgress):
        bar_length = 30
        filled_length = int(bar_length * progress.percentage / 100)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        print(f"\r[{bar}] {progress.percentage:.1f}% "
              f"({progress.completed_chunks}/{progress.total_chunks} chunks) "
              f"Status: {progress.status}", end='', flush=True)
        if progress.percentage == 100:
            print()  # New line when complete
    
    try:
        # Upload with custom parameters and progress tracking
        file_path = "downloads/example_video.mp4"  # Downloaded video file
        print(f"Starting async upload of {file_path}...")
        
        result = await client.multipart_upload.upload_file(
            file_path=file_path,
            filename="my-async-video.mp4",
            file_type="video",
            batch_size=8,  # Process chunks in batches of 8
            max_workers=4,  # Use 4 concurrent upload workers
            max_retries=5,  # More retries for async uploads
            retry_delay=0.5,  # Shorter delay for async (exponential backoff)
            progress_callback=progress_callback
        )
        print(f"✅ Async upload completed! Asset ID: {result.asset_id}")
        if result.asset_url:
            print(f"📁 Asset URL: {result.asset_url}")
        
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
    except UploadError as e:
        print(f"❌ Async upload failed: {e.message}")
        if e.chunk_index:
            print(f"   Failed at chunk: {e.chunk_index}")
        if e.original_error:
            print(f"   Original error: {e.original_error}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


def upload_with_wait_example():
    """Example of starting an upload and waiting for completion with timeout."""
    print("\n=== Upload with Wait Example ===")
    
    client = TwelveLabs(
        api_key=API_KEY,
    )
    
    def status_callback(status):
        print(f"Status: {status.status} - "
              f"{status.completed_chunks}/{status.total_chunks} chunks")
    
    try:
        # Start upload
        print("Starting upload...")
        result = client.multipart_upload.upload_file("downloads/example_video.mp4")
        print(f"✅ Upload completed! Asset ID: {result.asset_id}")
        
        # Example of waiting for upload completion (if you had an upload_id from a background process)
        # This is useful when you want to monitor an upload that was started elsewhere
        """
        upload_id = "some_upload_id_from_background_process"
        print(f"Waiting for upload {upload_id} to complete...")
        
        completed_upload = client.multipart_upload.wait_for_upload_completion(
            upload_id=upload_id,
            sleep_interval=5.0,
            max_wait_time=3600.0,  # 1 hour timeout
            callback=status_callback
        )
        print(f"✅ Upload monitoring completed! Status: {completed_upload.status}")
        """
        
        print("💡 Tip: Use wait_for_upload_completion() to monitor uploads started in background processes")
        
    except UploadError as e:
        print(f"❌ Upload failed: {e.message}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


async def advanced_async_example():
    """Advanced async example with multiple concurrent uploads."""
    print("\n=== Advanced Async Example - Multiple Uploads ===")
    
    client = AsyncTwelveLabs(
        api_key=API_KEY,
    )
    
    # List of files to upload (downloaded video files)
    files_to_upload = [
        "downloads/video1.mp4",
        "downloads/video2.mp4", 
        "downloads/video3.mp4"
    ]
    
    async def upload_single_file(file_path: str, index: int) -> typing.Optional[UploadResult]:
        """Upload a single file with progress tracking."""
        async def progress_callback(progress: UploadProgress):
            print(f"File {index + 1}: {progress.percentage:.1f}% "
                  f"({progress.completed_chunks}/{progress.total_chunks} chunks)")
        
        try:
            result = await client.multipart_upload.upload_file(
                file_path=file_path,
                filename=f"batch-upload-{index + 1}.mp4",
                progress_callback=progress_callback,
                max_retries=3
            )
            print(f"✅ File {index + 1} uploaded! Asset ID: {result.asset_id}")
            return result
        except Exception as e:
            print(f"❌ File {index + 1} failed: {e}")
            return None
    
    try:
        # Upload all files concurrently
        print(f"Starting concurrent upload of {len(files_to_upload)} files...")
        tasks = [
            upload_single_file(file_path, i) 
            for i, file_path in enumerate(files_to_upload)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Count successful uploads
        successful_uploads = [r for r in results if r is not None and not isinstance(r, Exception)]
        print(f"✅ Completed {len(successful_uploads)}/{len(files_to_upload)} uploads successfully")
        
    except Exception as e:
        print(f"❌ Batch upload failed: {e}")


def download_sample_videos():
    """Download video files from Google's sample video URLs to the downloads directory."""
    video_urls = [
        {
            "url": "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
            "filename": "example_video.mp4",
            "title": "For Bigger Blazes"
        },
        {
            "url": "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4", 
            "filename": "video1.mp4",
            "title": "For Bigger Escape"
        },
        {
            "url": "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
            "filename": "video2.mp4", 
            "title": "For Bigger Fun"
        }
    ]
    
    # Create downloads directory if it doesn't exist
    downloads_dir = Path("downloads")
    downloads_dir.mkdir(exist_ok=True)
    
    for video_info in video_urls:
        video_path = downloads_dir / video_info["filename"]
        
        if video_path.exists():
            print(f"📁 Video already exists: {video_path}")
            continue
            
        print(f"📥 Downloading {video_info['title']} ({video_info['filename']})...")
        
        try:
            # Download with progress indication
            def progress_hook(block_num, block_size, total_size):
                if total_size > 0:
                    percent = min(100, (block_num * block_size * 100) // total_size)
                    bar_length = 30
                    filled_length = int(bar_length * percent / 100)
                    bar = '█' * filled_length + '-' * (bar_length - filled_length)
                    print(f"\r[{bar}] {percent}%", end='', flush=True)
            
            urllib.request.urlretrieve(
                video_info["url"], 
                video_path,
                reporthook=progress_hook
            )
            print(f"\n✅ Downloaded: {video_path}")
            
        except Exception as e:
            print(f"\n❌ Failed to download {video_info['filename']}: {e}")
            # Create a small dummy file as fallback
            with open(video_path, 'wb') as f:
                f.write(b'0' * (1024 * 1024))  # 1MB dummy file
            print(f"📝 Created fallback dummy file: {video_path}")
    
    # Also create video3.mp4 as a copy of one of the downloaded files for batch upload example
    video3_path = downloads_dir / "video3.mp4"
    if not video3_path.exists():
        source_video = downloads_dir / "video2.mp4"
        if source_video.exists():
            import shutil
            shutil.copy2(source_video, video3_path)
            print(f"📋 Created copy for batch upload: {video3_path}")
    
    return downloads_dir


def main():
    """Main function to run all examples."""
    print("🚀 MultipartUploadClientWrapper Examples")
    print("=" * 60)
    
    # Check API key
    api_key = API_KEY
    if api_key == "YOUR_API_KEY":
        print("⚠️  Using placeholder API key. Set TWELVE_LABS_API_KEY environment variable for real uploads.")
    
    # Download sample videos if they don't exist
    download_sample_videos()
    
    # Run examples
    try:
        # Run synchronous example
        sync_upload_example()
        
        # Run asynchronous examples
        print("\n" + "=" * 60)
        asyncio.run(async_upload_example())
        
        # Run upload with wait example
        print("\n" + "=" * 60)
        upload_with_wait_example()
        
        # Run advanced async example (commented out by default)
        # print("\n" + "=" * 60)
        # asyncio.run(advanced_async_example())
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Examples interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Examples failed with error: {e}")
    
    print("\n🎉 All examples completed!")
    print("\n📝 Note: Replace 'YOUR_API_KEY' with your actual TwelveLabs API key to run these examples.")
    print("📝 Note: Replace file paths with your actual video files for real uploads.")


if __name__ == "__main__":
    main()