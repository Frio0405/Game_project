import pygame.draw

import random

import math
class Monster:
    def __init__(self, vent_shaft):
        """Main properties of the player"""
        self.vent_shaft = vent_shaft
        self.screen = vent_shaft.screen
        self.settings = vent_shaft.settings
        self.state = 0
        self.surface = pygame.Surface((30, 30), pygame.SRCALPHA)
        self.alpha = 255
        self.surface_rect = self.surface.get_rect()
        self.alpha_direction = 1
        self.monster_previous_row = 0
        self.monster_previous_column = 0
        self.visible_monster = False

    def random_position_monster(self, blocks):
        # Monster position
        self.monster_row = random.randint(4, 11)
        self.monster_column = random.randint(4, 11)

    def update_alpha_for_monster(self):
        """Controlling transparency"""
        if self.alpha <= 0 or self.alpha >= 255:
            self.alpha_direction *= -1
        self.alpha += self.alpha_direction * 5

    def display_monster(self, center_position):
        """Displaying a monster"""
        pygame.draw.circle(self.surface, (156, 17, 31, self.alpha), self.surface_rect.center, 12)
        self.screen.blit(self.surface, center_position)

    def monster_movement(self, blocks, sound_turns, player_position_row, player_position_column):
        """Monster moves randomly or to the target if the player makes sound"""
        if sound_turns:
            d_r = player_position_row - self.monster_row
            d_c = player_position_column - self.monster_column
            directions = []
            if d_r < 0:
                directions.append([-1, 0])
            elif d_r > 0:
                directions.append([1, 0])
            if d_c < 0:
                directions.append([0, -1])
            elif d_c > 0:
                directions.append([0, 1])
            self.monster_mechanism(directions, blocks)
        else:
            # Monster moves randomly
            directions = [[-1, 0], [0, -1], [1, 0], [0, 1]]
            self.monster_mechanism(directions, blocks)

    def monster_mechanism(self, directions, blocks):
        """Monster moving logic"""
        random.shuffle(directions)
        for direct in directions:
            if (-1 < self.monster_row + direct[0] < len(blocks)
                    and -1 < self.monster_column + direct[1] < len(blocks[0])):
                self.monster_previous_row = self.monster_row
                self.monster_previous_column = self.monster_column
                self.monster_row += direct[0]
                self.monster_column += direct[1]
                break

    def monster_close_to_player(self, player_position_row, player_position_column) :
        """Identifying if monster is close to player"""
        d_r = math.fabs(player_position_row - self.monster_row)
        d_c = math.fabs(player_position_column - self.monster_column)
        return (d_r == 1 and d_c == 0) or (d_r == 0 and d_c == 1) or (d_r == 0 and d_c == 0)



