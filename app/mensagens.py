from functools import lru_cache

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from app.llm import LLM
from app.modelos.monitoramento import EventoClimatico, Segurado


@lru_cache
def get_llm():
    return LLM().getLLM()


def mensagem_de_contingencia(segurado: Segurado, evento: EventoClimatico) -> str:
    recomendacoes = {
        "chuva_intensa": "proteja objetos próximos a áreas externas, verifique ralos e evite regiões alagadas",
        "granizo": "mantenha o veículo ou os bens protegidos em local coberto e evite deslocamentos durante o evento",
        "vento_forte": "recolha objetos soltos, mantenha distância de árvores e estruturas frágeis e permaneça em local seguro",
        "nevoeiro": "se precisar dirigir, reduza a velocidade, aumente a distância do veículo à frente e use farol baixo",
        "tempestade": "permaneça em local protegido, retire aparelhos sensíveis das tomadas e evite áreas abertas",
    }
    acao = recomendacoes[evento.tipo]
    return (
        f"Olá, {segurado.nome}. Identificamos {evento.titulo.lower()} em {evento.cidade}, "
        f"prevista para {evento.data}. Como você possui seguro {segurado.tipo_seguro} para "
        f"{segurado.bem_segurado}, recomendamos que {acao}. Esta é uma comunicação preventiva "
        "e não substitui os alertas das autoridades locais."
    )


class GeradorMensagem:
    def gerar(self, segurado: Segurado, evento: EventoClimatico) -> tuple[str, str]:
        template = """
Você é um agente de comunicação preventiva de uma seguradora brasileira.
Escreva uma mensagem curta, clara, empática e acionável em Português do Brasil.

Segurado: {nome}
Cidade: {cidade}
Seguro: {tipo_seguro}
Bem segurado: {bem_segurado}
Evento: {evento}
Data prevista: {data}
Severidade: {severidade}
Descrição técnica: {descricao}

Regras:
- Comece com "Olá, {nome}."
- Explique o risco sem alarmismo.
- Dê de duas a três orientações adequadas ao seguro e ao bem protegido.
- Informe que é uma comunicação preventiva e que alertas oficiais devem ser seguidos.
- Não prometa cobertura, indenização ou garantia contratual.
- Retorne somente a mensagem final, sem título e sem Markdown.
"""
        try:
            prompt = PromptTemplate.from_template(template)
            chain = prompt | get_llm() | StrOutputParser()
            mensagem = chain.invoke(
                {
                    "nome": segurado.nome,
                    "cidade": evento.cidade,
                    "tipo_seguro": segurado.tipo_seguro,
                    "bem_segurado": segurado.bem_segurado,
                    "evento": evento.titulo,
                    "data": evento.data,
                    "severidade": evento.severidade,
                    "descricao": evento.descricao,
                }
            ).strip()
            if mensagem:
                return mensagem, "IA"
        except Exception:
            pass

        return mensagem_de_contingencia(segurado, evento), "modelo de contingência"
