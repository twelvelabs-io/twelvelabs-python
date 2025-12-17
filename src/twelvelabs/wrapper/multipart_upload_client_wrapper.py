import typing
import time
import asyncio
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import httpx
from ..multipart_upload.types.create_asset_upload_request_type import CreateAssetUploadRequestType
from ..core.client_wrapper import SyncClientWrapper, AsyncClientWrapper
from ..multipart_upload.client import MultipartUploadClient, AsyncMultipartUploadClient
from ..types.completed_chunk import CompletedChunk
from ..core.request_options import RequestOptions
from ..core.pydantic_utilities import UniversalBaseModel
import pydantic

OMIT = typing.cast(typing.Any, ...)

# Configure logging
logger = logging.getLogger(__name__)


class UploadProgress(UniversalBaseModel):
    """Progress information for upload operations."""
    
    total_chunks: int = pydantic.Field(..., description="Total number of chunks")
    completed_chunks: int = pydantic.Field(..., description="Number of completed chunks")
    percentage: float = pydantic.Field(..., description="Upload percentage (0-100)")
    status: str = pydantic.Field(..., description="Current upload status")


class UploadResult(UniversalBaseModel):
    """Result of a successful multipart upload."""
    
    asset_id: str = pydantic.Field(..., description="The unique identifier of the uploaded asset")
    asset_url: str = pydantic.Field(..., description="The URL to access the uploaded asset")


class UploadStatus(UniversalBaseModel):
    """Status information for upload operations."""
    
    status: str = pydantic.Field(..., description="Upload status")
    completed_chunks: int = pydantic.Field(..., description="Number of completed chunks")
    total_chunks: int = pydantic.Field(..., description="Total number of chunks")


class UploadError(Exception):
    """Custom exception for upload-related errors."""
    
    def __init__(self, message: str, chunk_index: typing.Optional[int] = None, original_error: typing.Optional[Exception] = None):
        self.message = message
        self.chunk_index = chunk_index
        self.original_error = original_error
        super().__init__(message)


