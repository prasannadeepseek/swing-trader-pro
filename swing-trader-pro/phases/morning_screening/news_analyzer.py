# phases/1_morning_screening/news_analyzer.py
from typing import List, Dict, Any
import requests
import json
from textblob import TextBlob


class NewsAnalyzer:
    def __init__(self):
        with open('config/news_sources.json') as f:
            self.sources = json.load(f)

    def analyze(self, symbol):
        """Aggregate sentiment from all configured sources"""
        sentiments = []

        for source, config in self.sources.items():
            articles = self._fetch_news(source, symbol)
            source_sentiment = self._analyze_articles(articles)
            sentiments.append(source_sentiment * config.get('weight', 1.0))

        return sum(sentiments) / len(sentiments)

    def _fetch_news(self, source, symbol):
        """Fetch news articles for given symbol"""
        if source == 'moneycontrol':
            return self._fetch_moneycontrol(symbol)
        elif source == 'economic_times':
            return self._fetch_economic_times(symbol)
        elif source == 'twitter_finance':
            return self._fetch_twitter(symbol)
        return []

    def _analyze_articles(self, articles):
        """Calculate sentiment score for articles"""
        if not articles:
            return 0.0

        polarities = [
            TextBlob(article['title']).sentiment.polarity
            for article in articles
        ]
        return sum(polarities) / len(polarities)

# method 2


class NewsAnalyzer:
    SOURCES = [
        'moneycontrol',
        'twitter_finance',
        'economic_times'
    ]

    def analyze(self, symbol):
        sentiment_score = 0
        for source in self.SOURCES:
            news = self._fetch_news(source, symbol)
            sentiment_score += self._calculate_sentiment(news)
        return sentiment_score / len(self.SOURCES)

# method 3 final version


class NewsAnalyzer:
    """
    Aggregates and analyzes news sentiment for a given symbol from multiple sources.
    Sources and their weights are configurable via a JSON config file.
    """

    def __init__(self, config_path: str = 'config/news_sources.json'):
        """
        Initialize NewsAnalyzer with sources from config.

        Args:
            config_path (str): Path to JSON config listing sources and weights.
        """
        try:
            with open(config_path) as f:
                self.sources = json.load(f)
        except Exception as e:
            print(f"Error loading news sources config: {e}")
            # Fallback to default sources if config fails
            self.sources = {
                "moneycontrol": {"weight": 1.0},
                "economic_times": {"weight": 1.0},
                "twitter_finance": {"weight": 1.0}
            }

    def analyze(self, symbol: str) -> float:
        """
        Aggregate sentiment from all configured sources for a symbol.

        Args:
            symbol (str): The trading symbol.

        Returns:
            float: Weighted average sentiment score (-1 to 1).
        """
        sentiments = []
        total_weight = 0.0

        for source, config in self.sources.items():
            try:
                articles = self._fetch_news(source, symbol)
                source_sentiment = self._analyze_articles(articles)
                weight = config.get('weight', 1.0)
                sentiments.append(source_sentiment * weight)
                total_weight += weight
            except Exception as e:
                print(f"Error analyzing {source} for {symbol}: {e}")

        if not sentiments or total_weight == 0:
            return 0.0
        return sum(sentiments) / total_weight

    def _fetch_news(self, source: str, symbol: str) -> List[Dict[str, Any]]:
        """
        Fetch news articles for a given symbol from a specified source.

        Args:
            source (str): Source name.
            symbol (str): Trading symbol.

        Returns:
            list: List of article dicts with at least a 'title' key.
        """
        if source == 'moneycontrol':
            return self._fetch_moneycontrol(symbol)
        elif source == 'economic_times':
            return self._fetch_economic_times(symbol)
        elif source == 'twitter_finance':
            return self._fetch_twitter(symbol)
        else:
            print(f"Unknown news source: {source}")
            return []

    def _analyze_articles(self, articles: List[Dict[str, Any]]) -> float:
        """
        Calculate average sentiment polarity for a list of articles.

        Args:
            articles (list): List of article dicts with 'title'.

        Returns:
            float: Average sentiment polarity (-1 to 1).
        """
        if not articles:
            return 0.0

        polarities = [
            TextBlob(article.get('title', '')).sentiment.polarity
            for article in articles if 'title' in article
        ]
        return sum(polarities) / len(polarities) if polarities else 0.0

    def _fetch_moneycontrol(self, symbol: str) -> List[Dict[str, Any]]:
        """
        Fetch news articles from Moneycontrol for a symbol.
        (Stub implementation; replace with real API/web scraping.)

        Args:
            symbol (str): Trading symbol.

        Returns:
            list: List of article dicts.
        """
        # TODO: Implement actual fetching logic
        return []

    def _fetch_economic_times(self, symbol: str) -> List[Dict[str, Any]]:
        """
        Fetch news articles from Economic Times for a symbol.
        (Stub implementation; replace with real API/web scraping.)

        Args:
            symbol (str): Trading symbol.

        Returns:
            list: List of article dicts.
        """
        # TODO: Implement actual fetching logic
        return []

    def _fetch_twitter(self, symbol: str) -> List[Dict[str, Any]]:
        """
        Fetch news articles/tweets from Twitter Finance for a symbol.
        (Stub implementation; replace with real API.)

        Args:
            symbol (str): Trading symbol.

        Returns:
            list: List of article dicts.
        """
        # TODO: Implement actual fetching logic
        return []


