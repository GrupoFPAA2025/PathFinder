import pytest
from src.utils import validate_maze, find_points, manhattan_distance

def test_validate_maze_empty():
    """Testa validação de labirinto vazio"""
    maze = []
    is_valid, error_msg = validate_maze(maze)
    assert not is_valid
    assert error_msg == "Labirinto vazio"

def test_validate_maze_invalid_size():
    """Testa validação de labirinto com linhas de tamanhos diferentes"""
    maze = [
        ['S', '0', '1'],
        ['0', '1'],
        ['0', '0', 'E']
    ]
    is_valid, error_msg = validate_maze(maze)
    assert not is_valid
    assert error_msg == "Todas as linhas devem ter o mesmo tamanho"

def test_validate_maze_no_start():
    """Testa validação de labirinto sem ponto inicial"""
    maze = [
        ['0', '0', '1'],
        ['0', '1', '0'],
        ['0', '0', 'E']
    ]
    is_valid, error_msg = validate_maze(maze)
    assert not is_valid
    assert "Deve haver exatamente um ponto inicial (S)" in error_msg

def test_validate_maze_no_end():
    """Testa validação de labirinto sem ponto final"""
    maze = [
        ['S', '0', '1'],
        ['0', '1', '0'],
        ['0', '0', '0']
    ]
    is_valid, error_msg = validate_maze(maze)
    assert not is_valid
    assert "Deve haver exatamente um ponto final (E)" in error_msg

def test_validate_maze_invalid_char():
    """Testa validação de labirinto com caractere inválido"""
    maze = [
        ['S', '0', '1'],
        ['0', 'X', '0'],
        ['0', '0', 'E']
    ]
    is_valid, error_msg = validate_maze(maze)
    assert not is_valid
    assert "Caractere inválido" in error_msg

def test_validate_maze_valid():
    """Testa validação de labirinto válido"""
    maze = [
        ['S', '0', '1'],
        ['0', '1', '0'],
        ['0', '0', 'E']
    ]
    is_valid, error_msg = validate_maze(maze)
    assert is_valid
    assert error_msg is None

def test_find_points():
    """Testa a função de encontrar pontos inicial e final"""
    maze = [
        ['S', '0', '1'],
        ['0', '1', '0'],
        ['0', '0', 'E']
    ]
    start_pos, end_pos = find_points(maze)
    assert start_pos == (0, 0)
    assert end_pos == (2, 2)

def test_manhattan_distance():
    """Testa o cálculo da distância de Manhattan"""
    pos1 = (0, 0)
    pos2 = (3, 4)
    distance = manhattan_distance(pos1, pos2)
    assert distance == 7  # |3-0| + |4-0| = 3 + 4 = 7 