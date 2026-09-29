from __future__ import annotations
import requests
from typing import Any
import time

class WorldBankClient:
    def __init__(self, base_url: str = "https://api.worldbank.org/v2"):
        self.base_url = base_url.rstrip("/")

    def get_indicators(
        self,
        countries: list[str],
        indicators: list[str],
        start_year: int,
        end_year: int,
    ) -> list[dict[str, Any]]:

        country_param = ";".join(countries)
        all_data = []

        for indicator in indicators:
            url = f"{self.base_url}/country/{country_param}/indicator/{indicator}"
            
            # FASE 10: Implementar paginación explícita
            current_page = 1
            total_pages = 1
            
            while current_page <= total_pages:
                params = {
                    "date": f"{start_year}:{end_year}",
                    "format": "json",
                    "per_page": 100, 
                    "page": current_page
                }

                # --- NUEVO: Sistema de reintentos automáticos ---
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        # Aumentamos el timeout a 60 segundos
                        response = requests.get(url, params=params, timeout=60)
                        response.raise_for_status()
                        break # Si la petición es exitosa, rompemos el ciclo de reintentos
                    except requests.exceptions.RequestException as e:
                        if attempt < max_retries - 1:
                            print(f"      [!] Demora en la red. Reintentando ({attempt + 1}/{max_retries}) en 5 segundos...")
                            time.sleep(5)
                        else:
                            raise ValueError(f"Fallo crítico al conectar con la API tras {max_retries} intentos: {e}")
                # ------------------------------------------------

                payload = response.json()

                if len(payload) == 2 and payload[0] is not None and payload[1] is not None:
                    metadata = payload[0]
                    total_pages = metadata.get('pages', 1)
                    all_data.extend(payload[1])
                else:
                    break 
                
                current_page += 1
                time.sleep(0.5)

        if not all_data:
            raise ValueError("Unexpected World Bank API response or no data found.")

        return all_data