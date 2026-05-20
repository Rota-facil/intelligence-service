from openai import OpenAI
from http_routes.dto.route_data_request_dto import RouteContentRequestDTO
import os

OPEN_AI_API_KEY = os.environ.get("OPEN_AI_API_KEY", 'your_api_key')
client = OpenAI(
    api_key=OPEN_AI_API_KEY
)


class OpenAIService:
    def generate_route_interpretation(self, route_content: RouteContentRequestDTO):
        return client.responses.create(
            model="gpt-4.1-nano",
            input=f"""
            Você é a inteligência analítica do sistema Rota Fácil.

            Analise os dados históricos da rota e gere uma interpretação operacional inteligente.

            Sua análise deve:
            - usar métricas proporcionais e percentuais sempre que possível
            - identificar frequência de atrasos, cancelamentos e pontualidade
            - detectar tendências de crescimento ou redução de problemas
            - identificar padrões recorrentes
            - inferir possíveis comportamentos futuros da rota
            - justificar as conclusões com base nos dados

            Importante:
            - seja direto e objetivo
            - máximo de 2 parágrafos
            - evite repetir informações
            - não invente dados inexistentes
            - não explique funcionalidades do sistema
            - fale como uma IA interna do Rota Fácil
            - priorize insights operacionais relevantes

            Exemplos esperados:
            - "35% das viagens apresentaram atraso"
            - "houve aumento na recorrência de atrasos"
            - "a pontualidade permaneceu estável"
            - "cancelamentos representam baixa recorrência operacional"

            Dados:
            {route_content.model_dump_json(indent=2)}
            """
        ).output_text