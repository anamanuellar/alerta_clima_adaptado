import asyncio
import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

import requests
from fastapi import HTTPException

from app.mensagens import GeradorMensagem
from app.modelos.monitoramento import (
    EventoClimatico,
    NotificacaoSimulada,
    ResultadoMonitoramento,
    ResumoMonitoramento,
    Segurado,
)
from app.regras import segurado_deve_ser_notificado


ARQUIVO_SEGURADOS = Path(__file__).parent / "dados" / "segurados.json"
URL_OPEN_METEO = "https://api.open-meteo.com/v1/forecast"


def carregar_segurados() -> list[Segurado]:
    with ARQUIVO_SEGURADOS.open(encoding="utf-8") as arquivo:
        return [Segurado.model_validate(item) for item in json.load(arquivo)]


def _severidade(valor: float, limite_alto: float, limite_extremo: float) -> str:
    if valor >= limite_extremo:
        return "extrema"
    if valor >= limite_alto:
        return "alta"
    return "moderada"


def identificar_eventos(cidade: str, dados_diarios: dict) -> list[EventoClimatico]:
    eventos: list[EventoClimatico] = []

    for valores in zip(
        dados_diarios["time"],
        dados_diarios["weather_code"],
        dados_diarios["precipitation_sum"],
        dados_diarios["precipitation_probability_max"],
        dados_diarios["wind_gusts_10m_max"],
    ):
        data_evento, codigo, chuva, probabilidade, vento = valores
        chuva = float(chuva or 0)
        probabilidade = float(probabilidade or 0)
        vento = float(vento or 0)

        if codigo in {96, 99}:
            eventos.append(
                EventoClimatico(
                    tipo="granizo",
                    titulo="Risco de tempestade com granizo",
                    cidade=cidade,
                    data=data_evento,
                    severidade="extrema" if codigo == 99 else "alta",
                    descricao="Código WMO indica tempestade acompanhada de granizo.",
                    weather_code=codigo,
                    precipitacao_mm=chuva,
                    probabilidade_chuva=probabilidade,
                    rajada_vento_kmh=vento,
                    origem="Open-Meteo",
                )
            )
        elif codigo == 95:
            eventos.append(
                EventoClimatico(
                    tipo="tempestade",
                    titulo="Risco de tempestade",
                    cidade=cidade,
                    data=data_evento,
                    severidade="alta",
                    descricao="Código WMO indica ocorrência de tempestade.",
                    weather_code=codigo,
                    precipitacao_mm=chuva,
                    probabilidade_chuva=probabilidade,
                    rajada_vento_kmh=vento,
                    origem="Open-Meteo",
                )
            )
        elif codigo in {45, 48}:
            eventos.append(
                EventoClimatico(
                    tipo="nevoeiro",
                    titulo="Risco de baixa visibilidade por nevoeiro",
                    cidade=cidade,
                    data=data_evento,
                    severidade="moderada",
                    descricao="Código WMO indica nevoeiro e redução de visibilidade.",
                    weather_code=codigo,
                    precipitacao_mm=chuva,
                    probabilidade_chuva=probabilidade,
                    rajada_vento_kmh=vento,
                    origem="Open-Meteo",
                )
            )

        if codigo in {65, 82} or chuva >= 30 or (probabilidade >= 80 and chuva >= 20):
            eventos.append(
                EventoClimatico(
                    tipo="chuva_intensa",
                    titulo="Risco de chuva intensa",
                    cidade=cidade,
                    data=data_evento,
                    severidade=_severidade(chuva, 50, 80),
                    descricao=(
                        f"Previsão de {chuva:.1f} mm de chuva, com probabilidade máxima "
                        f"de {probabilidade:.0f}%."
                    ),
                    weather_code=codigo,
                    precipitacao_mm=chuva,
                    probabilidade_chuva=probabilidade,
                    rajada_vento_kmh=vento,
                    origem="Open-Meteo",
                )
            )

        if vento >= 60:
            eventos.append(
                EventoClimatico(
                    tipo="vento_forte",
                    titulo="Risco de ventos fortes",
                    cidade=cidade,
                    data=data_evento,
                    severidade=_severidade(vento, 75, 90),
                    descricao=f"Previsão de rajadas de vento de até {vento:.1f} km/h.",
                    weather_code=codigo,
                    precipitacao_mm=chuva,
                    probabilidade_chuva=probabilidade,
                    rajada_vento_kmh=vento,
                    origem="Open-Meteo",
                )
            )

    return eventos


