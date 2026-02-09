// Scripts do Sistema de Análise Super Sete

// Utilitários
const API_BASE = '/api';

// Função para fazer requisições à API
async function apiRequest(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, options);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Erro na requisição:', error);
        return { sucesso: false, erro: error.message };
    }
}

// Função para mostrar loading
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.classList.add('active');
    }
}

// Função para esconder loading
function hideLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.classList.remove('active');
    }
}

// Função para mostrar alertas
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Remover após 5 segundos
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
}

// Função para atualizar dados
async function atualizarDados() {
    showLoading('loading');
    
    const resultado = await apiRequest('/atualizar', {
        method: 'POST'
    });
    
    hideLoading('loading');
    
    if (resultado.sucesso) {
        showAlert(`Dados atualizados! ${resultado.dados.concursos_inseridos} novos concursos.`, 'success');
        
        // Recarregar página após atualização
        setTimeout(() => {
            window.location.reload();
        }, 1500);
    } else {
        showAlert(`Erro ao atualizar: ${resultado.erro}`, 'error');
    }
}

// Função para carregar último resultado
async function carregarUltimoResultado() {
    const resultado = await apiRequest('/ultimo-resultado');
    
    if (resultado.sucesso && resultado.dados) {
        const dados = resultado.dados;
        
        // Atualizar informações do concurso
        document.getElementById('concurso-numero').textContent = dados.numero;
        document.getElementById('concurso-data').textContent = dados.data_apuracao;
        
        // Atualizar grid de colunas
        for (let i = 1; i <= 7; i++) {
            const elemento = document.getElementById(`coluna-${i}`);
            if (elemento) {
                elemento.textContent = dados[`coluna_${i}`];
            }
        }
        
        // Atualizar informações de prêmio
        const acumulado = dados.acumulado ? 'Sim' : 'Não';
        document.getElementById('acumulado').textContent = acumulado;
        
        const valorAcumulado = new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        }).format(dados.valor_acumulado_proximo_concurso || 0);
        document.getElementById('valor-acumulado').textContent = valorAcumulado;
    }
}

// Função para carregar estatísticas
async function carregarEstatisticas() {
    const resultado = await apiRequest('/estatisticas');
    
    if (resultado.sucesso && resultado.dados) {
        const stats = resultado.dados;
        
        // Atualizar total de concursos
        document.getElementById('total-concursos').textContent = stats.total_concursos;
        
        // Criar heatmap de frequências
        criarHeatmap(stats.frequencia_por_coluna);
        
        // Mostrar números mais frequentes e atrasados
        mostrarEstatisticasPorColuna(stats);
    }
}

// Função para criar heatmap de frequências
/**
 * Cria um heatmap visual mostrando a frequência de cada número em cada coluna.
 * 
 * @param {Object} frequencias - Objeto com estrutura:
 *   {
 *     "coluna_1": {"0": freq, "1": freq, ..., "9": freq},
 *     "coluna_2": {...},
 *     ...
 *     "coluna_7": {...}
 *   }
 * 
 * Visual encoding:
 * - freq-low: intensidade 0-33% (cor mais clara)
 * - freq-medium: intensidade 34-66% (cor média)
 * - freq-high: intensidade 67-100% (cor mais escura/destaque)
 */
