from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class Segurado(BaseModel):
    id: str
    nome: str
    cidade: str
    latitude: float
    longitude: float
    tipo_seguro: Literal["residencial", "automovel", "rural", "empresarial"]
    bem_segurado: str
    canal: Literal["WhatsApp", "SMS", "E-mail", "Push"]


class EventoClimatico(BaseModel):
    tipo: Literal["chuva_intensa", "granizo", "vento_forte", "nevoeiro", "tempestade"]
    titulo: str
    cidade: str
    data: str
    severidade: Literal["moderada", "alta", "extrema"]
    descricao: str
    weather_code: int
    precipitacao_mm: float
    probabilidade_chuva: float
    rajada_vento_kmh: float
    origem: Literal["Open-Meteo", "Cenário demonstrativo"]


class NotificacaoSimulada(BaseModel):
    id: str
    segurado_id: str
    segurado: str
    cidade: str
    tipo_seguro: str
    bem_segurado: str
    canal: str
    evento: EventoClimatico
    mensagem: str
    gerada_por: Literal["IA", "modelo de contingência"]
    status: Literal["Envio simulado com sucesso"] = "Envio simulado com sucesso"
    processada_em: datetime


class ResumoMonitoramento(BaseModel):
    cidades_monitoradas: int
    segurados_analisados: int
    eventos_identificados: int
    segurados_elegiveis: int
    notificacoes_simuladas: int


class ResultadoMonitoramento(BaseModel):
    modo: Literal["real", "demonstrativo"]
    fonte_meteorologica: str = "Open-Meteo"
    resumo: ResumoMonitoramento
    eventos: list[EventoClimatico]
    notificacoes: list[NotificacaoSimulada]
    observacao: str = Field(
        description="Explica se os resultados vieram da previsão real ou de cenário demonstrativo."
    )
