from ui.buttons import Buttons
from core.maze import Maze
from ui.renderer import MazeRenderer
from config import MazeSize, Speed

class EventHandler:
    def __init__(self, maze: Maze, renderer: MazeRenderer):
        self.maze: Maze = maze
        self.renderer: MazeRenderer = renderer
    
    @staticmethod
    def _parse_positive_int(text: str, min: int, max: int) -> int:
        try:
            value = int(text)
            if value < min:
                return min
            if value > max:
                return max
            return value
        except ValueError:
            return MazeSize.min_size

    def handle_button_click(self, pos: tuple[int, int]) -> None:
        Speed.current = self._parse_positive_int(Buttons.speed_input_box.text, Speed.min_speed, Speed.max_speed)
        Buttons.speed_input_box.text = str(Speed.current)
        if Buttons.bfs.collidepoint(pos):
            self.maze.selected_algorithm = 'BFS'
            self.renderer.reset_screen()
        elif Buttons.dfs.collidepoint(pos):
            self.maze.selected_algorithm = 'DFS'
            self.renderer.reset_screen()
        elif Buttons.generate.collidepoint(pos):
            MazeSize.width = self._parse_positive_int(Buttons.columns_input_box.text, MazeSize.min_size, MazeSize.max_size)
            MazeSize.height = self._parse_positive_int(Buttons.rows_input_box.text, MazeSize.min_size, MazeSize.max_size)
            
            Buttons.columns_input_box.text = str(MazeSize.width)    
            Buttons.rows_input_box.text = str(MazeSize.height)
            
            self.maze.generate_random(MazeSize.width, MazeSize.height, (1, 1), (MazeSize.width-3, MazeSize.height-3), 0.025)
            self.renderer.reset_screen()
        elif Buttons.solve.collidepoint(pos):
            self.renderer.simulation_running = True
            self.maze.solve(self.maze.selected_algorithm)
        elif Buttons.reset.collidepoint(pos):
            self.renderer.reset_screen()
    