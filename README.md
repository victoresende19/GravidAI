# GravidAI

Sua plataforma definitiva para tirar dúvidas sobre a gravidez e a saúde do seu bebê!

## Acesse 
Para facilitar o teste do GravidAI, foi desenvolvido um website que realiza consultas à API criada. A API foi criada através das bibliotecas FastAPI, PyPDF2, LangChain e OpenAI, em linguagem Python, e é necessário obter uma API_KEY da OpenAI, a qual você pode criar gratuitamente, basta [clicar aqui](https://openai.com/index/openai-api/). Além disso, visando a acessibilidade, criou-se a plataforma SummsUpIA por meio do framework React, em linguagem JavaScript. 

O deploy da API foi realizado utilizando o [Google Cloud](https://cloud.google.com/?hl=pt-BR), sob o plano gratuito. Devido às limitações deste plano, como o uso de máquinas menos robustas, o tempo de resposta pode ser maior em comparação ao uso local da API. Por fim, o frontend da plataforma teve o deploy através do [Vercel](https://vercel.com/). Para acessar e testar o aplicativo, visite: [https://gravidai.vercel.app/](https://gravidai.vercel.app/).

![image](https://github.com/user-attachments/assets/93feae66-4737-4d62-baef-2f88cc3021ea)



<hr>

## Tecnologias
O agente foi criado a partir da técnica RAG (Retrieval-Augmented Generation), visando respostas mais assertivas sobre o assunto. Além disso, utilizou-se das seguintes tecnologias:
- Python 3.11 (com as respectivas bibliotecas): 
  - LangChain: biblioteca para utilização modular de códigos voltados a agentes de IA;
  - OpenAI (além do OpenAI Key): utilização dos modelos LLM OpenAI para a criação das descrições e títulos. Além disso, utilização do modelo DallE 3 para criação da thumbnail;
  - PyMongo: utilização para conexão ao banco de dados vetorial, alocação e pesquisa dos embeddings.
  - PyPDF2: extração de textos de PDFs;
  - Poetry: pacote para o controle de versões das bibiliotecas.
- MongoDB Atlas: utilizado para alocação e recuperação dos embeddings por meio da Vector Search e distância de cosseno.


## Conteúdos:
Para a utilização da técnica RAG, utilizou-se os conteúdos abaixo visando dar um contexto melhor ao assistente. Assim, as respostas são cada vez mais personalizadas e assertivas:
- [Caderneta da Gestante -  ministério da saúde, 4º edição 2018](https://bvsms.saude.gov.br/bvs/publicacoes/caderneta_gestante_4ed.pdf)
- [Assistência Pré-natal Manual Técnico - Ministério da saúde](https://bvsms.saude.gov.br/bvs/publicacoes/cd04_11.pdf)
- [Cartilha da gestante - Fundação ABRINQ](https://www.fadc.org.br/sites/default/files/2022-05/Cartilha-da-gestante-Fundacao-Abrinq_0.pdf)
- [Criança feliz, manual de apoio visitas domiciliares às gestantes - Ministério da Cidadania](https://mds.gov.br/webarquivos/cidadania/SNAPI%20-%20Crian%C3%A7a%20Feliz/Manual%20da%20Gestante.pdf)
- [CADERNETA DA CRIANÇA MENINA - Ministério da Saúde, 7ª edição 2024](https://bvsms.saude.gov.br/bvs/publicacoes/caderneta_crianca_menina_passaporte_cidadania_7ed.pdf)
- [CADERNETA DA CRIANÇA MENINO - Ministério da Saúde, 7ª edição 2024](https://bvsms.saude.gov.br/bvs/publicacoes/caderneta_crianca_menino_passaporte_cidadania_7ed.pdf)

## API
A API foi escrita em FastAPI através da lingugem Python e as devidas bibliotecas contidas no arquivo requirements.txt.

### Configurações - localmente
Instalação da biblioteca Poetry:
```
pip install poetry
```

Inicialização do Poetry:
```
poetry init
```

Instalação das bibliotecas necessárias:
```
poetry install
```

Ou há a possibilidade de apenas utilizar o comando abaixo para a instalação das bibliotecas:
```
pip install requirements.txt
```

Configuração arquivo .env:
```
ATLAS_CONNECTION_STRING=
OPENAI_API_KEY=
```

Ativação da API:
```
poetry run uvicorn main:app --reload
```

### Endpoints
Para executar a API localmente, os seguintes métodos estarão disponíveis. Utilize ferramentas como o Postman ou Insomnia para realizar as requisições:
- Introdução à API com informações de documentos utilizados:
  - ``` (GET): http://127.0.0.1:8000/ ```
- Criação dos embeddings:
  - ``` (GET):  http://127.0.0.1:8000/create_embeddings/ ```
- Assistente:
  - ``` (POST):  http://127.0.0.1:8000/ask_question/ ```
  - Corpo da Requisição JSON: ```{ "question": "Quais alimentos não posso comer enquanto estou grávida?" }```

## Frontend
O frontend foi escrito em React através da linguagem Typescript.

### Configurações - localmente
Instalação das bibliotecas:
```
npm install
```

Caso deseje, troque o endpoint de consulta, caso o teste seja feito local, em: gravidai > src > App.tsx:
```
http://127.0.0.1:8000/ask_question/
```

Ativação da interface:
```
npm start
```

<hr>
@Victor Resende
