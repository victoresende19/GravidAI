# DEM-1 — Nova cartilha

> Entrega implementada pelo fluxo multiagente e submetida como Draft PR para revisão humana.

## Demanda

Adicionar nova cartilha na base de conhecimento do repositório. Link cartilha: https://www.defensoria.df.gov.br/wp-content/uploads/2023/01/Cartilha-Os-Direitos-da-Crianca-e-do-Adolescente.pdf

## Repositório-alvo

- Repositório: https://github.com/victoresende19/GravidAI
- Branch base: `main`
- Linguagem predominante: Python (64.13%)

## Story — versão 1

## Sugestão inicial gerada a partir da demanda

Você pode aprovar esta versão diretamente ou usar o chat para solicitar ajustes.

História de Usuário Preliminar — Adicionar nova cartilha à base de conhecimento (GravidAI)

Entendimento da Demanda  
O objetivo é permitir que o conteúdo da “Cartilha - Os Direitos da Criança e do Adolescente” (https://www.defensoria.df.gov.br/wp-content/uploads/2023/01/Cartilha-Os-Direitos-da-Crianca-e-do-Adolescente.pdf) seja incluído na base de conhecimento do GravidAI. A inclusão desta cartilha visa ampliar o escopo de informações disponíveis para responder dúvidas sobre gravidez, direitos e saúde do bebê, abrangendo agora também direitos da criança e do adolescente conforme esse novo documento.

História no formato Como / Quero / Para  
Como administradora/or responsável pela base de conhecimento do GravidAI  
Quero incluir a cartilha “Os Direitos da Criança e do Adolescente” na base de conhecimento  
Para que perguntas feitas ao assistente também possam ter como referência esse material atualizado sobre direitos das crianças e adolescentes.

Regras Identificadas

- O sistema utiliza técnica RAG (Retrieval-Augmented Generation) para responder perguntas (Fonte 2, Fonte 1).
- Novas fontes/materiais de conhecimento vêm sendo incluídas na base por meio do processamento de PDFs, utilizando extração via PyPDF2, embeddings por LangChain/OpenAI, e persistência no MongoDB (Fonte 2, Fonte 1).
- No momento, não há regra ou script específico recuperado para adicionar uma nova cartilha PDF. A existência de endpoint “/create_embeddings” (Fonte 1) pode estar associada ao processamento de novas fontes, mas o trecho está incompleto.
- As respostas retornam, atualmente, informações sobre fontes utilizadas (Fonte 3), logo, após o processamento, a nova cartilha deve aparecer entre as fontes citadas nas respostas pertinentes.

Critérios de Aceitação (formato Dado / Quando / Então)

Dado  
Que a API do GravidAI já está em funcionamento e com as bibliotecas de extração (PyPDF2), embeddings (LangChain/OpenAI) e armazenamento (MongoDB) configuradas  
E a cartilha “Os Direitos da Criança e do Adolescente” disponível em PDF

Quando  
Um responsável seguir o fluxo/documentação de processamento e ingestão de um novo PDF para a base de conhecimento  
E concluir o processamento com sucesso

Então  
O conteúdo desta cartilha deve poder ser consultado pelas perguntas do usuário via assistente  
E as respostas geradas citando esse conteúdo devem fazer referência a este novo material como fonte, conforme o modelo atual de respostas  
E o processamento e ingestão dessa fonte devem estar rastreáveis e auditáveis no sistema (logs/processos)

Dúvidas e Lacunas

- Qual é exatamente o fluxo/documentação utilizada hoje para ingestão de um novo PDF/cartilha na base de conhecimento? Existe endpoint, script, interface administrativa? Não há esta informação nas fontes.
- O endpoint /create_embeddings, citado parcial e superficialmente, serve para inclusão de novos materiais ou só de atualização de embeddings de arquivos já existentes?
- Há limitação de formato, tamanho ou linguagem do PDF a ser processado?
- É necessário algum tratamento manual nas fontes ou é tudo automatizado pelo pipeline já existente?
- Há necessidade de revisão ou aprovação após ingestão do material, antes de ficar disponível para consulta dos usuários?

Fontes Utilizadas

- GravidAI/api/main.py — estrutura da API, endpoints e explicação geral de funcionamento (incluindo documentação sobre fontes processadas) [Fonte 1]
- GravidAI/README.md — visão geral do projeto, principais tecnologias, fluxo de funcionamento e relação das fontes existentes [Fonte 2]
- GravidAI/api/model/response.py — modelo de resposta (QuestionResponse), detalhando como fontes são apresentadas nas respostas [Fonte 3]
- GravidAI/repository-profile — informações sobre branch, linguagem, contexto do repositório [Fonte 4]

Observações  
Esta história é preliminar devido à ausência de informações detalhadas sobre fluxo de ingestão de novos PDFs/cartilhas nesta base. Recomendação: obter documentação/arquivos de código completos relacionados ao processo de ingestão (ex.: endpoint /create_embeddings ou pipelines de processamento de fontes), para refinamento dos critérios e regras de negócio.

## Refinement — versão 1

## Primeira versão gerada automaticamente

Este resultado usa como entrada o output aprovado da etapa anterior. Você pode aprová-lo diretamente ou usar o chat para solicitar ajustes.

# Refinamento — "Adicionar nova cartilha à base de conhecimento (GravidAI)"

## 1. Requisitos Funcionais

- **RF1**: O sistema deve permitir a ingestão do conteúdo completo da cartilha em PDF (“Cartilha - Os Direitos da Criança e do Adolescente” – https://www.defensoria.df.gov.br/wp-content/uploads/2023/01/Cartilha-Os-Direitos-da-Crianca-e-do-Adolescente.pdf) na base de conhecimento.
- **RF2**: O fluxo de ingestão deve envolver a extração de texto do PDF, geração de embeddings (LangChain/OpenAI) e persistência via MongoDB Atlas usando Vector Search.
- **RF3**: Após a ingestão, consultas de usuários ao assistente, cuja resposta dependa desse conteúdo, devem citar explicitamente essa nova cartilha como fonte (seguindo modelo de respostas existente – ver Fonte/Source em GravidAI/api/model/response.py).
- **RF4**: O processamento e a ingestão dessa fonte devem gerar logs/setups para rastreabilidade e auditoria (observabilidade).
- **RF5**: Todo o processamento deve ser realizado sem impactar as outras funcionalidades de consulta do assistente.

## 2. Requisitos Não Funcionais

- **RNF1**: A ingestão deve suportar arquivos PDF padrão e ser compatível com o pipeline já existente (uso de PyPDF2, LangChain; ver README e embedding_service.py).
- **RNF2**: O tempo de processamento deve ser razoável para PDFs de até 100 páginas (~10MB); limites específicos não estão documentados (lacuna).
- **RNF3**: Logs de sucesso/falha devem ser gerados para todas as etapas: extração, split, geração e persistência.
- **RNF4**: A atualização da base deve ser rastreável, mesmo que apenas via log (lembrando que não há documentação de interface/admin).
- **RNF5**: Manter padrão de resposta da API, incluindo formato Source e histórico para respostas com referência à nova cartilha.

## 3. Cenários BDD

### Cenário 1: Inclusão de nova cartilha via pipeline existente

**Dado**  
- Que a API está operacional  
- E o PDF da cartilha foi obtido  
- E as bibliotecas necessárias estão configuradas  

**Quando**  
- O responsável executa o fluxo/scrip ou aciona endpoint apropriado para ingestão do PDF na base  

**Então**  
- O conteúdo da cartilha é indexado  
- E perguntas relevantes são respondidas referenciando essa fonte  
- E os processos de ingestão ficam registrados em log

### Cenário 2: Resposta ao usuário citando a nova cartilha

**Dado**  
- Que o PDF foi processado e indexado com sucesso  
- E um usuário faz uma pergunta cujo conteúdo está na cartilha  

**Quando**  
- A pergunta é enviada ao assistente  

**Então**  
- A resposta do assistente inclui referência à cartilha nos metadados de fontes utilizadas

### Cenário 3: Auditoria do processamento

**Dado**  
- Que o processamento de ingestão foi realizado  

**Quando**  
- Um operador consulta os logs do sistema  

**Então**  
- Os registros apresentam detalhes da ingestão (inicialização, extração, fragmentação, embedding, armazenamento, sucesso/falha)

## 4. Dependências

- **LangChain** e **OpenAI API** para embedding;
- **PyPDF2** para extração de texto de PDFs;
- **MongoDB Atlas** para armazenamento dos embeddings;
- **Google Cloud** (deploy da API, conforme README) — infraestrutura, pode impactar tempo ou disponibilidade;
- **Endpoint/pipeline de ingestão**: suspeita-se da existência de um endpoint `/create_embeddings` (recuperado parcialmente), mas faltam detalhes do fluxo (lacuna);
- **Variáveis ambientais**: necessidade de chave OPENAI_API_KEY e acesso apropriado ao cluster MongoDB Atlas;
- **Scripts ou documentação administrativa** ainda ausentes (lacuna).

## 5. Impactos de Dados

- Inclusão de novos embeddings no banco MongoDB Atlas;
- A base vetorial se expandirá, o que pode impactar o tempo de busca e custo de operação/vetorização;
- Novos metadados relativos à fonte devem ser corretamente persistidos (modelos em GravidAI/api/model/response.py);
- Logs de processamento/erros devem ser gerados para rastreabilidade.

## 6. APIs e Componentes Impactados

- **GravidAI/api/main.py**: Definitions/uso de endpoints; presença, mas não recuperação completa, do endpoint `/create_embeddings`;
- **GravidAI/api/service/embedding_service.py**: Pipeline de ingestão, definição de funções de extração de PDFs, fragmentação, geração de embeddings, persistência;
- **GravidAI/api/model/response.py**: Formatos de fonte e resposta; mantido padrão Source;
- **MongoDB Atlas**: Persistência; uso da coleção para embeddings vetoriais.

> **Lacuna:** O método exato ou interface para ingestão (script/endpoint/exemplo de uso de função) não foi recuperado por completo.

## 7. Riscos

- **Documentação Insuficiente:** Fluxo de ingestão não está claramente documentado; risco de erro operacional ou inconsistência.
- **Limitações da Infraestrutura:** Deploy em plano gratuito do Google Cloud pode causar lentidão ou indisponibilidade temporária (README).
- **Erros de Parsing:** Formatos irregulares de PDF podem causar falhas silenciosas, já que não há política recuperada para erros/falhas de extração.
- **Atualização Involuntária:** Risco de sobrescrever, duplicar ou corromper embeddings antigos caso o pipeline não trate versão/atualização.
- **Segurança das Credenciais:** Necessidade de OPENAI_API_KEY; risco se manipulação não for segura.
- **Escalabilidade:** Crescimento da base pode afetar performance, custo e precisão/relevância nas respostas.

## 8. Observabilidade

- **Logs de processamento** são obrigatórios para auditoria (ver utils.observability e requisitos derivados da história).
- Logs devem abranger: início/fim de processamento, erros, sucesso na extração/split/embedding/armazenamento.
- Não há evidência de métricas específicas de ingestão (exemplo: quantidade de documentos/tempo por etapa); seria desejável para extensões futuras.

## 9. Segurança

- **Controle de acesso:** Não há menção a autenticação no endpoint/pipeline de ingestão — risco de ingestão não autorizada.
- **Armazenamento seguro de credenciais:** OPENAI_API_KEY é carregada de variável de ambiente via dotenv, o que segue boas práticas, porém visibilidade e proteção dessas variáveis fora do escopo dos fontes recuperados.
- **Validação de arquivo:** PDF deve ser validado/checado para evitar insegurança ou ingestão de arquivos maliciosos. Não há detalhamento recuperado sobre esta etapa.

## 10. Acessibilidade

- **Irrelevante** para o processamento/back-end/ingestão do PDF — acessibilidade é focada no front-end conforme README; não impacta esta entrega.

## 11. Tarefas Técnicas

1. **(Lacuna: confirmar método de ingestão)** Rever/extrair do código completo ou da documentação qual fluxo se segue para ingestão de novos PDFs na base (endpoint, script, etc).
2. Colocar o PDF da cartilha disponível na pasta usada para ingestão (provavelmente FOLDER_PATH = ./data/ conforme main.py/embedding_service.py).  
3. Executar o pipeline de ingestão (função suspeita: create_embedding_mongodb, detalhe em embedding_service.py) apontando para o novo arquivo.
4. Garantir geração de embedding e persistência bem-sucedidas no MongoDB Atlas.
5. Verificar logs para garantir rastreabilidade e identificação de sucesso/falha.
6. Realizar consulta de teste via API, simulando pergunta relacionada ao conteúdo da cartilha, e verificar se ela é referenciada corretamente nas respostas do assistente (campo Source).
7. Documentar o procedimento adotado, já que não há referência consistente de documentação de ingestão.
8. (Opcional, desejável) Implementar/garantir checagem e validação básica do PDF antes da ingestão.
9. (Opcional) Propor melhoria para autenticação e registro de operações administrativas na ingestão.

---

## Lacunas e Ações Recomendadas

- **Lacuna principal:** Não foi recuperado o fluxo/documentação/método detalhado para ingestão de PDFs. Falta de exemplos ou instruções do uso de create_embedding_mongodb e endpoint /create_embeddings.
    - **Ação:** Recomenda-se obter todo o código/README relacionado à ingestão/administração da base ou sincronizar os arquivos faltantes.
    - **Ação:** Registrar, após a execução, como foi realizado o procedimento para futuras manutenções.

---

**Fontes citadas:**  
- GravidAI/api/main.py  
- GravidAI/api/service/embedding_service.py  
- GravidAI/api/model/response.py  
- GravidAI/README.md

**Observação final:** Não foi possível mapear todo o fluxo de ingestão, nem confirmar mecanismos de autenticação, interface administrativa ou limites da operação. O refinamento aqui está limitado à informação recuperada e depende de análise direta dos scripts completos para fechamento de todo o ciclo de ingestão.

## Relatório da execução Tech Lead → Desenvolvedor(es) → QA

## Primeira versão gerada automaticamente

Este resultado usa como entrada o output aprovado da etapa anterior. Você pode aprová-lo diretamente ou usar o chat para solicitar ajustes.

## Execução de desenvolvimento multiagente

> As alterações abaixo já foram aplicadas em um clone isolado. Nenhum commit ou push
> foi realizado. A aprovação humana publicará a branch e abrirá o Draft PR.

### Roteamento

- Agentes selecionados: **Python**
- Motivo: inserção e validação da nova cartilha via pipeline Python existente (create_embedding_mongodb / endpoint /create_embeddings)
- QA: obrigatório
- Veredito do QA: **APROVADO_COM_RESSALVAS**

### Tech Lead

Entendimento técnico (resumo)
- Objetivo: adicionar a cartilha PDF à base RAG do GravidAI, usando o pipeline existente que processa PDFs em ./data/, gera embeddings (OpenAI/LangChain) e persiste no MongoDB Atlas (coleção gravidai_embeddings / índice vector_index). Endpoint disponível: GET /create_embeddings que chama create_embedding_mongodb(FOLDER_PATH).

Arquivos e símbolos relevantes (existentes)
- api/main.py: endpoints — /create_embeddings -> process_pdfs(), /ask_question -> ask_question_endpoint()
- api/service/embedding_service.py: load_pdfs_from_folder(folder_path), create_embedding_mongodb(folder_path)
- api/service/answer_service.py: ask_question(question) — retriever setup, uso de MongoDBAtlasVectorSearch, format_docs/format_source
- api/db/database.py: get_mongodb_collection(), configure_mongodb(), create_vector_search_index()
- api/model/response.py: Source, QuestionResponse models (formato esperado)
- api/utils/observability.py: log_observability(prompt, answer, tokens_used, response_time)
- README.md: explica FOLDER_PATH = ./data/ e endpoints

Plano de implementação (ordem executável)
1. Preparação (manual): colocar o PDF da cartilha em ./data/ com nome claro (ex.: direitos_crianca_adolescente.pdf).
2. Verificar .env: ATLAS_CONNECTION_STRING e OPENAI_API_KEY (e opcional LANGSMITH_API_KEY) configuradas.
3. Local: rodar a API (poetry/uvicorn) ou executar diretamente a função create_embedding_mongodb apontando para ./data/ via endpoint GET /create_embeddings.
4. Validar ingestão: checar logs do terminal e coleção MongoDB (documentos inseridos, presença do índice vector_index).
5. Teste funcional: usar POST /ask_question com perguntas relacionadas ao conteúdo; confirmar que field "source" nas respostas referencia o novo PDF.
6. Registrar procedimento e resultado (README ou docs/operacional).
7. (Opcional) adicionar validação básica ao pipeline: checagem de extensão, tamanho e tratamento de exceções com logs mais verbosos.

Estratégia de testes
- Testes manuais:
  - Confirmar que GET /create_embeddings retorna 200 e mensagem de sucesso.
  - Verificar via MongoDB (client) que novos documentos (fragments) foram adicionados.
  - Fazer POST /ask_question com perguntas-chave do PDF e validar "source" inclui o nome do arquivo e páginas.
- Observabilidade:
  - Conferir saída de print/logs e chamadas a log_observability (se LANGSMITH_API_KEY presente).
- Não há testes automatizados existentes para ingestão; sugerir criar smoke test que chama /create_embeddings e valida coleção não vazia.

Riscos e rollback
- Riscos:
  - Falha por falta de OPENAI_API_KEY ou ATLAS_CONNECTION_STRING -> pipeline lança erros.
  - Duplicação de embeddings se rodar múltiplas vezes sem deduplicação.
  - PDFs mal formatados podem gerar chunks inválidos.
- Rollback:
  - Antes de ingestão, fazer backup/inspeção: exportar documentos atuais da coleção (mongodump ou export).
  - Em caso de ingestão indesejada, remover documentos inseridos pelo filename (campo source/path nos docs) ou restaurar backup.

Dúvidas impeditivas (se não respondidas, marcar bloqueado)
1. Há metadado persistido que identifica a origem (nome do arquivo/page) nos documentos gravados? (importante para rollback/consulta)
2. Existe política de deduplicação/versão para reprocessamentos? Como evitar duplicatas?
3. A conta MongoDB Atlas tem permissões e quota para novos embeddings?
4. Deseja que eu implemente validação/checagem automática do PDF antes de ingestão e/ou idempotência no pipeline?

Decisão de roteamento
- Requer desenvolvimento Python (alterações mínimas: documentação e, opcionalmente, validação/idempotência). QA manual obrigatório para checagens em Mongo e respostas do assistente.

ROUTING_JSON: {"required_agents":["python"],"reason":"inserção e validação da nova cartilha via pipeline Python existente (create_embedding_mongodb / endpoint /create_embeddings)","qa_required":true,"blocked":false}

### Desenvolvedor Python

Resumo rápido (ações e por que foram feitas)
- Objetivo: adicionar suporte e validações ao pipeline de ingestão e facilitar inclusão da nova cartilha PDF.
- Ações: melhorar robustez de api/service/embedding_service.py, criar scripts para baixar a cartilha e checar PDFs. Tentativa de download falhou por problema de verificação SSL no ambiente (detalhes abaixo).

Arquivos alterados / criados
- Modificado:
  - api/service/embedding_service.py
    - validações: verifica existência da pasta, ignora arquivos não-PDF, alerta para arquivos grandes.
    - enriquece metadados de fragmentos (source_file, source_path).
    - valida OPENAI_API_KEY e adiciona logs e tratamento de exceção.
- Criado:
  - scripts/download_cartilha.sh — script para baixar a cartilha para ./data/
  - scripts/check_pdfs.py — script leve que lista e valida PDFs em ./data/

Comportamento implementado
- load_pdfs_from_folder:
  -.raise ValueError se pasta não existe ou não contém PDFs.
  -Adds metadata fields source_file and source_path to each fragment for rastreabilidade.
  -Logs warnings for large files (>=10MB) and errors per-file without breaking entire run.
- create_embedding_mongodb:
  -Raises EnvironmentError if OPENAI_API_KEY não estiver configurada.
  -Logs início/fim, chama configure_mongodb() (que cria o índice) e trata exceções com logger.exception.
  -Does not change persistence schema; only improves validation and observability.

Scripts e comandos executados (e resultados)
1) Criação de diretórios:
   - Command: mkdir -p scripts data
   - Resultado: diretórios criados (ok).

2) Edição/Criação de arquivos:
   - Files edited/created as list acima (ok).

