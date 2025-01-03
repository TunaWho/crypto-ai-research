import ccxt
import pandas as pd
from config import Config
import logging

logger = logging.getLogger('crypto_analyzer.price_collector')

class PriceCollector:
    def __init__(self):
        logger.debug("Initializing PriceCollector")
        self.exchange = ccxt.binance({
            'apiKey': Config.BINANCE_API_KEY,
            'secret': Config.BINANCE_SECRET_KEY
        })
        self.pairs = Config.CRYPTO_PAIRS
        self.collected_prices = {}
    
    def collect_prices(self):
        """
        Collect cryptocurrency price data from Binance
        Returns DataFrame with OHLCV data
        """
        logger.info("Starting price collection process")
        try:
            all_data = {}
            for pair in self.pairs:
                logger.debug(f"Fetching OHLCV data for {pair}")
                ohlcv = self.exchange.fetch_ohlcv(
                    symbol=pair,
                    timeframe=Config.TIMEFRAME,
                    limit=Config.HISTORICAL_DAYS * 24
                )
                
                df = pd.DataFrame(
                    ohlcv, 
                    columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
                )
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                all_data[pair] = df
                logger.info(f"Successfully collected {len(df)} candles for {pair}")
            
            logger.info("Completed price collection for all pairs")
            self.collected_prices = all_data
            return all_data
            
        except Exception as e:
            logger.error(f"Error collecting price data: {str(e)}", exc_info=True)
            return None

    def run(self):
        """Main execution method"""
        logger.info("Running price collection pipeline")
        self.collect_prices()