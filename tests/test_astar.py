import pytest
from src.maze import Maze
from src.astar import astar, Node

@pytest.fixture
def simple_maze():
    """Fixture com um labirinto simples para testes"""
    return [
        ['S', '0', '0'],
        ['#', '#', '0'],
        ['0', '0', 'E']
    ]

@pytest.fixture
def no_solution_maze():
    """Fixture com um labirinto sem solução"""
    return [
        ['S', '0', '0'],
        ['#', '#', '#'],
        ['0', '0', 'E']
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

def test_node_creation():
    """Testa a criação de nós"""
    node = Node((0, 0), 5.0, 3.0)
    assert node.pos == (0, 0)
    assert node.g_cost == 5.0
    assert node.h_cost == 3.0
    assert node.f_cost == 8.0
    assert node.parent is None

def test_node_comparison():
    """Testa a comparação entre nós"""
    node1 = Node((0, 0), 5.0, 3.0)  # f_cost = 8.0
    node2 = Node((1, 1), 4.0, 3.0)  # f_cost = 7.0
    assert node2 < node1  # node2 tem menor f_cost

def test_astar_simple_maze(simple_maze):
    """Testa o algoritmo A* em um labirinto simples"""
    maze = Maze(simple_maze)
    path = astar(maze)
    
    # Verifica se o caminho foi encontrado
    assert path is not None
    
    # Verifica se o caminho começa no início e termina no fim
    assert path[0] == maze.start_pos
    assert path[-1] == maze.end_pos
    
    # Verifica se o caminho é válido (posições adjacentes)
    for i in range(len(path) - 1):
        pos1 = path[i]
        pos2 = path[i + 1]
        # Verifica se as posições são adjacentes (ortogonal ou diagonal)
        assert abs(pos1[0] - pos2[0]) <= 1 and abs(pos1[1] - pos2[1]) <= 1

def test_astar_no_solution(no_solution_maze):
    """Testa o algoritmo A* em um labirinto sem solução"""
    maze = Maze(no_solution_maze)
    path = astar(maze)
    assert path is None

def test_astar_diagonal_maze(diagonal_maze):
    """Testa o algoritmo A* em um labirinto com movimentos diagonais"""
    maze = Maze(diagonal_maze)
    path = astar(maze)
    
    # Verifica se o caminho foi encontrado
    assert path is not None
    
    # Verifica se o caminho começa no início e termina no fim
    assert path[0] == maze.start_pos
    assert path[-1] == maze.end_pos
    
    # Verifica se o caminho é válido
    for i in range(len(path) - 1):
        pos1 = path[i]
        pos2 = path[i + 1]
        # Verifica se as posições são adjacentes (ortogonal ou diagonal)
        assert abs(pos1[0] - pos2[0]) <= 1 and abs(pos1[1] - pos2[1]) <= 1
    
    # Verifica se o caminho usa movimentos diagonais
    has_diagonal_move = False
    for i in range(len(path) - 1):
        pos1 = path[i]
        pos2 = path[i + 1]
        if abs(pos1[0] - pos2[0]) == 1 and abs(pos1[1] - pos2[1]) == 1:
            has_diagonal_move = True
            break
    assert has_diagonal_move, "O caminho deveria incluir pelo menos um movimento diagonal"

def test_astar_complex_maze():
    """Testa o algoritmo A* em um labirinto mais complexo"""
    maze_data = [
        ['S', '0', '0', '0', '0'],
        ['#', '#', '0', '#', '0'],
        ['0', '0', '0', '0', '0'],
        ['0', '#', '#', 'E', '0']
    ]
    maze = Maze(maze_data)
    path = astar(maze)
    
    # Verifica se o caminho foi encontrado
    assert path is not None
    
    # Verifica se o caminho começa no início e termina no fim
    assert path[0] == maze.start_pos
    assert path[-1] == maze.end_pos
    
    # Verifica se o caminho é válido
    for i in range(len(path) - 1):
        pos1 = path[i]
        pos2 = path[i + 1]
        # Verifica se as posições são adjacentes (ortogonal ou diagonal)
        assert abs(pos1[0] - pos2[0]) <= 1 and abs(pos1[1] - pos2[1]) <= 1 