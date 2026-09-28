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
                    "per_page": 100, # Reducimos para forzar/probar la paginación si hay muchos datos
                    "page": current_page
                }

                response = requests.get(url, params=params, timeout=30)
                response.raise_for_status()
                payload = response.json()

                if len(payload) == 2 and payload[0] is not None and payload[1] is not None:
                    # Extraer metadatos de paginación del índice 0
                    metadata = payload[0]
                    total_pages = metadata.get('pages', 1)
                    
                    # Extraer las observaciones del índice 1
                    all_data.extend(payload[1])
                else:
                    break # Salir si la respuesta no tiene el formato esperado
                
                current_page += 1
                time.sleep(0.5) # Buena práctica: no saturar la API en el ciclo while

        if not all_data:
            raise ValueError("Unexpected World Bank API response or no data found.")

        return all_data