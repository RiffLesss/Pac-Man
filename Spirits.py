import os
import sys
import pygame

pygame.init()
all_sprites = pygame.sprite.Group()
spirits_group = pygame.sprite.Group()
tile_width = tile_height = 24


class Blinky(pygame.sprite.Sprite):                                                  # Блинки - Красный призрак
    def __init__(self, pos_x, pos_y, choord_x, choord_y, filename):
        super().__init__(spirits_group, all_sprites)
        self.mission = ('', '')
        self.image = filename
        self.choord_x = choord_x
        self.choord_y = choord_y
        self.rect = self.image.get_rect().move(tile_width * pos_x - 10, tile_height * pos_y - 10)

    def get_a_mission(self, choord_x, choord_y):
        self.mission = (choord_x, choord_y)

    def folow(self, karta, blinky_last_position, x, y, m_x, m_y):
        x = int(x)
        y = int(y)
        possible_turns = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        for i in range(len(possible_turns)):
            if possible_turns[i] == blinky_last_position:
                del possible_turns[i]
                break
        if karta[x + 1][y] == '1':
            for i in range(len(possible_turns)):
                if possible_turns[i] == 'UP':
                    del possible_turns[i]
                    break
        if karta[x - 1][y] == '1':
            for i in range(len(possible_turns)):
                if possible_turns[i] == 'DOWN':
                    del possible_turns[i]
                    break
        if karta[x][y + 1] == '1':
            for i in range(len(possible_turns)):
                if possible_turns[i] == 'RIGHT':
                    del possible_turns[i]
                    break
        if karta[x + 1][y] == '1':
            for i in range(len(possible_turns)):
                if possible_turns[i] == 'LEFT':
                    del possible_turns[i]
                    break
        min_l = 0
        min_way = ''
        if len(possible_turns) == 1:
            min_way = possible_turns[0]
            return min_way
        else:
            possible_turns_coords = list()
            for turn in possible_turns:
                if turn == 'UP':
                    sp_x, sp_y = x - 1, y
                    possible_turns_coords.append([sp_x, sp_y, 'UP'])
                if turn == 'DOWN':
                    sp_x, sp_y = x + 1, y
                    possible_turns_coords.append([sp_x, sp_y, 'DOWN'])
                if turn == 'LEFT':
                    sp_x, sp_y = x, y - 1
                    possible_turns_coords.append([sp_x, sp_y, 'LEFT'])
                if turn == 'RIGHT':
                    sp_x, sp_y = x, y + 1
                    possible_turns_coords.append([sp_x, sp_y, 'RIGHT'])
            for coords in possible_turns_coords:
                l = (((int(m_y) - int(coords[1])) ** 2) * ((int(m_x) - int(coords[0])) ** 2)) ** 0.5
                if l < 0:
                    l = -l
                coords.append(l)
                if l > min_l:
                    min_l = 0
                    min_way = coords[2]
            return min_way