3) Tentativa de download da cartilha:
   - Command: scripts/download_cartilha.sh (usa curl -fSL)
   - Resultado: falha com curl exit code 60 — SSL certificate problem: unable to get local issuer certificate.
     - Nota: ambiente não pôde verificar a autoridade do certificado. Não alterei o script para forçar verificação por segurança.

4) Checagem de ./data/:
   - Command: ls -la ./data
   - Resultado: pasta está vazia (nenhum PDF presente).

Validações automáticas e limitações
- Não foi possível baixar automaticamente o PDF devido a erro SSL do curl no ambiente (curl retornou código 60). Opções:
  - Forçar download ignorando verificação SSL (curl -k) — inseguro; requer confirmação.
  - Baixar manualmente o PDF e colocá-lo em ./data/ com nome: direitos_crianca_adolescente.pdf (recomendado).
- Não executei create_embedding_mongodb nem rodei a API /create_embeddings:
  - create_embedding_mongodb exige OPENAI_API_KEY e conexão ao MongoDB Atlas (ATLAS_CONNECTION_STRING). Essas variáveis e acesso não foram configuradas no ambiente — executar sem elas causará erros.
- Não modifiquei o esquema de persistência nem fiz deduplicação automática (mudança potencialmente arriscada sem conhecer como os documentos são armazenados). Apenas adicionei metadados que permitem deduplicação/rollback futuros (source_file/source_path).

