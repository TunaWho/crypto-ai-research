import aiohttp
import asyncio
from bs4 import BeautifulSoup
from config import Config
import logging

logger = logging.getLogger('crypto_analyzer.news_scraper')

class NewsScraper:
    def __init__(self):
        logger.debug("Initializing NewsScraper")
        self.keywords = Config.CRYPTO_NEWS_KEYWORDS
        self.news_api_key = Config.NEWS_API_KEY
        self.base_url = "https://newsapi.org/v2/everything"
        self.collected_news = []
    
    async def fetch_news_by_category(self, category='market'):
        """
        Fetch news from specific category of sources
        """
        sources = {
            'premium': Config.PREMIUM_SOURCES,
            'technical': Config.TECHNICAL_SOURCES,
            'market': Config.MARKET_NEWS_SOURCES
        }.get(category, Config.MARKET_NEWS_SOURCES)

        query = " OR ".join(self.keywords)
        logger.debug(f"Fetching {category} news for keywords: {query}")
        
        params = {
            'q': query,
            'apiKey': self.news_api_key,
            'sortBy': 'publishedAt',
            'language': 'en',
            'domains': ','.join(sources)
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                logger.debug(f"Making API request to {self.base_url}")
                async with session.get(self.base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        articles = data.get('articles', [])
                        logger.info(f"Successfully fetched {len(articles)} articles")
                        return articles
                    else:
                        logger.error(f"API request failed with status {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Error fetching news: {str(e)}", exc_info=True)
            return []
    
    def collect_news(self):
        """
        Collect and process crypto news
        """
        logger.info("Starting news collection process")
        results = asyncio.run(self.fetch_news_by_category())
        self.collected_news = results
        logger.info(f"Completed news collection. Total articles: {len(results)}")
        return results

    def run(self):
        """Main execution method"""
        logger.info("Running news collection pipeline")
        self.collect_news()