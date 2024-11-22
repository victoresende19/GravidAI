"""Responsável pela lógica de Schema"""

from pydantic import BaseModel

class QuestionRequest(BaseModel):
    """
    Modelo de requisição utilizado para representar a pergunta enviada pelo usuário.

    Atributos
    ---------
    question : str
        A pergunta que o usuário deseja enviar para o processamento.
    """

    question: str

    class Config:
        """
        Modelo de requisição utilizado para representar a pergunta enviada pelo usuário.
        """

        json_schema_extra = {
            "example": {
                "question": "Quais alimentos não posso comer durante a gestação?",
            }
        }