# method 4 final version with error handling and logging


class NewsAnalyzer:
    """
    Aggregates and analyzes news sentiment for a given symbol from multiple sources.
    Sources and their weights are configurable via a JSON config file.
    """

    def __init__(self, config_path: str = 'config/news_sources.json'):
        """
        Initialize NewsAnalyzer with sources from config.

        Args:
            config_path (str): Path to JSON config listing sources and weights.
        """
        try:
            with open(config_path) as f:
                self.sources = json.load(f)
        except Exception as e:
            print(f"Error loading news sources config: {e}")
            # Fallback to default sources if config fails
            self.sources = {
                "moneycontrol": {"weight": 1.0},
                "economic_times": {"weight": 1.0},
                "twitter_finance": {"weight": 1.0}
            }

    def analyze(self, symbol: str) -> float:
        """
        Aggregate sentiment from all configured sources for a symbol.

        Args:
            symbol (str): The trading symbol.

        Returns:
            float: Weighted average sentiment score (-1 to 1).
        """
        sentiments = []
        total_weight = 0.0

        for source, config in self.sources.items():
            try:
                articles = self._fetch_news(source, symbol)
                source_sentiment = self._analyze_articles(articles)
                weight = config.get('weight', 1.0)
                sentiments.append(source_sentiment * weight)
                total_weight += weight
            except Exception as e:
                print(f"Error analyzing {source} for {symbol}: {e}")

        if not sentiments or total_weight == 0:
            return 0.0
        return sum(sentiments) / total_weight

    def _fetch_news(self, source: str, symbol: str) -> List[Dict[str, Any]]:
        """
        Fetch news articles for a given symbol from a specified source.

        Args:
            source (str): Source name.
            symbol (str): Trading symbol.

        Returns:
            list: List of article dicts with at least a 'title' key.
        """
        if source == 'moneycontrol':
            return self._fetch_moneycontrol(symbol)
        elif source == 'economic_times':
            return self._fetch_economic_times(symbol)
        elif source == 'twitter_finance':
            return self._fetch_twitter(symbol)
        else:
            print(f"Unknown news source: {source}")
            return []

    def _analyze_articles(self, articles: List[Dict[str, Any]]) -> float:
        """
        Calculate average sentiment polarity for a list of articles.

        Args:
            articles (list): List of article dicts with 'title'.

        Returns:
            float: Average sentiment polarity (-1 to 1).
        """
        if not articles:
            return 0.0

        polarities = [
            TextBlob(article.get('title', '')).sentiment.polarity
            for article in articles if 'title' in article
        ]
        return sum(polarities) / len(polarities) if polarities else 0.0

    def _fetch_moneycontrol(self, symbol: str) -> List[Dict[str, Any]]:
        """
        Fetch news articles from Moneycontrol for a symbol.
        Simulated implementation: Replace with real API/web scraping.

        Args:
            symbol (str): Trading symbol.

        Returns:
            list: List of article dicts.
        """
        # Example: Simulate fetching with a public RSS feed or placeholder
        try:
            url = f"https://newsapi.org/v2/everything?q={symbol}+moneycontrol&apiKey=YOUR_NEWSAPI_KEY"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [{"title": article["title"]} for article in data.get("articles", [])]
        except Exception as e:
            print(f"Moneycontrol fetch error: {e}")
        # Fallback: Simulated articles
        return [
            {"title": f"{symbol} sees strong buying interest, says Moneycontrol"},
            {"title": f"{symbol} faces resistance at key level, Moneycontrol reports"}
        ]

    def _fetch_economic_times(self, symbol: str) -> List[Dict[str, Any]]:
        """
        Fetch news articles from Economic Times for a symbol.
        Simulated implementation: Replace with real API/web scraping.

        Args:
            symbol (str): Trading symbol.

        Returns:
            list: List of article dicts.
        """
        try:
            url = f"https://newsapi.org/v2/everything?q={symbol}+economic+times&apiKey=YOUR_NEWSAPI_KEY"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [{"title": article["title"]} for article in data.get("articles", [])]
        except Exception as e:
            print(f"Economic Times fetch error: {e}")
        # Fallback: Simulated articles
        return [
            {"title": f"Economic Times: {symbol} outlook positive for next quarter"},
            {"title": f"{symbol} underperforms sector, Economic Times analysis"}
        ]

    def _fetch_twitter(self, symbol: str) -> List[Dict[str, Any]]:
        """
        Fetch news articles/tweets from Twitter Finance for a symbol.
        Simulated implementation: Replace with real API.

        Args:
            symbol (str): Trading symbol.

        Returns:
            list: List of article dicts.
        """
        # In production, use Twitter API (tweepy or similar) to fetch tweets
        # For now, simulate with static examples
        return [
            {"title": f"Twitter: {symbol} breakout expected soon!"},
            {"title": f"Bearish sentiment rising for {symbol} on Twitter"}
        ]
