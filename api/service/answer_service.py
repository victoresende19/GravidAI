"""Responsável pela lógica de assistente"""

import time
from tiktoken import encoding_for_model
from db.database import get_mongodb_collection
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_community.chat_models import ChatOpenAI
from utils.format import format_docs, format_chat_history, format_source
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
atlas_collection = get_mongodb_collection()

# Coleção existente no MongoDB Atlas
vector_store = MongoDBAtlasVectorSearch(
    collection=atlas_collection,
    embedding=OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY),
    index_name="vector_index"
)

# Recuperador de vetores (retriever)
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={'k': 5, 'fetch_k': 50}
)

OPENAI_MODEL = "gpt-3.5-turbo-0125"
llm_model = ChatOpenAI(model=OPENAI_MODEL)

# Memória com a chave 'history'
memory = ConversationBufferMemory(memory_key="history", return_messages=True)

# Cadeia de conversação com o histórico
conversation_chain = ConversationChain(
    llm=llm_model,
    verbose=False,
    memory=memory
)

def ask_question(question: str):
    """
    Processa uma pergunta utilizando um modelo de linguagem e retorna a 
    resposta juntamente com o histórico da conversa.
    """
    start_time = time.time()

    # Traz os documentos relevantes
    docs = retriever.invoke(question)
    context = format_docs(docs)

    template = """
    You are an expert in health and pregnancy, with in-depth knowledge of obstetrics, nutrition, exercise for pregnant women, fetal development and postnatal development. 
    Use only the content provided below to answer the questions. 
    Don't make up information and, if you don't know it, say so explicitly.

    **Retrieval
    Relevant information about pregnancy or postnatal baby health, taken from reliable sources, is below:
    {context}

    **Instruction:**
    Answer in a clear, precise and easy-to-understand way, adapting the tone for a lay person. 
    Your answer should help resolve the query without overloading it with unnecessary technical information.

    **Context:**
    The question has been asked by a pregnant person or by someone who is looking for health-related information during pregnancy or after giving birth.

    **Explanation:**
    Include detailed explanations where necessary, based on the content provided, to help the user understand the reason for the answer. 
    If the context provides links or references, cite them.

    **Attention**
    Always answer in pt-BR.

    Question: {question}
    """

    prompt = template.format(context=context, question=question)
    answer = conversation_chain.run(prompt)
    chat_history = format_chat_history(conversation_chain.memory.chat_memory.messages, docs)
    source = format_source(docs)

    end_time = time.time()
    response_time = end_time - start_time
    encoding = encoding_for_model(OPENAI_MODEL)
    prompt_tokens = len(encoding.encode(prompt))
    response_tokens = len(encoding.encode(answer))
    tokens_used = prompt_tokens + response_tokens

    metrics = {
        "tokens_used": tokens_used,
        "response_time": response_time
    }

    return answer, chat_history, prompt, source, metrics
