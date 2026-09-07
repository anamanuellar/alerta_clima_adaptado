from app.modelos.monitoramento import EventoClimatico, Segurado


TIPOS_DE_SEGURO_POR_EVENTO = {
    "chuva_intensa": {"residencial", "rural", "empresarial"},
    "granizo": {"automovel", "residencial", "rural", "empresarial"},
    "vento_forte": {"residencial", "automovel", "rural", "empresarial"},
    "nevoeiro": {"automovel"},
    "tempestade": {"residencial", "automovel", "rural", "empresarial"},
}


def segurado_deve_ser_notificado(segurado: Segurado, evento: EventoClimatico) -> bool:
    """Aplica as regras de negócio de localização e compatibilidade da cobertura."""
    tipos_elegiveis = TIPOS_DE_SEGURO_POR_EVENTO.get(evento.tipo, set())
    return (
        segurado.cidade.casefold() == evento.cidade.casefold()
        and segurado.tipo_seguro in tipos_elegiveis
    )


def explicar_regra(evento: EventoClimatico) -> str:
    tipos = sorted(TIPOS_DE_SEGURO_POR_EVENTO.get(evento.tipo, set()))
    return f"Evento {evento.tipo}: notificar seguros {', '.join(tipos)} na cidade afetada."
