from typing import Dict, List
import logging
import asyncio
import pandas as pd
from datetime import datetime, timedelta
from pycoingecko import CoinGeckoAPI
from binance.client import Client as BinanceClient
from glassnode.client import GlassnodeClient
from config import Config

logger = logging.getLogger('crypto_analyzer.market_data_agent')

class MarketDataAgent:
    """
    Market Data Agent collects comprehensive market data using multiple APIs:
    
    1. CoinGecko API (Free tier available):
       - Get API key: https://www.coingecko.com/api/pricing
       - Free tier: 50 calls/minute
       - Provides: Market data, prices, volumes, market caps
    
    2. Binance API (Free):
       - Get API key: https://www.binance.com/en/support/faq/how-to-create-api-360002502072
       - Free tier: 1200 requests/minute
       - Provides: Real-time trading data, order book, recent trades
    
    3. Glassnode API (Paid, but worth it for on-chain data):
       - Get API key: https://docs.glassnode.com/basic-api/api-key
       - Provides: On-chain metrics, network data, institutional flows
    """
    
    def __init__(self):
        logger.debug("Initializing MarketDataAgent")
        
        # Initialize API clients
        self.cg = CoinGeckoAPI()
        self.binance = BinanceClient(
            Config.BINANCE_API_KEY,
            Config.BINANCE_SECRET_KEY
        )
        self.glassnode = GlassnodeClient(Config.GLASSNODE_API_KEY)
        
        # Cache for storing data
        self.market_data = {}
        self.last_update = None

    async def get_market_overview(self) -> Dict:
        """Get comprehensive market overview"""
        try:
            # Get top coins market data
            market_data = self.cg.get_coins_markets(
                vs_currency='usd',
                order='market_cap_desc',
                per_page=Config.TOP_COINS_COUNT,
                sparkline=True,
                price_change_percentage='1h,24h,7d'
            )
            
            # Process and structure the data
            overview = {
                'global_market_cap': sum(coin['market_cap'] for coin in market_data),
                'total_volume_24h': sum(coin['total_volume'] for coin in market_data),
                'bitcoin_dominance': self._calculate_btc_dominance(market_data),
                'top_gainers': self._get_top_movers(market_data, 'gainers'),
                'top_losers': self._get_top_movers(market_data, 'losers'),
                'sector_performance': await self._get_sector_performance(),
                'market_metrics': await self._get_market_metrics()
            }
            
            return overview
            
        except Exception as e:
            logger.error(f"Error fetching market overview: {str(e)}", exc_info=True)
            raise

    async def get_onchain_metrics(self) -> Dict:
        """Get on-chain metrics from Glassnode"""
        try:
            metrics = {
                'network_growth': self.glassnode.get_metric('network_growth'),
                'active_addresses': self.glassnode.get_metric('active_addresses'),
                'transaction_volume': self.glassnode.get_metric('transaction_volume'),
                'exchange_flows': self.glassnode.get_metric('exchange_flows'),
                'institutional_metrics': await self._get_institutional_metrics()
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error fetching on-chain metrics: {str(e)}", exc_info=True)
            return {}

    async def get_trading_metrics(self) -> Dict:
        """Get trading metrics from Binance"""
        try:
            trading_data = {}
            
            for pair in Config.CRYPTO_PAIRS:
                # Get recent trades
                trades = self.binance.get_recent_trades(symbol=pair)
                
                # Get order book
                depth = self.binance.get_order_book(symbol=pair)
                
                # Get 24h ticker
                ticker = self.binance.get_ticker(symbol=pair)
                
                trading_data[pair] = {
                    'recent_trades': trades[:100],  # Last 100 trades
                    'order_book': depth,
                    'ticker_24h': ticker
                }
            
            return trading_data
            
        except Exception as e:
            logger.error(f"Error fetching trading metrics: {str(e)}", exc_info=True)
            return {}

    async def _get_sector_performance(self) -> Dict:
        """Calculate performance by sector"""
        try:
            sector_data = {}
            
            for category in Config.TREND_CATEGORIES:
                # Get coins in category
                coins = self.cg.get_coins_markets(
                    vs_currency='usd',
                    category=category,
                    order='market_cap_desc',
                    per_page=20,
                    sparkline=False
                )
                
                sector_data[category] = {
                    'market_cap': sum(coin['market_cap'] for coin in coins),
                    'volume_24h': sum(coin['total_volume'] for coin in coins),
                    'price_change_24h': sum(coin['price_change_percentage_24h'] for coin in coins) / len(coins)
                }
            
            return sector_data
            
        except Exception as e:
            logger.error(f"Error calculating sector performance: {str(e)}", exc_info=True)
            return {}

    def _calculate_btc_dominance(self, market_data: List) -> float:
        """Calculate Bitcoin dominance"""
        total_market_cap = sum(coin['market_cap'] for coin in market_data)
        btc_market_cap = next(coin['market_cap'] for coin in market_data if coin['symbol'] == 'btc')
        return (btc_market_cap / total_market_cap) * 100

    async def run(self):
        """Execute market data collection pipeline"""
        logger.info("Starting market data collection")
        try:
            self.market_data = {
                'overview': await self.get_market_overview(),
                'onchain_metrics': await self.get_onchain_metrics(),
                'trading_metrics': await self.get_trading_metrics(),
                'timestamp': datetime.now().isoformat()
            }
            self.last_update = datetime.now()
            
            logger.info("Market data collection completed successfully")
            return self.market_data
            
        except Exception as e:
            logger.error(f"Error in market data collection: {str(e)}", exc_info=True)
            raise 