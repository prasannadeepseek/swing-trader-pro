# phases/1_morning_screening/news_analyzer.py
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


class NewsSentimentAnalyzer:
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
