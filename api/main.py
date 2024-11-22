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
        return {
            "message": "Todos os PDFs foram processados e os embeddings foram armazenados no Cloud MongoDB Atlas."
        }
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
