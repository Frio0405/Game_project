import pygame

class Settings:
    def __init__(self):
        """Main settings"""
        # Screen settings
        self.screen_width = 1600
        self.screen_height = 900
        self.screen_bg_color = (15, 37, 49)

        # Main properties of the block
        self.block_state = 0
        self.block_width = 30
        self.block_height = 30

        # Colors of block
        self.block_common_color = (255, 255, 255)
        self.block_exit_color = (175, 25, 25)
        self.block_fix_color = (196, 96, 30)
        self.block_audio_color = (42, 176, 56)

        # Text when the player wins
        self.font_won = pygame.font.SysFont(None, 72)  # Шрифт по умолчанию, размер 72
        self.win_text = self.font_won.render("YOU WON!", True, (255, 255, 255))  # Белый цвет
        self.win_text_rect = self.win_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 100))

        # Text when the player loses
        self.font_lost = pygame.font.SysFont(None, 72)  # Шрифт по умолчанию, размер 72
        self.lose_text = self.font_lost.render("GAME OVER", True, (164, 0, 16))
        self.lose_text_rect = self.win_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 100))
