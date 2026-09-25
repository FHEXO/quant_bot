import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

# Cargar el archivo secreto de credenciales (.env)
load_dotenv()

# Conexión Segura con Exness (Nivel de infraestructura)
ACCOUNT_ID = int(os.getenv("EXNESS_ACCOUNT_ID", "0"))
ACCOUNT_PASSWORD = os.getenv("EXNESS_PASSWORD", "")
ACCOUNT_SERVER = os.getenv("EXNESS_SERVER", "Exness-MT5Trial11")

# --- CONFIGURACIÓN DE MERCADOS CENTRALIZADA ---

# 1. Módulo Forex Majors (Sufijo Exness Standard)
FOREX_SYMBOLS = [
    "EURUSDm", "GBPUSDm", "USDJPYm", "AUDUSDm", 
    "NZDUSDm", "USDCADm", "USDCHFm"
]
FOREX_MAGIC = 1000
FOREX_STEP = 0.0010  # Distancia en Pips

# 2. Módulo Metales y Materiales Industriales (Sufijo Exness Standard)
METALS_SYMBOLS = [
    "XAUUSDm", "XAUAUDm", "XAUEURm", "XAUGBPm",  # Complejo de Oro
    "XAGUSDm", "XAGAUDm", "XAGEURm", "XAGGBPm",  # Complejo de Plata
    "XALUSDm",  # Aluminio vs US Dollar
    "XCUUSDm",  # Cobre vs US Dollar
    "XNIUSDm",  # Níquel vs US Dollar
    "XPBUSDm",  # Plomo vs US Dollar
    "XPDUSDm",  # Paladio vs US Dollar
    "XPTUSDm",  # Platino vs US Dollar
    "XZNUSDm"   # Zinc vs US Dollar
]
METALS_MAGIC = 3000
METALS_STEP = 2.0  # Distancia de seguridad adaptada en Dólares

# 3. Módulo Criptoactivos
CRYPTO_SYMBOLS = ["BTCUSDm", "ETHUSDm"]
CRYPTO_MAGIC = 2000
CRYPTO_STEP = 15.0   # Distancia en Dólares

# 4. Módulo Índices Bursátiles (Con sufijo Exness Standard)
INDICES_SYMBOLS = [
    "AUS200m", "DE30m", "DXYm", "FR40m", "HK50m", "JP225m", 
    "STOXX50m", "UK100m", "US30(x10)m", "US30m", 
    "US500(x100)m", "US500m", "USTEC(x100)m", "USTECm"
]
INDICES_MAGIC = 4000
INDICES_STEP = 15.0  

# 5. Módulo Energía (Con sufijo Exness Standard)
ENERGY_SYMBOLS = ["USOILm", "UKOILm", "XNGUSDm"]
ENERGY_MAGIC = 5000
ENERGY_STEP = 0.50  

# 6. Módulo Acciones (Wall Street & Global Stocks)
STOCKS_SYMBOLS = [
    "AAPLm", "ABBVm", "ABTm", "ADBEm", "ADPm", "AMDm", "AMGNm", "AMTm", "AMZNm", "ATVIm",
    "AVGOm", "BABAm", "BACm", "BAm", "BEKEm", "BIDUm", "BIIBm", "BILIm", "BMYm", "CHTRm",
    "CMCSAm", "CMEm", "COSTm", "CSCOm", "CSXm", "CVSm", "Cm", "EBAYm", "EDUm", "EQIXm",
    "FBm", "FTNTm", "FUTUm", "Fm", "GILDm", "HDm", "IBMm", "INTCm", "INTUm", "ISRGm",
    "JDm", "JNJm", "JPMm", "KOm", "LINm", "LIm", "LLYm", "LMTm", "MAm", "MCDm",
    "MDLZm", "METAm", "MMMm", "MOm", "MRKm", "MSFTm", "MSm", "NFLXm", "NIOm", "NKEm",
    "NTESm", "NVDAm", "ORCLm", "PDDm", "PEPm", "PFEm", "PGm", "PMm", "PYPLm", "REGNm",
    "SBUXm", "SPCXm", "TALm", "TMEm", "TMOm", "TMUSm", "TSLAm", "TSMm", "Tm", "UNHm",
    "UPSm", "VIPSm", "VRTXm", "VZm", "Vm", "WFCm", "WMTm", "XOMm", "XPEVm", "YUMCm", "ZTOm"
]
STOCKS_MAGIC = 6000
STOCKS_STEP = 1.0  # Escudo de rastreo: 1 dólar de movimiento a tu favor

