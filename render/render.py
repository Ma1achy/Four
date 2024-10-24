import pygame.gfxdraw
import pygame, math
import numpy as np
from config import StructConfig
from core.state.struct_render import StructRender
from core.state.struct_flags import StructFlags
from core.state.struct_gameinstance import StructGameInstance
from core.state.struct_timing import StructTiming
from core.state.struct_debug import StructDebug
from utils import lerpBlendRGBA, get_tetromino_blocks, get_prefix, smoothstep, TransformSurface, RotateSurface, ScaleSurface

from render.UI.debug_menu import UIDebug
from render.UI.key_states_overlay import UIKeyStates
from render.board.board import Board
from render.fonts import Fonts

class Render():
    def __init__(self, Config:StructConfig, RenderStruct:StructRender, Flags:StructFlags, GameInstanceStruct:StructGameInstance, TimingStruct:StructTiming, DebugStruct:StructDebug):  
        """
        Render an instance of four onto a window
        
        args:
            self.window (pygame.Surface): the window to render the game onto
        """
        
        self.Config = Config
        self.RenderStruct = RenderStruct
        self.FlagStruct = Flags
        self.GameInstanceStruct = GameInstanceStruct
        self.TimingStruct = TimingStruct
        self.DebugStruct = DebugStruct
        
        self.angle = 0
    
        self.board_center_screen_pos_x = self.RenderStruct.WINDOW_WIDTH // 2 
        self.board_center_screen_pos_y = self.RenderStruct.WINDOW_HEIGHT // 2
      
        self.window = self.__init_window()
        self.Fonts = Fonts(self.RenderStruct)
        
        self.Board = Board(self.Config, self.RenderStruct, self.FlagStruct, self.GameInstanceStruct, self.TimingStruct, self.DebugStruct, self.Fonts)
        self.UI_Debug = UIDebug(self.Config, self.RenderStruct, self.DebugStruct, self.FlagStruct, self.Fonts)
        self.UI_KeyStates = UIKeyStates(self.RenderStruct, self.Fonts)
        
        self.image_path = 'render\image.jpg'
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, (self.RenderStruct.WINDOW_WIDTH, self.RenderStruct.WINDOW_HEIGHT))
        
    def __init_window(self):
        """
        Create the window to draw to
        """
        pygame.display.set_caption(self.RenderStruct.CAPTION)
        return pygame.display.set_mode((self.RenderStruct.WINDOW_WIDTH, self.RenderStruct.WINDOW_HEIGHT), pygame.HWSURFACE|pygame.DOUBLEBUF)
     
    def RenderFrame(self):
        """
        Render the frame of the Four Instance
        """
        # self.RenderStruct.surfaces = []

        self.window.fill((32, 32, 32))
        self.window.blit(self.image, (0, 0))
        
        board_surface = self.Board.get_board_surface()
        self.Board.draw(board_surface)
        
        self.angle = 0
        offset_x, offset_y = 0, 0
        scale = 1
        
        transformed_surface, transformed_rect = TransformSurface(board_surface, scale, self.angle, (self.Board.board_center_x_board_space, self.Board.board_center_y_board_space), (self.board_center_screen_pos_x, self.board_center_screen_pos_y), (offset_x, offset_y))
        
        self.window.blit(transformed_surface, transformed_rect.topleft)
    
        # self.angle = 0
        # offset_x, offset_y = 0, 0
        # scale = 1
    
        # transformed_surface, transformed_rect = TransformSurface(self.board_surface, scale, self.angle, (self.board_center_x_board_space, self.board_center_y_board_space), (self.board_center_screen_pos_x, self.board_center_screen_pos_y), (offset_x, offset_y))
        # self.RenderStruct.surfaces.append((transformed_surface, transformed_rect.topleft))
    
        # for surface, coords in self.RenderStruct.surfaces:
        #     self.window.blit(surface, coords)
        
        # if self.RenderStruct.draw_guide_lines:
        #     pygame.draw.line(self.window, (255, 0, 255), (self.RenderStruct.WINDOW_WIDTH // 2, 0), (self.RenderStruct.WINDOW_WIDTH // 2, self.RenderStruct.WINDOW_HEIGHT), 1)
        #     pygame.draw.line(self.window, (255, 0, 255), (0, self.RenderStruct.WINDOW_HEIGHT // 2), (self.RenderStruct.WINDOW_WIDTH, self.RenderStruct.WINDOW_HEIGHT // 2), 1)
        #     pygame.draw.line(self.window, (0, 255, 0), (self.RenderStruct.WINDOW_WIDTH // 4, 0), (self.RenderStruct.WINDOW_WIDTH // 4, self.RenderStruct.WINDOW_HEIGHT), 1)
        #     pygame.draw.line(self.window, (0, 255, 0), (0, self.RenderStruct.WINDOW_HEIGHT // 4), (self.RenderStruct.WINDOW_WIDTH, self.RenderStruct.WINDOW_HEIGHT // 4), 1)
        #     pygame.draw.line(self.window, (0, 255, 0), (self.RenderStruct.WINDOW_WIDTH // 4 * 3, 0), (self.RenderStruct.WINDOW_WIDTH // 4 * 3, self.RenderStruct.WINDOW_HEIGHT), 1)
        #     pygame.draw.line(self.window, (0, 255, 0), (0, self.RenderStruct.WINDOW_HEIGHT // 4 * 3), (self.RenderStruct.WINDOW_WIDTH, self.RenderStruct.WINDOW_HEIGHT // 4 * 3), 1)
    
        self.UI_Debug.draw(self.window)
        self.UI_KeyStates.draw(self.window)
        
        pygame.display.update()


