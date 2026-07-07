import MetaTrader5 as mt5
import logging

logger = logging.getLogger(__name__)

class RiskManager:
    _manual_cooldowns = {}
    @staticmethod
    def has_open_positions(symbol: str, magic_number: int, step_distance: float) -> bool:
        """Mide el riesgo usando los parámetros dinámicos de cada hilo."""
        positions = mt5.positions_get(symbol=symbol)

        if positions is None or len(positions) == 0:
            return False

        # Filtrar posiciones que pertenezcan SOLO a este bot/mercado
        bot_positions = [p for p in positions if p.magic == magic_number]

        if len(bot_positions) >= 5:  # Máximo 5 posiciones por mercado
            return True

        if len(bot_positions) > 0:
            tick = mt5.symbol_info_tick(symbol)
            if tick is None:
                return True

            current_price = tick.ask
            last_price = bot_positions[-1].price_open

            if abs(current_price - last_price) < step_distance:
                return True  # Bloqueo por distancia corta

        return False

    @staticmethod
    def apply_trailing_stop(symbol: str, magic_number: int):
        """Módulo Institucional: Persigue el precio para asegurar ganancias y bloquear pérdidas."""
        positions = mt5.positions_get(symbol=symbol)
        if positions is None or len(positions) == 0:
            return

        # Filtrar solo las posiciones de este hilo/mercado específico
        bot_positions = [p for p in positions if p.magic == magic_number]
        if not bot_positions:
            return

        # Calibración de distancias por volatilidad de activo
        is_forex = "m" in symbol and not any(x in symbol for x in ["BTC", "ETH", "XAU", "XAG"])
        
        if is_forex:
            activation = 0.0015  # Se activa a los 15 Pips de ganancia
            distance = 0.0005    # Persigue el precio a 5 Pips de distancia
        elif "BTC" in symbol:
            activation = 100.0   # Se activa a los $100 USD de ganancia
            distance = 50.0      # Persigue el precio a $50 USD de distancia
        elif "ETH" in symbol:
            activation = 15.0    # Se activa a los $15 USD de ganancia
            distance = 5.0       # Persigue a $5 USD de distancia
        elif "XAU" in symbol:
            activation = 3.0     # Oro: Activa a $3 USD
            distance = 1.0       # Persigue a $1 USD
        else:
            activation = 15.0
            distance = 5.0

        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            return

        for pos in bot_positions:
            new_sl = pos.sl
            modified = False

            # Lógica para posiciones en COMPRA (BUY)
            if pos.type == mt5.ORDER_TYPE_BUY:
                if tick.bid - pos.price_open > activation:
                    proposed_sl = tick.bid - distance
                    if proposed_sl > pos.sl:  # Solo movemos el SL hacia arriba, nunca hacia abajo
                        new_sl = proposed_sl
                        modified = True

            # Lógica para posiciones en VENTA (SELL)
            elif pos.type == mt5.ORDER_TYPE_SELL:
                if pos.price_open - tick.ask > activation:
                    proposed_sl = tick.ask + distance
                    if proposed_sl < pos.sl or pos.sl == 0: # Movemos hacia abajo para asegurar
                        new_sl = proposed_sl
                        modified = True

            # Inyección de la modificación al broker
            if modified:
                request = {
                    "action": mt5.TRADE_ACTION_SLTP,
                    "position": pos.ticket,
                    "symbol": symbol,
                    "sl": round(new_sl, 5 if is_forex else 2),
                    "tp": pos.tp,
                    "magic": magic_number
                }
                result = mt5.order_send(request)
                if result is not None and result.retcode == mt5.TRADE_RETCODE_DONE:
                    print(f"[🛡️] Trailing Stop Activado en {symbol} | Ganancia asegurada. Nuevo SL: {new_sl}")

    @staticmethod
    def set_cooldown(symbol, minutes=5):
        from datetime import datetime, timedelta
        RiskManager._manual_cooldowns[symbol] = datetime.now() + timedelta(minutes=minutes)

    @staticmethod
    def is_in_cooldown(symbol, cooldown_minutes=30):
        from datetime import datetime, timedelta
        import MetaTrader5 as mt5
        
        now = datetime.now()
        
        if symbol in RiskManager._manual_cooldowns:
            if now < RiskManager._manual_cooldowns[symbol]:
                logger.warning(f"[COOLDOWN MANUAL] {symbol} en cuarentena anti-spam.")
                return True
            else:
                del RiskManager._manual_cooldowns[symbol]

        from_date = now - timedelta(minutes=cooldown_minutes)
        
        # Extraer todo el historial de transacciones (deals) en la ventana de tiempo
        deals = mt5.history_deals_get(from_date, now)
        
        if deals is None or len(deals) == 0:
            return False  # No hay historial reciente, el activo está frío y listo.
            
        # Filtrar si hay alguna transacción que coincida con el símbolo actual
        for deal in deals:
            if deal.symbol == symbol:
                logger.warning(f"[COOLDOWN] {symbol} bloqueado. Operación reciente detectada.")
                return True # El activo sigue caliente, abortar.
                
        return False