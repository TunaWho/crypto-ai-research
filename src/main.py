from data_collection.news_scraper import NewsScraper
from data_collection.price_collector import PriceCollector
from analysis.sentiment_analyzer import SentimentAnalyzer
from analysis.technical_analyzer import TechnicalAnalyzer
from report.report_generator import ReportGenerator
from utils.logger import setup_logger

logger = setup_logger()

def main():
    try:
        logger.info("Starting crypto analysis process...")

        # Initialize and run components
        news_scraper = NewsScraper()
        price_collector = PriceCollector()
        sentiment_analyzer = SentimentAnalyzer()
        technical_analyzer = TechnicalAnalyzer()
        report_generator = ReportGenerator()

        # Execute analysis pipeline
        news_scraper.run()
        price_collector.run()
        sentiment_analyzer.run()
        technical_analyzer.run()
        report_generator.run()

        logger.info("Analysis completed successfully!")

    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main()