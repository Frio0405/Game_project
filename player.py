import pygame.draw


class Player:
    def __init__(self, vent_shaft):
        """Main properties of player"""
        self.screen = vent_shaft.screen
        self.settings = vent_shaft.settings
        self.state = 0
        self.surface = pygame.Surface((30, 30), pygame.SRCALPHA)
        self.alpha = 255
        self.surface_rect = self.surface.get_rect()
        self.alpha_direction = 1
        # For turns and fixing
        # Storing information about the number of turns
        self.turns = 0
        self.previous_turn = 0

        # if fixing turns equals to 2, then the block is fixed
        self.fixing_turns = 0
        self.sound_turns = 0
        self.dynamic_settings()

    def dynamic_settings(self):
        self.player_previous_row = 0
        self.player_previous_column = 0
        self.player_position_row = 0
        self.player_position_column = 0

    def update_alpha(self):
        """Controlling transparency"""
        if self.alpha <= 0 or self.alpha >= 255:
            self.alpha_direction *= -1
        self.alpha += self.alpha_direction * 5

    def display_player(self, center_position):
        """Displaying player"""
        pygame.draw.circle(self.surface, (255, 255, 255, self.alpha), self.surface_rect.center, 10)
        self.screen.blit(self.surface, center_position)

    def player_movement(self, index_row, index_column):
        """Moving player"""
        # Saving its previous positions
        self.player_previous_row = self.player_position_row
        self.player_previous_column = self.player_position_column
        self.previous_turn = self.turns
        self.turns += 1
        self.player_position_row = index_row
        self.player_position_column = index_column
        self.sound_turns = 2

    def player_changed_block(self):
        """Did player move?"""
        return not (self.player_position_row == self.player_previous_row and
                   self.player_position_column == self.player_previous_column)

    def player_did_anything(self):
        # Did a player make a turn?
        return self.previous_turn != self.turns

    def fix_counter(self, fix_row, fix_column):
        """Checks if player can fix the block"""
        return (self.player_position_row == fix_row and
                self.player_position_column == fix_column)

    def update_fixing(self):
        # Checking if player is fixing the block
        if not self.player_changed_block():
            print(self.fixing_turns)
            self.fixing_turns += 1
        else:
            print(self.fixing_turns)
            self.fixing_turns = 0

        return self.fixing_turns == 2