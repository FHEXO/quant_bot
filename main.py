import time
import threading
import MetaTrader5 as mt5
from config.settings import (
    ACCOUNT_ID, ACCOUNT_PASSWORD, ACCOUNT_SERVER,
    FOREX_SYMBOLS, FOREX_MAGIC, FOREX_STEP,
    METALS_SYMBOLS, METALS_MAGIC, METALS_STEP,
    CRYPTO_SYMBOLS, CRYPTO_MAGIC, CRYPTO_STEP,
    INDICES_SYMBOLS, INDICES_MAGIC, INDICES_STEP,
    ENERGY_SYMBOLS, ENERGY_MAGIC, ENERGY_STEP,
    STOCKS_SYMBOLS, STOCKS_MAGIC, STOCKS_STEP, # <-- ESTO ES LO NUEVO
    MAX_POSITIONS, EMA_PERIOD, RSI_PERIOD
)
from core.analysis import MarketAnalysis
from core.execution import ExecutionManager
from core.risk_manager import RiskManager

import logging

# Configurar logging central
logging.basicConfig(
    level=logging.INFO, 
    format="[%(asctime)s] (Hilo: %(threadName)s) %(message)s", 
    datefmt="%Y-%m-%d %H:%M:%S", 
    handlers=[
        logging.FileHandler("logs/quant_bot.log", encoding="utf-8"), 
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def initialize_mt5():
    """Asegura la conexión única al servidor del broker."""
    if not mt5.initialize():
        logger.error("Error crítico al inicializar MetaTrader5")
        return False
    if not mt5.login(ACCOUNT_ID, password=ACCOUNT_PASSWORD, server=ACCOUNT_SERVER):
        logger.error(f"Error de autenticación en el servidor: {ACCOUNT_SERVER}")
        return False
    return True

def market_worker(symbols_list, magic_number, step_distance, market_name):
    threading.current_thread().name = market_name
    logger.info(f"Fila de patrullaje activada con Firma: {magic_number}")
    
    while True:
        # --> ESTA LÍNEA ES EL LATIDO
        logger.info(f"Patrullando {len(symbols_list)} activos...") 
        
        for symbol in symbols_list:
            try:
                # --------------------------------------------------------
                # 🛡️ ESCUDO DE ESTADO DE MERCADO (Evita bucles en activos cerrados)
                # --------------------------------------------------------
                symbol_info = mt5.symbol_info(symbol)
                if symbol_info is None:
                    continue
                
                # Si el activo no está visible o tiene la negociación completamente bloqueada
                if not symbol_info.visible or symbol_info.trade_mode == mt5.SYMBOL_TRADE_MODE_DISABLED:
                    continue
                
                # Verificación institucional de sesión: Si no acepta órdenes en este milisegundo
                if symbol_info.trade_mode == mt5.SYMBOL_TRADE_MODE_CLOSEONLY:
                    continue

                # 0. Módulo Asegurador: Ajustar Trailing Stop si estamos en verde
                RiskManager.apply_trailing_stop(symbol, magic_number)

                # --- 1. El bot SIEMPRE analiza el activo matemáticamente (Si el mercado está abierto)
                signal = MarketAnalysis.get_current_signals(symbol, ema_period=EMA_PERIOD, rsi_period=RSI_PERIOD)
                
                # 2. Si la matemática detecta una oportunidad "Sniper Elite"
                if signal in ["BUY", "SELL"]:
                    
                    # 🛡️ FILTRO GLOBAL: Verifica tu margen antes de jalar el gatillo
                    total_open_trades = mt5.positions_total()
                    if total_open_trades >= MAX_POSITIONS:
                        logger.warning(f"[{symbol}] 🎯 Señal de {signal} de Alta Probabilidad detectada. Ejecución ABORTADA: Límite de {MAX_POSITIONS} operaciones alcanzado.")
                        continue
                        
                    # 🛡️ Escudo de riesgo dinámico local (Operaciones por Símbolo)
                    if RiskManager.has_open_positions(symbol, magic_number, step_distance):
                        continue
                        
                    # 🛡️ Escudo Anti-Overtrading local (Freno de 30 minutos)
                    if RiskManager.is_in_cooldown(symbol, cooldown_minutes=30):
                        continue
                        
                    # --- EJECUCIÓN DE LA ORDEN ---
                    logger.info(f"[{symbol}] 🔥 Condiciones de disparo autorizadas. Ejecutando {signal}...")
                    
                    # Ejecutar la orden en el bróker
                    result = ExecutionManager.execute_order(symbol, signal, magic_number)
                    
                    # 🛡️ ESCUDO ANTI-SPAM DEFINITIVO: Si el bróker rechaza la orden
                    if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
                        logger.warning(f"[{symbol}] ⚠️ Orden rechazada por el bróker (Posible mercado cerrado o error). Activando cuarentena anti-spam de 5 minutos.")
                        # Metemos el activo manualmente en cooldown para frenar el bucle infinito
                        RiskManager.set_cooldown(symbol, minutes=5)
                        continue
            
            except Exception as e:
                logger.error(f"Error procesando {symbol}: {e}")

        # Pausa táctica de 15 segundos por ciclo
        time.sleep(15)

def main():
    logger.info("Inicializando motores del Quant Sniper Multi-Thread Bot...")
    if not initialize_mt5():
        return

    logger.info("Conexión establecida con éxito. Desplegando hilos de trabajo...")

    # 1. Asignación de memoria en el procesador (Multithreading)
    t_forex = threading.Thread(target=market_worker, args=(FOREX_SYMBOLS, FOREX_MAGIC, FOREX_STEP, "FOREX"))
    t_metals = threading.Thread(target=market_worker, args=(METALS_SYMBOLS, METALS_MAGIC, METALS_STEP, "METALES"))
    t_crypto = threading.Thread(target=market_worker, args=(CRYPTO_SYMBOLS, CRYPTO_MAGIC, CRYPTO_STEP, "CRIPTO"))
    t_indices = threading.Thread(target=market_worker, args=(INDICES_SYMBOLS, INDICES_MAGIC, INDICES_STEP, "INDICES"))
    t_energy = threading.Thread(target=market_worker, args=(ENERGY_SYMBOLS, ENERGY_MAGIC, ENERGY_STEP, "ENERGIA"))
    t_stocks = threading.Thread(target=market_worker, args=(STOCKS_SYMBOLS, STOCKS_MAGIC, STOCKS_STEP, "ACCIONES")) # <-- NUEVO

    # 2. Ignición simultánea de la máquina completa
    t_forex.start()
    t_metals.start()
    t_crypto.start()
    t_indices.start()
    t_energy.start()
    t_stocks.start() # <-- NUEVO

if __name__ == "__main__":
    main()