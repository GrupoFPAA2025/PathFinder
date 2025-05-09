import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import List, Optional
from .maze import Maze
from .astar import astar

class PathFinderGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("PathFinder A* - ESTRELA GUIA")
        
        # Configurações do labirinto
        self.rows = 10
        self.cols = 10
        self.cell_size = 40
        self.maze_data: List[List[str]] = []
        self.start_pos = None
        self.end_pos = None
        
        # Cores
        self.colors = {
            'S': '#00FF00',    # Verde para início
            'E': '#FF0000',    # Vermelho para fim
            '0': '#FFFFFF',    # Branco para caminho livre
            '1': '#FFE0E0',    # Rosa claro para terreno difícil
            '2': '#FFB0B0',    # Rosa médio para terreno muito difícil
            '3': '#FF8080',    # Rosa escuro para terreno extremamente difícil
            '#': '#000000',    # Preto para obstáculo
            '*': '#FFA500'     # Laranja para o caminho encontrado
        }
        
        self._init_ui()
        self._create_empty_maze()
    
    def _init_ui(self):
        """Inicializa a interface do usuário"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Frame do labirinto
        self.maze_frame = ttk.Frame(main_frame)
        self.maze_frame.grid(row=0, column=0, rowspan=2)
        
        # Frame de controles
        controls_frame = ttk.Frame(main_frame, padding="5")
        controls_frame.grid(row=0, column=1, sticky=tk.N)
        
        # Botões de controle
        ttk.Label(controls_frame, text="Ferramentas:").grid(row=0, column=0, pady=5)
        
        self.tool_var = tk.StringVar(value="start")
        tools = [
            ("Início (S)", "start"),
            ("Fim (E)", "end"),
            ("Obstáculo (#)", "wall"),
            ("Caminho (0)", "path0"),
            ("Terreno Difícil (1)", "path1"),
            ("Terreno Muito Difícil (2)", "path2"),
            ("Terreno Extremamente Difícil (3)", "path3")
        ]
        
        for i, (text, value) in enumerate(tools):
            ttk.Radiobutton(
                controls_frame,
                text=text,
                value=value,
                variable=self.tool_var
            ).grid(row=i+1, column=0, pady=2, sticky=tk.W)
        
        ttk.Separator(controls_frame, orient='horizontal').grid(
            row=len(tools)+1, column=0, pady=10, sticky=(tk.W, tk.E))
        
        # Botões de ação
        ttk.Button(
            controls_frame,
            text="Carregar Labirinto",
            command=self._load_maze
        ).grid(row=len(tools)+2, column=0, pady=5)
        
        ttk.Button(
            controls_frame,
            text="Resolver",
            command=self._solve_maze
        ).grid(row=len(tools)+3, column=0, pady=5)
        
        ttk.Button(
            controls_frame,
            text="Limpar",
            command=self._clear_maze
        ).grid(row=len(tools)+4, column=0, pady=5)
        
        # Canvas para desenhar o labirinto
        self.canvas = tk.Canvas(
            self.maze_frame,
            width=self.cols * self.cell_size,
            height=self.rows * self.cell_size
        )
        self.canvas.grid(row=0, column=0)
        
        # Bind eventos do mouse
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        self.canvas.bind("<B1-Motion>", self._on_canvas_drag)
    
    def _create_empty_maze(self):
        """Cria um labirinto vazio"""
        self.maze_data = [['0' for _ in range(self.cols)] for _ in range(self.rows)]
        self._draw_maze()
    
    def _draw_maze(self):
        """Desenha o labirinto no canvas"""
        self.canvas.delete("all")
        
        # Desenha as células
        for row in range(self.rows):
            for col in range(self.cols):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                cell_type = self.maze_data[row][col]
                color = self.colors[cell_type]
                
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline='gray'
                )
                
                # Adiciona texto para início, fim e pesos
                if cell_type in ['S', 'E']:
                    self.canvas.create_text(
                        (x1 + x2) / 2,
                        (y1 + y2) / 2,
                        text=cell_type,
                        fill='black'
                    )
                elif cell_type in ['1', '2', '3']:
                    self.canvas.create_text(
                        (x1 + x2) / 2,
                        (y1 + y2) / 2,
                        text=cell_type,
                        fill='black'
                    )
    
    def _get_cell_from_coords(self, event) -> Optional[tuple[int, int]]:
        """Converte coordenadas do mouse para posição na grade"""
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return row, col
        return None
    
    def _on_canvas_click(self, event):
        """Manipula clique no canvas"""
        pos = self._get_cell_from_coords(event)
        if pos:
            self._update_cell(pos)
    
    def _on_canvas_drag(self, event):
        """Manipula arrasto do mouse no canvas"""
        pos = self._get_cell_from_coords(event)
        if pos:
            tool = self.tool_var.get()
            if tool.startswith('path') or tool == 'wall':  # Permite arrasto para todos os tipos de terreno
                self._update_cell(pos)
    
    def _update_cell(self, pos: tuple[int, int]):
        """Atualiza uma célula do labirinto"""
        row, col = pos
        tool = self.tool_var.get()
        
        if tool == "start":
            # Remove início anterior
            if self.start_pos:
                old_row, old_col = self.start_pos
                self.maze_data[old_row][old_col] = '0'
            self.start_pos = (row, col)
            self.maze_data[row][col] = 'S'
            
        elif tool == "end":
            # Remove fim anterior
            if self.end_pos:
                old_row, old_col = self.end_pos
                self.maze_data[old_row][old_col] = '0'
            self.end_pos = (row, col)
            self.maze_data[row][col] = 'E'
            
        elif tool == "wall":
            if self.maze_data[row][col] not in ['S', 'E']:
                self.maze_data[row][col] = '#'
                
        elif tool.startswith("path"):
            if self.maze_data[row][col] not in ['S', 'E']:
                weight = tool[-1]  # Pega o último caractere (0, 1, 2 ou 3)
                self.maze_data[row][col] = weight
        
        self._draw_maze()
    
    def _load_maze(self):
        """Carrega um labirinto a partir de um arquivo"""
        file_path = filedialog.askopenfilename(
            title="Selecione um arquivo de labirinto",
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")],
            initialdir="examples"
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                
            # Remove espaços em branco e caracteres de nova linha
            maze_data = [line.strip().split() for line in lines]
            
            # Verifica se o labirinto tem o tamanho correto
            if len(maze_data) != self.rows or any(len(row) != self.cols for row in maze_data):
                messagebox.showerror(
                    "Erro",
                    f"O labirinto deve ter {self.rows}x{self.cols} células"
                )
                return
            
            # Atualiza o labirinto
            self.maze_data = maze_data
            self.start_pos = None
            self.end_pos = None
            
            # Encontra as posições de início e fim
            for row in range(self.rows):
                for col in range(self.cols):
                    if self.maze_data[row][col] == 'S':
                        self.start_pos = (row, col)
                    elif self.maze_data[row][col] == 'E':
                        self.end_pos = (row, col)
            
            self._draw_maze()
            messagebox.showinfo("Sucesso", "Labirinto carregado com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar o labirinto: {str(e)}")
    
    def _solve_maze(self):
        """Resolve o labirinto usando A*"""
        try:
            # Limpa o caminho anterior
            for row in range(self.rows):
                for col in range(self.cols):
                    if self.maze_data[row][col] == '*':
                        self.maze_data[row][col] = '0'
            
            # Cria instância do labirinto
            maze = Maze(self.maze_data)
            
            # Encontra o caminho
            path = astar(maze)
            
            if path:
                # Marca o caminho
                for row, col in path[1:-1]:  # Ignora início e fim
                    self.maze_data[row][col] = '*'
                self._draw_maze()
                messagebox.showinfo("Sucesso", "Caminho encontrado!")
            else:
                messagebox.showwarning("Aviso", "Não foi possível encontrar um caminho!")
                
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
    
    def _clear_maze(self):
        """Limpa o labirinto"""
        self.start_pos = None
        self.end_pos = None
        self._create_empty_maze()

def run_gui():
    """Inicia a interface gráfica"""
    root = tk.Tk()
    app = PathFinderGUI(root)
    root.mainloop() 