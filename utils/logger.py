import os
from datetime import datetime

class QuantLogger:
    def __init__(self, log_dir="logs"):
        self.log_path = os.path.join(log_dir, "quant_bot.log")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

    def log(self, message: str):
        """Escribe un mensaje formateado con fecha y hora en el archivo físico de log."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        
        # Imprimir en consola para monitoreo visual rápido
        print(formatted_message)
        
        # Guardar permanentemente en disco duro
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(formatted_message + "\n")