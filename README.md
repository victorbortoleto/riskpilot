# RiskPilot MVP

Dashboard inicial para análise de trading, gerenciamento de risco e curva de capital.

## O que essa versão faz

- Importa arquivos CSV e XLSX
- Tenta reconhecer automaticamente colunas comuns
- Normaliza os dados para um modelo padrão
- Calcula:
  - Net P&L
  - Winrate
  - Profit Factor
  - Max Drawdown
  - Média de ganhos
  - Média de perdas
  - Sequência máxima de perdas
  - Sequência máxima de ganhos
- Mostra:
  - curva de capital
  - resultado por dia
  - resultado por ativo
  - tabela normalizada
  - alertas simples de risco

## Como rodar

1. Instale o Python 3.10 ou superior.
2. Abra o terminal dentro da pasta do projeto.
3. Rode:

```bash
pip install -r requirements.txt
streamlit run app.py
```

4. O navegador vai abrir com o dashboard.

## Arquivo de exemplo

Use o arquivo `sample_trades.csv` para testar.

## Observação

Essa é uma versão MVP. A compatibilidade com plataformas reais melhora conforme você adiciona exemplos reais de exportação.