function criarHeatmap(frequencias) {
    const heatmapContainer = document.getElementById('heatmap-container');
    if (!heatmapContainer) return;
    
    // Limpar container
    heatmapContainer.innerHTML = '';
    
    // Criar grid
    const grid = document.createElement('div');
    grid.className = 'frequencia-grid';
    
    // Header da linha (números 0-9)
    grid.appendChild(createCell('', 'freq-header'));
    for (let num = 0; num <= 9; num++) {
        grid.appendChild(createCell(num, 'freq-header'));
    }
    
    // Encontrar máximo e mínimo para normalizar cores
    let maxFreq = 0;
    let minFreq = Infinity;
    
    for (let coluna = 1; coluna <= 7; coluna++) {
        const freqColuna = frequencias[`coluna_${coluna}`];
        for (let num = 0; num <= 9; num++) {
            const freq = freqColuna[num] || 0;
            maxFreq = Math.max(maxFreq, freq);
            minFreq = Math.min(minFreq, freq);
        }
    }
    
    // Linhas (uma por coluna)
    for (let coluna = 1; coluna <= 7; coluna++) {
        // Header da coluna
        grid.appendChild(createCell(`Col ${coluna}`, 'freq-header'));
        
        const freqColuna = frequencias[`coluna_${coluna}`];
        
        // Células de frequência
        for (let num = 0; num <= 9; num++) {
            const freq = freqColuna[num] || 0;
            const cell = createCell(freq, 'freq-cell');
            
            // Adicionar classe de intensidade
            const intensidade = (freq - minFreq) / (maxFreq - minFreq);
            if (intensidade > 0.66) {
                cell.classList.add('freq-high');
            } else if (intensidade > 0.33) {
                cell.classList.add('freq-medium');
            } else {
                cell.classList.add('freq-low');
            }
            
            cell.title = `Número ${num} na coluna ${coluna}: ${freq} vezes`;
            grid.appendChild(cell);
        }
    }
    
    heatmapContainer.appendChild(grid);
}

// Função auxiliar para criar células
function createCell(content, className) {
    const cell = document.createElement('div');
    cell.className = className;
    cell.textContent = content;
    return cell;
}

// Função para mostrar estatísticas por coluna
function mostrarEstatisticasPorColuna(stats) {
    const container = document.getElementById('stats-por-coluna');
    if (!container) return;
    
    container.innerHTML = '';
    
    for (let coluna = 1; coluna <= 7; coluna++) {
        const colDiv = document.createElement('div');
        colDiv.className = 'card';
        
        const maisFrequentes = stats.mais_frequentes_por_coluna[`coluna_${coluna}`] || [];
        const maisAtrasados = stats.mais_atrasados_por_coluna[`coluna_${coluna}`] || [];
        const paresImpares = stats.pares_impares_por_coluna[`coluna_${coluna}`] || {};
        
        colDiv.innerHTML = `
            <h3>Coluna ${coluna}</h3>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-label">Mais Frequente</div>
                    <div class="stat-value">${maisFrequentes[0] ? maisFrequentes[0][0] : '-'}</div>
                    <div class="stat-label">${maisFrequentes[0] ? maisFrequentes[0][1] + ' vezes' : ''}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Mais Atrasado</div>
                    <div class="stat-value">${maisAtrasados[0] ? maisAtrasados[0][0] : '-'}</div>
                    <div class="stat-label">${maisAtrasados[0] ? maisAtrasados[0][1] + ' concursos' : ''}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Pares</div>
                    <div class="stat-value">${paresImpares.pares || 0}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Ímpares</div>
                    <div class="stat-value">${paresImpares.impares || 0}</div>
                </div>
            </div>
        `;
        
        container.appendChild(colDiv);
    }
}

// Função para gerar palpites
async function gerarPalpites() {
    const estrategia = document.getElementById('estrategia').value;
    const quantidade = parseInt(document.getElementById('quantidade').value);
    
    if (quantidade < 1 || quantidade > 100) {
        showAlert('Quantidade deve estar entre 1 e 100', 'error');
        return;
    }
    
    showLoading('loading-palpites');
    
    const resultado = await apiRequest('/gerar-palpite', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            estrategia: estrategia,
            quantidade_jogos: quantidade
        })
    });
    
    hideLoading('loading-palpites');
    
    if (resultado.sucesso) {
        mostrarPalpites(resultado.palpites);
    } else {
        showAlert(`Erro ao gerar palpites: ${resultado.erro}`, 'error');
    }
}

