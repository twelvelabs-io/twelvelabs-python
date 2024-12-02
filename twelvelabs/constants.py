import httpx

BASE_URL = "https://api.twelvelabs.io"
API_KEY_HEADER = "x-api-key"
LATEST_API_VERSION = "v1.3"

# default timeout is 10 minutes
DEFAULT_TIMEOUT = httpx.Timeout(timeout=10 * 60.0, connect=5.0)
DEFAULT_MAX_RETRIES = 2
DEFAULT_LIMITS = httpx.Limits(max_connections=100, max_keepalive_connections=20)
