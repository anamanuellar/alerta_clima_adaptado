from copy import deepcopy
from typing import List

from app.modelos.tipsandcities import City, Tips


TIPS = {
    "temp": [
        "Mudanças bruscas de temperatura pedem atenção especial com crianças e idosos.",
        "Consulte a amplitude térmica antes de sair e leve uma camada extra de roupa.",
        "Proteja animais de estimação em períodos de calor ou frio intenso.",
    ],
    "tempest": [
        "Durante tempestades, permaneça em local protegido e longe de áreas abertas.",
        "Retire aparelhos sensíveis das tomadas quando houver risco de descargas elétricas.",
        "Evite se abrigar sob árvores, postes ou estruturas metálicas durante tempestades.",
    ],
    "rain": [
        "Antes de chuva forte, verifique ralos, calhas e pontos de entrada de água.",
        "Evite atravessar áreas alagadas, mesmo quando a profundidade parecer pequena.",
        "Mantenha documentos e objetos importantes protegidos da umidade.",
    ],
    "wind": [
        "Recolha vasos e objetos soltos de varandas quando houver previsão de ventos fortes.",
        "Evite estacionar veículos próximos a árvores, placas e estruturas frágeis.",
        "Mantenha portas e janelas fechadas durante rajadas intensas.",
    ],
    "humidity": [
        "Em baixa umidade, hidrate-se e evite exercícios nos horários mais quentes.",
        "Alta umidade favorece mofo; mantenha os ambientes ventilados quando for seguro.",
        "Acompanhe a umidade do ar para ajustar hidratação e cuidados respiratórios.",
    ],
    "uv": [
        "Use protetor solar mesmo em dias nublados quando o índice UV estiver elevado.",
        "Prefira sombra e proteção física entre 10h e 16h.",
        "Chapéu, roupas adequadas e óculos com proteção UV ajudam a reduzir a exposição.",
    ],
    "eye": [
        "Óculos com proteção UV ajudam a proteger os olhos em dias de radiação intensa.",
        "Em tempo seco, faça pausas de telas e mantenha os olhos hidratados.",
        "Evite coçar os olhos quando houver poeira ou baixa umidade.",
    ],
    "fog": [
        "Sob nevoeiro, dirija devagar, use farol baixo e aumente a distância de segurança.",
        "Evite ultrapassagens quando a visibilidade estiver reduzida.",
        "Não use farol alto no nevoeiro, pois o reflexo pode piorar a visibilidade.",
    ],
    "cold": [
        "No frio, proteja principalmente extremidades e mantenha roupas secas.",
        "Verifique aquecedores e nunca utilize equipamentos a combustão sem ventilação.",
        "Pessoas vulneráveis precisam de atenção especial durante quedas de temperatura.",
    ],
    "flood": [
        "Conheça rotas seguras e pontos elevados próximos à sua residência ou trabalho.",
        "Nunca caminhe ou dirija em correntezas e áreas inundadas.",
        "Em área de risco, mantenha documentos e itens essenciais prontos para evacuação.",
    ],
}


CITIES: List[City] = [
    {"city": "Salvador", "badge": "BA", "type": "brasileira"},
    {"city": "São Paulo", "badge": "SP", "type": "brasileira"},
    {"city": "Rio de Janeiro", "badge": "RJ", "type": "brasileira"},
    {"city": "Curitiba", "badge": "PR", "type": "brasileira"},
    {"city": "Recife", "badge": "PE", "type": "brasileira"},
    {"city": "Fortaleza", "badge": "CE", "type": "brasileira"},
    {"city": "Belo Horizonte", "badge": "MG", "type": "brasileira"},
    {"city": "Porto Alegre", "badge": "RS", "type": "brasileira"},
    {"city": "Lisboa", "badge": "PT", "type": "global"},
    {"city": "Londres", "badge": "GB", "type": "global"},
    {"city": "Nova York", "badge": "US", "type": "global"},
    {"city": "Tóquio", "badge": "JP", "type": "global"},
    {"city": "Sydney", "badge": "AU", "type": "global"},
    {"city": "Buenos Aires", "badge": "AR", "type": "global"},
]


class TipsandCities:
    """Catálogo confiável para conteúdos que não exigem IA Generativa."""

    def getCities(self) -> List[City]:
        return deepcopy(CITIES)

    def getTips(self) -> Tips:
        return Tips.model_validate(deepcopy(TIPS))
