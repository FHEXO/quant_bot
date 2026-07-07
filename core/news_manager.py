import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import dateutil.parser

class NewsManager:
    def __init__(self, pause_minutes=30):
        self.url = "https://nfs.forexfactory.com/ffcal/news/calendar.xml"
        self.pause_minutes = pause_minutes

    def is_market_dangerous(self) -> bool:
        """Determina si hay noticias, con tolerancia a fallas de conexión."""
        try:
            # Forzar headers de navegador comercial de última generación
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            req = urllib.request.Request(self.url, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as response:
                xml_data = response.read()
            
            root = ET.fromstring(xml_data)
            now_utc = datetime.utcnow()

            for event in root.findall('event'):
                impact = event.find('impact').text
                if impact != 'High':
                    continue

                date_str = event.find('date').text
                time_str = event.find('time').text
                
                full_date_str = f"{date_str} {time_str}"
                event_time_utc = dateutil.parser.parse(full_date_str).replace(tzinfo=None)

                start_block = event_time_utc - timedelta(minutes=self.pause_minutes)
                end_block = event_time_utc + timedelta(minutes=self.pause_minutes)

                if start_block <= now_utc <= end_block:
                    return True

            return False
        except Exception as e:
            # CONTINGENCIA: Si el servidor web falla, se loguea pero NO se congela el bot
            print(f"[⚠️] Servidor de noticias inaccesible. Modo de respaldo activado: Continuando operaciones...")
            return False