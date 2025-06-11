# phases/1_morning_screening/quant_screener.py
import talib
import pandas as pd


class QuantitativeScreener:
    def screen(self, universe):
        """Screen stocks based on quantitative factors"""
        screened = {}

        for symbol in universe:
            data = self._get_symbol_data(symbol)

            # Momentum filter
            rsi = talib.RSI(data['close'], timeperiod=14)[-1]
            mom_filter = 30 < rsi < 70

            # Volume filter
            volume_ma = talib.SMA(data['volume'], timeperiod=20)[-1]
            vol_filter = data['volume'][-1] > 1.5 * volume_ma

            if mom_filter and vol_filter:
                screened[symbol] = {
                    'rsi': rsi,
                    'volume_ratio': data['volume'][-1] / volume_ma
                }

        return screened
