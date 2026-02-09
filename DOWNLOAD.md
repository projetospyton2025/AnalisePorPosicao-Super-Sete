# 📥 Guia de Download de Dados - Super Sete

Este guia explica como baixar e atualizar os dados históricos da Super Sete.

## 🔄 Métodos de Atualização

### Método 1: Via Interface Web (Recomendado)

1. Acesse o sistema em `http://localhost:5057`
2. Na página inicial, clique no botão **"🔄 Atualizar Dados"**
3. Aguarde o processo de atualização
4. Uma mensagem confirmará quantos concursos foram baixados

**Vantagens:**
- Simples e visual
- Feedback em tempo real
- Não requer conhecimento técnico

### Método 2: Via API REST

```bash
curl -X POST http://localhost:5057/api/atualizar
```

**Resposta esperada:**
```json
{
  "sucesso": true,
  "dados": {
    "concursos_inseridos": 50,
    "concursos_atualizados": 0,
    "erros": 0,
    "ultimo_concurso": 728
  }
}
```

### Método 3: Via Python Script

Crie um script `atualizar.py`:

```python
import requests

response = requests.post('http://localhost:5057/api/atualizar')
resultado = response.json()

if resultado['sucesso']:
    print(f"✅ Sucesso!")
    print(f"Concursos inseridos: {resultado['dados']['concursos_inseridos']}")
    print(f"Último concurso: {resultado['dados']['ultimo_concurso']}")
else:
    print(f"❌ Erro: {resultado['erro']}")
```

Execute:
```bash
python atualizar.py
```

## 📊 Como Funciona

### Processo de Atualização

1. **Busca o último concurso na API da Caixa**
   - URL: `https://servicebus2.caixa.gov.br/portaldeloterias/api/supersete`

2. **Compara com o banco de dados local**
   - Verifica qual é o último concurso salvo

3. **Baixa apenas os concursos novos**
   - Atualização incremental
   - Não duplica dados existentes
   - Economiza tempo e banda

4. **Salva no SQLite**
   - Armazena todos os dados do concurso
   - Separa as 7 colunas individualmente
   - Mantém histórico completo

### Estrutura dos Dados

Cada concurso salvo contém:

```python
{
  "numero": 728,                    # Número do concurso
  "data_apuracao": "04/08/2025",    # Data do sorteio
  "coluna_1": 5,                     # Número da coluna 1
  "coluna_2": 0,                     # Número da coluna 2
  "coluna_3": 2,                     # Número da coluna 3
  "coluna_4": 3,                     # Número da coluna 4
  "coluna_5": 9,                     # Número da coluna 5
  "coluna_6": 8,                     # Número da coluna 6
  "coluna_7": 1,                     # Número da coluna 7
  "acumulado": 1,                    # 0 ou 1
  "valor_acumulado": 4568897.38,    # Valor acumulado
  # ... outros campos de premiação
}
```

## ⏰ Quando Atualizar

### Recomendações

- **Antes de gerar palpites**: Sempre tenha os dados mais recentes
- **Após cada sorteio**: Geralmente às segundas, quartas e sextas
- **Periodicidade**: Pelo menos uma vez por semana
- **Primeira vez**: Obrigatório ao instalar o sistema

### Automação (Opcional)

Você pode criar um cron job ou task scheduler para atualizar automaticamente:

**Linux/Mac (crontab):**
```bash
# Atualizar toda segunda, quarta e sexta às 21h
0 21 * * 1,3,5 curl -X POST http://localhost:5057/api/atualizar
```

**Windows (Task Scheduler):**
1. Abra o Agendador de Tarefas
2. Crie uma nova tarefa
3. Defina o gatilho (segundas, quartas e sextas)
4. Ação: executar script Python de atualização

## 🔍 Verificar Dados

### Ver Último Resultado

**Via Web:**
- Acesse a página inicial
- O último resultado é exibido no topo

**Via API:**
```bash
curl http://localhost:5057/api/ultimo-resultado
```

### Contar Total de Concursos

**Via API:**
```bash
curl http://localhost:5057/api/estatisticas
```

Procure por: `"total_concursos"`

### Listar Últimos N Resultados

**Via API:**
```bash
# Últimos 10 concursos
curl http://localhost:5057/api/resultados?limite=10
```

## 🚨 Solução de Problemas

### Erro: "Nenhum resultado encontrado"

**Causa:** Banco de dados vazio
**Solução:** Execute a atualização pela primeira vez

### Erro: "Timeout" ou "Connection Error"

**Causa:** Problema de conexão com a API da Caixa
**Possíveis soluções:**
1. Verifique sua conexão com a internet
2. Tente novamente em alguns minutos
3. Verifique se a API da Caixa está online

### Erro: "Database locked"

**Causa:** Múltiplos processos tentando acessar o banco simultaneamente
**Solução:** 
1. Feche outras instâncias do sistema
2. Aguarde processos em andamento finalizarem
3. Reinicie o servidor

### Dados Inconsistentes

**Solução drástica (apaga tudo e baixa novamente):**
```bash
# ⚠️ ATENÇÃO: Isso apaga o banco de dados!
rm database.db
python app.py
# Depois faça a atualização
```

## 📈 Estatísticas de Download

Após atualizar, você pode ver:

- **Total de concursos**: Quantos sorteios estão no banco
- **Último concurso**: Número do concurso mais recente
- **Concursos inseridos**: Quantos foram baixados agora
- **Erros**: Se houve algum problema

## 💡 Dicas

1. **Mantenha atualizado**: Dados recentes = estatísticas mais precisas
2. **Backup regular**: Copie o `database.db` periodicamente
3. **Não interrompa**: Deixe o processo terminar completamente
4. **Monitore logs**: Em caso de erro, verifique as mensagens no console

## 🔗 API da Caixa

O sistema usa a API oficial:

- **Endpoint:** `https://servicebus2.caixa.gov.br/portaldeloterias/api/supersete`
- **Último concurso:** GET `/supersete`
- **Concurso específico:** GET `/supersete/{numero}`
- **Formato:** JSON
- **Sem autenticação:** API pública

## 📞 Suporte

Se tiver problemas com o download:

1. Verifique o console do servidor para mensagens de erro
2. Consulte os logs da aplicação
3. Abra uma issue no GitHub
4. Verifique se sua conexão permite acesso à API da Caixa

---

**Mantenha seus dados sempre atualizados! 📊**
