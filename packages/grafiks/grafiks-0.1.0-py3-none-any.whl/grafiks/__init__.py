__version__ = '0.1.0'
import pygame
class Grafik:
    def __init__(self, screen_width, screen_height, title='Hello'):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.keys={}
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption(title)
    def draw_rect(self, x, y, width, height, color):
        # Draw a rectangle with the given parameters
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, color, rect)

    def draw_oval(self, x, y, radius, color):
        # Draw a circle with the given parameters
        center = (x, y)
        pygame.draw.circle(self.screen, color, center, radius)

    def draw_line(self, start_x, start_y, end_x, end_y, color, thickness):
        # Draw a line with the given parameters
        start_pos = (start_x, start_y)
        end_pos = (end_x, end_y)
        pygame.draw.line(self.screen, color, start_pos, end_pos, thickness)

    def draw_text(self, text, x, y, font_size, color):
        # Draw text with the given parameters
        font = pygame.font.Font("VictorMono-Medium.tff", font_size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_image(self, image_path, x, y):
        # Load an image and blit it onto the screen at the given position
        image = pygame.image.load(image_path)
        self.screen.blit(image, (x, y))

    def tick(self):
        self.keys={}
        # Update the screen with all the drawn elements
        pygame.display.flip()

    def clear(self,color):
        # Clear the screen
        self.screen.fill(color)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                self.keys[pygame.key.name(event.key)]=True
                print(self.keys)
    def key_pressed(self,key):
        try:
            if self.keys[key]==True:
                return True
        except:
            pass