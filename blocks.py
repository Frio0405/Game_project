import pygame

class Block:
    def __init__(self, vent_shaft,x_position, y_position):
        """Class for blocks in the vent shaft creation"""
        self.screen =vent_shaft.screen
        self.settings = vent_shaft.settings
        self.x_position = x_position
        self.y_position = y_position
        self.rect = pygame.Rect(x_position, y_position, self.settings.block_width, self.settings.block_height)


    def common(self):
        """For common blocks"""
        pygame.draw.rect(self.screen, self.settings.block_common_color, self.rect, width = 1)

    def exit(self):
        """For the exit block"""
        pygame.draw.rect(self.screen, self.settings.block_exit_color, self.rect, width = 1)

    def has_to_be_fixed(self):
        """For the block that has to be fixed"""
        pygame.draw.rect(self.screen, self.settings.block_fix_color, self.rect,width = 1)

    def audio_playing(self):
        """The block makes sound should turn green!"""
        pygame.draw.rect(self.screen, self.settings.block_audio_color, self.rect, width = 1)

