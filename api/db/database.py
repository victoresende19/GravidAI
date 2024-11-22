"""Responsável pelas conexões do MongoDB"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.operations import SearchIndexModel

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
ATLAS_CONNECTION_STRING = os.getenv("ATLAS_CONNECTION_STRING")

def get_mongodb_collection():
    """
    Configura e estabelece uma conexão com uma coleção no MongoDB Atlas.

    Retorna
    -------
    pymongo.collection.Collection
        A coleção configurada a partir do MongoDB Atlas.

    Exceções
    --------
    ValueError
        Se a string de conexão com o MongoDB Atlas não estiver definida nas variáveis de ambiente.
    """

    if not ATLAS_CONNECTION_STRING:
        raise ValueError("MongoDB Atlas connection string não está definida. Verifique seu arquivo .env.")

    client = MongoClient(ATLAS_CONNECTION_STRING)

    db_name = "mongodb_pdf_content"
    collection_name = "gravidai_embeddings"
    atlas_collection = client[db_name][collection_name]

    if atlas_collection.estimated_document_count() == 0:
        atlas_collection.insert_one({"init": "create collection"})

    return atlas_collection

def create_vector_search_index(atlas_collection, index_name="vector_index"):
    """
    Cria um índice de busca de vetores em uma coleção do MongoDB Atlas.

    Parâmetros
    ----------
    atlas_collection : pymongo.collection.Collection
        A coleção do MongoDB Atlas onde o índice será criado.
    index_name : str, opcional
        O nome do índice de busca de vetores a ser criado (o padrão é "vector_index").

    Retorna
    -------
    None
        A função não retorna nenhum valor, mas imprime uma mensagem 
        indicando que o índice foi criado com sucesso.
    """

    search_index_model = SearchIndexModel(
        definition={
            "fields": [
                {
                    "type": "vector",
                    "path": "embedding",
                    "numDimensions": 1536,
                    "similarity": "cosine"
                },
                {
                    "type": "filter",
                    "path": "page"
                }
            ]
        },
        name=index_name,
        type="vectorSearch"
    )

    atlas_collection.create_search_index(model=search_index_model)

    print(f"Índice de busca de vetores '{index_name}' criado com sucesso.")

def configure_mongodb():
    """
    Configura o MongoDB e garante que um índice de busca de vetores foi criado.

    Retorna
    -------
    pymongo.collection.Collection
        A coleção do MongoDB Atlas após a criação do índice de busca de vetores.
    """

    atlas_collection = get_mongodb_collection()
    create_vector_search_index(atlas_collection)
    return atlas_collection
