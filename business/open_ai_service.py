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
            Você é um analista inteligente de transporte.

            Analise os dados abaixo de uma rota de transporte universitário.

            Identifique:
            - padrões
            - tendências
            - possíveis problemas recorrentes
            - estabilidade da rota

            Gere uma descrição:
            - profissional
            - amigável
            - curta
            - objetiva

            Dados:
            {route_content.model_dump_json(indent=2)}
            """
        ).output_text