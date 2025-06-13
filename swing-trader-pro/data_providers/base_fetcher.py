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
