from textblob import TextBlob
import pandas as pd
import numpy as np
import logging
from data_collection.news_scraper import NewsScraper

logger = logging.getLogger('crypto_analyzer.sentiment_analyzer')

class SentimentAnalyzer:
    def __init__(self):
        logger.debug("Initializing SentimentAnalyzer")
        self.sentiment_scores = []
        self.news_scraper = NewsScraper()

    def analyze_text(self, texts):
        """
        Analyze sentiment of crypto news and social media content
        Returns sentiment scores with crypto-specific context
        """
        logger.info(f"Starting sentiment analysis for {len(texts)} texts")
        sentiments = []
        
        for i, text in enumerate(texts, 1):
            logger.debug(f"Analyzing text {i}/{len(texts)}")
            analysis = TextBlob(text)
            
            sentiment = {
                'text': text,
                'polarity': analysis.sentiment.polarity,
                'subjectivity': analysis.sentiment.subjectivity,
                'is_bullish': analysis.sentiment.polarity > 0.2,
                'is_bearish': analysis.sentiment.polarity < -0.2
            }
            sentiments.append(sentiment)
            
            if i % 100 == 0:  # Log progress every 100 texts
                logger.info(f"Processed {i}/{len(texts)} texts")

        logger.info("Completed sentiment analysis")
        return sentiments

    def get_market_sentiment(self):
        """
        Get overall crypto market sentiment
        Returns: float between -1 (very bearish) and 1 (very bullish)
        """
        logger.debug("Calculating overall market sentiment")
        if not self.sentiment_scores:
            logger.warning("No sentiment scores available")
            return 0
            
        sentiment = np.mean([score['polarity'] for score in self.sentiment_scores])
        logger.info(f"Overall market sentiment: {sentiment}")
        return sentiment 

    def run(self):
        """Main execution method"""
        logger.info("Running sentiment analysis pipeline")
        news_data = self.news_scraper.collected_news
        if not news_data:
            logger.warning("No news data available for analysis")
            return

        self.sentiment_scores = self.analyze_text([article['content'] for article in news_data]) 