def _consultar_cidade(segurado: Segurado) -> list[EventoClimatico]:
    parametros = {
        "latitude": segurado.latitude,
        "longitude": segurado.longitude,
        "daily": [
            "weather_code",
            "precipitation_sum",
            "precipitation_probability_max",
            "wind_gusts_10m_max",
        ],
        "forecast_days": 3,
        "timezone": "auto",
    }

    try:
        resposta = requests.get(URL_OPEN_METEO, params=parametros, timeout=15)
        resposta.raise_for_status()
        return identificar_eventos(segurado.cidade, resposta.json()["daily"])
    except (requests.RequestException, KeyError, TypeError, ValueError) as erro:
        raise HTTPException(
            status_code=502,
            detail=f"Não foi possível consultar a previsão para {segurado.cidade}: {erro}",
        ) from erro


def _eventos_demonstrativos() -> list[EventoClimatico]:
    amanha = (date.today() + timedelta(days=1)).isoformat()
    return [
        EventoClimatico(
            tipo="chuva_intensa",
            titulo="Risco de chuva intensa",
            cidade="Salvador",
            data=amanha,
            severidade="alta",
            descricao="Cenário didático com 65 mm de chuva e risco de alagamentos.",
            weather_code=65,
            precipitacao_mm=65,
            probabilidade_chuva=90,
            rajada_vento_kmh=45,
            origem="Cenário demonstrativo",
        ),
        EventoClimatico(
            tipo="granizo",
            titulo="Risco de tempestade com granizo",
            cidade="Curitiba",
            data=amanha,
            severidade="extrema",
            descricao="Cenário didático de tempestade com granizo forte.",
            weather_code=99,
            precipitacao_mm=35,
            probabilidade_chuva=85,
            rajada_vento_kmh=72,
            origem="Cenário demonstrativo",
        ),
        EventoClimatico(
            tipo="vento_forte",
            titulo="Risco de ventos fortes",
            cidade="Recife",
            data=amanha,
            severidade="alta",
            descricao="Cenário didático com rajadas de vento de até 78 km/h.",
            weather_code=3,
            precipitacao_mm=2,
            probabilidade_chuva=30,
            rajada_vento_kmh=78,
            origem="Cenário demonstrativo",
        ),
    ]


class ServicoMonitoramento:
    async def executar(self, demonstracao: bool = False) -> ResultadoMonitoramento:
        segurados = carregar_segurados()
        cidades: dict[str, Segurado] = {}
        for segurado in segurados:
            cidades.setdefault(segurado.cidade.casefold(), segurado)

        consultas = await asyncio.gather(
            *(asyncio.to_thread(_consultar_cidade, segurado) for segurado in cidades.values())
        )
        eventos_reais = [evento for resultado in consultas for evento in resultado]
        eventos = _eventos_demonstrativos() if demonstracao else eventos_reais

        pares_elegiveis = [
            (segurado, evento)
            for evento in eventos
            for segurado in segurados
            if segurado_deve_ser_notificado(segurado, evento)
        ]

        gerador = GeradorMensagem()
        mensagens = await asyncio.gather(
            *(
                asyncio.to_thread(gerador.gerar, segurado, evento)
                for segurado, evento in pares_elegiveis
            )
        )

        agora = datetime.now(timezone.utc)
        notificacoes = [
            NotificacaoSimulada(
                id=f"NOT-{uuid4().hex[:8].upper()}",
                segurado_id=segurado.id,
                segurado=segurado.nome,
                cidade=segurado.cidade,
                tipo_seguro=segurado.tipo_seguro,
                bem_segurado=segurado.bem_segurado,
                canal=segurado.canal,
                evento=evento,
                mensagem=mensagem,
                gerada_por=origem_mensagem,
                processada_em=agora,
            )
            for (segurado, evento), (mensagem, origem_mensagem) in zip(
                pares_elegiveis, mensagens
            )
        ]

        modo = "demonstrativo" if demonstracao else "real"
        observacao = (
            "Os dados da Open-Meteo foram consultados, mas os três eventos exibidos são "
            "cenários didáticos identificados como simulados."
            if demonstracao
            else "Todos os eventos listados foram identificados automaticamente na previsão da Open-Meteo."
        )

        return ResultadoMonitoramento(
            modo=modo,
            resumo=ResumoMonitoramento(
                cidades_monitoradas=len(cidades),
                segurados_analisados=len(segurados),
                eventos_identificados=len(eventos),
                segurados_elegiveis=len({item.segurado_id for item in notificacoes}),
                notificacoes_simuladas=len(notificacoes),
            ),
            eventos=eventos,
            notificacoes=notificacoes,
            observacao=observacao,
        )
