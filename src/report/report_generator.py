import jinja2
import matplotlib.pyplot as plt
from datetime import datetime
from data_collection.news_scraper import NewsScraper
from data_collection.price_collector import PriceCollector
from analysis.sentiment_analyzer import SentimentAnalyzer
from analysis.technical_analyzer import TechnicalAnalyzer
from utils.logger import setup_logger
from config import Config

logger = setup_logger()

class ReportGenerator:
    def __init__(self):
        logger.debug("Initializing ReportGenerator")
        self.news_scraper = NewsScraper()
        self.price_collector = PriceCollector()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.technical_analyzer = TechnicalAnalyzer()

    def generate_report(self):
        report_data = {
            'news_data': self.news_scraper.collected_news,
            'price_data': self.price_collector.collected_prices,
            'sentiment_results': self.sentiment_analyzer.sentiment_scores,
            'technical_results': self.technical_analyzer.analysis_results
        }
        # Generate report using the collected data
        return report_data

    def run(self):
        """Main execution method"""
        logger.info("Generating final report")
        self.generate_report()

    def generate_market_overview(self):
        """Generate market-wide overview and trends"""
        market_data = self.market_analyzer.market_trends
        
        overview = {
            'trending_sectors': [
                sector for sector in market_data['sector_performance']
                if sector['momentum'] > Config.TRENDING_THRESHOLD
            ],
            'emerging_narratives': market_data['narratives'][:5],  # Top 5 narratives
            'sentiment_shifts': market_data['market_sentiment'],
            'correlated_movements': self._identify_correlations(),
            'volume_trends': self._analyze_volume_patterns()
        }
        
        return overview