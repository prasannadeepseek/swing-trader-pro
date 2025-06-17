from typing import List, Dict, Any
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

# method 3 final versin


logger = logging.getLogger(__name__)


class NSDLFetcher(BaseFetcher):
    """
    Fetches FII/DII net investment data and sector flows from NSDL,
    with retry, caching, error handling, and fallback support.
    """

    BASE_URL = "https://www.nsdl.co.in/emi/ismr/fii_dii_archive.php"

    def get_fii_dii_activity(self, days: int = 3) -> pd.DataFrame:
        """
        Fetch FII/DII net investment data for the last `days` days.

        Args:
            days (int): Number of recent days to fetch.

        Returns:
            pd.DataFrame: DataFrame with columns ['date', 'fii_net', 'dii_net']
        """
        try:
            response = self._fetch_url(self.BASE_URL)
            soup = BeautifulSoup(response.text, 'html.parser')
            reports = self._parse_table(soup, days)
            return self._validate_output(reports, days)
        except Exception as e:
            logger.error(f"FII/DII fetch failed: {str(e)}")
            fallback = self._load_fallback_data("fii_dii_activity")
            if fallback is not None:
                try:
                    soup = BeautifulSoup(fallback.text, 'html.parser')
                    reports = self._parse_table(soup, days)
                    return self._validate_output(reports, days)
                except Exception as fallback_e:
                    logger.error(
                        f"Fallback FII/DII parse failed: {fallback_e}")
            return pd.DataFrame([])

    def _parse_table(self, soup: BeautifulSoup, days: int) -> List[Dict[str, Any]]:
        """
        Parse the FII/DII HTML table from NSDL.

        Args:
            soup (BeautifulSoup): Parsed HTML soup.
            days (int): Number of rows to extract.

        Returns:
            List[Dict[str, Any]]: List of dicts with 'date', 'fii_net', 'dii_net'.
        """
        reports = []
        table = soup.find('table')
        if not table:
            logger.error("No table found in NSDL FII/DII page.")
            return reports

        rows = table.find_all('tr')[1:]  # Skip header
        for row in rows[:days]:
            cols = row.find_all('td')
            if len(cols) < 3:
                continue
            try:
                date = cols[0].text.strip()
                fii_net = float(cols[1].text.replace(
                    ',', '').replace('--', '0') or 0)
                dii_net = float(cols[2].text.replace(
                    ',', '').replace('--', '0') or 0)
                reports.append({
                    'date': date,
                    'fii_net': fii_net,
                    'dii_net': dii_net
                })
            except Exception as e:
                logger.warning(f"Error parsing row: {e}")
        return reports

    def _validate_output(self, data: List[Dict[str, Any]], expected_days: int) -> pd.DataFrame:
        """
        Validate data completeness and return as DataFrame.

        Args:
            data (list): List of parsed data dicts.
            expected_days (int): Expected number of days.

        Returns:
            pd.DataFrame: DataFrame of results.
        """
        if len(data) < expected_days:
            logger.warning(
                f"Only got {len(data)} days of FII/DII data (expected {expected_days})")
        return pd.DataFrame(data)

    def get_sector_flows(self) -> Dict[str, float]:
        """
        Fetch sector-wise FII activity (from monthly reports).
        Placeholder: returns static data.

        Returns:
            dict: Sector name to net flow.
        """
        # TODO: Implement actual PDF parsing if required
        return {
            'BANKING': 1200.0,
            'IT': -450.0,
            'AUTO': 780.0
        }
