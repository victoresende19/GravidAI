"""Responsável pela lógica de Schema"""

from pydantic import BaseModel

class EmbeddingResponse(BaseModel):
    """
    Modelo de resposta utilizado para representar a mensagem de embedding gerada.

    Atributos
    ---------
    message : str
        A mensagem de embedding retornada pelo processamento.
    """

    message: str

    class Config:
        """
        Configuração do modelo EmbeddingResponse, com exemplo de uso.
        """

        json_schema_extra = {
            "example": {
                "message": "Embedding gerado com sucesso.",
            }
        }
