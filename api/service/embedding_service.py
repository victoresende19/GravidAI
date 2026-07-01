"""Responsável pela criação dos Embeddings"""

import os
import logging
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from db.database import configure_mongodb
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_pdfs_from_folder(folder_path):
    """
    Carrega e processa todos os arquivos PDF em uma pasta, dividindo o conteúdo
    em fragmentos menores para armazenamento.

    Validações adicionadas:
    - verifica existência da pasta
    - inclui metadados (source_file, source_path)
    - ignora arquivos que não terminam em .pdf (case-insensitive)
    - alerta para arquivos grandes (>= 10MB)

    Retorna
    -------
    list
        Lista de Document do LangChain pronta para vetorização.

    Lança
    -----
    ValueError
        Se não for encontrado nenhum PDF na pasta.
    """

    if not os.path.isdir(folder_path):
        raise ValueError(f"Pasta não existe: {folder_path}")

    documents = []
    found = False

    for filename in os.listdir(folder_path):
        if not filename.lower().endswith('.pdf'):
            continue

        found = True
        file_path = os.path.join(folder_path, filename)
        try:
            size_bytes = os.path.getsize(file_path)
            if size_bytes >= 10 * 1024 * 1024:
                logger.warning(f"Arquivo grande (>10MB): {file_path} ({size_bytes} bytes). Processando mesmo assim.")

            logger.info(f"Carregando PDF: {file_path}")
            loader = PyPDFLoader(file_path)
            data = loader.load()

            # Dividir o PDF em fragmentos menores
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
            docs = text_splitter.split_documents(data)

            # Enriquecer metadados de cada fragmento para rastreabilidade
            for d in docs:
                # preserva metadados existentes (ex.: page), adiciona source_file e source_path
                md = d.metadata or {}
                md.setdefault('source_file', filename)
                md.setdefault('source_path', file_path)
                d.metadata = md

            documents.extend(docs)

        except Exception as e:
            logger.error(f"Falha ao processar {file_path}: {e}")

    if not found:
        raise ValueError(f"Nenhum arquivo PDF encontrado na pasta: {folder_path}")

    logger.info(f"Total de fragmentos carregados: {len(documents)}")
    return documents


def create_embedding_mongodb(folder_path: str):
    """
    Processa os PDFs da pasta, gera embeddings e armazena no MongoDB Atlas.

    Melhorias:
    - validação de OPENAI_API_KEY com mensagem clara
    - tratamento de exceções e logs informativos
    - garante criação do índice via configure_mongodb()
    """

    if not OPENAI_API_KEY:
        raise EnvironmentError("OPENAI_API_KEY não encontrada nas variáveis de ambiente. Verifique seu .env.")

    try:
        docs = load_pdfs_from_folder(folder_path)
        if not docs:
            logger.warning("Nenhum documento foi carregado para criação de embeddings.")
            return

        logger.info("Configurando MongoDB Atlas e índice...")
        atlas_collection = configure_mongodb()

        logger.info("Iniciando geração de embeddings e persistência no MongoDB Atlas...")
        MongoDBAtlasVectorSearch.from_documents(
            documents=docs,
            embedding=OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY),
            collection=atlas_collection,
            index_name="vector_index"
        )

        logger.info("Embeddings criados e armazenados com sucesso.")

    except Exception as e:
        logger.exception(f"Erro durante a criação de embeddings: {e}")
        raise
