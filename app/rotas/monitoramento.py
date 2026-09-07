from fastapi import APIRouter, Query

from app.modelos.monitoramento import ResultadoMonitoramento, Segurado
from app.monitoramento import ServicoMonitoramento, carregar_segurados


router = APIRouter(prefix="/api/v1", tags=["Monitoramento preventivo"])


@router.get(
    "/insureds",
    response_model=list[Segurado],
    summary="Listar os segurados fictícios usados pelo protótipo",
)
async def listar_segurados() -> list[Segurado]:
    return carregar_segurados()


@router.post(
    "/monitoring/run",
    response_model=ResultadoMonitoramento,
    summary="Executar o fluxo preventivo completo",
    description=(
        "Consulta a Open-Meteo, identifica eventos, aplica regras de negócio, seleciona "
        "segurados, gera mensagens personalizadas e simula o envio. Use demonstracao=true "
        "para apresentar o fluxo mesmo quando não houver risco na previsão real."
    ),
)
async def executar_monitoramento(
    demonstracao: bool = Query(default=False),
) -> ResultadoMonitoramento:
    return await ServicoMonitoramento().executar(demonstracao=demonstracao)
