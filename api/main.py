"""Responsável pelos endpoints"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from service.answer_service import ask_question
from service.embedding_service import create_embedding_mongodb
from model.embedding import EmbeddingResponse
from model.request import QuestionRequest
from model.response import QuestionResponse
from utils.observability import log_observability

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_methods=["GET", "POST"],
    allow_credentials=True,
    allow_origins=["*"],
    allow_headers=["*"]
)

FOLDER_PATH = "./data/"

@app.get("/")
def gravidai():
    """
    Endpoint inicial para explicar sobre a API GravidAI.
    """

    return JSONResponse(
        status_code=200,
        content={
            "message": """
                O GravidAI é um assistente virtual criado para ajudar futuras mamães a tirarem dúvidas sobre gravidez de forma simples, confiável e acessível. Ele utiliza uma tecnologia avançada chamada RAG (Retrieval-Augmented Generation), que combina inteligência artificial com uma base de conhecimento médico especializado. Isso garante respostas precisas e sempre baseadas em fontes confiáveis.
                Os arquivos utilizados em combinação com o méotodo RAG foram:
                - Caderneta da Gestante -  ministério da saúde, 4º edição 2018: https://bvsms.saude.gov.br/bvs/publicacoes/caderneta_gestante_4ed.pdf
                - Assistência Pré-natal Manual Técnico - Ministério da saúde: https://bvsms.saude.gov.br/bvs/publicacoes/cd04_11.pdf
                - Cartilha da gestante - Fundação ABRINQ: https://www.fadc.org.br/sites/default/files/2022-05/Cartilha-da-gestante-Fundacao-Abrinq_0.pdf
                - Criança feliz, manual de apoio visitas domiciliares às gestantes - Ministério da Cidadania: https://mds.gov.br/webarquivos/cidadania/SNAPI%20-%20Crian%C3%A7a%20Feliz/Manual%20da%20Gestante.pdf
                - CADERNETA DA CRIANÇA MENINA - Ministério da Saúde, 7ª edição 2024: https://bvsms.saude.gov.br/bvs/publicacoes/caderneta_crianca_menina_passaporte_cidadania_7ed.pdf
                - CADERNETA DA CRIANÇA MENINO - Ministério da Saúde, 7ª edição 2024: https://bvsms.saude.gov.br/bvs/publicacoes/caderneta_crianca_menino_passaporte_cidadania_7ed.pdf
            """
        }
    )

@app.get("/create_embeddings", response_model=EmbeddingResponse)
def process_pdfs():
    """
    Endpoint para processar os PDFs de uma pasta, gerar os embeddings 
    e armazená-los no MongoDB Atlas.
    """

    if not os.path.exists(FOLDER_PATH):
        raise HTTPException(status_code=400, detail="Caminho da pasta não existe.")

    try:
        create_embedding_mongodb(FOLDER_PATH)
        return JSONResponse(
            status_code=200,
            content={"message": "Todos os PDFs foram processados e os embeddings foram armazenados no Cloud MongoDB Atlas."}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Erro ao processar os PDFs: {str(e)}"}
        )

@app.post("/ask_question", response_model=QuestionResponse)
async def ask_question_endpoint(query: QuestionRequest):
    """
    Endpoint da API que processa uma pergunta do usuário, obtém a resposta através 
    de um modelo de linguagem, e retorna informações detalhadas sobre a execução.
    """
    
    question = query.question

    try:
        answer, chat_history, prompt, source, metrics = ask_question(question)

        return JSONResponse(
            status_code=200,
            content={
                "question": question,
                "answer": answer,
                "prompt": prompt,
                "source": source,
                "history": chat_history,
                "metrics": metrics
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Erro ao processar a pergunta: {str(e)}"}
        )