# --- DICCIONARIO DE VOLÚMENES CALIBRADOS ---
# Registramos estrictamente cada activo con la "m" para que el ExecutionManager no falle
# NOTA: Para materiales exóticos e industriales, el lote se clava en 0.01 para cuidar el margen.
SYMBOL_LOTS = {
    # Forex Majors
    "EURUSDm": 0.01, "GBPUSDm": 0.01, "USDJPYm": 0.01, "AUDUSDm": 0.01,
    "NZDUSDm": 0.01, "USDCADm": 0.01, "USDCHFm": 0.01,
    # Cripto
    "BTCUSDm": 0.01, "ETHUSDm": 0.1,
    # Nuevos Índices Globales y Apalancados
    "AUS200m": 0.01, "DE30m": 0.01, "DXYm": 0.01, "FR40m": 0.01, 
    "HK50m": 0.1, "JP225m": 0.1, "STOXX50m": 0.01, "UK100m": 0.01, 
    "US30(x10)m": 0.01, "US30m": 0.1, "US500(x100)m": 0.01, 
    "US500m": 0.1, "USTEC(x100)m": 0.01, "USTECm": 0.1,
    # Energía
    "USOILm": 0.01, "UKOILm": 0.01, "XNGUSDm": 0.01,
    # Metales y Materiales Industriales
    "XAUUSDm": 0.01, "XAUAUDm": 0.01, "XAUEURm": 0.01, "XAUGBPm": 0.01,
    "XAGUSDm": 0.01, "XAGAUDm": 0.01, "XAGEURm": 0.01, "XAGGBPm": 0.01,
    "XALUSDm": 0.01, "XCUUSDm": 0.01, "XNIUSDm": 0.01, "XPBUSDm": 0.01,
    "XPDUSDm": 0.01, "XPTUSDm": 0.01, "XZNUSDm": 0.01,

    # Acciones Globales (Lote mínimo estricto por alto requerimiento de margen)
    "AAPLm": 0.01, "ABBVm": 0.01, "ABTm": 0.01, "ADBEm": 0.01, "ADPm": 0.01, "AMDm": 0.01,
    "AMGNm": 0.01, "AMTm": 0.01, "AMZNm": 0.01, "ATVIm": 0.01, "AVGOm": 0.01, "BABAm": 0.01,
    "BACm": 0.01, "BAm": 0.01, "BEKEm": 0.01, "BIDUm": 0.01, "BIIBm": 0.01, "BILIm": 0.01,
    "BMYm": 0.01, "CHTRm": 0.01, "CMCSAm": 0.01, "CMEm": 0.01, "COSTm": 0.01, "CSCOm": 0.01,
    "CSXm": 0.01, "CVSm": 0.01, "Cm": 0.01, "EBAYm": 0.01, "EDUm": 0.01, "EQIXm": 0.01,
    "FBm": 0.01, "FTNTm": 0.01, "FUTUm": 0.01, "Fm": 0.01, "GILDm": 0.01, "HDm": 0.01,
    "IBMm": 0.01, "INTCm": 0.01, "INTUm": 0.01, "ISRGm": 0.01, "JDm": 0.01, "JNJm": 0.01,
    "JPMm": 0.01, "KOm": 0.01, "LINm": 0.01, "LIm": 0.01, "LLYm": 0.01, "LMTm": 0.01,
    "MAm": 0.01, "MCDm": 0.01, "MDLZm": 0.01, "METAm": 0.01, "MMMm": 0.01, "MOm": 0.01,
    "MRKm": 0.01, "MSFTm": 0.01, "MSm": 0.01, "NFLXm": 0.01, "NIOm": 0.01, "NKEm": 0.01,
    "NTESm": 0.01, "NVDAm": 0.01, "ORCLm": 0.01, "PDDm": 0.01, "PEPm": 0.01, "PFEm": 0.01,
    "PGm": 0.01, "PMm": 0.01, "PYPLm": 0.01, "REGNm": 0.01, "SBUXm": 0.01, "SPCXm": 0.01,
    "TALm": 0.01, "TMEm": 0.01, "TMOm": 0.01, "TMUSm": 0.01, "TSLAm": 0.01, "TSMm": 0.01,
    "Tm": 0.01, "UNHm": 0.01, "UPSm": 0.01, "VIPSm": 0.01, "VRTXm": 0.01, "VZm": 0.01,
    "Vm": 0.01, "WFCm": 0.01, "WMTm": 0.01, "XOMm": 0.01, "XPEVm": 0.01, "YUMCm": 0.01, "ZTOm": 0.01
}

