import os
from dotenv import load_dotenv

load_dotenv()

CONFIG = {
    'api_keys': {
        'coinmarketcap': os.getenv('COINMARKETCAP_API_KEY'),
        'twitter': os.getenv('TWITTER_API_KEY'),
        'reddit': os.getenv('REDDIT_API_KEY')
    },
    'data_sources': {
        'news_sites': [
            'https://cointelegraph.com',
            'https://cryptonews.com',
            # Add more sources
        ],
        'update_interval': 3600  # seconds
    },
    'database': {
        'url': os.getenv('DATABASE_URL'),
        'name': 'crypto_research'
    }
}
