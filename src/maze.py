from typing import List, Tuple, Optional, Dict
import numpy as np
from .utils import validate_maze, find_points

class Maze:
    def __init__(self, maze_data: List[List[str]], cell_weights: Optional[Dict[str, float]] = None):
        """
        Inicializa o labirinto.
        
        Args:
            maze_data: Matriz 2D representando o labirinto
                      'S': Ponto inicial
                      'E': Ponto final
                      '0'-'9': Caminho com peso
                      '#': Obstáculo
            cell_weights: Dicionário com pesos para cada tipo de célula
        """
        # Valida o labirinto
        is_valid, error_msg = validate_maze(maze_data)
        if not is_valid:
            raise ValueError(error_msg)
        
        self.maze = maze_data
        self.rows = len(maze_data)
        self.cols = len(maze_data[0])
        self.start_pos, self.end_pos = find_points(maze_data)
        
        # Pesos para diferentes tipos de movimento
        self.movement_weights = {
            'orthogonal': 1,  # Movimento ortogonal (cima, baixo, esquerda, direita)
            'diagonal': 1.4   # Movimento diagonal (aproximadamente √2)
        }
        
        # Pesos para diferentes tipos de célula
        self.cell_weights = cell_weights or {
            'S': 1.0,  # Início
            'E': 1.0,  # Fim
            '0': 1.0,  # Caminho normal
            '1': 2.0,  # Terreno difícil
            '2': 3.0,  # Terreno muito difícil
            '3': 4.0,  # Terreno extremamente difícil
            '#': float('inf')  # Obstáculo
        }
        
        # Converte para matriz numpy para melhor performance
        self.maze_array = np.array(maze_data)
    
    def is_valid_position(self, pos: Tuple[int, int]) -> bool:
        """
        Verifica se uma posição é válida no labirinto.
        
        Args:
            pos: Tupla (linha, coluna) representando a posição
            
        Returns:
            bool: True se a posição é válida, False caso contrário
        """
        row, col = pos
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return False
        
        cell = self.maze[row][col]
        return cell != '#' and self.cell_weights.get(cell, float('inf')) < float('inf')
    
    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Retorna os vizinhos válidos de uma posição, incluindo diagonais.
        
        Args:
            pos: Tupla (linha, coluna) representando a posição
            
        Returns:
            List[Tuple[int, int]]: Lista de posições vizinhas válidas
        """
        row, col = pos
        neighbors = []
        
        # Movimentos ortogonais
        orthogonal_moves = [
            (row-1, col),  # Cima
            (row+1, col),  # Baixo
            (row, col-1),  # Esquerda
            (row, col+1)   # Direita
        ]
        
        # Movimentos diagonais
        diagonal_moves = [
            (row-1, col-1),  # Diagonal superior esquerda
            (row-1, col+1),  # Diagonal superior direita
            (row+1, col-1),  # Diagonal inferior esquerda
            (row+1, col+1)   # Diagonal inferior direita
        ]
        
        # Verifica movimentos ortogonais
        for new_pos in orthogonal_moves:
            if self.is_valid_position(new_pos):
                neighbors.append(new_pos)
        
        # Verifica movimentos diagonais
        for new_pos in diagonal_moves:
            if self.is_valid_position(new_pos):
                # Verifica se os movimentos ortogonais adjacentes são válidos
                # para evitar "cortar cantos" através de obstáculos
                row1, col1 = new_pos
                if (self.is_valid_position((row1, col)) and 
                    self.is_valid_position((row, col1))):
                    neighbors.append(new_pos)
        
        return neighbors
    
    def get_cost(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """
        Calcula o custo de movimento entre duas posições adjacentes.
        
        Args:
            pos1: Tupla (linha, coluna) da posição inicial
            pos2: Tupla (linha, coluna) da posição final
            
        Returns:
            float: Custo do movimento
        """
        row1, col1 = pos1
        row2, col2 = pos2
        
        # Custo base do movimento (ortogonal ou diagonal)
        if abs(row1 - row2) == 1 and abs(col1 - col2) == 1:
            base_cost = self.movement_weights['diagonal']
        else:
            base_cost = self.movement_weights['orthogonal']
        
        # Custo do terreno (média entre as duas células)
        cell1 = self.maze[row1][col1]
        cell2 = self.maze[row2][col2]
        terrain_cost = (self.cell_weights[cell1] + self.cell_weights[cell2]) / 2
        
        return base_cost * terrain_cost
    
    def mark_path(self, path: List[Tuple[int, int]]) -> List[List[str]]:
        """
        Marca o caminho encontrado no labirinto.
        
        Args:
            path: Lista de posições representando o caminho
            
        Returns:
            List[List[str]]: Cópia do labirinto com o caminho marcado
        """
        # Cria uma cópia do labirinto
        marked_maze = [row[:] for row in self.maze]
        
        # Marca o caminho (exceto início e fim)
        for pos in path[1:-1]:
            row, col = pos
            marked_maze[row][col] = '*'
        
        return marked_maze
    
    def __str__(self) -> str:
        """
        Retorna uma representação em string do labirinto.
        
        Returns:
            str: Representação do labirinto
        """
        return '\n'.join(' '.join(row) for row in self.maze) 