from dotenv import load_dotenv
import os
import requests
import logging

load_dotenv()

logger = logging.getLogger(__name__)

class Config:
    # API Keys and Credentials
    BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
    BINANCE_SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')
    NEWS_API_KEY = os.getenv('NEWS_API_KEY')
    COINMARKETCAP_API_KEY = os.getenv('COINMARKETCAP_API_KEY')
    TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
    REDDIT_API_KEY = os.getenv('REDDIT_API_KEY')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    COINGECKO_API_KEY = os.getenv('COINGECKO_API_KEY')
    GLASSNODE_API_KEY = os.getenv('GLASSNODE_API_KEY')
    
    # Database Configuration
    DATABASE_URL = os.getenv('DATABASE_URL')
    DATABASE_NAME = 'crypto_research'
    
    # Crypto Trading Settings
    CRYPTO_PAIRS = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT']
    CRYPTO_NEWS_KEYWORDS = ['bitcoin', 'ethereum', 'crypto']
    
    # Data Sources
    NEWS_SOURCES = [
        # Major Crypto News Platforms
        'https://cointelegraph.com',
        'https://coindesk.com',
        'https://bitcoinmagazine.com',
        'https://cryptonews.com',
        'https://decrypt.co',
        'https://theblock.co',
        
        # Financial News with Crypto Coverage
        'https://bloomberg.com/crypto',
        'https://reuters.com/technology/crypto',
        'https://forbes.com/crypto-blockchain',
        'https://ft.com/cryptocurrencies',
        'https://cnbc.com/crypto',
        
        # Technical Analysis Focused
        'https://tradingview.com/news',
        'https://cryptoslate.com',
        'https://ambcrypto.com',
        
        # Regional Crypto News
        'https://forkast.news',           # Asia Focus
        'https://bitcoinist.com',         # Global
        'https://newsbtc.com',            # Global
        
        # Research and Analysis
        'https://messari.io',
        'https://glassnode.com/insights',
        'https://cryptoquant.com/blog',
        
        # Exchange News Platforms
        'https://binance.com/en/news',
        'https://blog.coinbase.com',
        'https://kraken.com/learn',
        
        # Community and Social
        'https://reddit.com/r/CryptoCurrency',  # Reddit's main crypto community
        'https://medium.com/tag/cryptocurrency'  # Curated crypto articles
    ]
    
    # You might want to categorize them for different types of analysis
    PREMIUM_SOURCES = [
        'https://bloomberg.com/crypto',
        'https://ft.com/cryptocurrencies',
        'https://theblock.co'
    ]

    TECHNICAL_SOURCES = [
        'https://tradingview.com/news',
        'https://glassnode.com/insights',
        'https://cryptoquant.com/blog'
    ]

    MARKET_NEWS_SOURCES = [
        'https://cointelegraph.com',
        'https://coindesk.com',
        'https://decrypt.co'
    ]
    
    # Time Settings
    HISTORICAL_DAYS = 30
    TIMEFRAME = '1h'
    UPDATE_INTERVAL = 300  # 5 minutes

    # Market Trend Analysis Settings
    TRENDING_THRESHOLD = 0.15  # 15% movement threshold
    VOLUME_SURGE_THRESHOLD = 2.0  # 2x normal volume
    TOP_COINS_COUNT = 100  # Number of top coins to analyze
    CORRELATION_THRESHOLD = 0.7  # Strong correlation threshold
    
    # Trend Categories
    TREND_CATEGORIES = [
        'defi',
        'gaming',
        'layer1',
        'layer2',
        'meme',
        'ai',
        'web3',
        'metaverse'
    ]

    # Groq API Settings
    GROQ_API_BASE = "https://api.groq.com/v1"
    
    # AI Model Settings
    AI_MODEL = "mixtral-8x7b-32768"  # Fast and efficient
    MAX_TOKENS = 4096
    TEMPERATURE = 0.7
    SYSTEM_TIMEOUT = 30  # seconds
    
    # Analysis Settings
    ANALYSIS_RETRY_ATTEMPTS = 3
    MINIMUM_ANALYSIS_LENGTH = 500  # characters
    
    # Agent Settings
    UPDATE_FREQUENCY = 3600  # How often to update analysis (1 hour)
    MINIMUM_CONFIDENCE = 0.8  # Minimum confidence for including insights

    # Market Data Settings
    MARKET_DATA_UPDATE_INTERVAL = 300  # 5 minutes
    PRICE_CHANGE_THRESHOLDS = {
        'significant': 5.0,  # 5% change
        'major': 10.0,      # 10% change
        'extreme': 20.0     # 20% change
    }

    @classmethod
    def validate(cls):
        """Validate all required configuration is present"""
        required_keys = [
            'BINANCE_API_KEY',
            'BINANCE_SECRET_KEY',
            'NEWS_API_KEY',
            'DATABASE_URL'
        ]
        for key in required_keys:
            if not getattr(cls, key):
                raise ValueError(f"Missing required configuration: {key}") 

    @classmethod
    def validate_sources(cls):
        invalid_sources = []
        for source in cls.NEWS_SOURCES:
            if not validate_news_source(source):
                invalid_sources.append(source)
        
        if invalid_sources:
            logger.warning(f"Invalid news sources found: {invalid_sources}")

    @classmethod
    def validate_sources_by_category(cls):
        """
        Validate news sources by category and check their availability
        """
        validation_results = {
            'premium': [],
            'technical': [],
            'market': [],
            'invalid': []
        }

        for source in cls.NEWS_SOURCES:
            if not validate_news_source(source):
                validation_results['invalid'].append(source)
                continue

            if source in cls.PREMIUM_SOURCES:
                validation_results['premium'].append(source)
            elif source in cls.TECHNICAL_SOURCES:
                validation_results['technical'].append(source)
            elif source in cls.MARKET_NEWS_SOURCES:
                validation_results['market'].append(source)

        return validation_results

def validate_news_source(url):
    """
    Validate if a news source is accessible and returns valid data
    """
    try:
        response = requests.head(url)
        return response.status_code == 200
    except Exception:
        return False 