Instruções recomendadas para próximo passo (manuais e reproduzíveis)
1) Baixar a cartilha manualmente (ou permitir download inseguro):
   - Manual: coloque o PDF em repository/data/ com o nome direitos_crianca_adolescente.pdf
   - Ou, para forçar download (inseguro): scripts/download_cartilha.sh pode ser alterado para usar curl -k; ou executar:
     curl -k -fSL \"https://www.defensoria.df.gov.br/wp-content/uploads/2023/01/Cartilha-Os-Direitos-da-Crianca-e-do-Adolescente.pdf\" -o data/direitos_crianca_adolescente.pdf

2) Configurar variáveis de ambiente (ex.: em .env):
   - OPENAI_API_KEY=...
   - ATLAS_CONNECTION_STRING=...
   - (opcional) LANGSMITH_API_KEY=...
   - Observação: não colocar chaves no repositório.

3) Rodar ingestão:
   - Opção A (API endpoint): iniciar FastAPI (ex.: uvicorn api.main:app --reload) e chamar GET /create_embeddings
   - Opção B (direto): abrir REPL Python e executar:
       from api.service.embedding_service import create_embedding_mongodb
       create_embedding_mongodb('./data/')
     (requer as variáveis de ambiente setadas e dependências instaladas)

4) Verificações pós-ingestão:
   - Confirmar documentos inseridos na coleção mongodb_pdf_content.gravidai_embeddings e presença do índice vector_index.
   - Fazer POST /ask_question com perguntas relacionadas e verificar campo "source" nas respostas.