// Função para mostrar palpites
function mostrarPalpites(palpites) {
    const container = document.getElementById('palpites-container');
    if (!container) return;
    
    container.innerHTML = '';
    
    palpites.forEach((palpite, index) => {
        const palpiteDiv = document.createElement('div');
        palpiteDiv.className = 'palpite-item';
        
        const colunasHtml = palpite.map((numero, idx) => `
            <div class="coluna-item">
                <h3>Col ${idx + 1}</h3>
                <div class="coluna-numero">${numero}</div>
            </div>
        `).join('');
        
        palpiteDiv.innerHTML = `
            <div class="palpite-header">
                <div class="palpite-numero">Jogo ${index + 1}</div>
            </div>
            <div class="colunas-grid">
                ${colunasHtml}
            </div>
        `;
        
        container.appendChild(palpiteDiv);
    });
}

// Função para conferir palpite
async function conferirPalpite() {
    const palpite = [];
    
    // Coletar números do palpite
    for (let i = 1; i <= 7; i++) {
        const valor = parseInt(document.getElementById(`palpite-col-${i}`).value);
        if (isNaN(valor) || valor < 0 || valor > 9) {
            showAlert(`Valor inválido na coluna ${i}. Deve estar entre 0 e 9.`, 'error');
            return;
        }
        palpite.push(valor);
    }
    
    const numeroConcurso = document.getElementById('numero-concurso').value;
    
    showLoading('loading-conferencia');
    
    const body = { palpite: palpite };
    if (numeroConcurso) {
        body.numero_concurso = parseInt(numeroConcurso);
    }
    
    const resultado = await apiRequest('/conferir', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    });
    
    hideLoading('loading-conferencia');
    
    if (resultado.sucesso) {
        mostrarResultadoConferencia(resultado);
    } else {
        showAlert(`Erro ao conferir: ${resultado.erro}`, 'error');
    }
}

// Função para mostrar resultado da conferência
function mostrarResultadoConferencia(resultado) {
    const container = document.getElementById('resultado-conferencia');
    if (!container) return;
    
    const conferencia = resultado.conferencia;
    const detalhesHtml = conferencia.detalhes.map(detalhe => `
        <div class="detalhe-coluna ${detalhe.acertou ? 'acertou' : 'errou'}">
            <div><strong>Col ${detalhe.coluna}</strong></div>
            <div>Seu: ${detalhe.palpite}</div>
            <div>Sorteado: ${detalhe.resultado}</div>
            <div>${detalhe.acertou ? '✓' : '✗'}</div>
        </div>
    `).join('');
    
    let faixaTexto = '';
    if (conferencia.faixa_premiacao) {
        const faixas = {
            1: '🏆 7 acertos - PRÊMIO MÁXIMO!',
            2: '🎉 6 acertos - Faixa 2',
            3: '👏 5 acertos - Faixa 3',
            4: '👍 4 acertos - Faixa 4',
            5: '😊 3 acertos - Faixa 5'
        };
        faixaTexto = `<div style="text-align: center; font-size: 1.2rem; margin: 1rem 0; color: var(--cor-sucesso);">
            ${faixas[conferencia.faixa_premiacao] || ''}
        </div>`;
    }
    
    container.innerHTML = `
        <div class="conferencia-resultado">
            <div class="acertos-info">
                Você acertou ${conferencia.total_acertos} de 7 números
            </div>
            ${faixaTexto}
            <div style="text-align: center; margin-bottom: 1rem;">
                Concurso ${resultado.concurso} - ${resultado.data}
            </div>
            <div class="detalhes-conferencia">
                ${detalhesHtml}
            </div>
        </div>
    `;
    
    container.style.display = 'block';
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Carregar dados na página inicial
    if (document.getElementById('ultimo-resultado')) {
        carregarUltimoResultado();
        carregarEstatisticas();
    }
    
    // Event listeners are handled via onclick attributes in HTML
    // to avoid duplicate handlers
});
