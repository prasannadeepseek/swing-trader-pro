import logging
from .base_fetcher import BaseFetcher
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


class NSDLFetcher:

    BASE_URL = "https://www.nsdl.co.in/emi/ismr/fii_dii_archive.php"

    @staticmethod
    def get_fii_dii_activity(days=3):
        """Fetch FII/DII net investment data"""
        response = requests.get(NSDLFetcher.BASE_URL)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract latest reports (example parsing - adjust per actual HTML)
        reports = []
        for row in soup.select('table tr')[1:4]:  # Last 3 days
            cols = row.find_all('td')
            reports.append({
                'date': cols[0].text.strip(),
                'fii_net': float(cols[1].text.replace(',', '')),
                'dii_net': float(cols[2].text.replace(',', ''))
            })
        return pd.DataFrame(reports)

    @staticmethod
    def get_sector_flows():
        """Fetch sector-wise FII activity (from monthly reports)"""
        # Implementation would parse sector reports PDF
        # This is a placeholder structure
        return {
            'BANKING': 1200,
            'IT': -450,
            'AUTO': 780
        }

# method 2


logger = logging.getLogger(__name__)


class NSDLFetcher(BaseFetcher):

    BASE_URL = "https://www.nsdl.co.in/emi/ismr/fii_dii_archive.php"

    def get_fii_dii_activity(self, days=3):
        """Fetch with retry and cache"""
        try:
            response = self._fetch_url(self.BASE_URL)
            soup = BeautifulSoup(response.text, 'html.parser')
            reports = self._parse_table(soup)
            return self._validate_output(reports, days)
        except Exception as e:
            logger.error(f"FII/DII fetch failed: {str(e)}")
            return self._load_fallback_data("fii_dii_activity")

    def _parse_table(self, soup):
        """Parse HTML table - implementation specific to NSDL's structure"""
        # Your existing parsing logic
        return []

    def _validate_output(self, data, expected_days):
        """Validate data completeness"""
        if len(data) < expected_days:
            logger.warning(f"Only got {len(data)} days of FII data")
        return pd.DataFrame(data)