Observações finais e riscos remanescentes
- Risco: duplicação se reprocessar o mesmo PDF; agora há metadados que permitem identificar documentos por source_file, mas deduplicação automática não foi implementada para evitar alterações perigosas sem teste.
- Risco: se bibliotecas (langchain, langchain_community, etc.) não estiverem instaladas, create_embedding_mongodb falhará ao importar/instanciar embeddings. Verificar ambiente Python/Poetry conforme README.
- Não foi feito commit; todas as alterações estão no working tree conforme solicitado (arquivos criados/alterados no repositório local).

Se desejar, posso:
- Retentar o download usando curl com --insecure (dev mode) e colocar o PDF em ./data/ (peça explícita necessária).
- Implementar deduplicação segura baseada em source_file (recomendado: procurar por documentos existentes com o mesmo metadata antes de inserir).
- Tentar rodar create_embedding_mongodb localmente se fornecer (ou configurar) variáveis OPENAI_API_KEY e ATLAS_CONNECTION_STRING no ambiente temporário.

Quer que:
- eu tente baixar com --insecure agora, ou
- aguarde você colocar o PDF em ./data/ e eu executo a ingestão (se fornecer as chaves), ou
- implemente deduplicação automática baseada em source_file antes de executar a ingestão?

### QA

Veredito: APROVADO_COM_RESSALVAS

