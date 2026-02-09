# 🚀 Guia Rápido - Super Sete

Comece a usar o sistema em 5 minutos!

## ⚡ Instalação Rápida

### 1. Clone e Entre no Diretório
```bash
git clone https://github.com/projetospyton2025/AnalisePorPosicao-Super-Sete.git
cd AnalisePorPosicao-Super-Sete
```

### 2. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 3. Inicie o Servidor
```bash
python app.py
```

### 4. Acesse o Sistema
Abra seu navegador em: **http://localhost:5057**

## 📥 Primeiro Uso

### Atualizar Base de Dados

Ao acessar o sistema pela primeira vez, você precisa baixar os dados históricos:

1. Na página inicial, clique no botão **"🔄 Atualizar Dados"**
2. Aguarde alguns segundos enquanto o sistema busca os concursos da API da Caixa
3. Pronto! Os dados estão carregados

**Via linha de comando:**
```bash
curl -X POST http://localhost:5057/api/atualizar
```

## 🎯 Como Usar

### Ver Estatísticas

1. Acesse a página inicial (`http://localhost:5057`)
2. Veja:
   - Último resultado sorteado
   - Heatmap de frequências
   - Estatísticas detalhadas por coluna

### Gerar Palpites

1. Acesse **Palpites** no menu
2. Escolha uma estratégia
3. Defina quantos jogos quer gerar (1-100)
4. Clique em **"✨ Gerar Palpites"**

### Conferir Palpites

1. Na página de **Palpites**, role até "Conferir Palpite"
2. Digite os 7 números do seu jogo (um por coluna)
3. Opcionalmente, informe o número do concurso
4. Clique em **"🔍 Conferir Palpite"**

## 🔧 Configuração (Opcional)

Se quiser personalizar o sistema:

1. Copie o arquivo de exemplo:
```bash
cp .env.example .env
```

2. Edite o `.env` com suas preferências:
```bash
# Porta do servidor (padrão: 5057)
PORT=5057

# Modo debug
DEBUG=True

# Outras configurações...
```

## 📊 Comandos Úteis via API

### Buscar último resultado
```bash
curl http://localhost:5057/api/ultimo-resultado
```

### Ver estatísticas de uma coluna
```bash
curl http://localhost:5057/api/estatisticas/coluna/1
```

### Gerar palpite
```bash
curl -X POST http://localhost:5057/api/gerar-palpite \
  -H "Content-Type: application/json" \
  -d '{"estrategia": "equilibrada", "quantidade_jogos": 3}'
```

## 🐛 Solução de Problemas

### Porta já em uso
Se a porta 5057 já estiver em uso, mude no `.env`:
```
PORT=5058
```

### Erro ao conectar com a API
Verifique sua conexão com a internet. O sistema precisa acessar a API da Caixa.

### Banco de dados vazio
Execute a atualização:
```bash
curl -X POST http://localhost:5057/api/atualizar
```

## 📚 Próximos Passos

- Leia o [README.md](README.md) completo para mais detalhes
- Veja [DOWNLOAD.md](DOWNLOAD.md) para informações sobre download de dados
- Consulte [ONDE-ESTAO-ARQUIVOS.md](ONDE-ESTAO-ARQUIVOS.md) para entender a estrutura

## ⚠️ Lembre-se

- Este sistema é para fins educacionais e de entretenimento
- Jogue com responsabilidade
- Não há garantia de acertos

---

**Pronto! Você já pode usar o sistema! 🎉**
