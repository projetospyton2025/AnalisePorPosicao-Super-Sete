# Sistema de Análise por Posição - SUPER SETE

Sistema completo de análise estatística e geração inteligente de palpites para a loteria **Super Sete** da Caixa Econômica Federal.

![Super Sete](https://i.postimg.cc/wBthkvvc/supersete.png)

## 📋 Sobre a Super Sete

A Super Sete é uma modalidade única de loteria que consiste em:

- **7 colunas independentes**, cada uma com números de **0 a 9**
- Um número é sorteado por coluna em cada concurso
- Prêmios para quem acertar 3, 4, 5, 6 ou 7 colunas
- Sorteios realizados pela Caixa Econômica Federal

### Diferencial deste Sistema

Este sistema realiza **análise por coluna**, reconhecendo que cada coluna da Super Sete é independente e possui suas próprias estatísticas e padrões.

## ✨ Funcionalidades

### 📊 Análise Estatística Completa

- **Frequência por coluna**: Quantas vezes cada número (0-9) apareceu em cada coluna
- **Atrasos por coluna**: Há quantos concursos cada número não aparece em cada coluna
- **Heatmap visual**: Visualização gráfica das frequências em formato de matriz 7x10
- **Números quentes e frios**: Identifica os números mais e menos frequentes por coluna
- **Distribuição pares/ímpares**: Análise da distribuição por coluna
- **Padrões e sequências**: Identifica combinações que aparecem com frequência

### 🎲 Geração Inteligente de Palpites

O sistema oferece **6 estratégias diferentes**:

1. **Equilibrada** 🎯: Combina números frequentes e atrasados
2. **Agressiva** 🔥: Prioriza números mais frequentes
3. **Conservadora** ❄️: Foca em números atrasados
4. **Mista** 🎨: Alterna estratégias por coluna
5. **Atrasados** ⏰: Apenas números com maior atraso
6. **Aleatório Inteligente** 🎰: Sorteio ponderado por frequência

### ✅ Conferência de Palpites

- Confira seus jogos com resultados oficiais
- Veja quantas colunas acertou
- Identifique em qual faixa de premiação você se enquadraria
- Análise detalhada coluna por coluna

### 🔄 Atualização Automática

- Integração direta com a API oficial da Caixa
- Atualização incremental (apenas novos concursos)
- Dados sempre atualizados e precisos

## 🚀 Instalação

### Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone o repositório**:
```bash
git clone https://github.com/projetospyton2025/AnalisePorPosicao-Super-Sete.git
cd AnalisePorPosicao-Super-Sete
```

2. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente** (opcional):
```bash
cp .env.example .env
# Edite o arquivo .env se necessário
```

4. **Inicie o servidor**:
```bash
python app.py
```

5. **Acesse o sistema**:
```
http://localhost:5057
```

## 📖 Como Usar

### Interface Web

1. **Página Inicial (Estatísticas)**
   - Visualize o último resultado
   - Veja o heatmap de frequências
   - Analise estatísticas detalhadas por coluna
   - Clique em "Atualizar Dados" para buscar novos concursos

2. **Página de Palpites**
   - Escolha uma estratégia
   - Defina a quantidade de jogos (1-100)
   - Clique em "Gerar Palpites"
   - Confira seus próprios palpites inserindo os números

### API REST

O sistema também oferece uma API REST completa:

#### Endpoints Disponíveis

**Atualizar Dados**
```bash
POST /api/atualizar
```

**Último Resultado**
```bash
GET /api/ultimo-resultado
```

**Listar Resultados**
```bash
GET /api/resultados?limite=10
```

**Buscar Concurso Específico**
```bash
GET /api/resultado/728
```

**Estatísticas Completas**
```bash
GET /api/estatisticas
```

**Estatísticas de Uma Coluna**
```bash
GET /api/estatisticas/coluna/1
```

**Gerar Palpites**
```bash
POST /api/gerar-palpite
Content-Type: application/json

{
  "estrategia": "equilibrada",
  "quantidade_jogos": 3
}
```

**Conferir Palpite**
```bash
POST /api/conferir
Content-Type: application/json

{
  "palpite": [5, 0, 2, 3, 9, 8, 1],
  "numero_concurso": 728
}
```

## 🏗️ Arquitetura

### Backend (Python/Flask)

```
├── app.py                      # Aplicação Flask principal
├── config.py                   # Configurações
├── models/
│   └── resultado_model.py     # Model SQLite
├── services/
│   ├── api_caixa_service.py   # API da Caixa
│   ├── estatistica_service.py # Cálculos estatísticos
│   └── supersete_service.py   # Geração de palpites
└── routes/
    ├── main_routes.py         # Rotas HTML
    └── api_routes.py          # Rotas API REST
```

### Frontend (HTML/CSS/JavaScript)

```
├── static/
│   ├── css/
│   │   └── styles.css         # Estilos com cores da Super Sete
│   └── js/
│       └── scripts.js         # Lógica interativa
└── templates/
    ├── base.html              # Template base
    ├── index.html             # Página de estatísticas
    └── palpites.html          # Página de palpites
```

### Banco de Dados

SQLite com tabela `resultados` contendo:
- Dados completos de cada concurso
- 7 colunas separadas (coluna_1 a coluna_7)
- Informações de premiação
- Metadados do sorteio

## 🎨 Identidade Visual

O sistema usa a paleta oficial da Super Sete:

- **Cor Principal**: `#A9CF46` (verde-limão)
- **Gradientes**: Do verde claro ao verde escuro
- **Logo Oficial**: Integrada no header

## 📊 Estratégias de Palpites

### Como Funcionam

Cada estratégia analisa as estatísticas históricas **por coluna** para gerar palpites inteligentes:

- **Equilibrada**: Para cada coluna, alterna entre um número frequente e um atrasado
- **Agressiva**: Escolhe entre os 5 números mais frequentes de cada coluna
- **Conservadora**: Escolhe entre os 5 números mais atrasados de cada coluna
- **Mista**: Usa uma estratégia aleatória para cada coluna
- **Atrasados**: Foca nos 3 números com maior atraso por coluna
- **Aleatório Inteligente**: Sorteia com probabilidade proporcional à frequência

### Personalização

É possível definir estratégias diferentes para cada coluna via API:

```json
{
  "estrategias_por_coluna": {
    "coluna_1": "agressiva",
    "coluna_2": "conservadora",
    "coluna_3": "equilibrada",
    "coluna_4": "atrasados",
    "coluna_5": "mista",
    "coluna_6": "aleatorio_inteligente",
    "coluna_7": "agressiva"
  }
}
```

## 🔧 Tecnologias Utilizadas

- **Backend**: Python 3, Flask
- **Banco de Dados**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **API Externa**: API oficial da Caixa Econômica Federal
- **Versionamento**: Git

## ⚠️ Avisos Importantes

1. **Este sistema é apenas para fins educacionais e de entretenimento**
2. Não há garantia de acertos - a loteria é baseada em sorteio aleatório
3. Jogue com responsabilidade
4. O sistema usa dados reais, mas análises estatísticas não garantem resultados futuros

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer um fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abrir um Pull Request

## 📞 Suporte

Se encontrar algum problema ou tiver sugestões:

- Abra uma [issue](https://github.com/projetospyton2025/AnalisePorPosicao-Super-Sete/issues)
- Entre em contato através do GitHub

## 🔗 Links Úteis

- [API Oficial da Caixa](https://servicebus2.caixa.gov.br/portaldeloterias/api/supersete)
- [Super Sete - Site Oficial](https://loterias.caixa.gov.br/Paginas/Super-Sete.aspx)
- [Documentação Flask](https://flask.palletsprojects.com/)

---

**Desenvolvido com 💚 por projetospyton2025**

*Última atualização: Fevereiro 2025*
