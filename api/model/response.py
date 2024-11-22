from pydantic import BaseModel
from typing import List

class Source(BaseModel):
    """
    Modelo para representar uma fonte de informação.
    """
    source: str
    page: int


class History(BaseModel):
    """
    Modelo para representar o histórico de interações.
    """
    human: str
    ia: str
    source: List[Source]
    datetime: str


class Metrics(BaseModel):
    """
    Modelo para representar as métricas da resposta.
    """
    tokens_used: int
    response_time: float


class QuestionResponse(BaseModel):
    """
    Modelo de resposta utilizado para representar a pergunta e a resposta gerada.

    Atributos
    ---------
    question : str
        A pergunta enviada pelo usuário.
    answer : str
        A resposta gerada para a pergunta enviada.
    prompt : str
        O prompt usado para gerar a resposta.
    source : List[Source]
        Lista de fontes utilizadas na resposta.
    history : List[History]
        Histórico de perguntas e respostas anteriores.
    metrics : Metrics
        Métricas associadas à resposta.
    """
    question: str
    answer: str
    prompt: str
    source: List[Source]
    history: List[History]
    metrics: Metrics

    class Config:
        """
        Configuração do modelo QuestionResponse, com exemplo de uso.
        """
        json_schema_extra = {
            "example": {
                "question": "Quais alimentos não posso comer durante a gestação?",
                "answer": (
                    "Durante a gestação, é importante evitar alimentos que possam causar desconfortos ou problemas "
                    "para você e seu bebê. Alguns desses alimentos incluem bebidas alcoólicas, cigarros e outras drogas. "
                    "Essas substâncias podem ser prejudiciais para o desenvolvimento fetal e para a sua saúde também. "
                    "Por isso, é recomendado manter uma alimentação saudável e diversificada, principalmente com alimentos "
                    "de origem vegetal. Assim, você estará protegendo tanto a si mesma quanto ao seu filho ou filha. "
                    "Espero que essas informações sejam úteis para você!"
                ),
                "prompt": (
                    "\n    Você é um especialista em saúde e gestação, com profundo conhecimento em obstetrícia, nutrição, "
                    "exercícios para gestantes e desenvolvimento fetal. \n    Utilize apenas o conteúdo fornecido abaixo para "
                    "responder às perguntas. \n    Não invente informações e, se não souber, diga explicitamente.\n\n    **Recuperação:**\n"
                    "    As informações relevantes sobre gestação, extraídas de fontes confiáveis, estão abaixo:\n    alimento "
                    "provocou cólicas no bebê. Evite bebidas alcoólicas, \ncigarro e outras drogas. Desta forma você estará protegendo você \n"
                    "e seu(sua) filho(a).\n\n12\nReceita para uma gravidez saudável!\nComo está sua alimentação?  Durante a gestação \n"
                    "procure ter uma alimentação saudável e diversificada, \npredominantemente de origem vegetal, rica em alimentos\n\n"
                    "    **Instrução:**\n    Responda de maneira clara, precisa e fácil de entender, adaptando o tom para uma pessoa leiga. \n"
                    "    Sua resposta deve ajudar a resolver a dúvida sem sobrecarregar com informações técnicas desnecessárias.\n\n"
                    "    **Contexto:**\n    A pergunta foi feita por uma pessoa gestante ou alguém buscando informações relacionadas à "
                    "saúde durante a gestação.\n\n    **Explicação:**\n    Inclua explicações detalhadas quando necessário, com base no "
                    "conteúdo fornecido, para ajudar o usuário a entender o motivo por trás da resposta. \n    Se o contexto fornecer links "
                    "ou referências, cite-os.\n\n    Pergunta: Quais alimentos não posso comer durante a gestação?\n"
                ),
                "source": [
                    {"source": "Caderneta da gestante.pdf", "page": 44},
                    {"source": "Caderneta da gestante.pdf", "page": 15}
                ],
                "history": [
                    {
                        "human": (
                            "\n    Você é um especialista em saúde e gestação, com profundo conhecimento em obstetrícia, nutrição, "
                            "exercícios para gestantes e desenvolvimento fetal. \n    Utilize apenas o conteúdo fornecido abaixo para "
                            "responder às perguntas. \n    Não invente informações e, se não souber, diga explicitamente.\n\n    **Recuperação:**\n"
                            "    As informações relevantes sobre gestação, extraídas de fontes confiáveis, estão abaixo:\n    alimento "
                            "provocou cólicas no bebê. Evite bebidas alcoólicas, \ncigarro e outras drogas. Desta forma você estará protegendo você \n"
                            "e seu(sua) filho(a).\n\n12\nReceita para uma gravidez saudável!\nComo está sua alimentação?  Durante a gestação \n"
                            "procure ter uma alimentação saudável e diversificada, \npredominantemente de origem vegetal, rica em alimentos\n\n"
                            "    **Instrução:**\n    Responda de maneira clara, precisa e fácil de entender, adaptando o tom para uma pessoa leiga. \n"
                            "    Sua resposta deve ajudar a resolver a dúvida sem sobrecarregar com informações técnicas desnecessárias.\n\n"
                            "    **Contexto:**\n    A pergunta foi feita por uma pessoa gestante ou alguém buscando informações relacionadas à "
                            "saúde durante a gestação.\n\n    **Explicação:**\n    Inclua explicações detalhadas quando necessário, com base no "
                            "conteúdo fornecido, para ajudar o usuário a entender o motivo por trás da resposta. \n    Se o contexto fornecer links "
                            "ou referências, cite-os.\n\n    Pergunta: Quais alimentos não posso comer durante a gestação?\n"
                        ),
                        "ia": (
                            "Durante a gestação, é importante evitar alimentos que possam causar desconfortos ou problemas "
                            "para você e seu bebê. Alguns desses alimentos incluem bebidas alcoólicas, cigarros e outras drogas. "
                            "Essas substâncias podem ser prejudiciais para o desenvolvimento fetal e para a sua saúde também. "
                            "Por isso, é recomendado manter uma alimentação saudável e diversificada, principalmente com alimentos "
                            "de origem vegetal. Assim, você estará protegendo tanto a si mesma quanto ao seu filho ou filha. "
                            "Espero que essas informações sejam úteis para você!"
                        ),
                        "source": [{"source": "Caderneta da gestante.pdf", "page": 44}],
                        "datetime": "2024-11-21T09:53:05.197941"
                    }
                ],
                "metrics": {"tokens_used": 512, "response_time": 3.459}
            }
        }
