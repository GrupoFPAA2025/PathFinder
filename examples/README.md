# Exemplos de Labirintos

Esta pasta contém exemplos de labirintos em diferentes formatos para demonstração e teste do algoritmo PathFinder.

## Formatos dos Arquivos

Os arquivos de labirinto seguem o seguinte formato:
- `S`: Ponto inicial
- `E`: Ponto final
- `0`: Caminho livre (custo 1.0)
- `1`: Terreno difícil (custo 2.0)
- `2`: Terreno muito difícil (custo 3.0)
- `3`: Terreno extremamente difícil (custo 4.0)
- `#`: Obstáculo (impassável)

## Exemplos Disponíveis

1. `simple_maze.txt`: Labirinto simples com caminho direto
2. `weighted_maze.txt`: Labirinto com diferentes tipos de terreno
3. `no_solution_maze.txt`: Labirinto sem solução possível

## Como Usar

Você pode usar estes exemplos para:
- Testar o algoritmo A*
- Verificar o comportamento com diferentes tipos de terreno
- Demonstrar casos de borda
- Testar a interface gráfica

Para carregar um exemplo na interface gráfica, use a opção "Carregar Labirinto" e selecione um dos arquivos desta pasta. 