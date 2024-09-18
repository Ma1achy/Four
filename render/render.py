from instance.matrix import Matrix
import pygame
from config import Config
from utils import lerpBlendRGBA, Font, tetromino_previews, get_prefix

class Render():
    def __init__(self, window:pygame.Surface):
        """
        Render an instance of four onto a window
        
        args:
            self.window (pygame.Surface): the window to render the game onto
        """
        self.surfaces = []
        
        pygame.font.init()
        self.window = window
        self.config = Config()
        self.four_surface = self.__init_four_surface()
        self.danger = False
        self.game_over = False
        
        # fonts
        self.hun2_big = Font(self.config.GRID_SIZE).hun2()
        self.hun2_small = Font(self.config.GRID_SIZE//2).hun2()
        self.pfw_small = Font(self.config.GRID_SIZE//2).pfw()
        self.action_ui = Font(self.config.GRID_SIZE).action_ui()
            
    def __init_four_surface(self):
        """
        Create the surface to render the matrix, border and blocks to which can be rendered elsewhere on the window
        """
        return pygame.surface.Surface((self.config.FOUR_INSTANCE_WIDTH, self.config.FOUR_INSTANCE_HEIGHT))
    
    def render_frame(self, four, key_dict, debug_dict):
        """
        Render the frame of the Four Instance
        
        args:
            four (Four): the Four instance to render
            key_dict (dict): the dictionary of key states
            debug_dict (dict): the dictionary of debug information
        """
        self.surfaces = []
        self.danger = four.danger
        self.game_over = four.game_over
        self.four_surface.fill((0, 0, 0))
        self.window.fill((0, 0, 0))
        
        self.__render_matrix(four)
        self.__render_hold(four)
        self.__render_queue(four)
            
        for surface, coords in self.surfaces:
            self.four_surface.blit(surface, coords)
        
        self.window.blit(self.four_surface, self.__get_four_coords_for_window_center())
        
        if debug_dict:
            self.__draw_debug(debug_dict)
        
        if key_dict:
            self.__draw_key_states(key_dict)
            
        pygame.display.update()
        
    def __get_four_coords_for_window_center(self):
        """
        Get the coordinates for the four surface to be centered in the window
        """
        return (self.config.WINDOW_WIDTH - self.config.FOUR_INSTANCE_WIDTH) // 2, (self.config.WINDOW_HEIGHT - self.config.FOUR_INSTANCE_HEIGHT) // 2
              
    def __draw_grid(self, matrix_surface_rect:pygame.Rect):
        """
        Draw the grid in the background of the matrix
        
        args:
            matrix_surface_rect (pygame.Rect): the rectangle that the matrix is drawn in
        """
        grid_colour = lerpBlendRGBA((0, 0, 0), self.__get_border_colour(), 0.25)
        
        for idx in range(self.config.MATRIX_HEIGHT // 2, self.config.MATRIX_HEIGHT + 1):
            pygame.draw.line(self.four_surface, grid_colour,
                             (matrix_surface_rect.x, matrix_surface_rect.y + idx * self.config.GRID_SIZE - self.config.MATRIX_SURFACE_HEIGHT),
                             (matrix_surface_rect.x + self.config.MATRIX_WIDTH * self.config.GRID_SIZE, matrix_surface_rect.y + idx * self.config.GRID_SIZE - self.config.MATRIX_SURFACE_HEIGHT)
                             )
            
        for idx in range(self.config.MATRIX_WIDTH + 1):
            pygame.draw.line(self.four_surface, grid_colour,
                             (matrix_surface_rect.x + idx * self.config.GRID_SIZE, matrix_surface_rect.y + self.config.MATRIX_SURFACE_HEIGHT),
                             (matrix_surface_rect.x + idx * self.config.GRID_SIZE, matrix_surface_rect.y + self.config.MATRIX_HEIGHT // 2 * self.config.GRID_SIZE - self.config.MATRIX_SURFACE_HEIGHT)
                             )
            
    def __draw_blocks(self, matrix:Matrix, matrix_surface_rect:pygame.Rect, transparent:bool, alpha:float):
        """
        Draw the blocks in the matrix
        
        args:
            matrix (Matrix): the matrix to draw the blocks from
            matrix_surface_rect (pygame.Rect): the rectangle that the matrix is drawn in
            transparent (bool): whether the blocks should be transparent
            alpha (float): the alpha value of the transparency
        """
        for i, row in enumerate(matrix):
            for j, value in enumerate(row):
                if value != 0:
                    if self.game_over:
                        colour = self.config.COLOUR_MAP[8]
                    else:
                        colour = self.config.COLOUR_MAP[value]
                    if transparent:
                        colour = lerpBlendRGBA((0, 0, 0), colour, alpha)
                    pygame.draw.rect(self.four_surface, colour, 
                                     (matrix_surface_rect.x + j * self.config.GRID_SIZE, matrix_surface_rect.y + i * self.config.GRID_SIZE - self.config.MATRIX_SURFACE_HEIGHT, self.config.GRID_SIZE, self.config.GRID_SIZE)
                                     )

    def __draw_matrix_border(self):
        """
        Draw a border around the matrix, garbage, queue and hold
        """
        # ====== MATRIX ======
        
        pygame.draw.line(self.four_surface, self.__get_border_colour(), # matrix left border
                 (self.config.MATRIX_SCREEN_CENTER_X - self.config.BORDER_WIDTH // 2 - 1, self.config.MATRIX_SCREEN_CENTER_Y), 
                 (self.config.MATRIX_SCREEN_CENTER_X - self.config.BORDER_WIDTH // 2 - 1, self.config.MATRIX_SCREEN_CENTER_Y + self.config.MATRIX_SURFACE_HEIGHT - 1), 
                 self.config.BORDER_WIDTH)

        pygame.draw.line(self.four_surface, self.__get_border_colour(),   # matrix right border
                        (self.config.MATRIX_SCREEN_CENTER_X + self.config.MATRIX_SURFACE_WIDTH + self.config.BORDER_WIDTH // 2, self.config.MATRIX_SCREEN_CENTER_Y), 
                        (self.config.MATRIX_SCREEN_CENTER_X + self.config.MATRIX_SURFACE_WIDTH + self.config.BORDER_WIDTH // 2, self.config.MATRIX_SCREEN_CENTER_Y + self.config.MATRIX_SURFACE_HEIGHT - 1), 
                        self.config.BORDER_WIDTH)

        pygame.draw.line(self.four_surface, self.__get_border_colour(),  # matrix bottom border
                        (self.config.MATRIX_SCREEN_CENTER_X - self.config.BORDER_WIDTH - self.config.GRID_SIZE, self.config.MATRIX_SCREEN_CENTER_Y + self.config.MATRIX_SURFACE_HEIGHT + self.config.BORDER_WIDTH // 2 - 1), 
                        (self.config.MATRIX_SCREEN_CENTER_X + self.config.MATRIX_SURFACE_WIDTH + self.config.BORDER_WIDTH - 1, self.config.MATRIX_SCREEN_CENTER_Y + self.config.MATRIX_SURFACE_HEIGHT + self.config.BORDER_WIDTH // 2 - 1), 
                        self.config.BORDER_WIDTH)

        # ====== GARBAGE =======
        
        pygame.draw.line(self.four_surface, self.__get_border_colour(), # left garbage border
                        (self.config.MATRIX_SCREEN_CENTER_X - self.config.BORDER_WIDTH // 2 - 1 - self.config.GRID_SIZE, self.config.MATRIX_SCREEN_CENTER_Y), 
                        (self.config.MATRIX_SCREEN_CENTER_X - self.config.BORDER_WIDTH // 2 - 1 - self.config.GRID_SIZE, self.config.MATRIX_SCREEN_CENTER_Y + self.config.MATRIX_SURFACE_HEIGHT - 1), 
                        self.config.BORDER_WIDTH)
        
        pygame.draw.line(self.four_surface, self.__get_border_colour(),  
                        (self.config.MATRIX_SCREEN_CENTER_X - self.config.BORDER_WIDTH - self.config.GRID_SIZE, self.config.MATRIX_SCREEN_CENTER_Y + self.config.MATRIX_SURFACE_HEIGHT - self.config.GRID_SIZE * 8 + self.config.BORDER_WIDTH // 2 - 1) , 
                        (self.config.MATRIX_SCREEN_CENTER_X - self.config.BORDER_WIDTH , self.config.MATRIX_SCREEN_CENTER_Y + self.config.MATRIX_SURFACE_HEIGHT - self.config.GRID_SIZE * 8 + self.config.BORDER_WIDTH // 2 - 1), 
                        self.config.BORDER_WIDTH)
        
    def __draw_queue_border(self):
        
        match self.config.QUEUE_LENGTH:
            case 1:
                queue_size = self.config.GRID_SIZE * 4.5
            case 2: 
                queue_size = self.config.GRID_SIZE * 7.5
            case 3:
                queue_size = self.config.GRID_SIZE * 10.5
            case 4:
                queue_size = self.config.GRID_SIZE * 13.5
            case 5:
                queue_size = self.config.GRID_SIZE * 16.5
            case 6:
                queue_size = self.config.GRID_SIZE * 19.5
            case _:
                queue_size = self.config.GRID_SIZE * 19.5
      
        pygame.draw.line(self.four_surface, self.__get_border_colour(), # queue left border
                        (self.config.MATRIX_SCREEN_CENTER_X + self.config.MATRIX_SURFACE_WIDTH + 6 * self.config.GRID_SIZE + self.config.BORDER_WIDTH, self.config.MATRIX_SCREEN_CENTER_Y + self.config.GRID_SIZE // 2 - 1),
                        (self.config.MATRIX_SCREEN_CENTER_X + self.config.MATRIX_SURFACE_WIDTH + 6 * self.config.GRID_SIZE + self.config.BORDER_WIDTH, self.config.MATRIX_SCREEN_CENTER_Y + queue_size - self.config.GRID_SIZE // 2 - 1),
                        self.config.BORDER_WIDTH)
        
        pygame.draw.line(self.four_surface, self.__get_border_colour(), # queue bottom border
                (self.config.MATRIX_SCREEN_CENTER_X + self.config.MATRIX_SURFACE_WIDTH + self.config.BORDER_WIDTH + 6 * self.config.GRID_SIZE  + self.config.BORDER_WIDTH // 2, self.config.MATRIX_SCREEN_CENTER_Y + queue_size - self.config.GRID_SIZE // 2 - 1),
                (self.config.MATRIX_SCREEN_CENTER_X + self.config.MATRIX_SURFACE_WIDTH + self.config.BORDER_WIDTH // 2, self.config.MATRIX_SCREEN_CENTER_Y + queue_size - self.config.GRID_SIZE // 2 - 1),
                self.config.BORDER_WIDTH)

        pygame.draw.line(self.four_surface, self.__get_border_colour(), # queue top border
                        (self.config.MATRIX_SCREEN_CENTER_X + self.config.MATRIX_SURFACE_WIDTH + self.config.BORDER_WIDTH + 6 * self.config.GRID_SIZE  + self.config.BORDER_WIDTH // 2, self.config.MATRIX_SCREEN_CENTER_Y + self.config.GRID_SIZE // 2 - 1),
                        (self.config.MATRIX_SCREEN_CENTER_X + self.config.MATRIX_SURFACE_WIDTH + self.config.BORDER_WIDTH // 2, self.config.MATRIX_SCREEN_CENTER_Y + self.config.GRID_SIZE // 2 - 1),
                        self.config.GRID_SIZE)
    
        text_surface = self.hun2_big.render('NEXT', True, (0, 0, 0))
        self.surfaces.append((text_surface, (self.config.MATRIX_SCREEN_CENTER_X + self.config.GRID_SIZE * 10 + self.config.BORDER_WIDTH , self.config.MATRIX_SCREEN_CENTER_Y + self.config.GRID_SIZE * 0.15))) 
        
    def __draw_hold_border(self):
        
        pygame.draw.line(self.four_surface, self.__get_border_colour(), # hold left border
                        (self.config.MATRIX_SCREEN_CENTER_X - 7 * self.config.GRID_SIZE - self.config.BORDER_WIDTH //2 - 1, self.config.MATRIX_SCREEN_CENTER_Y + self.config.GRID_SIZE // 2 - 1),
                        (self.config.MATRIX_SCREEN_CENTER_X - 7 * self.config.GRID_SIZE - self.config.BORDER_WIDTH //2 - 1, self.config.MATRIX_SCREEN_CENTER_Y + 4 * self.config.GRID_SIZE),
                        self.config.BORDER_WIDTH)

        pygame.draw.line(self.four_surface, self.__get_border_colour(), # hold bottom border
                        (self.config.MATRIX_SCREEN_CENTER_X - 7 * self.config.GRID_SIZE - self.config.BORDER_WIDTH, self.config.MATRIX_SCREEN_CENTER_Y + 4 * self.config.GRID_SIZE),
                        (self.config.MATRIX_SCREEN_CENTER_X - self.config.GRID_SIZE - self.config.BORDER_WIDTH, self.config.MATRIX_SCREEN_CENTER_Y + 4 * self.config.GRID_SIZE),
                        self.config.BORDER_WIDTH)

        pygame.draw.line(self.four_surface, self.__get_border_colour(), # hold top border
            (self.config.MATRIX_SCREEN_CENTER_X - 7 * self.config.GRID_SIZE - self.config.BORDER_WIDTH, self.config.MATRIX_SCREEN_CENTER_Y + self.config.GRID_SIZE // 2 - 1),
            (self.config.MATRIX_SCREEN_CENTER_X - self.config.GRID_SIZE - self.config.BORDER_WIDTH, self.config.MATRIX_SCREEN_CENTER_Y + self.config.GRID_SIZE // 2 - 1),
            self.config.GRID_SIZE)
        
            
        text_surface = self.hun2_big.render('HOLD', True, (0, 0, 0))
        self.surfaces.append((text_surface, (self.config.MATRIX_SCREEN_CENTER_X - self.config.GRID_SIZE * 7, self.config.MATRIX_SCREEN_CENTER_Y + self.config.GRID_SIZE * 0.15)))
        
    def draw_danger_crosses(self, matrix: Matrix):
        """
        Draw crosses on the danger matrix
        
        args:
            matrix (Matrix): the matrix to draw the crosses on
        """
        offset = self.config.GRID_SIZE // 5
        for i, row in enumerate(matrix):
            for j, value in enumerate(row):
                if value == -1:
                    start_x = self.config.MATRIX_SCREEN_CENTER_X + j * self.config.GRID_SIZE + offset
                    start_y = self.config.MATRIX_SCREEN_CENTER_Y + i * self.config.GRID_SIZE - self.config.MATRIX_SURFACE_HEIGHT + offset
                    end_x = self.config.MATRIX_SCREEN_CENTER_X + (j + 1) * self.config.GRID_SIZE - offset
                    end_y = self.config.MATRIX_SCREEN_CENTER_Y + (i + 1) * self.config.GRID_SIZE - self.config.MATRIX_SURFACE_HEIGHT - offset
                    
                    pygame.draw.line(self.four_surface, (255, 0, 0), 
                                    (start_x, start_y), 
                                    (end_x, end_y), 
                                    5)
                    pygame.draw.line(self.four_surface, (255, 0, 0), 
                                    (end_x, start_y), 
                                    (start_x, end_y), 
                                    5)
    
    def __get_border_colour(self):
        """
        Get the colour of the border
        """
        if self.danger:
            return (255, 0, 0)
        else:
            return (255, 255, 255)
                          
    def __render_matrix(self, four):
        """
        Render the matrix onto the window
        
        args:
            four (Four): the Four instance to render
        """
        matrix_surface_rect = pygame.Rect(self.config.MATRIX_SCREEN_CENTER_X, self.config.MATRIX_SCREEN_CENTER_Y, self.config.MATRIX_SURFACE_WIDTH, self.config.MATRIX_SURFACE_HEIGHT)
        
        self.__draw_blocks(four.matrix.ghost, matrix_surface_rect, transparent = True, alpha = 0.33)
        self.__draw_grid(matrix_surface_rect)
        self.__draw_blocks(four.matrix.matrix, matrix_surface_rect, transparent = False, alpha = 1)
        self.__draw_blocks(four.matrix.piece, matrix_surface_rect, transparent = False, alpha = 1)
        
        if self.danger:
            self.draw_danger_crosses(four.matrix.danger)
        
        self.__draw_matrix_border() 
        
    
    def __render_queue(self, four):
        """
        Render the queue onto the window
        
        args:
            four (Four): the Four instance to render
        """
        queue_rect = self.__queue_rect(four.queue.length)
        pygame.draw.rect(self.four_surface, (0, 0, 0), queue_rect)
        for idx, tetromino in enumerate(four.queue.queue):
            
            # split queue_rect into four.queue.length number of rows
            row_height = queue_rect.height // four.queue.length
            row_y = queue_rect.y + idx * row_height
            
            preview_rect = pygame.Rect(queue_rect.x, row_y, queue_rect.width, row_height)
            self.__render_tetromino_preview(tetromino, preview_rect)
            self.__draw_queue_border()
       
    def __queue_rect(self, queue_length):
        """
        Get the rectangle for the queue
        
        args:
            queue_length (int): the length of the queue
        """
        rect_x = self.config.MATRIX_SCREEN_CENTER_X + self.config.MATRIX_SURFACE_WIDTH + self.config.BORDER_WIDTH
        rect_y =  self.config.MATRIX_SCREEN_CENTER_Y + 1 * self.config.GRID_SIZE
        rect_width = 6 * self.config.GRID_SIZE
        rect_height = 3 * queue_length * self.config.GRID_SIZE - self.config.BORDER_WIDTH // 2
    
        return pygame.Rect(rect_x, rect_y, rect_width, rect_height)	
        
    def __hold_rect(self):
        """
        Get the rectangle for the hold
        """
        rect_x = self.config.MATRIX_SCREEN_CENTER_X - 7 * self.config.GRID_SIZE
        rect_y =  self.config.MATRIX_SCREEN_CENTER_Y + 1 * self.config.GRID_SIZE
        rect_width = 6 * self.config.GRID_SIZE - self.config.BORDER_WIDTH
        rect_height = 3 * self.config.GRID_SIZE - self.config.BORDER_WIDTH // 2
    
        return pygame.Rect(rect_x, rect_y, rect_width, rect_height)
    
    def __render_hold(self, four):
        """
        Render the hold onto the window
        
        args:
            four (Four): the Four instance
        """
        tetromino = four.held_tetromino    
        hold_rect = self.__hold_rect()
        pygame.draw.rect(self.four_surface, (0, 0, 0), hold_rect)
        if tetromino is not None:
            self.__render_tetromino_preview(tetromino, hold_rect)
        self.__draw_hold_border()
    
    def __render_tetromino_preview(self, tetromino, rect):
        """
        Render a tetromino preview
        
        args:
            tetromino (list): the type of tetromino to render
            rect (pygame.Rect): the rectangle to draw the tetromino in
        """
        tetromino = tetromino_previews(tetromino)
        tetromino_height = len(tetromino) * self.config.GRID_SIZE
        tetromino_width = len(tetromino[0]) * self.config.GRID_SIZE

        offset_x = (rect.width - tetromino_width) // 2
        offset_y = (rect.height - tetromino_height) // 2

        for i, row in enumerate(tetromino):
            for j, value in enumerate(row):
                if value != 0:
                    colour = self.config.COLOUR_MAP[value]
                    pygame.draw.rect(self.four_surface, colour, 
                                    (rect.x + offset_x + j * self.config.GRID_SIZE, rect.y + offset_y + i * self.config.GRID_SIZE, self.config.GRID_SIZE, self.config.GRID_SIZE)
                                    )
    
    def __draw_debug(self, debug_dict):
        """
        Draw the debug information onto the window
        
        args:
            debug_dict (dict): the dictionary of debug information
        """
        debug_surfaces = []

        if debug_dict['FPS'] < self.config.FPS * 0.95:
            fps_colour = (255, 255, 0)
        elif debug_dict['FPS'] < self.config.FPS * 0.5:
            fps_colour = (255, 0, 0)
        elif self.config.UNCAPPED_FPS:
            fps_colour = (0, 255, 255)
        else:
            fps_colour = (0, 255, 0)

        # FPS debug information
        fps_text = f'FPS: {int(debug_dict["FPS"])}'
        if self.config.UNCAPPED_FPS:
            fps_text += ' (UNCAPPED)'
        debug_surfaces.append((self.hun2_big.render(fps_text, True, fps_colour), (self.config.GRID_SIZE // 2, self.config.GRID_SIZE // 2)))

        debug_surfaces.append((self.pfw_small.render(f'worst: {int(debug_dict["WORST_FPS"])} | best: {int(debug_dict["BEST_FPS"])} | current: {int(debug_dict["FPS_RAW"])}', True, fps_colour), (self.config.GRID_SIZE // 2, self.config.GRID_SIZE * 1.5)))

        debug_surfaces.append((self.hun2_small.render(f'Render Time: {get_prefix(debug_dict["REN_T"], "s")}', True, fps_colour), (self.config.GRID_SIZE // 2, self.config.GRID_SIZE * 2)))

        debug_surfaces.append((self.pfw_small.render(f'worst: {get_prefix(debug_dict["WORST_REN_T"], "s")} | best: {get_prefix(debug_dict["BEST_REN_T"], "s")} | current: {get_prefix(debug_dict["REN_T_RAW"], "s")}', True, fps_colour), (self.config.GRID_SIZE // 2, self.config.GRID_SIZE * 2.5)))

        if debug_dict['DF_RAW'] is None:
            debug_dict['DF_RAW'] = 0

        if debug_dict['TPS'] < self.config.TPS * 0.95:
            tps_colour = (255, 0, 0)
        else:
            tps_colour = (0, 255, 0)

        # TPS debug information
        debug_surfaces.append((self.hun2_big.render(f'TPS: {int(debug_dict["TPS"])}', True, tps_colour), (self.config.GRID_SIZE // 2, self.config.GRID_SIZE * 3.5)))

        debug_surfaces.append((self.pfw_small.render(f'worst: {int(debug_dict["WORST_TPS"])} | best: {int(debug_dict["BEST_TPS"])} | current: {int(debug_dict["TPS_RAW"])}', True, tps_colour), (self.config.GRID_SIZE // 2, self.config.GRID_SIZE * 4.5)))

        debug_surfaces.append((self.hun2_small.render(f'Execution Time: {get_prefix(debug_dict["SIM_T"], "s")}', True, tps_colour), (self.config.GRID_SIZE // 2, self.config.GRID_SIZE * 5)))

        debug_surfaces.append((self.pfw_small.render(f'worst: {get_prefix(debug_dict["WORST_SIM_T"], "s")} | best: {get_prefix(debug_dict["BEST_SIM_T"], "s")} | current: {get_prefix(debug_dict["SIM_T_RAW"], "s")}', True, tps_colour), (self.config.GRID_SIZE // 2, self.config.GRID_SIZE * 5.5)))

        debug_surfaces.append((self.hun2_small.render(f'df: {debug_dict["DF"]:.2f}', True, tps_colour), (self.config.GRID_SIZE // 2, self.config.GRID_SIZE * 6)))

        debug_surfaces.append((self.pfw_small.render(f'worst: {debug_dict["WORST_DF"]} | best: {debug_dict["BEST_DF"]} | current: {int(debug_dict["DF_RAW"])}', True, tps_colour), (self.config.GRID_SIZE // 2, self.config.GRID_SIZE * 6.5)))

        debug_surfaces.append((self.hun2_small.render(f'Tick: {debug_dict["TICKCOUNT"]}', True, tps_colour), (self.config.GRID_SIZE // 2, self.config.GRID_SIZE * 7)))
        
        # handling debug information
        
        if debug_dict['POLLING_RATE'] < self.config.POLLING_RATE * 0.95:
            poll_colour = (255, 0, 0)
        else:
            poll_colour = (0, 255, 0)
        
        debug_surfaces.append((self.hun2_big.render(f'POLL: {int(debug_dict["POLLING_RATE"])}', True, poll_colour), (self.config.GRID_SIZE // 2, self.config.GRID_SIZE * 8)))
        
        debug_surfaces.append((self.pfw_small.render(f'worst: {int(debug_dict["WORST_POLLING_RATE"])} | best: {int(debug_dict["BEST_POLLING_RATE"])} | current: {int(debug_dict["POLLING_RATE_RAW"])}', True, poll_colour), (self.config.GRID_SIZE // 2, self.config.GRID_SIZE * 9)))
        
        debug_surfaces.append((self.hun2_small.render(f'Polling Time: {get_prefix(debug_dict["POLLING_T"], "s")}', True, poll_colour), (self.config.GRID_SIZE // 2, self.config.GRID_SIZE * 9.5)))
        
        debug_surfaces.append((self.pfw_small.render(f'worst: {get_prefix(debug_dict["WORST_POLLING_T"], "s")} | best: {get_prefix(debug_dict["BEST_POLLING_T"], "s")} | current: {get_prefix(debug_dict["POLLING_T_RAW"], "s")}', True, poll_colour), (self.config.GRID_SIZE // 2, self.config.GRID_SIZE * 10)))


        if debug_dict['DAS_COUNTER'] < debug_dict['DAS']:
            das_colour = (255, 255, 255)
        else:
            das_colour = (0, 255, 0)

        debug_surfaces.append((self.hun2_big.render(f'DAS: {int(debug_dict["DAS_COUNTER"])} ms', True, das_colour), (self.config.GRID_SIZE // 2, self.config.GRID_SIZE * 11)))
        
        debug_surfaces.append((self.hun2_small.render(f'Threshold: {debug_dict["DAS"]} ms', True, das_colour), (self.config.GRID_SIZE // 2, self.config.GRID_SIZE * 12)))
        
        debug_surfaces.append((self.pfw_small.render(f'DCD: {debug_dict["DCD"]} | DAS Cancel: {debug_dict["DAS_CANCEL"]}', True, das_colour), (self.config.GRID_SIZE // 2, self.config.GRID_SIZE * 12.5)))
        
        if debug_dict['ARR_COUNTER'] < debug_dict['ARR']:
            arr_colour = (255, 255, 255)
        else:
            arr_colour = (0, 255, 0)
        
        debug_surfaces.append((self.hun2_big.render(f'ARR: {int(debug_dict["ARR_COUNTER"])} ms', True, arr_colour), (self.config.GRID_SIZE // 2, self.config.GRID_SIZE * 13.5)))
        
        debug_surfaces.append((self.hun2_small.render(f'Threshold: {debug_dict["ARR"]} ms', True, arr_colour), (self.config.GRID_SIZE // 2, self.config.GRID_SIZE * 14.5)))
        
        debug_surfaces.append((self.pfw_small.render(f'SDF: {debug_dict["SDF"]} | PrevAccHD: {debug_dict["PREVHD"]} | PrefSD: {debug_dict["PREFSD"]}', True, (255, 255, 255)), (self.config.GRID_SIZE // 2, self.config.GRID_SIZE * 15)))
        
        for surface, coords in debug_surfaces:
            self.window.blit(surface, coords)

    def __draw_key_states(self, key_dict):
        """
        Draw the key states onto the window
        
        args:
            key_dict (dict): the dictionary of key states
        """
        key_surfaces = []
        
        left_colour = (255, 255, 255)       if key_dict['KEY_LEFT']               else lerpBlendRGBA((0, 0, 0), (255, 255, 255), 0.33)
        right_colour = (255, 255, 255)      if key_dict['KEY_RIGHT']              else lerpBlendRGBA((0, 0, 0), (255, 255, 255), 0.3)
        softdrop_colour = (255, 255, 255)   if key_dict['KEY_SOFT_DROP']          else lerpBlendRGBA((0, 0, 0), (255, 255, 255), 0.33)
        ccw_colour = (255, 255, 255)        if key_dict['KEY_COUNTERCLOCKWISE']   else lerpBlendRGBA((0, 0, 0), (255, 255, 255), 0.33)
        cw_colour = (255, 255, 255)         if key_dict['KEY_CLOCKWISE']          else lerpBlendRGBA((0, 0, 0), (255, 255, 255), 0.33)
        colour_180 = (255, 255, 255)        if key_dict['KEY_180']                else lerpBlendRGBA((0, 0, 0), (255, 255, 255), 0.33)
        harddrop_colour = (255, 255, 255)   if key_dict['KEY_HARD_DROP']          else lerpBlendRGBA((0, 0, 0), (255, 255, 255), 0.33)
        hold_colour = (255, 255, 255)       if key_dict['KEY_HOLD']               else lerpBlendRGBA((0, 0, 0), (255, 255, 255), 0.33)
        
        key_surfaces.append((self.action_ui.render('B', True, left_colour), (self.config.GRID_SIZE // 2, self.config.GRID_SIZE * 26.5)))

        key_surfaces.append((self.action_ui.render('A', True, right_colour), (self.config.GRID_SIZE *2 , self.config.GRID_SIZE * 26.5)))

        key_surfaces.append((self.action_ui.render('C', True, softdrop_colour), (self.config.GRID_SIZE * 3.5, self.config.GRID_SIZE * 26.5)))

        key_surfaces.append((self.action_ui.render('G', True, harddrop_colour), (self.config.GRID_SIZE * 5, self.config.GRID_SIZE * 26.5)))

        key_surfaces.append((self.action_ui.render('E', True, ccw_colour), (self.config.GRID_SIZE * 6.5, self.config.GRID_SIZE * 26.5)))

        key_surfaces.append((self.action_ui.render('D', True, cw_colour), (self.config.GRID_SIZE * 8, self.config.GRID_SIZE * 26.5)))

        key_surfaces.append((self.action_ui.render('F', True, colour_180), (self.config.GRID_SIZE * 9.5, self.config.GRID_SIZE * 26.5)))

        key_surfaces.append((self.action_ui.render('H', True, hold_colour), (self.config.GRID_SIZE * 11, self.config.GRID_SIZE * 26.5))) 
        
        for surface, coords in key_surfaces:
            self.window.blit(surface, coords)