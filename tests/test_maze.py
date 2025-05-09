import pytest
from src.maze import Maze

@pytest.fixture
def valid_maze():
    """Fixture com um labirinto válido para testes"""
    return [
        ['S', '0', '#'],
        ['0', '#', '0'],
        ['0', '0', 'E']
    ]

@pytest.fixture
def weighted_maze():
    """Fixture com um labirinto com diferentes pesos"""
    return [
        ['S', '1', '0', '0'],
        ['2', '#', '1', '0'],
        ['0', '3', '0', '0'],
        ['0', '0', '0', 'E']
    ]

@pytest.fixture
def diagonal_maze():
    """Fixture com um labirinto que permite movimentos diagonais"""
    return [
        ['S', '0', '0', '0'],
        ['0', '0', '0', '0'],
        ['0', '0', '0', '0'],
        ['0', '0', '0', 'E']
    ]

def test_maze_initialization(valid_maze):
    """Testa a inicialização da classe Maze"""
    maze = Maze(valid_maze)
    assert maze.rows == 3
    assert maze.cols == 3
    assert maze.start_pos == (0, 0)
    assert maze.end_pos == (2, 2)
    assert maze.movement_weights['orthogonal'] == 1
    assert maze.movement_weights['diagonal'] == 1.4

def test_maze_initialization_with_weights(weighted_maze):
    """Testa a inicialização com pesos personalizados"""
    custom_weights = {
        'S': 1.0,
        'E': 1.0,
        '0': 1.0,
        '1': 3.0,
        '2': 5.0,
        '3': 7.0,
        '#': float('inf')
    }
    maze = Maze(weighted_maze, custom_weights)
    assert maze.cell_weights == custom_weights

def test_maze_invalid_initialization():
    """Testa a inicialização com labirinto inválido"""
    invalid_maze = [
        ['S', '0', '#'],
        ['0', '#'],  # Linha com tamanho diferente
        ['0', '0', 'E']
    ]
    with pytest.raises(ValueError):
        Maze(invalid_maze)

def test_is_valid_position(valid_maze):
    """Testa a validação de posições no labirinto"""
    maze = Maze(valid_maze)
    
    # Posições válidas
    assert maze.is_valid_position((0, 0))  # S
    assert maze.is_valid_position((0, 1))  # 0
    assert maze.is_valid_position((2, 2))  # E
    
    # Posições inválidas
    assert not maze.is_valid_position((0, 2))  # # (obstáculo)
    assert not maze.is_valid_position((1, 1))  # # (obstáculo)
    assert not maze.is_valid_position((-1, 0))  # Fora dos limites
    assert not maze.is_valid_position((3, 0))   # Fora dos limites

def test_get_neighbors(valid_maze):
    """Testa a obtenção de vizinhos válidos"""
    maze = Maze(valid_maze)
    
    # Testa vizinhos do ponto inicial
    neighbors = maze.get_neighbors((0, 0))
    assert len(neighbors) == 2  # (0, 1) e (1, 0) são válidos
    assert (0, 1) in neighbors
    assert (1, 0) in neighbors
    
    # Testa vizinhos de uma posição central
    neighbors = maze.get_neighbors((1, 0))
    assert len(neighbors) == 2  # (0, 0) e (2, 0)
    assert (0, 0) in neighbors
    assert (2, 0) in neighbors

def test_get_neighbors_diagonal(diagonal_maze):
    """Testa a obtenção de vizinhos válidos incluindo diagonais"""
    maze = Maze(diagonal_maze)
    
    # Testa vizinhos do ponto inicial
    neighbors = maze.get_neighbors((0, 0))
    assert len(neighbors) == 3  # (0, 1), (1, 0) e (1, 1) são válidos
    assert (0, 1) in neighbors
    assert (1, 0) in neighbors
    assert (1, 1) in neighbors
    
    # Testa vizinhos de uma posição central
    neighbors = maze.get_neighbors((2, 2))
    assert len(neighbors) == 8  # Todos os vizinhos são válidos
    assert (1, 1) in neighbors
    assert (1, 2) in neighbors
    assert (1, 3) in neighbors
    assert (2, 1) in neighbors
    assert (2, 3) in neighbors
    assert (3, 1) in neighbors
    assert (3, 2) in neighbors
    assert (3, 3) in neighbors

def test_get_cost_weighted(weighted_maze):
    """Testa o cálculo de custo com diferentes pesos"""
    custom_weights = {
        'S': 1.0,
        'E': 1.0,
        '0': 1.0,
        '1': 3.0,
        '2': 5.0,
        '3': 7.0,
        '#': float('inf')
    }
    maze = Maze(weighted_maze, custom_weights)
    
    # Testa custo de movimento ortogonal
    assert maze.get_cost((0, 0), (0, 1)) == 2.0  # S -> 1 (média: (1 + 3) / 2)
    assert maze.get_cost((1, 0), (2, 0)) == 3.0  # 2 -> 0 (média: (5 + 1) / 2)
    
    # Testa custo de movimento diagonal
    assert maze.get_cost((0, 0), (1, 1)) == float('inf')  # S -> # (obstáculo)
    assert maze.get_cost((2, 1), (3, 2)) == 5.6  # 3 -> 0 (média: (7 + 1) * 1.4)

def test_mark_path(valid_maze):
    """Testa a marcação do caminho no labirinto"""
    maze = Maze(valid_maze)
    path = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
    marked_maze = maze.mark_path(path)
    
    # Verifica se o caminho foi marcado corretamente
    assert marked_maze[0][0] == 'S'  # Início
    assert marked_maze[2][2] == 'E'  # Fim
    assert marked_maze[1][0] == '*'  # Caminho
    assert marked_maze[2][0] == '*'  # Caminho
    assert marked_maze[2][1] == '*'  # Caminho

def test_str_representation(valid_maze):
    """Testa a representação em string do labirinto"""
    maze = Maze(valid_maze)
    expected = "S 0 #\n0 # 0\n0 0 E"
    assert str(maze) == expected 