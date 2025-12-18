# Calculadora de Juros Compostos (Flet)

Aplicação simples em Flet que calcula a evolução de um investimento com aportes mensais e capitalização mensal.

Funcionalidades
- Entradas: capital inicial, aporte mensal, taxa anual (%), período (anos)
- Cálculo mês a mês
- Gráfico da evolução (matplotlib) exibido na interface
- Tabela com saldo ao final de cada ano
- Exportar resultados para CSV (`calculadora_juros_result.csv`)

Como executar
1. Instale dependências: `pip install flet matplotlib`
2. Execute: `python exercicios_flet/calculadora_juros/main.py`

Observações
- A exportação gera um CSV no diretório atual.
- Se quiser adaptar para outros períodos de capitalização é só alterar a função `calcular_historico`.
