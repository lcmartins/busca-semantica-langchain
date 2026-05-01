# Desafio Busca Semântica

## Descrição

Este projeto é um sistema de **busca semântica em documentos PDF** utilizando técnicas de RAG (Retrieval-Augmented Generation). O sistema permite fazer perguntas sobre o conteúdo de arquivos PDF e receber respostas baseadas exclusivamente no contexto dos documentos, utilizando embeddings semanticamente ricos e LLM da OpenAI.

### Características principais:
- 📄 Processamento de documentos PDF com extração de texto
- 🔍 Busca semântica avançada com embeddings
- 🧠 Integração com GPT-4 da OpenAI para geração de respostas
- 🗄️ Armazenamento de vetores no PostgreSQL com extensão pgvector
- 💬 Interface interativa via linha de comando

---

## Pré-requisitos

Antes de iniciar, certifique-se de ter os seguintes componentes instalados:

### Obrigatórios:
- **Python 3.10+** ([Download](https://www.python.org/downloads/))
- **Docker** ([Download](https://docs.docker.com/get-docker/))
- **Docker Compose** ([Documentação](https://docs.docker.com/compose/install/))
- **Git** ([Download](https://git-scm.com/))
- **Chave de API OpenAI** ([Criar em](https://platform.openai.com/account/api-keys))

### Verificar instalações:
```bash
python3 --version
docker --version
docker compose version
git --version
```

---

## Estrutura do Projeto

```
desafio-busca-semantica/
├── chat.py                    # Interface interativa principal
├── search.py                  # Módulo de busca semântica
├── ingest.py                  # Módulo de ingestão de PDFs
├── document.pdf               # Documento a ser indexado
├── docker-compose.yml         # Configuração Docker para PostgreSQL
├── requirements.txt           # Dependências Python
├── .env                       # Variáveis de ambiente (não versionado)
├── sql/
│   └── 01-cria-extensao-vector.sql  # Script SQL para extensão pgvector
└── README.md                  # Este arquivo
```

---

## Instalação e Configuração

### 1. Clonar ou copiar o repositório

```bash
cd ~/estudos/mba/desafio-busca-semantica
```

### 2. Criar ambiente virtual Python

```bash
python3 -m venv venv
```

### 3. Ativar o ambiente virtual

**Linux/macOS:**
```bash
source venv/bin/activate
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

### 4. Instalar dependências

```bash
pip install -r requirements.txt
```

### 5. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
OPENAI_API_KEY=sua_chave_api_aqui
```

**Como obter a chave OpenAI:**
1. Acesse [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)
2. Faça login ou crie uma conta OpenAI
3. Clique em "Create new secret key"
4. Copie a chave gerada e adicione ao arquivo `.env`

⚠️ **Importante:** Nunca compartilhe ou versione a chave API na sua chave `.env`. O arquivo `.env` deve estar no `.gitignore`.

### 6. Iniciar os serviços Docker

```bash
docker compose up -d
```

Este comando irá:
- Baixar a imagem PostgreSQL com pgvector
- Iniciar um container PostgreSQL
- Criar o banco de dados `rag`
- Executar o script SQL para criar a extensão pgvector
- Criar um volume persistente para os dados

**Verificar status:**
```bash
docker compose ps
```

**Ver logs:**
```bash
docker compose logs -f postgres
```

---

## Como Usar

### Preparar o Documento

1. Coloque seu arquivo PDF na raiz do projeto com o nome `document.pdf`
2. O sistema automaticamente:
   - Carregará o PDF
   - Dividirá o conteúdo em chunks de 1000 caracteres com sobreposição de 150
   - Criará embeddings usando o modelo `text-embedding-3-small`
   - Armazenará no PostgreSQL

### Executar o Chat Interativo

Com o ambiente virtual ativado, execute:

```bash
python3 chat.py
```

O programa iniciará um loop interativo onde você pode:
1. Digitar suas perguntas em português
2. Receber respostas baseadas no conteúdo do PDF
3. Digitar `sair` para encerrar o programa

**Exemplo de uso:**
```
Digite sua pergunta (ou 'sair' para encerrar): Qual é o tema principal do documento?
Resposta:
 1. [Resposta baseada no resultado 1]
 2. [Resposta baseada no resultado 2]
...
Digite sua pergunta (ou 'sair' para encerrar): sair
Encerrando o programa.
```

---

## Fluxo de Funcionamento

```
┌─────────────────────────────────────────────────────────────┐
│                     FLUXO DO SISTEMA                        │
└─────────────────────────────────────────────────────────────┘

1. INGESTÃO (ingest.py)
   ├─ Carrega PDF (document.pdf)
   ├─ Divide em chunks (1000 chars, overlap 200)
   ├─ Gera embeddings (OpenAI text-embedding-3-small)
   └─ Armazena em PostgreSQL+pgvector

2. BUSCA (search.py)
   ├─ Recebe pergunta do usuário
   ├─ Cria embedding da pergunta
   ├─ Busca 10 resultados mais similares no DB
   ├─ Enriquece com contexto dos chunks
   └─ Envia para GPT-4 com prompt estruturado

3. RESPOSTA (chat.py)
   ├─ Apresenta 10 respostas numeradas
   ├─ Cada resposta baseada em um chunk relevante
   └─ Retorna ao usuário

```

---

## Configuração das Dependências

### Principais bibliotecas utilizadas:

| Biblioteca | Versão | Propósito |
|-----------|--------|----------|
| `langchain` | >=1.2.0 | Framework para aplicações com LLM |
| `langchain-openai` | >=1.2.0 | Integração com OpenAI |
| `langchain-postgres` | >=0.0.15 | Suporte a PostgreSQL como vector store |
| `langchain-community` | >=0.4.0 | Integrações comunitárias (PyPDFLoader) |
| `psycopg2-binary` | >=2.9.0 | Driver PostgreSQL |
| `pypdf` | >=3.0.0 | Processamento de PDFs |
| `python-dotenv` | >=1.0.0 | Carregamento de variáveis de ambiente |

---

## Solução de Problemas

### ❌ Erro: "Connection refused" ao conectar ao PostgreSQL

**Solução:**
```bash
# Verificar se Docker está rodando
docker ps

# Reiniciar os serviços
docker compose restart postgres

# Verificar logs
docker compose logs postgres
```

### ❌ Erro: "OPENAI_API_KEY not found"

**Solução:**
1. Verifique se o arquivo `.env` existe na raiz do projeto
2. Confirme que contém `OPENAI_API_KEY=sua_chave_aqui`
3. Recarregue o terminal ou IDE para aplicar as mudanças

### ❌ Erro: "ModuleNotFoundError"

**Solução:**
```bash
# Verificar se o ambiente virtual está ativado (deve ter "(venv)" no prompt)
# Se não, ativar:
source venv/bin/activate  # Linux/macOS

# Reinstalar dependências
pip install -r requirements.txt
```

### ❌ Erro: "document.pdf not found"

**Solução:**
1. Coloque o arquivo `document.pdf` na raiz do projeto
2. Certifique-se do nome e extensão corretos
3. O arquivo deve estar no mesmo diretório que `ingest.py`

### ⚠️ Aviso: Conexão lenta ou respostas atrasadas

**Soluções:**
- Verifique conexão com a internet
- Verifique limites de taxa da API OpenAI
- Considere aumentar `chunk_size` em `ingest.py` para chunks maiores

---

## Parar os Serviços

### Parar containers mantendo dados:
```bash
docker compose stop
```

### Parar e remover containers (mantém volumes):
```bash
docker compose down
```

### Remover tudo (incluindo dados do PostgreSQL):
```bash
docker compose down -v
```

---

## Desativar o Ambiente Virtual

```bash
deactivate
```

---

## Desenvolvimento e Customizações

### Modificar o prompt (search.py)
Para customizar como as respostas são geradas, edite a `prompt_template` na classe `Search`.

### Ajustar tamanho de chunks (ingest.py)
```python
RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Aumentar para contexto mais longo
    chunk_overlap=200,    # Aumentar para mais contexto sobreposto
    add_start_index=True
)
```

### Mudar modelo de embedding
```python
embedding = OpenAIEmbeddings(model="text-embedding-3-large")  # Mais preciso, mais caro
```

### Ajustar número de resultados
```python
search_kwargs={"k": 10}  # Mudar para número desejado de resultados
```

---

## Variáveis de Ambiente Completas

```env
# Chave de API OpenAI (obrigatória)
OPENAI_API_KEY=sk-...

# Configurações do PostgreSQL (opcionais, já estão nos valores padrão)
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=rag
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/rag
```

---

## Arquitetura Técnica

### Stack de Tecnologias:
- **Python 3.10+** - Linguagem de programação
- **LangChain** - Framework para orquestração
- **OpenAI API** - Embeddings e LLM
- **PostgreSQL 17** - Banco de dados
- **pgvector** - Extensão para buscas vetoriais
- **Docker Compose** - Containerização

### Modelos OpenAI Utilizados:
- `text-embedding-3-small` - Para gerar embeddings de documentos e perguntas
- `gpt-4-turbo` - Para gerar respostas contextalizadas

---

## Contribuições

Se encontrar bugs ou tiver sugestões de melhoria, considere:
1. Documentar o problema com detalhes
2. Testar em diferentes ambientes
3. Propor soluções

---

## Licença

Este projeto foi desenvolvido como desafio de estudos MBA.

---

## Suporte

Para dúvidas ou problemas:
1. Verifique a seção "Solução de Problemas"
2. Consulte a [documentação do LangChain](https://python.langchain.com/)
3. Verifique a [documentação da OpenAI](https://platform.openai.com/docs)
4. Consulte a [documentação do pgvector](https://github.com/pgvector/pgvector)

---

**Última atualização:** Maio 2026
