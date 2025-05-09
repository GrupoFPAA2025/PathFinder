from typing import List, Tuple, Dict, Set, Optional
import heapq
from .utils import manhattan_distance
from .maze import Maze

class Node:
    def __init__(self, pos: Tuple[int, int], g_cost: float, h_cost: float, parent: Optional['Node'] = None):
        self.pos = pos
        self.g_cost = g_cost  # Custo do caminho do início até este nó
        self.h_cost = h_cost  # Custo estimado deste nó até o objetivo
        self.parent = parent  # Nó pai para reconstruir o caminho
        
    @property
    def f_cost(self) -> float:
        """Custo total do nó (g_cost + h_cost)"""
        return self.g_cost + self.h_cost
    
    def __lt__(self, other: 'Node') -> bool:
        """Comparação para ordenação na fila de prioridade"""
        if abs(self.f_cost - other.f_cost) < 1e-10:  # Comparação com tolerância para números flutuantes
            return self.h_cost < other.h_cost  # Desempata pelo h_cost
        return self.f_cost < other.f_cost

def astar(maze: Maze) -> Optional[List[Tuple[int, int]]]:
    """
    Implementa o algoritmo A* para encontrar o menor caminho no labirinto.
    
    Args:
        maze: Instância da classe Maze representando o labirinto
        
    Returns:
        Optional[List[Tuple[int, int]]]: Lista de posições representando o caminho,
                                        ou None se não houver solução
    """
    # Inicializa as estruturas de dados
    open_set: List[Node] = []  # Fila de prioridade para nós a serem explorados
    closed_set: Set[Tuple[int, int]] = set()  # Conjunto de nós já explorados
    node_dict: Dict[Tuple[int, int], Node] = {}  # Dicionário para acessar nós por posição
    
    # Cria o nó inicial
    start_node = Node(
        pos=maze.start_pos,
        g_cost=0.0,
        h_cost=manhattan_distance(maze.start_pos, maze.end_pos)
    )
    
    # Adiciona o nó inicial à fila de prioridade
    heapq.heappush(open_set, start_node)
    node_dict[maze.start_pos] = start_node
    
    while open_set:
        # Pega o nó com menor f_cost
        current = heapq.heappop(open_set)
        
        # Se chegou ao objetivo, reconstrói e retorna o caminho
        if current.pos == maze.end_pos:
            path = []
            while current:
                path.append(current.pos)
                current = current.parent
            return path[::-1]  # Inverte para começar do início
        
        # Marca o nó atual como explorado
        closed_set.add(current.pos)
        
        # Explora os vizinhos
        for neighbor_pos in maze.get_neighbors(current.pos):
            # Se o vizinho já foi explorado, pula
            if neighbor_pos in closed_set:
                continue
            
            # Calcula o novo g_cost
            new_g_cost = current.g_cost + maze.get_cost(current.pos, neighbor_pos)
            
            # Se o vizinho já foi visitado
            if neighbor_pos in node_dict:
                neighbor_node = node_dict[neighbor_pos]
                # Se o novo caminho é melhor, atualiza
                if new_g_cost < neighbor_node.g_cost:
                    neighbor_node.g_cost = new_g_cost
                    neighbor_node.parent = current
                    # Reinsere na fila de prioridade
                    heapq.heappush(open_set, neighbor_node)
            else:
                # Cria um novo nó para o vizinho
                neighbor_node = Node(
                    pos=neighbor_pos,
                    g_cost=new_g_cost,
                    h_cost=manhattan_distance(neighbor_pos, maze.end_pos),
                    parent=current
                )
                # Adiciona ao dicionário e à fila de prioridade
                node_dict[neighbor_pos] = neighbor_node
                heapq.heappush(open_set, neighbor_node)
    
    # Se chegou aqui, não há solução
    return None 