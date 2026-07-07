import MetaTrader5 as mt5
from config.settings import SYMBOL_LOTS

class ExecutionManager:
    @staticmethod
    def execute_order(symbol: str, order_type: str, magic_number: int) -> bool:
        """Inyecta órdenes con Stop Loss y Take Profit calibrados por la volatilidad del activo."""
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            return False

        volume = SYMBOL_LOTS.get(symbol, 0.01)
        price = tick.ask if order_type == "BUY" else tick.bid
        type_action = mt5.ORDER_TYPE_BUY if order_type == "BUY" else mt5.ORDER_TYPE_SELL

        # Lógica central de escalado de riesgo corregida
        is_forex = "m" in symbol and not any(x in symbol for x in ["BTC", "ETH", "XAU", "XAG"])
        
        if is_forex:
            sl_dist = 0.0015  # 15 Pips
            tp_dist = 0.0030  # 30 Pips
        elif "BTC" in symbol:
            sl_dist = 150.0   
            tp_dist = 300.0   
        elif "ETH" in symbol:
            sl_dist = 15.0    
            tp_dist = 30.0
        elif "XAU" in symbol:
            sl_dist = 3.0     # $3 USD para el Oro
            tp_dist = 6.0
        elif "XAG" in symbol:
            sl_dist = 0.50    # Plata: Stop Loss ajustado a 50 centavos de dólar
            tp_dist = 1.50    # Plata: Take Profit ajustado a 1.50 dólares
        else:
            sl_dist = 15.0
            tp_dist = 30.0

        if order_type == "BUY":
            sl = price - sl_dist
            tp = price + tp_dist
        else:
            sl = price + sl_dist
            tp = price - tp_dist

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": type_action,
            "price": price,
            "sl": round(sl, 5 if is_forex else 2),
            "tp": round(tp, 5 if is_forex else 2),
            "deviation": 10,
            "magic": magic_number,
            "comment": f"Sniper {magic_number}",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(request)
        if result is not None and result.retcode == mt5.TRADE_RETCODE_DONE:
            print(f"[🔥] ¡ORDEN EJECUTADA! {order_type} en {symbol} | Hilo: {magic_number}")
        
        return result
