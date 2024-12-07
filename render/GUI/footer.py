import pygame
from utils import hex_to_rgb, load_image, draw_linear_gradient, draw_solid_colour, draw_border, brightness, align_top_edge, align_bottom_edge, align_right_edge, align_left_edge, align_centre, align_bottom_left, align_bottom_right, align_top_right, align_top_left, apply_gaussian_blur_with_alpha
from render.GUI.font import Font

class Footer:
    def __init__(self, container, height, text, background, border, image = None):
        self.container = container
        self.height = height
        self.text = text
        self.background = background
        self.border = border
              
        self.font = Font('hun2', 30)
        self.image = image
        
        self.shadow_radius = 5
        
        self.__get_rect_and_surface()
        self.__load_image()
        self.render()

    def __get_rect_and_surface(self):
        self.width = self.container.width
        
        self.rect = align_bottom_edge(self.container, self.width, self.height, 0, 0)
        self.footer_surface = pygame.Surface((self.width, self.height), pygame.HWSURFACE)
        
        self.shadow_rect = pygame.Rect(self.rect.left - self.shadow_radius * 2, self.rect.top - self.shadow_radius * 2, self.rect.width + self.shadow_radius * 4, self.rect.height + self.shadow_radius * 4)
        self.shadow_surface = pygame.Surface((self.shadow_rect.width, self.shadow_rect.height), pygame.HWSURFACE|pygame.SRCALPHA)
        
    def render(self):
        self.__render_shadow()
        self.__render_background()
        self.__render_border()
        self.__render_text()
        self.__render_image()
    
    def __load_image(self):
        if self.image:
            self.image = load_image(self.image["path"])
        else:
            self.image = None
    
    def __render_background(self):
        if self.background['style'] == 'linear_gradient':
            draw_linear_gradient(self.footer_surface, self.background['colours'][0], self.background['colours'][1], self.footer_surface.get_rect())
        elif self.background['style'] == 'solid':
            draw_solid_colour(self.footer_surface, self.background['colour'], self.footer_surface.get_rect())
            
    def __render_border(self):
        draw_border(self.footer_surface, self.border, self.footer_surface.get_rect())
    
    def __render_text(self):
        self.font.draw(self.footer_surface, self.text['display_text'], self.text['colour'], 'left', 20, 0)
         
    def __render_image(self):
        
        if self.image is None:
            return
        
        aspect_ratio = self.image.get_width() / self.image.get_height()
        new_height = self.height - 25
        new_width = int(new_height * aspect_ratio)
        
        image = pygame.transform.smoothscale(self.image, (new_width, new_height))
        image_rect = align_centre(self.footer_surface.get_rect(), image.get_width(), image.get_height(), 0, 0)

        self.footer_surface.blit(image, (image_rect.left + self.footer_surface.get_rect().width//2 - new_width - 45, image_rect.top))
    
    def __render_shadow(self):
        pygame.draw.rect(self.shadow_surface, (0, 0, 0), pygame.Rect(self.shadow_radius * 2, self.shadow_radius * 2, self.shadow_rect.width - 4 * self.shadow_radius, self.shadow_rect.height - 4 * self.shadow_radius))
        self.shadow_surface = apply_gaussian_blur_with_alpha(self.shadow_surface, self.shadow_radius)
        
        
    def draw(self, surface):
        surface.blit(self.shadow_surface, self.shadow_rect.topleft)
        surface.blit(self.footer_surface, self.rect.topleft)
        
    def handle_window_resize(self):
        self.__get_rect_and_surface()
        self.render()