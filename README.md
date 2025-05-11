# 🎯 PathFinder - Resolve o Labirinto 2D com o Algoritmo A*

## 📝 Descrição do Projeto

Este projeto implementa o algoritmo A* para encontrar o menor caminho em um labirinto 2D entre dois pontos. O algoritmo combina o custo do caminho já percorrido e uma estimativa (heurística) da distância até o destino para encontrar a solução de forma eficiente.

### 🔍 Implementação do Algoritmo

O algoritmo implementado segue os seguintes passos:

1. **Inicialização**:
   * Recebe uma matriz que representa o labirinto
   * Valida a existência dos pontos inicial (S) e final (E)
   * Inicializa as estruturas de dados necessárias

2. **Heurística**:
   * Utiliza a distância de Manhattan como heurística
   * h(n) = |x_atual - x_final| + |y_atual - y_final|
   * Garante uma estimativa admissível do custo restante

3. **Busca A***:
   * Mantém uma lista de nós a serem explorados (open_set)
   * Explora os nós em ordem de f_cost (g_cost + h_cost)
   * Atualiza caminhos quando encontra rotas mais eficientes
   * Para quando encontra o destino ou esgota as possibilidades

### 🌟 Funcionalidades Extras

- **Movimentos Ortogonais**:
  * Esta versão permite movimentos apenas nas 4 direções ortogonais (cima, baixo, esquerda, direita).
  * Não são permitidos movimentos diagonais.

2. **Interface Gráfica**:
   * Interface intuitiva com Tkinter
   * Ferramentas para desenhar o labirinto
   * Visualização do caminho encontrado
   * Feedback visual do resultado

3. **Terrenos com Pesos**:
   * Diferentes tipos de terreno com custos variados
   * Terreno normal (0): Custo 1.0
   * Terreno difícil (1): Custo 2.0
   * Terreno muito difícil (2): Custo 3.0
   * Terreno extremamente difícil (3): Custo 4.0
   * Obstáculos (#): Custo infinito

## 📊 Análise Técnica

### Classes de Complexidade

O algoritmo A* tem as seguintes características de complexidade:

1. **Complexidade Temporal**:

* **Pior Caso**: O(b^d), onde *b* é o fator de ramificação e *d* é a profundidade.
* **Caso Médio**: O(b^d).
* **Melhor Caso**: O(d), quando a heurística guia diretamente ao objetivo.

  
2. **Complexidade Espacial**:
   * O(b^d) para armazenar os nós na fila de prioridade
   * Requer memória para manter os conjuntos open_set e closed_set

### Otimizações Implementadas

1. **Estruturas de Dados Eficientes**:
   * Uso de heap para a fila de prioridade
   * Conjunto (set) para nós já explorados
   * Dicionário para acesso rápido aos nós

2. **Heurística Admissível**:
   * A distância de Manhattan nunca superestima o custo real
   * Garante que o caminho encontrado é ótimo

## ✨ Funcionalidades

* 🗺️ Leitura e validação de labirintos 2D
* 🔍 Busca do menor caminho usando A*
* 📊 Visualização do caminho encontrado
* ⚡ Detecção de casos sem solução
* 🧪 Suite completa de testes
* 🎮 Interface gráfica interativa
* 🌈 Suporte a diferentes tipos de terreno
* Movimentos apenas ortogonais (cima, baixo, esquerda, direita)

## 📁 Estrutura do Projeto

```
pathfinder/
├── src/
│   ├── __init__.py
│   ├── maze.py        # Classe para representação do labirinto
│   ├── astar.py       # Implementação do algoritmo A*
│   ├── utils.py       # Funções utilitárias
│   └── gui.py         # Interface gráfica
├── tests/
│   ├── __init__.py
│   ├── test_maze.py
│   ├── test_astar.py
│   └── test_utils.py
└── requirements.txt
```

## 🚀 Como Executar

### 📋 Pré-requisitos

* Python 3.8+
* pip (gerenciador de pacotes Python)

### 🔧 Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITÓRIO]
cd pathfinder
```

2. (Recomendado) Crie um ambiente virtual:
```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

### ▶️ Execução

1. Interface Gráfica:
```bash
python main.py
```

2. Execução dos Testes:
```bash
python -m pytest tests/ -v
```

## 📊 Exemplos

### Labirinto de Entrada
```
S 0 # 0 0
2 # 1 0 #
0 3 0 0 0
# 0 0 E 1
```

### Saída
```
S * # 0 0
2 # 1 * #
0 3 0 * 0
# 0 0 E 1
```

## 🔧 Troubleshooting

### Problemas Comuns

1. **Erro ao instalar dependências**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **Erro ao executar a interface gráfica**:
   - Verifique se o Python está instalado corretamente
   - Certifique-se de que todas as dependências foram instaladas
   - Verifique se está no ambiente virtual correto

3. **Labirinto não é reconhecido**:
   - Verifique se o formato está correto (S, E, 0-3, #)
   - Certifique-se de que há exatamente um S e um E
   - Verifique se não há caracteres inválidos

### Exemplos Adicionais

#### Exemplo 1: Labirinto Simples
```
S 0 0 0 0
0 # # 0 0
0 0 0 0 0
0 0 0 0 E
```

#### Exemplo 2: Labirinto com Terrenos Diferentes
```
S 1 2 3 0
0 # # 0 0
2 1 0 0 0
0 0 0 0 E
```

#### Exemplo 3: Labirinto Sem Solução
```
S # # # #
# 0 0 0 #
# 0 0 0 #
# # # # E
```

## 🧪 Testes

O projeto inclui uma suite completa de testes unitários. Para executar:

```bash
# Executar todos os testes
python -m pytest tests/ -v

# Executar testes específicos
python -m pytest tests/test_astar.py -v
python -m pytest tests/test_maze.py -v
python -m pytest tests/test_utils.py -v
```

### Cobertura de Testes
- Testes de casos válidos e inválidos
- Testes de performance
- Testes de casos de borda
- Testes de integração

## 👥 Contribuição

Este é um projeto acadêmico desenvolvido como parte do curso de FPAA (Fundamentos de Projeto e Análise de Algoritmos).

## 📄 Licença

Este projeto está sob a licença MIT. 
