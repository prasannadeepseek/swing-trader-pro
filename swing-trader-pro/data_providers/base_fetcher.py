from typing import Optional, Dict, Any, Union
from tenacity import retry, stop_after_attempt, wait_exponential
import requests_cache
import requests
import logging
from datetime import datetime, timedelta

# Configure logging
logger = logging.getLogger(__name__)

# Install cache for all requests
requests_cache.install_cache(
    'data_cache',
    expire_after=3600,  # 1 hour cache
    allowable_methods=['GET', 'POST']
)


class BaseFetcher:
    """Base class with common data fetching utilities"""

    @retry(stop=stop_after_attempt(3),
           wait=wait_exponential(multiplier=1, min=4, max=10))
    def _fetch_url(self, url, headers=None):
        try:
            response = requests.get(
                url,
                headers=headers or {},
                timeout=10
            )
            response.raise_for_status()
            self._validate_freshness(response)
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {url}: {str(e)}")
            raise

    @staticmethod
    def _validate_freshness(response):
        """Check if cached data is fresh enough"""
        if getattr(response, 'from_cache', False):
            cache_age = datetime.now() - response.created_at
            if cache_age > timedelta(hours=4):
                logger.warning(f"Using stale cached data (age: {cache_age})")
                # Consider forcing refresh here if needed
        return True

    def _load_fallback_data(self, cache_key):
        """Implement your fallback data loading logic"""
        # Example: Read from a local backup file
        return None

# method 2 final version


# Configure logging if not already configured elsewhere
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurable cache and freshness
CACHE_EXPIRE_SECONDS = 3600  # 1 hour
FRESHNESS_THRESHOLD = timedelta(hours=1)  # Should match cache expiry

# Install cache for all requests
requests_cache.install_cache(
    'data_cache',
    expire_after=CACHE_EXPIRE_SECONDS,
    allowable_methods=['GET', 'POST']
)


class BaseFetcher:
    """Base class with common data fetching utilities and fallback support."""

    def __init__(self, timeout: int = 10, max_retries: int = 3):
        self.timeout = timeout
        self.max_retries = max_retries

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _fetch_url(self, url: str, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """
        Fetch a URL with GET, retrying on failure. Falls back to local cache if all retries fail.
        """
        try:
            response = requests.get(
                url, headers=headers or {}, timeout=self.timeout)
            response.raise_for_status()
            self._validate_freshness(response)
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {url}: {str(e)}")
            # Attempt fallback
            cache_key = self._generate_cache_key(url, headers)
            fallback = self._load_fallback_data(cache_key)
            if fallback is not None:
                logger.warning(f"Loaded fallback data for {url}")
                return fallback
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _fetch(self, method: str, url: str, headers: Optional[Dict[str, str]] = None,
               data: Optional[Union[Dict, str]] = None, json: Optional[Any] = None) -> requests.Response:
        """
        Generic fetch method supporting GET and POST.
        """
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers or {},
                data=data,
                json=json,
                timeout=self.timeout
            )
            response.raise_for_status()
            self._validate_freshness(response)
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"{method} request failed for {url}: {str(e)}")
            cache_key = self._generate_cache_key(url, headers, data, json)
            fallback = self._load_fallback_data(cache_key)
            if fallback is not None:
                logger.warning(f"Loaded fallback data for {url}")
                return fallback
            raise

    @staticmethod
    def _validate_freshness(response: requests.Response) -> bool:
        """
        Check if cached data is fresh enough.
        """
        if getattr(response, 'from_cache', False):
            created_at = getattr(response, 'created_at', None)
            if created_at:
                cache_age = datetime.now() - created_at
                if cache_age > FRESHNESS_THRESHOLD:
                    logger.warning(
                        f"Using stale cached data (age: {cache_age})")
            else:
                logger.warning(
                    "Cached response missing 'created_at' attribute.")
        return True

    def _load_fallback_data(self, cache_key: str) -> Optional[requests.Response]:
        """
        Load fallback data from a local file if available.
        """
        import os
        import pickle

        fallback_path = f"fallback_cache/{cache_key}.pkl"
        if os.path.exists(fallback_path):
            try:
                with open(fallback_path, "rb") as f:
                    response = pickle.load(f)
                logger.info(f"Loaded fallback data from {fallback_path}")
                return response
            except Exception as e:
                logger.error(f"Failed to load fallback data: {e}")
        return None

    def _save_fallback_data(self, cache_key: str, response: requests.Response) -> None:
        """
        Save response data to a local file for fallback use.
        """
        import os
        import pickle

        os.makedirs("fallback_cache", exist_ok=True)
        fallback_path = f"fallback_cache/{cache_key}.pkl"
        try:
            with open(fallback_path, "wb") as f:
                pickle.dump(response, f)
            logger.info(f"Saved fallback data to {fallback_path}")
        except Exception as e:
            logger.error(f"Failed to save fallback data: {e}")

    @staticmethod
    def _generate_cache_key(url: str, headers: Optional[Dict[str, str]] = None,
                            data: Optional[Any] = None, json: Optional[Any] = None) -> str:
        """
        Generate a simple cache key based on request parameters.
        """
        import hashlib
        key_str = f"{url}|{headers}|{data}|{json}"
        return hashlib.md5(key_str.encode('utf-8')).hexdigest()
