# Desafio Busca Semântica - RAG com PGVector

Sistema de Busca Semântica usando **LangChain**, **PostgreSQL** com extensão **pgvector**, e **OpenAI**.

## Pré-requisitos

- Python 3.10+
- Docker e Docker Compose
- Variáveis de ambiente configuradas (`.env`)
   - [arquivo de exemplo](.env.example)

## Setup

### 1. Instalar dependências

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente

Crie um arquivo `.env` com:

```env
OPENAI_API_KEY=sua_chave_aqui
PGVECTOR_CONNECTION=postgresql+psycopg2://postgres:postgres@localhost:5432/rag
EMBEDDINGS_MODEL=text-embedding-3-small
LLM_MODEL=gpt-5-nano
CHUNK_SIZE=1000
CHUNK_OVERLAP=150
```

### 3. Iniciar o PostgreSQL com pgvector

```bash
docker compose up -d
```

Aguarde até que o container esteja saudável:
```bash
docker compose ps
```

## Uso

### Passo 1: Indexar documentos (uma única vez)

```bash
python src/ingest.py
```

Este script:
- Carrega o PDF (`src/document.pdf`)
- Divide o texto em chunks
- Gera embeddings com OpenAI
- Salva os dados no PostgreSQL (tabelas `langchain_pg_collection` e `langchain_pg_embedding`)

**Output esperado:**
```
Iniciando a ingestão do documento...
Ingestão concluída, pronto para responder suas perguntas!
```

### Passo 2: Iniciar o Chat

```bash
python src/chat.py
```

Agora você pode fazer perguntas e o sistema retornará respostas baseadas nos documentos indexados:

```
Digite sua pergunta (ou 'sair' para encerrar): sua pergunta aqui
Resposta:
 [resposta gerada...]
```

## Estrutura do Projeto

```
.
├── src/
│   ├── ingest.py          # Script para indexar documentos
│   ├── chat.py            # Interface de chat
│   ├── search.py          # Lógica de busca semântica
│   └── document.pdf       # Arquivo para processar
├── sql/
│   └── 01-cria-extensao-vector.sql  # Script SQL (extensão vector)
├── docker-compose.yml     # Configuração PostgreSQL + pgvector
├── requirements.txt       # Dependências Python
├── .env                   # Variáveis de ambiente
└── README.md
```

## Fluxo de Funcionamento

1. **Ingestão (`src/ingest.py`)**:
   - Carrega PDF → Divide em chunks → Gera embeddings → Salva no PostgreSQL

2. **Busca (`src/search.py`)**:
   - Recebe query do usuário → Converte em embedding → Busca similar no pgvector → Retorna top K resultados

3. **Chat (`src/chat.py`)**:
   - Loop interativo que chama a busca para cada pergunta do usuário

## Tabelas PostgreSQL criadas

- **`langchain_pg_collection`**: Armazena metadados das coleções
- **`langchain_pg_embedding`**: Armazena embeddings (vetores) e textos

## Troubleshooting

### PostgreSQL não conecta
```bash
# Verificar status do container
docker compose ps

# Ver logs
docker compose logs postgres

# Reiniciar
docker compose down && docker compose up -d
```

### Erro "Collection not found"
- Execute `src/ingest.py` primeiro para criar as tabelas

### Erro "OPENAI_API_KEY"
- Verifique se `.env` está configurado corretamente
- Reload do terminal pode ser necessário após alterações no `.env`
