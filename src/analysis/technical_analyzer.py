import pandas as pd
import numpy as np
import talib
import logging
from data_collection.price_collector import PriceCollector

logger = logging.getLogger('crypto_analyzer.technical_analyzer')

class TechnicalAnalyzer:
    def __init__(self):
        logger.debug("Initializing TechnicalAnalyzer")
        self.price_collector = PriceCollector()
        self.analysis_results = {}
        
        # Define technical analysis parameters
        self.params = {
            'rsi_period': 14,
            'ma_short': 20,
            'ma_long': 50,
            'macd_fast': 12,
            'macd_slow': 26,
            'macd_signal': 9,
            'bbands_period': 20,
            'bbands_dev': 2
        }

    def calculate_indicators(self, df):
        """Calculate technical indicators for a given price DataFrame"""
        try:
            indicators = {}
            
            # RSI (Relative Strength Index)
            indicators['rsi'] = talib.RSI(df['close'], 
                                        timeperiod=self.params['rsi_period'])

            # Moving Averages
            indicators['ma_short'] = talib.SMA(df['close'], 
                                             timeperiod=self.params['ma_short'])
            indicators['ma_long'] = talib.SMA(df['close'], 
                                            timeperiod=self.params['ma_long'])

            # MACD (Moving Average Convergence Divergence)
            macd, signal, hist = talib.MACD(df['close'],
                                          fastperiod=self.params['macd_fast'],
                                          slowperiod=self.params['macd_slow'],
                                          signalperiod=self.params['macd_signal'])
            indicators['macd'] = macd
            indicators['macd_signal'] = signal
            indicators['macd_hist'] = hist

            # Bollinger Bands
            upper, middle, lower = talib.BBANDS(df['close'],
                                              timeperiod=self.params['bbands_period'],
                                              nbdevup=self.params['bbands_dev'],
                                              nbdevdn=self.params['bbands_dev'])
            indicators['bb_upper'] = upper
            indicators['bb_middle'] = middle
            indicators['bb_lower'] = lower

            # Volume indicators
            indicators['obv'] = talib.OBV(df['close'], df['volume'])
            
            return indicators
            
        except Exception as e:
            logger.error(f"Error calculating indicators: {str(e)}", exc_info=True)
            return None

    def generate_signals(self, df, indicators):
        """Generate trading signals based on technical indicators"""
        signals = {
            'rsi_oversold': indicators['rsi'] < 30,  # RSI oversold signal
            'rsi_overbought': indicators['rsi'] > 70,  # RSI overbought signal
            'ma_crossover': indicators['ma_short'] > indicators['ma_long'],  # Golden cross
            'ma_crossunder': indicators['ma_short'] < indicators['ma_long'],  # Death cross
            'macd_crossover': indicators['macd'] > indicators['macd_signal'],  # MACD bullish
            'macd_crossunder': indicators['macd'] < indicators['macd_signal'],  # MACD bearish
            'price_above_bb': df['close'] > indicators['bb_upper'],  # Price above upper BB
            'price_below_bb': df['close'] < indicators['bb_lower']   # Price below lower BB
        }
        
        # Generate overall signal
        bullish_signals = sum([
            signals['rsi_oversold'],
            signals['ma_crossover'],
            signals['macd_crossover'],
            signals['price_below_bb']
        ])
        
        bearish_signals = sum([
            signals['rsi_overbought'],
            signals['ma_crossunder'],
            signals['macd_crossunder'],
            signals['price_above_bb']
        ])
        
        return {
            'signals': signals,
            'bullish_count': bullish_signals,
            'bearish_count': bearish_signals,
            'overall_bias': 'bullish' if bullish_signals > bearish_signals else 'bearish'
        }

    def analyze_pair(self, pair, df):
        """Analyze a single trading pair"""
        logger.info(f"Analyzing {pair}")
        
        # Calculate technical indicators
        indicators = self.calculate_indicators(df)
        if indicators is None:
            return None
            
        # Generate trading signals
        signals = self.generate_signals(df, indicators)
        
        # Combine results
        return {
            'indicators': indicators,
            'signals': signals,
            'last_close': df['close'].iloc[-1],
            'last_updated': df['timestamp'].iloc[-1]
        }

    def run(self):
        """Main execution method"""
        logger.info("Running technical analysis pipeline")
        
        # Get price data from collector
        price_data = self.price_collector.collected_prices
        if not price_data:
            logger.warning("No price data available for analysis")
            return

        # Analyze each trading pair
        for pair, df in price_data.items():
            self.analysis_results[pair] = self.analyze_pair(pair, df)
            logger.info(f"Completed analysis for {pair}")
