import MetaTrader5 as mt5
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class MarketAnalysis:

    @staticmethod
    def get_current_signals(symbol, ema_period=200, rsi_period=14):
        """
        Motor Cuantitativo de Triple Confirmación (MTFA)
        Filtra el ruido exigiendo alineación entre la tendencia de 1 Hora y el gatillo de 1 Minuto.
        """
        try:
            # --- 1. FILTRO MACRO: TENDENCIA EN H1 ---
            rates_h1 = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_H1, 0, ema_period + 1)
            if rates_h1 is None or len(rates_h1) < ema_period: 
                return "WAIT"
                
            df_h1 = pd.DataFrame(rates_h1)
            close_h1 = df_h1['close'].iloc[-1]
            
            # Cálculo de Media Móvil Exponencial (EMA 200) nativo en Pandas
            ema_200_h1 = df_h1['close'].ewm(span=ema_period, adjust=False).mean().iloc[-1]
            macro_trend = "UP" if close_h1 > ema_200_h1 else "DOWN"

            # --- 2. GATILLO MICRO: RSI EN M1 ---
            rates_m1 = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, rsi_period + 50)
            if rates_m1 is None or len(rates_m1) < rsi_period: 
                return "WAIT"
                
            df_m1 = pd.DataFrame(rates_m1)
            
            # Cálculo de RSI Clásico
            delta = df_m1['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
            rs = gain / loss
            df_m1['RSI'] = 100 - (100 / (1 + rs))
            
            current_rsi = df_m1['RSI'].iloc[-1]

            # --- 3. EJECUCIÓN DEL FRANCOTIRADOR ---
            # Compras: Tendencia H1 Alcista + RSI M1 en Sobrevendida extrema
            if macro_trend == "UP" and current_rsi < 30.0:
                logger.info(f"[🎯 ALINEACIÓN] {symbol} | Tendencia H1: UP | RSI M1: {current_rsi:.2f} -> BUY")
                return "BUY"

            # Ventas: Tendencia H1 Bajista + RSI M1 en Sobrecomprada extrema
            if macro_trend == "DOWN" and current_rsi > 70.0:
                logger.info(f"[🎯 ALINEACIÓN] {symbol} | Tendencia H1: DOWN | RSI M1: {current_rsi:.2f} -> SELL")
                return "SELL"

            return "WAIT"

        except Exception as e:
            logger.error(f"[-] Error en cálculo cuantitativo de {symbol}: {e}")
            return "WAIT"