class MultipartUploadClientWrapper(MultipartUploadClient):
    """Wrapper for the MultipartUploadClient that adds high-level upload functionality."""

    def __init__(self, client_wrapper: SyncClientWrapper):
        """Initialize the MultipartUploadClientWrapper."""
        super().__init__(client_wrapper=client_wrapper)

    def upload_file(
        self,
        file_path: typing.Union[str, Path],
        *,
        filename: typing.Optional[str] = None,
        file_type: CreateAssetUploadRequestType = "video",
        batch_size: int = 10,
        max_workers: int = 5,
        progress_callback: typing.Optional[typing.Callable[[UploadProgress], None]] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> UploadResult:
        """
        Upload a file using multipart upload with automatic chunking and progress tracking.

        Parameters
        ----------
        file_path : typing.Union[str, Path]
            Path to the file to upload.

        filename : typing.Optional[str]
            Name to use for the asset (defaults to file basename).

        file_type : CreateAssetUploadRequestType
            Asset type (default: "video").

        batch_size : int
            Number of chunks to report in each batch (default: 10).

        max_workers : int
            Maximum number of concurrent upload workers (default: 5).

        progress_callback : typing.Optional[typing.Callable[[UploadProgress], None]]
            Optional callback function to track upload progress.

        max_retries : int
            Maximum number of retry attempts for failed chunks (default: 3).

        retry_delay : float
            Delay in seconds between retry attempts (default: 1.0).

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        UploadResult
            A dictionary containing:
            - asset_id: The unique identifier of the uploaded asset
            - asset_url: The URL to access the uploaded asset

        Examples
        --------
        from twelvelabs import TwelveLabs

        client = TwelveLabs(
            api_key="YOUR_API_KEY",
        )

        # Simple upload
        result = client.multipart_upload.upload_file("video.mp4")
        print(f"Asset ID: {result.asset_id}")
        print(f"Asset URL: {result.asset_url}")

        # Upload with progress tracking
        def progress_callback(progress):
            print(f"Progress: {progress.percentage:.1f}% ({progress.completed_chunks}/{progress.total_chunks} chunks)")

        result = client.multipart_upload.upload_file(
            "large_video.mp4",
            filename="my-video.mp4",
            progress_callback=progress_callback,
            batch_size=5
        )
        print(f"Upload completed! Asset ID: {result.asset_id}")
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if filename is None:
            filename = file_path.name

        total_size = file_path.stat().st_size
        chunk_files = []

        try:
            logger.info(f"Creating upload session for {filename} ({total_size:,} bytes)")
            # Step 1: Create upload session
            upload_session = self.create(
                filename=filename,
                type=file_type,
                total_size=total_size,
                request_options=request_options
            )
            
            if not upload_session.upload_id or not upload_session.chunk_size:
                raise UploadError("Invalid upload session response: missing upload_id or chunk_size")
                
            upload_id = upload_session.upload_id
            chunk_size = upload_session.chunk_size
            logger.info(f"Upload session created: {upload_id} (chunk size: {chunk_size:,} bytes)")

            # Step 2: Split file into chunks
            chunk_files = self._split_file(file_path, chunk_size)
            total_chunks = len(chunk_files)
            logger.info(f"File split into {total_chunks} chunks")
            
            if total_chunks == 0:
                raise UploadError("No chunks created from file")

            # Step 3: Upload chunks in batches
            current_urls: typing.Dict[int, str] = {}
            if upload_session.upload_urls:
                for url in upload_session.upload_urls:
                    if url.chunk_index is not None and url.url is not None:
                        current_urls[url.chunk_index] = url.url
            completed_chunks_count = 0

            for batch_start in range(0, total_chunks, batch_size):
                batch_end = min(batch_start + batch_size, total_chunks)
                batch_chunk_files = chunk_files[batch_start:batch_end]
                batch_indices = list(range(batch_start + 1, batch_end + 1))  # 1-based indexing

                # Ensure we have URLs for all chunks in this batch
                missing_urls = [idx for idx in batch_indices if idx not in current_urls]
                if missing_urls:
                    min_chunk = min(missing_urls)
                    max_chunk = max(missing_urls)
                    
                    logger.debug(f"Fetching URLs for chunks {min_chunk}-{max_chunk} ({len(missing_urls)} missing)")
                    start = min_chunk
                    count = max_chunk - min_chunk + 1
                    
                    additional_urls = self.get_additional_presigned_urls(
                        upload_id, start=start, count=count, request_options=request_options
                    )
                    
                    if additional_urls.upload_urls:
                        for url_info in additional_urls.upload_urls:
                            if url_info.chunk_index is not None and url_info.url is not None and url_info.chunk_index in missing_urls:
                                current_urls[url_info.chunk_index] = url_info.url

                # Upload batch chunks in parallel with retry logic
                batch_completed_chunks = self._upload_chunk_batch_with_retry(
                    batch_chunk_files,
                    batch_indices,
                    current_urls,
                    max_workers,
                    max_retries,
                    retry_delay
                )

                # Report completed batch
                result = self.report_chunk_batch(
                    upload_id,
                    completed_chunks=batch_completed_chunks,
                    request_options=request_options
                )

                completed_chunks_count += len(batch_completed_chunks)

                # Update progress
                if progress_callback:
                    progress = UploadProgress(
                        total_chunks=total_chunks,
                        completed_chunks=completed_chunks_count,
                        percentage=(completed_chunks_count / total_chunks) * 100,
                        status="uploading"
                    )
                    progress_callback(progress)

                # Check if upload is complete
                if result.url:
                    logger.info(f"Upload completed successfully! Asset ID: {upload_session.asset_id}")
                    return UploadResult(
                        asset_id=upload_session.asset_id,
                        asset_url=result.url,
                    )

            # All chunks have been uploaded and reported
            logger.info(f"Upload completed successfully! Asset ID: {upload_session.asset_id}")
            return UploadResult(
                asset_id=upload_session.asset_id,
                asset_url="",  # URL will be available after processing
            )
            
        except UploadError:
            raise
        except Exception as e:
            raise UploadError(f"Upload failed: {str(e)}", original_error=e)
        finally:
            # Cleanup temporary files
            if chunk_files:
                try:
                    self._cleanup_chunks(chunk_files)
                except Exception as e:
                    logger.warning(f"Failed to cleanup chunk files: {e}")

    def _split_file(self, file_path: Path, chunk_size: int) -> typing.List[Path]:
        """Split file into chunks and return list of chunk file paths."""
        chunk_files = []
        chunk_dir = file_path.parent / f"{file_path.stem}_chunks"
        
        try:
            chunk_dir.mkdir(exist_ok=True)

            with open(file_path, 'rb') as f:
                chunk_num = 1
                while True:
                    chunk_data = f.read(chunk_size)
                    if not chunk_data:
                        break

                    chunk_file = chunk_dir / f"chunk_{chunk_num:04d}"
                    with open(chunk_file, 'wb') as chunk_f:
                        chunk_f.write(chunk_data)

                    chunk_files.append(chunk_file)
                    chunk_num += 1
        except Exception as e:
            # Clean up any partial chunks on error
            self._cleanup_chunks(chunk_files)
            raise UploadError(f"Failed to split file into chunks: {e}", original_error=e)

        return chunk_files

    def _upload_chunk_to_s3(self, chunk_file: Path, presigned_url: str) -> str:
        """Upload a single chunk to S3 and return ETag."""
        try:
            with open(chunk_file, 'rb') as f:
                response = httpx.put(
                    presigned_url,
                    content=f,
                    headers={'Content-Type': 'application/octet-stream'},
                    timeout=300.0  # 5 minute timeout for large chunks
                )

            response.raise_for_status()
            etag = response.headers.get('ETag', '').strip('"')
            if not etag:
                raise UploadError("No ETag received from S3 upload")
            return etag
        except httpx.HTTPError as e:
            raise UploadError(f"HTTP error during chunk upload: {e}", original_error=e)
        except Exception as e:
            raise UploadError(f"Failed to upload chunk: {e}", original_error=e)

    def _upload_chunk_batch_with_retry(
        self,
        chunk_files: typing.List[Path],
        chunk_indices: typing.List[int],
        presigned_urls: typing.Dict[int, str],
        max_workers: int,
        max_retries: int,
        retry_delay: float
    ) -> typing.List[CompletedChunk]:
        """Upload a batch of chunks in parallel with retry logic."""
        completed_chunks = []
        max_workers = min(len(chunk_files), max_workers)

        def upload_chunk_with_retry(chunk_file: Path, chunk_index: int) -> CompletedChunk:
            presigned_url = presigned_urls[chunk_index]
            last_error = None
            
            for attempt in range(max_retries + 1):
                try:
                    etag = self._upload_chunk_to_s3(chunk_file, presigned_url)
                    chunk_size_bytes = chunk_file.stat().st_size
                    return CompletedChunk(
                        chunk_index=chunk_index,
                        proof=etag,
                        proof_type="etag",
                        chunk_size=chunk_size_bytes
                    )
                except Exception as e:
                    last_error = e
                    if attempt < max_retries:
                        logger.warning(f"Chunk {chunk_index} upload failed (attempt {attempt + 1}/{max_retries + 1}): {e}")
                        time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                    else:
                        logger.error(f"Chunk {chunk_index} upload failed after {max_retries + 1} attempts")
            
            raise UploadError(f"Chunk {chunk_index} upload failed after {max_retries + 1} attempts", 
                            chunk_index=chunk_index, original_error=last_error)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_chunk = {}
            for i, chunk_file in enumerate(chunk_files):
                chunk_index = chunk_indices[i]
                future = executor.submit(upload_chunk_with_retry, chunk_file, chunk_index)
                future_to_chunk[future] = (chunk_index, chunk_file)

            for future in as_completed(future_to_chunk):
                chunk_index, chunk_file = future_to_chunk[future]
                try:
                    completed_chunk = future.result()
                    completed_chunks.append(completed_chunk)
                except Exception as e:
                    raise UploadError(f"Chunk {chunk_index} upload failed: {e}", 
                                    chunk_index=chunk_index, original_error=e)

        return completed_chunks

    def _cleanup_chunks(self, chunk_files: typing.List[Path]):
        """Clean up temporary chunk files."""
        if not chunk_files:
            return
            
        chunk_dir = None
        for chunk_file in chunk_files:
            try:
                if chunk_file.exists():
                    chunk_file.unlink()
                if chunk_dir is None:
                    chunk_dir = chunk_file.parent
            except OSError as e:
                logger.warning(f"Failed to delete chunk file {chunk_file}: {e}")

        # Remove chunk directory if empty
        if chunk_dir and chunk_dir.exists():
            try:
                chunk_dir.rmdir()
            except OSError:
                # Directory not empty or other error, ignore
                pass

    def wait_for_upload_completion(
        self,
        upload_id: str,
        *,
        sleep_interval: float = 5.0,
        max_wait_time: typing.Optional[float] = None,
        callback: typing.Optional[typing.Callable[[UploadStatus], None]] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> UploadStatus:
        """
        Wait for a multipart upload to complete by periodically checking its status.

        Parameters
        ----------
        upload_id : str
            The unique identifier of the upload session.

        sleep_interval : float, optional
            The time in seconds to wait between status checks, by default 5.0

        max_wait_time : typing.Optional[float], optional
            Maximum time to wait in seconds before timing out, by default None (no timeout)

        callback : typing.Optional[typing.Callable[[UploadStatus], None]], optional
            A function to call after each status check with the upload status, by default None

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        UploadStatus
            The final upload status with completion information

        Raises
        ------
        UploadError
            If the upload fails or times out

        Examples
        --------
        from twelvelabs import TwelveLabs

        client = TwelveLabs(
            api_key="YOUR_API_KEY",
        )

        # Start upload in background
        upload_id = "507f1f77bcf86cd799439011"

        # Wait for completion with timeout
        completed_upload = client.multipart_upload.wait_for_upload_completion(
            upload_id=upload_id,
            sleep_interval=10.0,
            max_wait_time=3600.0,  # 1 hour timeout
        )
        """
        if sleep_interval <= 0:
            raise ValueError("sleep_interval must be greater than 0")

        start_time = time.time()
        
        while True:
            try:
                # Get chunk status
                chunk_status = self.get_status(upload_id, request_options=request_options)
                completed_chunks = 0
                total_chunks = 0
                failed_chunks = []

                # Count completed and failed chunks
                for chunk in chunk_status:
                    total_chunks += 1
                    if chunk.status is not None and chunk.status == "completed":
                        completed_chunks += 1
                    elif chunk.status is not None and chunk.status == "failed":
                        failed_chunks.append(chunk.index)

                # Check for failed chunks
                if failed_chunks:
                    raise UploadError(f"Chunks {failed_chunks} failed to upload")

                # Create status object
                status = UploadStatus(
                    status="completed" if completed_chunks == total_chunks else "in_progress",
                    completed_chunks=completed_chunks,
                    total_chunks=total_chunks
                )

                # Call callback if provided
                if callback:
                    callback(status)

                # Check if complete
                if completed_chunks == total_chunks:
                    return status

                # Check timeout
                if max_wait_time and (time.time() - start_time) > max_wait_time:
                    raise UploadError(f"Upload timed out after {max_wait_time} seconds")

                time.sleep(sleep_interval)

            except UploadError:
                raise
            except Exception as e:
                logger.warning(f"Error checking upload status: {e}")
                time.sleep(sleep_interval)


class AsyncMultipartUploadClientWrapper(AsyncMultipartUploadClient):
    """Async wrapper for the MultipartUploadClient that adds high-level upload functionality."""

    def __init__(self, client_wrapper: AsyncClientWrapper):
        """Initialize the AsyncMultipartUploadClientWrapper."""
        super().__init__(client_wrapper=client_wrapper)

    async def upload_file(
        self,
        file_path: typing.Union[str, Path],
        *,
        filename: typing.Optional[str] = None,
        file_type: CreateAssetUploadRequestType = "video",
        batch_size: int = 10,
        max_workers: int = 5,
        progress_callback: typing.Optional[
            typing.Callable[[UploadProgress], typing.Awaitable[None]]
        ] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> UploadResult:
        """
        Upload a file using multipart upload with automatic chunking and progress tracking.

        Parameters
        ----------
        file_path : typing.Union[str, Path]
            Path to the file to upload.

        filename : typing.Optional[str]
            Name to use for the asset (defaults to file basename).

        file_type : CreateAssetUploadRequestType
            Asset type (default: "video").

        batch_size : int
            Number of chunks to report in each batch (default: 10).

        max_workers : int
            Maximum number of concurrent upload workers (default: 5).

        progress_callback : typing.Optional[typing.Callable[[UploadProgress], typing.Awaitable[None]]]
            Optional async callback function to track upload progress.

        max_retries : int
            Maximum number of retry attempts for failed chunks (default: 3).

        retry_delay : float
            Delay in seconds between retry attempts (default: 1.0).

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        UploadResult
            A dictionary containing:
            - asset_id: The unique identifier of the uploaded asset
            - asset_url: The URL to access the uploaded asset

        Examples
        --------
        import asyncio
        from twelvelabs import AsyncTwelveLabs

        client = AsyncTwelveLabs(
            api_key="YOUR_API_KEY",
        )

        async def main() -> None:
            # Simple upload
            result = await client.multipart_upload.upload_file("video.mp4")
            print(f"Asset ID: {result.asset_id}")
            print(f"Asset URL: {result.asset_url}")

            # Upload with progress tracking
            async def progress_callback(progress):
                print(f"Progress: {progress.percentage:.1f}% ({progress.completed_chunks}/{progress.total_chunks} chunks)")

            result = await client.multipart_upload.upload_file(
                "large_video.mp4",
                filename="my-video.mp4",
                progress_callback=progress_callback,
                batch_size=5
            )
            print(f"Upload completed! Asset ID: {result.asset_id}")

        asyncio.run(main())
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if filename is None:
            filename = file_path.name

        total_size = file_path.stat().st_size
        chunk_files = []

        try:
            logger.info(f"Creating upload session for {filename} ({total_size:,} bytes)")
            # Step 1: Create upload session
            upload_session = await self.create(
                filename=filename,
                type=file_type,
                total_size=total_size,
                request_options=request_options
            )
            
            if not upload_session.upload_id or not upload_session.chunk_size:
                raise UploadError("Invalid upload session response: missing upload_id or chunk_size")
                
            upload_id = upload_session.upload_id
            chunk_size = upload_session.chunk_size
            logger.info(f"Upload session created: {upload_id} (chunk size: {chunk_size:,} bytes)")

            # Step 2: Split file into chunks
            chunk_files = await self._split_file_async(file_path, chunk_size)
            total_chunks = len(chunk_files)
            logger.info(f"File split into {total_chunks} chunks")
            
            if total_chunks == 0:
                raise UploadError("No chunks created from file")

            # Step 3: Upload chunks in batches
            current_urls: typing.Dict[int, str] = {}
            if upload_session.upload_urls:
                for url in upload_session.upload_urls:
                    if url.chunk_index is not None and url.url is not None:
                        current_urls[url.chunk_index] = url.url
            completed_chunks_count = 0

            for batch_start in range(0, total_chunks, batch_size):
                batch_end = min(batch_start + batch_size, total_chunks)
                batch_chunk_files = chunk_files[batch_start:batch_end]
                batch_indices = list(range(batch_start + 1, batch_end + 1))  # 1-based indexing

                # Ensure we have URLs for all chunks in this batch
                missing_urls = [idx for idx in batch_indices if idx not in current_urls]
                if missing_urls:
                    min_chunk = min(missing_urls)
                    max_chunk = max(missing_urls)
                    
                    logger.debug(f"Fetching URLs for chunks {min_chunk}-{max_chunk} ({len(missing_urls)} missing)")
                    start = min_chunk
                    count = max_chunk - min_chunk + 1
                    
                    additional_urls = await self.get_additional_presigned_urls(
                        upload_id, start=start, count=count, request_options=request_options
                    )
                    
                    if additional_urls.upload_urls:
                        for url_info in additional_urls.upload_urls:
                            if url_info.chunk_index is not None and url_info.url is not None and url_info.chunk_index in missing_urls:
                                current_urls[url_info.chunk_index] = url_info.url

                # Upload batch chunks in parallel with retry logic
                batch_completed_chunks = await self._upload_chunk_batch_async_with_retry(
                    batch_chunk_files,
                    batch_indices,
                    current_urls,
                    max_workers,
                    max_retries,
                    retry_delay
                )

                # Report completed batch
                result = await self.report_chunk_batch(
                    upload_id,
                    completed_chunks=batch_completed_chunks,
                    request_options=request_options
                )

                completed_chunks_count += len(batch_completed_chunks)

                # Update progress
                if progress_callback:
                    progress = UploadProgress(
                        total_chunks=total_chunks,
                        completed_chunks=completed_chunks_count,
                        percentage=(completed_chunks_count / total_chunks) * 100,
                        status="uploading"
                    )
                    await progress_callback(progress)

                # Check if upload is complete
                if result.url:
                    logger.info(f"Upload completed successfully! Asset ID: {upload_session.asset_id}")
                    return UploadResult(
                        asset_id=upload_session.asset_id,
                        asset_url=result.url,
                    )

            # All chunks have been uploaded and reported
            logger.info(f"Upload completed successfully! Asset ID: {upload_session.asset_id}")
            return UploadResult(
                asset_id=upload_session.asset_id,
                asset_url="",  # URL will be available after processing
            )
            
        except UploadError:
            raise
        except Exception as e:
            raise UploadError(f"Upload failed: {str(e)}", original_error=e)
        finally:
            # Cleanup temporary files
            if chunk_files:
                try:
                    await self._cleanup_chunks_async(chunk_files)
                except Exception as e:
                    logger.warning(f"Failed to cleanup chunk files: {e}")

    async def _split_file_async(self, file_path: Path, chunk_size: int) -> typing.List[Path]:
        """Split file into chunks asynchronously and return list of chunk file paths."""
        chunk_files = []
        chunk_dir = file_path.parent / f"{file_path.stem}_chunks"
        
        try:
            chunk_dir.mkdir(exist_ok=True)

            with open(file_path, 'rb') as f:
                chunk_num = 1
                while True:
                    chunk_data = f.read(chunk_size)
                    if not chunk_data:
                        break

                    chunk_file = chunk_dir / f"chunk_{chunk_num:04d}"
                    with open(chunk_file, 'wb') as chunk_f:
                        chunk_f.write(chunk_data)

                    chunk_files.append(chunk_file)
                    chunk_num += 1
        except Exception as e:
            # Clean up any partial chunks on error
            await self._cleanup_chunks_async(chunk_files)
            raise UploadError(f"Failed to split file into chunks: {e}", original_error=e)

        return chunk_files

    async def _upload_chunk_to_s3_async(self, chunk_file: Path, presigned_url: str) -> str:
        """Upload a single chunk to S3 asynchronously and return ETag."""
        try:
            # Read file content first, then upload asynchronously
            with open(chunk_file, 'rb') as f:
                file_content = f.read()
            
            async with httpx.AsyncClient(timeout=300.0) as client:  # 5 minute timeout
                response = await client.put(
                    presigned_url,
                    content=file_content,
                    headers={'Content-Type': 'application/octet-stream'}
                )

            response.raise_for_status()
            etag = response.headers.get('ETag', '').strip('"')
            if not etag:
                raise UploadError("No ETag received from S3 upload")
            return etag
        except httpx.HTTPError as e:
            raise UploadError(f"HTTP error during chunk upload: {e}", original_error=e)
        except Exception as e:
            raise UploadError(f"Failed to upload chunk: {e}", original_error=e)

    async def _upload_chunk_batch_async_with_retry(
        self,
        chunk_files: typing.List[Path],
        chunk_indices: typing.List[int],
        presigned_urls: typing.Dict[int, str],
        max_workers: int,
        max_retries: int,
        retry_delay: float
    ) -> typing.List[CompletedChunk]:
        """Upload a batch of chunks in parallel asynchronously with retry logic."""
        completed_chunks = []
        max_workers = min(len(chunk_files), max_workers)

        # Create semaphore to limit concurrent uploads
        semaphore = asyncio.Semaphore(max_workers)

        async def upload_single_chunk_with_retry(chunk_file: Path, chunk_index: int) -> CompletedChunk:
            async with semaphore:
                presigned_url = presigned_urls[chunk_index]
                last_error = None
                
                for attempt in range(max_retries + 1):
                    try:
                        etag = await self._upload_chunk_to_s3_async(chunk_file, presigned_url)
                        chunk_size_bytes = chunk_file.stat().st_size
                        return CompletedChunk(
                            chunk_index=chunk_index,
                            proof=etag,
                            proof_type="etag",
                            chunk_size=chunk_size_bytes
                        )
                    except Exception as e:
                        last_error = e
                        if attempt < max_retries:
                            logger.warning(f"Chunk {chunk_index} upload failed (attempt {attempt + 1}/{max_retries + 1}): {e}")
                            await asyncio.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                        else:
                            logger.error(f"Chunk {chunk_index} upload failed after {max_retries + 1} attempts")
                
                raise UploadError(f"Chunk {chunk_index} upload failed after {max_retries + 1} attempts", 
                                chunk_index=chunk_index, original_error=last_error)

        # Create tasks for all chunks
        tasks = [
            upload_single_chunk_with_retry(chunk_file, chunk_indices[i])
            for i, chunk_file in enumerate(chunk_files)
        ]

        # Wait for all uploads to complete
        try:
            completed_chunks = await asyncio.gather(*tasks)
        except Exception as e:
            raise UploadError(f"Batch upload failed: {e}", original_error=e)

        return completed_chunks

    async def _cleanup_chunks_async(self, chunk_files: typing.List[Path]):
        """Clean up temporary chunk files asynchronously."""
        if not chunk_files:
            return
            
        chunk_dir = None
        for chunk_file in chunk_files:
            try:
                if chunk_file.exists():
                    chunk_file.unlink()
                if chunk_dir is None:
                    chunk_dir = chunk_file.parent
            except OSError as e:
                logger.warning(f"Failed to delete chunk file {chunk_file}: {e}")

        # Remove chunk directory if empty
        if chunk_dir and chunk_dir.exists():
            try:
                chunk_dir.rmdir()
            except OSError:
                # Directory not empty or other error, ignore
                pass

    async def wait_for_upload_completion(
        self,
        upload_id: str,
        *,
        sleep_interval: float = 5.0,
        max_wait_time: typing.Optional[float] = None,
        callback: typing.Optional[
            typing.Callable[[UploadStatus], typing.Awaitable[None]]
        ] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> UploadStatus:
        """
        Wait for a multipart upload to complete by periodically checking its status.

        Parameters
        ----------
        upload_id : str
            The unique identifier of the upload session.

        sleep_interval : float, optional
            The time in seconds to wait between status checks, by default 5.0

        max_wait_time : typing.Optional[float], optional
            Maximum time to wait in seconds before timing out, by default None (no timeout)

        callback : typing.Optional[typing.Callable[[UploadStatus], typing.Awaitable[None]]], optional
            An async function to call after each status check with the upload status, by default None

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        UploadStatus
            The final upload status with completion information

        Raises
        ------
        UploadError
            If the upload fails or times out

        Examples
        --------
        import asyncio
        from twelvelabs import AsyncTwelveLabs

        client = AsyncTwelveLabs(
            api_key="YOUR_API_KEY",
        )

        async def main() -> None:
            # Start upload in background
            upload_id = "507f1f77bcf86cd799439011"

            # Wait for completion with timeout
            completed_upload = await client.multipart_upload.wait_for_upload_completion(
                upload_id=upload_id,
                sleep_interval=10.0,
                max_wait_time=3600.0,  # 1 hour timeout
            )

        asyncio.run(main())
        """
        if sleep_interval <= 0:
            raise ValueError("sleep_interval must be greater than 0")

        start_time = time.time()
        
        while True:
            try:
                # Get chunk status
                chunk_status = await self.get_status(upload_id, request_options=request_options)
                completed_chunks = 0
                total_chunks = 0
                failed_chunks = []

                # Count completed and failed chunks - fix async iteration
                async for chunk in chunk_status:
                    total_chunks += 1
                    if chunk.status is not None and chunk.status == "completed":
                        completed_chunks += 1
                    elif chunk.status is not None and chunk.status == "failed":
                        failed_chunks.append(chunk.index)

                # Check for failed chunks
                if failed_chunks:
                    raise UploadError(f"Chunks {failed_chunks} failed to upload")

                # Create status object
                status = UploadStatus(
                    status="completed" if completed_chunks == total_chunks else "in_progress",
                    completed_chunks=completed_chunks,
                    total_chunks=total_chunks
                )

                # Call callback if provided
                if callback:
                    await callback(status)

                # Check if complete
                if completed_chunks == total_chunks:
                    return status

                # Check timeout
                if max_wait_time and (time.time() - start_time) > max_wait_time:
                    raise UploadError(f"Upload timed out after {max_wait_time} seconds")

                await asyncio.sleep(sleep_interval)

            except UploadError:
                raise
            except Exception as e:
                logger.warning(f"Error checking upload status: {e}")
                await asyncio.sleep(sleep_interval)