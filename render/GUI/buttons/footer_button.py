import pygame
from utils import hex_to_rgb, load_image, draw_linear_gradient, draw_solid_colour, draw_border, brightness, align_top_edge, align_bottom_edge, align_right_edge, align_left_edge, align_centre, align_bottom_left, align_bottom_right, align_top_right, align_top_left
from render.GUI.font import Font

class FooterButton():
    def __init__(self, function, Mouse, surface, container, definition):
        
        self.function = function
        self.Mouse = Mouse
        
        self.surface = surface
        self.container = container
        self.definition = definition
        self.width = 70
        self.height = 70
        self.x_start = 70
        self.y_offset = 35
        
        self.__get_rect_and_surface()
        self.render_button()
        self.render_image()
        self.get_hovered_image()
        self.get_pressed_image()
        
        self.state = None
        self.previous_state = None
    
    def __get_rect_and_surface(self):
        self.rect = pygame.Rect(self.container.right - 90, self.container.bottom - self.x_start, self.width, self.height)
        self.button_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.HWSURFACE|pygame.SRCALPHA)
        
    def render_button(self):
        draw_solid_colour(self.button_surface, self.definition['background']['colour'], self.button_surface.get_rect())
        draw_border(self.button_surface, self.definition['border'], self.button_surface.get_rect())
        
    def render_image(self):
        x_padding = self.definition['image']['padding'][0]
        y_padding = self.definition['image']['padding'][1]
        button_width = self.rect.width - x_padding

        image = load_image(self.definition['image']['path'])     
        
        aspect_ratio = image.get_width() / image.get_height()
        new_height = int(button_width * aspect_ratio)

        image = pygame.transform.smoothscale(image, (button_width, new_height))
        image_rect = align_centre(self.button_surface.get_rect(), image.get_width(), image.get_height(), 0, -self.height//2 + y_padding - 2)
        
        self.button_surface.blit(image, image_rect.topleft)
    
    def get_hovered_image(self):
        self.hovered_surface = self.button_surface.copy()
        brightness(self.hovered_surface, 1.2)
    
    def get_pressed_image(self):
        self.pressed_surface = self.button_surface.copy()
        brightness(self.pressed_surface, 1.5)
        
    def draw(self):
        if self.state == 'hovered':
            self.surface.blit(self.hovered_surface, (self.rect.left, self.rect.top))
        elif self.state == 'pressed':
            self.surface.blit(self.pressed_surface, (self.rect.left, self.rect.top))
        else:
            self.surface.blit(self.button_surface, (self.rect.left, self.rect.top))

    def handle_window_resize(self):
        self.__get_rect_and_surface()
        self.render_button()
        self.render_image()
        self.get_hovered_image()
        self.get_pressed_image()
    
    def check_hover(self):
        x, y = self.Mouse.position 
        x -= self.container.left
        y -= self.container.top
        
        if self.rect.collidepoint((x, y)):
            if self.state == 'pressed':
                return
            self.state = 'hovered'
        else:
            self.state = None
       
    def check_events(self):
        
        events_to_remove = []
        
        for event in self.Mouse.events.queue:
            for button, info in event.items():
                if button == 'scrollwheel':
                    return

                event_x, event_y = info['pos']
                event_x -= self.container.left
                event_y -= self.container.top
                
                mouse_x, mouse_y = self.Mouse.position
                mouse_x -= self.container.left
                mouse_y -= self.container.top
                
                if button == 'mb1' and info['down'] and self.rect.collidepoint((event_x, event_y)) and self.rect.collidepoint((mouse_x, mouse_y)):
                    self.state = 'pressed'
                    events_to_remove.append(event)
                
                if button == 'mb1' and info['up'] and self.rect.collidepoint((event_x, event_y)) and self.rect.collidepoint((mouse_x, mouse_y)):
                    self.state = None
                    events_to_remove.append(event)
                    self.function()

        for event in events_to_remove:
            self.Mouse.events.queue.remove(event)
    
    def update(self):
        self.check_hover()
        self.check_events()
        
        if self.state != self.previous_state:
            self.draw()
        
        self.previous_state = self.state