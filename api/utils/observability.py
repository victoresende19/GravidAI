"""Observabilidade"""

from langsmith.client import Client as LangSmithClient
import os

client = LangSmithClient(api_key=os.getenv("LANGSMITH_API_KEY"))

def log_observability(prompt, answer, tokens_used, response_time):
    """
    Registra informações de uso para análise de observabilidade.

    Parâmetros
    ----------
    prompt : str
        O prompt enviado ao modelo.
    answer : str
        A resposta gerada pelo modelo.
    tokens_used : int
        O número de tokens utilizados na interação.
    response_time : float
        O tempo de resposta em segundos.
    """
    # Cria um trace (registro detalhado de execução) no LangSmith
    client.create_trace(
        name="Interaction Trace",
        inputs={
            "prompt": prompt
        },
        outputs={
            "response": answer
        },
        metadata={
            "tokens_used": tokens_used,
            "response_time": response_time
        }
    )
    print(f"Observabilidade registrada: tokens={tokens_used}, tempo={response_time:.2f}s")