# Parámetros Técnicos Universales
EMA_PERIOD = 200
RSI_PERIOD = 14
RSI_OVERBOUGHT = 80  # Nivel Institucional Extremo: Rechaza mercados locos
RSI_OVERSOLD = 20    # Nivel Institucional Extremo: Solo compra si hay pánico total

# --- PARÁMETROS GLOBALES Y DE CONTINGENCIA ---
NEWS_PAUSE_MINUTES = 30
MICRO_TIMEFRAME = "M1"
MAX_POSITIONS = 5

# Símbolos activos escaneados por el bot
SYMBOLS = FOREX_SYMBOLS + METALS_SYMBOLS + CRYPTO_SYMBOLS + INDICES_SYMBOLS + ENERGY_SYMBOLS + STOCKS_SYMBOLS

# Helper dinámico para resolver parámetros por activo
def get_symbol_config(symbol: str) -> dict:
    if symbol in FOREX_SYMBOLS:
        return {
            "magic": FOREX_MAGIC,
            "step": FOREX_STEP,
            "sl": 0.0015,  # Stop Loss a 15 pips
            "tp": 0.0030   # Take Profit a 30 pips
        }
    elif symbol in METALS_SYMBOLS:
        if "XAU" in symbol: # Aplica para todo el complejo de Oro (XAUUSDm, XAUEURm, etc)
            return {
                "magic": METALS_MAGIC,
                "step": METALS_STEP,
                "sl": 3.0,   # Stop Loss a 3.0 USD
                "tp": 6.0    # Take Profit a 6.0 USD
            }
        elif "XAG" in symbol: # Aplica para todo el complejo de Plata
            return {
                "magic": METALS_MAGIC,
                "step": METALS_STEP,
                "sl": 0.3,   # Stop Loss a 0.3 USD en Plata
                "tp": 0.6    # Take Profit a 0.6 USD en Plata
            }
        else: # Materiales Industriales (Platino, Paladio, Cobre, etc.)
            return {
                "magic": METALS_MAGIC,
                "step": METALS_STEP,
                "sl": 5.0,   # SL más amplio por volatilidad de materiales pesados
                "tp": 10.0   
            }
    elif symbol in CRYPTO_SYMBOLS:
        return {
            "magic": CRYPTO_MAGIC,
            "step": CRYPTO_STEP,
            "sl": 15.0,    # Stop Loss a 15.0 USD
            "tp": 30.0     # Take Profit a 30.0 USD
        }
    elif symbol in INDICES_SYMBOLS:
        return {
            "magic": INDICES_MAGIC,
            "step": INDICES_STEP,
            "sl": 15.0,
            "tp": 30.0
        }
    elif symbol in ENERGY_SYMBOLS:
        return {
            "magic": ENERGY_MAGIC,
            "step": ENERGY_STEP,
            "sl": 0.50,
            "tp": 1.00
        }
    elif symbol in STOCKS_SYMBOLS:
        return {
            "magic": STOCKS_MAGIC,
            "step": STOCKS_STEP,
            "sl": 5.0,   # Stop Loss a $5 USD de movimiento de la acción
            "tp": 10.0   # Take Profit a $10 USD
        }
    # Respaldo genérico
    return {
        "magic": 9999,
        "step": 0.01,
        "sl": 0.01,
        "tp": 0.02
    }
