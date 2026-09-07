import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.latlong import normalizar_cidade
from app.main import app
from app.modelos.monitoramento import EventoClimatico, Segurado
from app.monitoramento import ServicoMonitoramento, identificar_eventos
from app.regras import segurado_deve_ser_notificado


class RegrasDeNegocioTest(unittest.TestCase):
    def test_normaliza_frase_com_nome_da_cidade(self):
        self.assertEqual(normalizar_cidade("veja o clima em salvador"), "salvador")

    def test_codigo_82_e_identificado_como_chuva_intensa(self):
        dados = {
            "time": ["2026-09-08"],
            "weather_code": [82],
            "precipitation_sum": [38],
            "precipitation_probability_max": [90],
            "wind_gusts_10m_max": [42],
        }

        eventos = identificar_eventos("Salvador", dados)

        self.assertIn("chuva_intensa", {evento.tipo for evento in eventos})

    def test_rajada_acima_do_limite_gera_evento(self):
        dados = {
            "time": ["2026-09-08"],
            "weather_code": [2],
            "precipitation_sum": [0],
            "precipitation_probability_max": [10],
            "wind_gusts_10m_max": [65],
        }

        eventos = identificar_eventos("Recife", dados)

        self.assertEqual(eventos[0].tipo, "vento_forte")

    def test_regra_exige_cidade_e_seguro_compativeis(self):
        evento = EventoClimatico(
            tipo="nevoeiro",
            titulo="Nevoeiro",
            cidade="Curitiba",
            data="2026-09-08",
            severidade="moderada",
            descricao="Baixa visibilidade.",
            weather_code=45,
            precipitacao_mm=0,
            probabilidade_chuva=10,
            rajada_vento_kmh=5,
            origem="Open-Meteo",
        )
        auto_curitiba = Segurado(
            id="1",
            nome="Carlos",
            cidade="Curitiba",
            latitude=-25.4,
            longitude=-49.2,
            tipo_seguro="automovel",
            bem_segurado="veículo",
            canal="SMS",
        )
        residencial_curitiba = auto_curitiba.model_copy(
            update={"tipo_seguro": "residencial"}
        )

        self.assertTrue(segurado_deve_ser_notificado(auto_curitiba, evento))
        self.assertFalse(segurado_deve_ser_notificado(residencial_curitiba, evento))


class FluxoCompletoTest(unittest.IsolatedAsyncioTestCase):
    @patch("app.monitoramento._consultar_cidade", return_value=[])
    @patch(
        "app.monitoramento.GeradorMensagem.gerar",
        return_value=("Mensagem preventiva personalizada.", "IA"),
    )
    async def test_cenario_demonstrativo_percorre_fluxo_completo(
        self, _gerar_mensagem, _consultar
    ):
        resultado = await ServicoMonitoramento().executar(demonstracao=True)

        self.assertEqual(resultado.modo, "demonstrativo")
        self.assertEqual(resultado.resumo.eventos_identificados, 3)
        self.assertEqual(resultado.resumo.notificacoes_simuladas, 3)
        self.assertTrue(
            all(item.status == "Envio simulado com sucesso" for item in resultado.notificacoes)
        )


class EndpointsSemLLMTest(unittest.TestCase):
    def test_dicas_e_cidades_nao_dependem_de_chave_de_ia(self):
        with TestClient(app) as client:
            dicas = client.get("/api/v1/tips")
            cidades = client.get("/api/v1/cities")

        self.assertEqual(dicas.status_code, 200)
        self.assertEqual(cidades.status_code, 200)
        self.assertEqual(len(dicas.json()["rain"]), 3)
        self.assertEqual(len(cidades.json()), 14)


if __name__ == "__main__":
    unittest.main()
