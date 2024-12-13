"""Responsável pela criação dos Embeddings"""

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from db.database import configure_mongodb
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def load_pdfs_from_folder(folder_path):
    """
    Carrega e processa todos os arquivos PDF em uma pasta, dividindo o conteúdo 
    em fragmentos menores para armazenamento.

    Parâmetros
    ----------
    folder_path : str
        O caminho da pasta que contém os arquivos PDF a serem processados.

    Retorna
    -------
    list
        Uma lista contendo os documentos processados e fragmentados. 
        Cada documento é dividido em partes menores, de acordo com o tamanho 
        definido pelo `RecursiveCharacterTextSplitter`.

    Exceções
    --------
    ValueError
        Se nenhum arquivo PDF for encontrado na pasta especificada.
    """

    documents = []

    # Itera sobre todos os PDFs da pasta
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            print(f"Carregando PDF: {file_path}")

            loader = PyPDFLoader(file_path)
            data = loader.load()

            # Dividir o PDF em fragmentos menores
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
            docs = text_splitter.split_documents(data)

            # Adicionar os fragmentos à lista de documentos
            documents.extend(docs)

    return documents

def create_embedding_mongodb(folder_path: str):
    """
    Processa os arquivos PDF de uma pasta, cria embeddings a partir do 
    conteúdo e armazena-os em uma coleção do MongoDB Atlas.

    A função carrega todos os arquivos PDF de uma pasta, divide o 
    conteúdo em fragmentos menores, gera embeddings utilizando o modelo 
    de embeddings OpenAI, e armazena esses embeddings em um banco de dados MongoDB Atlas.

    Parâmetros
    ----------
    folder_path : str
        O caminho da pasta que contém os arquivos PDF a serem processados.

    Retorna
    -------
    None
        A função não retorna nenhum valor, mas imprime mensagens de status 
        sobre o carregamento e armazenamento dos embeddings.

    Exceções
    --------
    Exception
        Se nenhum documento for encontrado ou ocorrer algum erro no processo, uma exceção 
        será capturada e uma mensagem de erro será exibida.
    """

    MongoDBAtlasVectorSearch.from_documents(
        documents=load_pdfs_from_folder(folder_path),
        embedding=OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY),
        collection=configure_mongodb(),
        index_name="vector_index"
    )
