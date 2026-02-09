# 📁 Onde Estão os Arquivos - Super Sete

Mapa completo da estrutura de arquivos do projeto e suas responsabilidades.

## 🗂️ Estrutura Completa

```
AnalisePorPosicao-Super-Sete/
│
├── 📄 app.py                          # Aplicação Flask principal (porta 5057)
├── ⚙️ config.py                       # Configurações e constantes
├── 📦 requirements.txt                # Dependências Python
├── 🔒 .env.example                    # Exemplo de variáveis de ambiente
├── 🚫 .gitignore                      # Arquivos ignorados pelo Git
│
├── 📚 README.md                       # Documentação completa
├── 🚀 QUICKSTART.md                   # Guia rápido de início
├── 📥 DOWNLOAD.md                     # Guia de download de dados
├── 📁 ONDE-ESTAO-ARQUIVOS.md          # Este arquivo
│
├── 💾 database.db                     # Banco SQLite (criado automaticamente)
│
├── 📂 models/                         # Modelos de dados
│   ├── __init__.py
│   └── resultado_model.py             # Model para resultados da Super Sete
│
├── 📂 services/                       # Lógica de negócio
│   ├── __init__.py
│   ├── api_caixa_service.py          # Integração com API da Caixa
│   ├── estatistica_service.py        # Cálculos estatísticos
│   └── supersete_service.py          # Lógica de palpites
│
├── 📂 routes/                         # Rotas da aplicação
│   ├── __init__.py
│   ├── main_routes.py                # Rotas de páginas HTML
│   └── api_routes.py                 # Rotas da API REST
│
├── 📂 static/                         # Arquivos estáticos
│   ├── 📂 css/
│   │   └── styles.css                # Estilos (cores da Super Sete)
│   └── 📂 js/
│       └── scripts.js                # JavaScript interativo
│
└── 📂 templates/                      # Templates HTML
    ├── base.html                      # Template base
    ├── index.html                     # Página principal
    └── palpites.html                  # Página de palpites
```

## 📄 Descrição dos Arquivos

### 🔧 Arquivos de Configuração

#### `app.py`
**Responsabilidade:** Ponto de entrada da aplicação
- Cria a instância do Flask
- Registra os blueprints
- Inicia o servidor na porta 5057

**Quando modificar:**
- Adicionar novos blueprints
- Configurar middlewares
- Alterar configurações de inicialização

#### `config.py`
**Responsabilidade:** Centralize todas as configurações
- Define constantes da Super Sete (7 colunas, números 0-9)
- Carrega variáveis de ambiente
- Cores da identidade visual
- URLs da API

**Quando modificar:**
- Alterar configurações globais
- Adicionar novas constantes
- Mudar cores ou URLs

#### `requirements.txt`
**Responsabilidade:** Lista de dependências Python
```
Flask==3.0.0
requests==2.31.0
python-dotenv==1.0.0
```

**Quando modificar:**
- Adicionar nova biblioteca
- Atualizar versões

#### `.env.example`
**Responsabilidade:** Template de variáveis de ambiente
- Não contém valores sensíveis
- Serve como exemplo para criar o `.env`

**Quando modificar:**
- Adicionar nova variável de ambiente necessária

#### `.gitignore`
**Responsabilidade:** Define o que não vai para o Git
- Ignora `database.db`, `.env`, `__pycache__`, etc.

**Quando modificar:**
- Adicionar novos arquivos/pastas a ignorar

### 📚 Documentação

#### `README.md`
**Responsabilidade:** Documentação principal e completa
- Visão geral do projeto
- Instruções de instalação
- Como usar
- Documentação da API

#### `QUICKSTART.md`
**Responsabilidade:** Guia rápido para começar
- Passos mínimos para rodar o sistema
- Comandos básicos

#### `DOWNLOAD.md`
**Responsabilidade:** Guia de download de dados
- Como baixar dados da API
- Atualização e manutenção
- Solução de problemas

#### `ONDE-ESTAO-ARQUIVOS.md`
**Responsabilidade:** Este arquivo - mapa do projeto
- Estrutura de diretórios
- Descrição de cada arquivo
- Quando e como modificar

### 💾 Banco de Dados

#### `database.db`
**Responsabilidade:** Banco SQLite com todos os resultados
- Tabela `resultados` com dados de cada concurso
- Colunas separadas (coluna_1 a coluna_7)
- Criado automaticamente na primeira execução

**Localização dos dados:**
- Números sorteados: `coluna_1` até `coluna_7`
- Informações do concurso: `numero`, `data_apuracao`
- Premiação: `ganhadores_faixa_X`, `valor_premio_faixa_X`

### 📂 Models (Modelos de Dados)

#### `models/resultado_model.py`
**Responsabilidade:** Gerencia o banco de dados
- Cria a tabela de resultados
- Métodos CRUD (Create, Read, Update, Delete)
- `inserir()`: Salva novo concurso
- `buscar_ultimo()`: Retorna último resultado
- `buscar_todos()`: Lista resultados com paginação
- `buscar_por_numero()`: Busca concurso específico

**Quando modificar:**
- Adicionar novos campos na tabela
- Criar novos métodos de consulta
- Otimizar queries

### 📂 Services (Lógica de Negócio)

#### `services/api_caixa_service.py`
**Responsabilidade:** Integração com API da Caixa
- `buscar_ultimo_concurso()`: GET na API
- `buscar_concurso_especifico(numero)`: Busca por número
- `atualizar_base_completa()`: Atualização incremental

