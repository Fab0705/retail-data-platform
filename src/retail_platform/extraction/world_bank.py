from __future__ import annotations

import requests
from typing import Any


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
        indicator_param = ";".join(indicators)

        url = (
            f"{self.base_url}/country/"
            f"{country_param}/indicator/"
            f"{indicator_param}"
        )

        params = {
            "date": f"{start_year}:{end_year}",
            "format": "json",
            "per_page": 1000,
        }

        response = requests.get(
            url,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        payload = response.json()

        if len(payload) < 2:
            raise ValueError("Unexpected World Bank API response.")

        return payload[1]