Testes/comandos executados:
- ls -la (repositório)
- python -m py_compile api/service/embedding_service.py scripts/check_pdfs.py (syntax OK)
- python3 scripts/check_pdfs.py -> saiu "Nenhum PDF encontrado em ./data"
- tentativa: importar/exec create_embedding_mongodb -> falha: ModuleNotFoundError: langchain_community

Resultados observados:
- Arquivo modificado: api/service/embedding_service.py — adiciona validações, logs e metadados (source_file, source_path) e valida OPENAI_API_KEY.
- Arquivos criados: scripts/check_pdfs.py, scripts/download_cartilha.sh
- check_pdfs detectou diretório data vazio.
- Não foi possível executar a ingestão completa (create_embedding_mongodb) por dependências ausentes e variáveis de ambiente não configuradas.

Problemas encontrados / notas:
- Dependências necessárias (langchain_community, langchain_openai, pymongo, etc.) não instaladas — impede execução do pipeline.
- OPENAI_API_KEY e ATLAS_CONNECTION_STRING não configuradas no ambiente — create_embedding_mongodb requer ambas.
- Não há deduplicação: reprocessamentos podem gerar duplicatas (metadados agora permitem identificação para rollback/dedup).
- scripts/download_cartilha.sh usa curl -fSL (seguro); em ambiente anterior o download falhou por verificação SSL do host externo (ambiente), não pelo script.

