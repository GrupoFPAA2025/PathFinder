from typing import List, Tuple, Optional
import numpy as np

def validate_maze(maze: List[List[str]]) -> Tuple[bool, Optional[str]]:
    """
    Valida um labirinto.
    
    Args:
        maze: Matriz 2D representando o labirinto
        
    Returns:
        Tuple[bool, Optional[str]]: (True, None) se o labirinto é válido,
                                   (False, mensagem_erro) caso contrário
    """
    # Verifica se o labirinto está vazio
    if not maze or not maze[0]:
        return False, "Labirinto vazio"
    
    # Verifica se todas as linhas têm o mesmo tamanho
    width = len(maze[0])
    if not all(len(row) == width for row in maze):
        return False, "Todas as linhas devem ter o mesmo tamanho"
    
    # Conta pontos iniciais e finais
    start_count = sum(cell == 'S' for row in maze for cell in row)
    end_count = sum(cell == 'E' for row in maze for cell in row)
    
    # Verifica se há exatamente um ponto inicial
    if start_count != 1:
        return False, "Deve haver exatamente um ponto inicial (S)"
    
    # Verifica se há exatamente um ponto final
    if end_count != 1:
        return False, "Deve haver exatamente um ponto final (E)"
    
    # Verifica se há caracteres inválidos
    valid_chars = {'S', 'E', '#', '0', '1', '2', '3', '*'}
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell not in valid_chars:
                return False, f"Caractere inválido '{cell}' na posição ({i}, {j})"
    
    return True, None

def find_points(maze: List[List[str]]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Encontra os pontos inicial e final no labirinto.
    
    Args:
        maze: Matriz 2D representando o labirinto
        
    Returns:
        Tuple[Tuple[int, int], Tuple[int, int]]: Posições inicial e final
    """
    start_pos = end_pos = None
    
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == 'S':
                start_pos = (i, j)
            elif cell == 'E':
                end_pos = (i, j)
    
    return start_pos, end_pos

def manhattan_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
    """
    Calcula a distância de Manhattan entre duas posições.
    
    Args:
        pos1: Primeira posição (x1, y1)
        pos2: Segunda posição (x2, y2)
        
    Returns:
        int: Distância de Manhattan
    """
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2) 