**Quando modificar:**
- API da Caixa mudar
- Adicionar cache
- Melhorar tratamento de erros

#### `services/estatistica_service.py`
**Responsabilidade:** Cálculos estatísticos por coluna
- `calcular_frequencia_por_coluna()`: Conta aparições
- `calcular_atrasos_por_coluna()`: Calcula atrasos
- `calcular_numeros_mais_frequentes_por_coluna()`: Top números
- `calcular_pares_impares_por_coluna()`: Distribuição
- `calcular_sequencias_comuns()`: Padrões

**Quando modificar:**
- Adicionar novas estatísticas
- Otimizar cálculos
- Implementar cache

#### `services/supersete_service.py`
**Responsabilidade:** Geração de palpites
- `gerar_palpite()`: Cria jogos com base em estratégia
- Estratégias: equilibrada, agressiva, conservadora, mista, atrasados, aleatorio_inteligente
- `conferir_palpite()`: Compara com resultado oficial

**Quando modificar:**
- Adicionar novas estratégias
- Melhorar algoritmos
- Ajustar pesos e probabilidades

### 📂 Routes (Rotas)

#### `routes/main_routes.py`
**Responsabilidade:** Rotas que retornam HTML
- `GET /`: Página inicial (index.html)
- `GET /palpites`: Página de palpites (palpites.html)

**Quando modificar:**
- Adicionar novas páginas
- Passar dados para templates

#### `routes/api_routes.py`
**Responsabilidade:** API REST (retorna JSON)
- `POST /api/atualizar`: Atualiza dados
- `GET /api/ultimo-resultado`: Último concurso
- `GET /api/resultados`: Lista concursos
- `GET /api/resultado/<numero>`: Concurso específico
- `GET /api/estatisticas`: Todas estatísticas
- `GET /api/estatisticas/coluna/<numero>`: Stats de uma coluna
- `POST /api/gerar-palpite`: Gera jogos
- `POST /api/conferir`: Confere palpite

**Quando modificar:**
- Adicionar novos endpoints
- Modificar validações
- Mudar formato de resposta

### 📂 Static (Arquivos Estáticos)

#### `static/css/styles.css`
**Responsabilidade:** Estilos visuais do sistema
- Cores da Super Sete (#A9CF46)
- Grid de 7 colunas
- Heatmap de frequências
- Design responsivo

**Quando modificar:**
- Alterar cores ou layout
- Adicionar novos componentes visuais
- Melhorar responsividade

#### `static/js/scripts.js`
**Responsabilidade:** Interatividade do frontend
- Requisições à API via fetch
- Atualização dinâmica de dados
- Geração e exibição de palpites
- Conferência de jogos
- Criação do heatmap

**Quando modificar:**
- Adicionar novas funcionalidades
- Melhorar UX
- Integrar com novos endpoints

### 📂 Templates (HTML)

#### `templates/base.html`
**Responsabilidade:** Template base para todas as páginas
- Header com logo
- Menu de navegação
- Footer
- Imports de CSS e JS

**Quando modificar:**
- Alterar header/footer global
- Adicionar meta tags
- Mudar estrutura base

#### `templates/index.html`
**Responsabilidade:** Página principal de estatísticas
- Último resultado (7 colunas)
- Heatmap de frequências
- Estatísticas por coluna
- Botão de atualizar dados

**Quando modificar:**
- Adicionar novas visualizações
- Reorganizar layout
- Mostrar mais estatísticas

#### `templates/palpites.html`
**Responsabilidade:** Página de palpites
- Formulário de geração (estratégia + quantidade)
- Exibição dos palpites gerados
- Conferência de jogos (7 inputs)
- Resultado da conferência

**Quando modificar:**
- Adicionar novas estratégias
- Melhorar exibição de palpites
- Adicionar features de conferência

## 🔄 Fluxo de Dados

### Atualização de Dados
```
API Caixa → api_caixa_service → resultado_model → database.db
```

### Geração de Palpites
```
database.db → resultado_model → estatistica_service → supersete_service → API response
```

### Visualização
```
database.db → resultado_model → routes → templates → browser
```

## 🎯 Onde Fazer Mudanças Comuns

### Adicionar Nova Estatística
1. `services/estatistica_service.py`: Adicionar método de cálculo
2. `routes/api_routes.py`: Criar endpoint se necessário
3. `static/js/scripts.js`: Adicionar função de exibição
4. `templates/index.html`: Adicionar visualização

### Adicionar Nova Estratégia de Palpite
1. `config.py`: Adicionar nome na lista ESTRATEGIAS
2. `services/supersete_service.py`: Implementar método
3. `templates/palpites.html`: Adicionar no select

### Mudar Layout/Cores
1. `static/css/styles.css`: Modificar estilos
2. `config.py`: Alterar constantes de cores se necessário

### Adicionar Nova Página
1. `templates/nova_pagina.html`: Criar template
2. `routes/main_routes.py`: Adicionar rota
3. `templates/base.html`: Adicionar link no menu

## 📞 Precisa de Ajuda?

- **Não sabe onde fazer uma mudança?** Consulte este arquivo
- **Erro em algum arquivo?** Verifique a responsabilidade descrita
- **Quer adicionar feature?** Siga o fluxo de dados

---

**Mantenha este arquivo atualizado ao modificar a estrutura do projeto! 📁**
