import pygame

import sys

from blocks import Block

from settings import Settings

from player import Player

import random

from button import Button

from monster import Monster

class VentShaft:
    def __init__(self):
        """Game resource initialization and creation"""
        pygame.init()
        self.settings= Settings()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Vent Shaft")
        self.player = Player(self)
        self.monster = Monster(self)

        # Sounds
        self.vent_sound = pygame.mixer.Sound("sounds/creepy vent.mp3")
        self.vent_sound.set_volume(0.7)  # Громкость от 0 до 1
        self.vent_channel = None

        # Creating blocks
        self.blocks = []
        self.create_grid()

        # Creating a flag for a game
        self.game_active = "not active"

        # Creating a play button
        self.play_button = Button(self,"Play")

        self.fixed = False

        # if exit status is False, the exit is visible. Otherwise, it is invisible
        self.exit_status_flag = False

        self.radar_active = False

        # the number of available radar use
        self.radar_left = 20

        # this variable is needed to remember the last time when radar was used
        self.radar_turn = -10

        # The number of available audio use
        self.audio_left = 10

        # this variable is needed to remember the last time when radar was used
        self.audio_turn = 0

        # this variable is needed when player uses audio
        self.audio_flag = False

        # row and column are needed to identify where player wants to play audio
        self.audio_row = ""
        self.audio_column = ""

        # random monster spawn
        self.monster.random_position_monster(self.blocks)

        # This variable is used specifically for player movement
        self.death = False

        # Cooldown
        # when player moved last time
        self.last_move_time = 0

        # time delay for each movement
        self.move_delay = 1000

    def run_game(self):
        """Starts the main loop"""
        while True:
            # Tracking events
            self.check_events()

            # Displaying the last screen
            self.update_screen()
            self.clock.tick(60)

    def check_events(self):
        """Checking events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_play_button_click(mouse_pos)
                self.check_mouse_click(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)

    def check_keydown_events(self,event):
        # Reacting when a key is pressed
        if self.game_active == "active":
            if  event.key == pygame.K_y:
                # Player doesn't make any sound
                self.made_sound_this_turn = False

                # Updating player's previous positions
                self.player.player_previous_row = self.player.player_position_row
                self.player.player_previous_column = self.player.player_position_column

                # Updating player's previous turns
                self.player.previous_turn = self.player.turns
                # Add +1 to the current turns
                self.player.turns += 1
            elif event.key == pygame.K_r:

                # Player can use a radar when there is one available and only if player used it 3 or more turns ago
                if self.radar_left > 0 and self.player.turns - self.radar_turn >= 3:

                    # Player makes sound(it attracts monster in close range)
                    self.made_sound_this_turn = True
                    self.radar_active = True
                    self.player.previous_turn = self.player.turns
                    self.radar_activation()
                    self.radar_left -= 1

                    # Updating the last turns when a radar was used
                    self.radar_turn = self.player.turns

            elif event.key == pygame.K_v:

                # Player can use audio when there is one available and only if player used it 10 or more turns ago
                if self.audio_left > 0 and self.player.turns - self.audio_turn >= 10:

                    # Player makes sound(it attracts monster in close range)
                    self.made_sound_this_turn = True
                    mouse_pos = pygame.mouse.get_pos()
                    self.audio_play(mouse_pos)
                    self.audio_turn = self.player.turns
        if event.key == pygame.K_q:
            sys.exit()

    def audio_play(self, mouse_pos):
        """Playing audio in a block that will attract a monster"""
        for index_row, x in enumerate(self.blocks):
            for index_column, block in enumerate(x):
                # if mouse is on any block
                if block.rect.collidepoint(mouse_pos):
                    self.player.player_previous_row = self.player.player_position_row
                    self.player.player_previous_column = self.player.player_position_column
                    self.current_turn_audio = self.player.turns
                    self.player.previous_turn = self.player.turns
                    self.player.turns += 1
                    self.audio_flag = True

                    # Audio attracts a monster during 5 turns
                    self.audio_duration = 4
                    self.audio_row = index_row
                    self.audio_column = index_column

    def audio_stop_playing(self):
        """Stops audio after 4 turns"""
        if self.current_turn_audio + 4 <= self.player.turns:
            self.audio_flag = False

    def radar_activation(self):
        """Checking nearby blocks, is there an exit?"""
        self.player.player_previous_row = self.player.player_position_row
        self.player.player_previous_column = self.player.player_position_column
        self.player.turns += 1

        # Time when it was activated
        self.radar_activated_at = pygame.time.get_ticks()

        # Radar itself
        new_row = self.player.player_position_row
        new_column = self.player.player_position_column

        # checks area 5 x 5
        for row in range(-2, 3):
            for column in range(-2, 3):
                check_row = new_row + row
                check_column = new_column + column
                if check_row == self.exit_row and check_column == self.exit_column:
                    self.exit_status_flag = True
                if check_row == self.monster.monster_row and check_column == self.monster.monster_column:
                    self.monster.visible_monster = True


    def radar_deactivation(self):
        """When radar should deactivate"""
        self.current_time = pygame.time.get_ticks()

        # 5 seconds
        if self.player.turns - self.radar_turn >= 1:
            self.exit_status_flag = False
            self.monster.visible_monster = False
            self.radar_active = False

    def monster_go_away(self):
        """Monster ignores the player if he doesn't move, the monster should go to another direction"""
        d_r = self.player.player_position_row - self.monster.monster_row
        d_c = self.player.player_position_column - self.monster.monster_column
        directions = [[-1, 0], [0, -1], [1, 0], [0, 1]]
        directions.remove([int(d_r), int(d_c)])
        self.monster.monster_mechanism(directions, self.blocks)

    def check_mouse_click(self, mouse_pos):
        """Checks if the player clicks on a block"""
        for index_row, x in enumerate(self.blocks):
            for index_column, block in enumerate(x):
                if block.rect.collidepoint(mouse_pos):
                    self.check_adjacent_blocks(index_row, index_column)
                    break

    def check_play_button_click(self,mouse_pos):
        """Starts a new game if PLAY is pressed"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and (self.game_active in ["not active", "Game over", "won"]):

           # Resetting the player's and monster's positions
           self.player.player_position_row = 0
           self.player.player_position_column = 0
           self.monster.random_position_monster(self.blocks)

           # Resetting turns, fix, radar and audio:
           self.player.turns = 0
           self.player.previous_turn = 0
           self.player.fixing_turns = 0
           self.fixed = False
           self.exit_status_flag = False
           self.radar_active = False
           self.audio_flag = False
           self.radar_left = 20
           self.radar_turn = -10
           self.audio_left = 10
           self.audio_turn = -10
           self.monster.visible_monster = False
           self.death = False
           self.last_move_time = 0

           # Creating an exit
           self.exit_row = random.randint(6, (len(self.blocks) - 1))
           self.exit_column = random.randint(7, (len(self.blocks[0]) - 1))
           self.fix_row = random.randint(5, (len(self.blocks) - 1))
           self.fix_column = random.randint(5, (len(self.blocks[0]) - 1))
           self.game_active = "active"

    def check_adjacent_blocks(self, index_row, index_column):
        """Checks if chosen block is adjacent to current player's position and moves player to it"""
        current_row = self.player.player_position_row
        current_column = self.player.player_position_column
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time >= self.move_delay:
            if index_column == current_column:
                if index_row == current_row + 1 or index_row == current_row - 1:
                    self.player.player_movement(index_row, index_column)
                    self.last_move_time = current_time
                    # if player moves and is 1 block away from a monster, then he dies
                    if self.death:
                        self.game_active = "Game over"
                    self.made_sound_this_turn = True
            elif (
                    index_column == current_column + 1 or index_column == current_column - 1) and index_row == current_row:
                self.player.player_movement(index_row, index_column)
                self.last_move_time = current_time
                if self.death:
                    self.game_active = "Game over"
                self.made_sound_this_turn = True

    def creepy_vent_play(self):
        """Background sounds"""
        if not self.vent_channel or not self.vent_channel.get_busy():
            self.vent_channel = self.vent_sound.play(loops=-1)

    def creepy_vent_stop(self):
        if self.vent_channel and self.vent_channel.get_busy():
            self.vent_channel.stop()

    def update_screen(self):
        """Updating the screen"""
        self.screen.fill(self.settings.screen_bg_color)

        # If game is not active, it shows the button Play
        if self.game_active == "not active":
            self.play_button.draw_button()
            self.creepy_vent_stop()
        # if player won the game, it shows button Play and a text
        elif self.game_active == "won":
            self.screen.blit(self.settings.win_text, self.settings.win_text_rect)
            self.play_button.draw_button()
            self.creepy_vent_stop()

        elif self.game_active == "active":
        # Displaying blocks
            self.display_blocks()

            # Identifying which block is used by player
            used_block = self.blocks[self.player.player_position_row][self.player.player_position_column]

            # Displaying player
            self.player.display_player((used_block.x_position, used_block.y_position))

            # Adding sounds while player is in the vent
            self.creepy_vent_play()

            # Blinking
            self.player.update_alpha()
            monster_used_block = self.blocks[self.monster.monster_row][self.monster.monster_column]

            if self.monster.visible_monster:
                self.monster.display_monster((monster_used_block.x_position, monster_used_block.y_position))
                self.monster.update_alpha_for_monster()

            # if monster is 1 block away from player
            if self.monster.monster_close_to_player(self.player.player_position_row, self.player.player_position_column):
                self.death = True
            else:
                self.death = False
            # Did player make a turn?
            if self.player.player_did_anything():
                # When player doesn't move, sound turns decreases
                if not self.player.player_changed_block() and self.player.sound_turns > 0:
                    self.player.sound_turns -= 1
                self.player.previous_turn = self.player.turns

                # monster moves
                if self.monster.monster_close_to_player(self.player.player_position_row,
                                                        self.player.player_position_column):
                    if self.made_sound_this_turn:
                        self.game_active = "Game over"
                    else:
                        self.monster_go_away()

                else:
                    if not self.audio_flag:
                        self.monster.monster_movement(self.blocks, self.player.sound_turns,
                                                        self.player.player_position_row,
                                                      self.player.player_position_column)
                    else:
                        self.monster.monster_movement(self.blocks, self.audio_duration,
                                                      self.audio_row, self.audio_column)

                # If he is in the block that has to be fixed
                if self.fixed == False and self.player.fix_counter(self.fix_row, self.fix_column):
                    self.fixed = self.player.update_fixing()

            # Radar stops working
            if self.radar_active:
                self.radar_deactivation()
            self.check_event_win()
            if self.audio_flag:
                self.audio_stop_playing()

        # When the monster catches player
        elif self.game_active == "Game over":
            self.creepy_vent_stop()
            self.screen.blit(self.settings.lose_text, self.settings.lose_text_rect)
            self.play_button.draw_button()
        pygame.display.flip()

    def check_event_win(self):
        """Checking if player found an exit"""
        player_row = self.player.player_position_row
        player_column = self.player.player_position_column
        if self.fixed and player_row == self.exit_row and player_column == self.exit_column:
            """The player wins!"""
            self.game_active = "won"

    def create_grid(self):
        """Creating blocks"""
        y_position = 100

        # Creating columns
        for y in range(12):
            x_position = 100
            row = []
            # Creating rows
            for x in range(22):
                block = Block(self, x_position, y_position)
                row.append(block)

                # Interval x
                x_position += 2 * self.settings.block_width

            # Interval y
            y_position += 2 * self.settings.block_height
            self.blocks.append(row)

    def display_blocks(self):
        """Display blocks"""
        for index_row, row in enumerate(self.blocks):
            for index_column, block in enumerate(row):
                self.common_exit_audio_and_fix_blocks(index_row, index_column, block)

    def common_exit_audio_and_fix_blocks(self,index_row, index_column,block):
        """Randomly choosing which block is an exit and saving its coordinates"""
        if index_row == self.exit_row and index_column == self.exit_column:
            if self.exit_status_flag:
                block.exit()
            else:
                block.common()
        elif index_row == self.fix_row and index_column == self.fix_column:
            if self.fixed:
                block.common()
            else:
                block.has_to_be_fixed()
        elif self.audio_flag and index_row == self.audio_row and index_column == self.audio_column:
            block.audio_playing()
        else:
            block.common()


if __name__ == "__main__":
    """Creating a game module and launching it"""
    vt = VentShaft()
    vt.run_game()