import pandas as pd
import numpy as np
from collections import defaultdict
from config import Config
import logging

logger = logging.getLogger('crypto_analyzer.market_analyzer')

class MarketAnalyzer:
    def __init__(self):
        self.price_collector = PriceCollector()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.technical_analyzer = TechnicalAnalyzer()
        self.market_trends = {}
        
    def analyze_sector_performance(self):
        """Analyze performance by crypto sectors/categories"""
        sector_performance = defaultdict(list)
        
        for pair, analysis in self.technical_analyzer.analysis_results.items():
            for category in Config.TREND_CATEGORIES:
                if self._is_in_category(pair, category):
                    performance = self._calculate_performance(analysis)
                    sector_performance[category].append(performance)
        
        return {
            category: {
                'average_return': np.mean(performances),
                'momentum': self._calculate_momentum(performances),
                'volume_trend': self._analyze_volume_trend(category)
            }
            for category, performances in sector_performance.items()
        }
    
    def identify_market_trends(self):
        """Identify emerging market trends"""
        trends = {
            'rising_sectors': [],
            'falling_sectors': [],
            'volume_surges': [],
            'correlated_moves': [],
            'sentiment_shifts': [],
            'emerging_narratives': []
        }
        
        # Analyze sector movements
        sector_perf = self.analyze_sector_performance()
        for sector, data in sector_perf.items():
            if data['momentum'] > Config.TRENDING_THRESHOLD:
                trends['rising_sectors'].append({
                    'sector': sector,
                    'momentum': data['momentum'],
                    'volume_change': data['volume_trend']
                })
            elif data['momentum'] < -Config.TRENDING_THRESHOLD:
                trends['falling_sectors'].append(sector)
        
        # Analyze sentiment trends
        sentiment_trends = self._analyze_sentiment_trends()
        trends['sentiment_shifts'] = sentiment_trends
        
        # Identify narrative changes
        trends['emerging_narratives'] = self._identify_emerging_narratives()
        
        return trends
    
    def _analyze_sentiment_trends(self):
        """Analyze sentiment trends across different categories"""
        sentiment_data = self.sentiment_analyzer.sentiment_scores
        
        # Group sentiment by category and time
        categorized_sentiment = defaultdict(list)
        for score in sentiment_data:
            for category in Config.TREND_CATEGORIES:
                if any(keyword in score['text'].lower() for keyword in self._get_category_keywords(category)):
                    categorized_sentiment[category].append(score['polarity'])
        
        return {
            category: {
                'average_sentiment': np.mean(scores),
                'sentiment_change': self._calculate_sentiment_change(scores),
                'confidence': len(scores)  # Number of mentions
            }
            for category, scores in categorized_sentiment.items()
        }
    
    def _identify_emerging_narratives(self):
        """Identify new and emerging narratives in the crypto market"""
        news_data = self.news_scraper.collected_news
        
        # Extract common themes and topics
        themes = defaultdict(int)
        for article in news_data:
            topics = self._extract_topics(article['content'])
            for topic in topics:
                themes[topic] += 1
        
        # Filter for emerging narratives
        emerging = []
        for theme, count in themes.items():
            if count > 5:  # Minimum mention threshold
                sentiment = self._calculate_theme_sentiment(theme, news_data)
                emerging.append({
                    'theme': theme,
                    'mention_count': count,
                    'sentiment': sentiment,
                    'related_assets': self._find_related_assets(theme)
                })
        
        return sorted(emerging, key=lambda x: x['mention_count'], reverse=True)
    
    def run(self):
        """Execute market analysis pipeline"""
        logger.info("Starting market-wide analysis")
        
        # Collect and analyze market data
        self.market_trends = {
            'sector_performance': self.analyze_sector_performance(),
            'emerging_trends': self.identify_market_trends(),
            'market_sentiment': self._analyze_sentiment_trends(),
            'narratives': self._identify_emerging_narratives()
        }
        
        logger.info("Market analysis completed")
        return self.market_trends 