Correções aplicadas:
- Nenhuma alteração adicional além das já no working tree (nenhum commit realizado).

Pendências recomendadas:
1) Colocar o PDF em ./data/ (ex.: direitos_crianca_adolescente.pdf) or allow explicit --insecure download if accepted.
2) Instalar dependências do projeto (poetry/pip) e exportar OPENAI_API_KEY e ATLAS_CONNECTION_STRING.
3) Opcional: implementar deduplicação segura por metadata['source_file'] antes da persistência se evitar duplicatas for desejado.
4) Após 1+2, executar endpoint GET /create_embeddings ou chamar create_embedding_mongodb('./data/') e validar coleção Mongo (documentos e índice vector_index) e POST /ask_question funcionalidade.

Arquivos alterados/criados:
- Modified: api/service/embedding_service.py
- Added: scripts/check_pdfs.py, scripts/download_cartilha.sh

Nenhuma correção de código foi necessária além do que já está no working tree. Execução completa do pipeline não pôde ser verificada por limitações de ambiente (dependências e variáveis).

QA_VERDICT: APROVADO_COM_RESSALVAS

### Arquivos alterados

- `api/service/embedding_service.py`
- `scripts/`

### Resumo do diff

```text
api/service/embedding_service.py | 118 ++++++++++++++++++++++++---------------
 1 file changed, 74 insertions(+), 44 deletions(-)
scripts/ | novo arquivo
```

### Branch preparada

`ai/dem-1-nova-cartilha`

## Arquivos publicados

- `api/service/embedding_service.py`
- `scripts/`

## Comentário da aprovação humana

Aprovado sem comentário adicional.

## Guardrails

- O Pull Request permanece em modo **Draft**.
- Merge e deploy dependem de revisão humana.
- Os subagentes não executaram commit, push, merge ou deploy.
