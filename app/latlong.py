import re

import requests
from fastapi import HTTPException


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"


def normalizar_cidade(texto: str) -> str:
    """Aceita tanto o nome isolado quanto frases simples em Português."""
    cidade = " ".join(texto.strip().split())
    if not cidade:
        raise HTTPException(status_code=422, detail="Informe o nome de uma cidade.")

    padroes = [
        r"^(?:veja|ver|mostre|mostrar|consulte|consultar)\s+(?:(?:a|o)\s+)?(?:previsão(?:\s+do\s+tempo)?|clima|tempo)\s+(?:em|de|para)\s+(.+)$",
        r"^(?:qual\s+(?:é|e)\s+)?(?:(?:a|o)\s+)?(?:previsão(?:\s+do\s+tempo)?|clima|tempo)\s+(?:em|de|para)\s+(.+)$",
    ]
    for padrao in padroes:
        resultado = re.match(padrao, cidade, flags=re.IGNORECASE)
        if resultado:
            cidade = resultado.group(1).strip()
            break

    return cidade


class LatLong:
    """Obtém coordenadas na API oficial de geocodificação da Open-Meteo."""

    def getLatLong(self, city: str):
        cidade = normalizar_cidade(city)
        try:
            resposta = requests.get(
                GEOCODING_URL,
                params={"name": cidade, "count": 1, "language": "pt", "format": "json"},
                timeout=10,
            )
            resposta.raise_for_status()
            resultados = resposta.json().get("results", [])
        except (requests.RequestException, TypeError, ValueError) as erro:
            raise HTTPException(
                status_code=502,
                detail="Não foi possível consultar a localização. Tente novamente.",
            ) from erro

        if not resultados:
            raise HTTPException(
                status_code=404,
                detail=f"Cidade não encontrada: {cidade}.",
            )

        resultado = resultados[0]
        return {
            "cidade": resultado.get("name", cidade),
            "latitude": float(resultado["latitude"]),
            "longitude": float(resultado["longitude"]),
            "timezone": resultado.get("timezone", "auto"),
        }
