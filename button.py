import pygame.font

class Button:
    """Class for creating buttons for the game"""

    def __init__(self,ai_game,msg):
        """Game initialization"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Giving properties to a button
        self.width, self.height = 200,50
        self.button_color = (30,87,152)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None,48)

        # Creating the button's rect and centering alignment
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Message appears only once
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Transforms message into a rect and centers it"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Displays an empty button and shows the message"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
