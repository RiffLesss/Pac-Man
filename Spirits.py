import os
import sys
import pygame
from random import randint


pygame.init()
all_sprites = pygame.sprite.Group()
spirits_group = pygame.sprite.Group()
tile_width = tile_height = 24
STEP = 24


class Blinky(pygame.sprite.Sprite):                                            # TODO Блинки - Красный призрак TODO
    def __init__(self, pos_x, pos_y, choord_x, choord_y, filename):
        super().__init__(spirits_group, all_sprites)
        self.mission = ('', '')
        self.image = filename
        self.choord_x = choord_x
        self.choord_y = choord_y
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect().move(tile_width * self.pos_x - 10, tile_height * self.pos_y - 10)

    def get_a_mission(self, choord_x, choord_y, red_terror):
        if red_terror:
            self.mission = (0, 25)
        else:
            self.mission = (choord_x, choord_y)

    def folow(self, karta, blinky_last_position, x, y, m_x, m_y, possible_turns):
        x = int(x)
        y = int(y)
        for i in range(len(possible_turns)):
            if possible_turns[i] == blinky_last_position:
                del possible_turns[i]
                break
        if karta[x + 1][y] == '1' or karta[x + 1][y] == 'x' or karta[x + 1][y] == 'S':
            for i in range(len(possible_turns)):
                if possible_turns[i] == 'DOWN':
                    del possible_turns[i]
                    break
        if karta[x - 1][y] == '1' or karta[x - 1][y] == 'x' or karta[x - 1][y] == 'S':
            for i in range(len(possible_turns)):
                if possible_turns[i] == 'UP':
                    del possible_turns[i]
                    break
        if karta[x][y + 1] == '1' or karta[x][y + 1] == 'x' or karta[x][y + 1] == 'S':
            for i in range(len(possible_turns)):
                if possible_turns[i] == 'RIGHT':
                    del possible_turns[i]
                    break
        if karta[x][y - 1] == '1' or karta[x][y - 1] == 'x' or karta[x][y - 1] == 'S':
            for i in range(len(possible_turns)):
                if possible_turns[i] == 'LEFT':
                    del possible_turns[i]
                    break
        min_l = 999999999
        min_way = ''
        if len(possible_turns) < 2:
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
                m_y = int(m_y)
                m_x = int(m_x)
                coords[0] = int(coords[0])
                coords[1] = int(coords[1])
                l = (((m_x - coords[0]) ** 2) + (m_y - coords[1]) ** 2) ** 0.5
                if l < 0:
                    l += 2 * l
                coords.append(l)
                if l < min_l:
                    min_l = l
                    min_way = coords[2]
            return min_way


class Pinky(pygame.sprite.Sprite):                                              # TODO Пинки - Розовый призрак TODO
    def __init__(self, pos_x, pos_y, choord_x, choord_y, filename):
        super().__init__(spirits_group, all_sprites)
        self.mission = ('', '')
        self.image = filename
        self.choord_x = choord_x
        self.choord_y = choord_y
        self.rect = self.image.get_rect().move(tile_width * pos_x - 10, tile_height * pos_y - 10)

    def get_a_mission(self, choord_x, choord_y, karta, pink_terror):
        if pink_terror:
            self.mission = (0, 2)
        else:
            min_m_x = int(choord_x) - 4
            if min_m_x < 3:
                min_m_x = 3
            max_m_x = int(choord_x) + 4
            if max_m_x > 31:
                max_m_x = 31
            min_m_y = int(choord_y) - 4
            if min_m_y < 1:
                min_m_y = 1
            max_m_y = int(choord_y) + 4
            if max_m_y > 26:
                max_m_y = 26
            m_x = randint(min_m_x, max_m_x)
            m_y = randint(min_m_y, max_m_y)
            while karta[m_x][m_y] == '1':
                m_x = randint(min_m_x, max_m_x)
                m_y = randint(min_m_y, max_m_y)
            self.mission = (m_x, m_y)

    def folow(self, karta, pinky_last_position, x, y, m_x, m_y, possible_turns, pinky_leave_home):
        x = int(x)
        y = int(y)
        for i in range(len(possible_turns)):
            if possible_turns[i] == pinky_last_position:
                del possible_turns[i]
                break
        if karta[x + 1][y] == '1' or karta[x + 1][y] == 'x' or karta[x + 1][y] == 'B' or karta[x + 1][y] == 'O':
            for i in range(len(possible_turns)):
                if possible_turns[i] == 'DOWN':
                    del possible_turns[i]
                    break
        if karta[x - 1][y] == '1' or karta[x - 1][y] == 'x' or karta[x - 1][y] == 'B' or karta[x - 1][y] == 'O':
            for i in range(len(possible_turns)):
                if possible_turns[i] == 'UP':
                    del possible_turns[i]
                    break
        if karta[x][y + 1] == '1' or karta[x][y + 1] == 'x' or karta[x][y + 1] == 'B' or karta[x][y + 1] == 'O':
            for i in range(len(possible_turns)):
                if possible_turns[i] == 'RIGHT':
                    del possible_turns[i]
                    break
        if karta[x][y - 1] == '1' or karta[x][y - 1] == 'x' or karta[x][y - 1] == 'B' or karta[x][y - 1] == 'O':
            for i in range(len(possible_turns)):
                if possible_turns[i] == 'LEFT':
                    del possible_turns[i]
                    break
        if pinky_leave_home:
            if karta[x + 1][y] == 'S':
                for i in range(len(possible_turns)):
                    if possible_turns[i] == 'DOWN':
                        del possible_turns[i]
                        break
        min_l = 999999999
        min_way = ''
        if len(possible_turns) < 2:
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
                m_y = int(m_y)
                m_x = int(m_x)
                coords[0] = int(coords[0])
                coords[1] = int(coords[1])
                l = (((m_x - coords[0]) ** 2) + (m_y - coords[1]) ** 2) ** 0.5
                if l < 0:
                    l += 2 * l
                coords.append(l)
                if l < min_l:
                    min_l = l
                    min_way = coords[2]
            return min_way


class Inky(pygame.sprite.Sprite):                                                # TODO Инки - Голубой призрак TODO
    def __init__(self, pos_x, pos_y, choord_x, choord_y, filename):
        super().__init__(spirits_group, all_sprites)
        self.mission = ('', '')
        self.image = filename
        self.choord_x = choord_x
        self.choord_y = choord_y
        self.rect = self.image.get_rect().move(tile_width * pos_x - 10, tile_height * pos_y - 10)

    def get_a_mission(self, choord_x, choord_y, blinky_red_spirit_choord_x, blinky_red_spirit_choord_y, blue_terror):
        if blue_terror:
            self.mission = (35, 27)
        else:
            m_x = 2 * int(choord_x) - int(blinky_red_spirit_choord_x)
            m_y = 2 * int(choord_y) - int(blinky_red_spirit_choord_y)
            self.mission = (m_x, m_y)

    def folow(self, karta, inky_last_position, x, y, m_x, m_y, possible_turns, inky_leave_home_1, inky_leave_home_2):
        x = int(x)
        y = int(y)
        for i in range(len(possible_turns)):
            if possible_turns[i] == inky_last_position:
                del possible_turns[i]
                break
        if karta[x + 1][y] == '1' or karta[x + 1][y] == 'x' or karta[x + 1][y] == 'O':
            for i in range(len(possible_turns)):
                if possible_turns[i] == 'DOWN':
                    del possible_turns[i]
                    break
        if karta[x - 1][y] == '1' or karta[x - 1][y] == 'x' or karta[x - 1][y] == 'O':
            for i in range(len(possible_turns)):
                if possible_turns[i] == 'UP':
                    del possible_turns[i]
                    break
        if karta[x][y + 1] == '1' or karta[x][y + 1] == 'x' or karta[x][y + 1] == 'O':
            for i in range(len(possible_turns)):
                if possible_turns[i] == 'RIGHT':
                    del possible_turns[i]
                    break
        if karta[x][y - 1] == '1' or karta[x][y - 1] == 'x' or karta[x][y - 1] == 'O':
            for i in range(len(possible_turns)):
                if possible_turns[i] == 'LEFT':
                    del possible_turns[i]
                    break
        if inky_leave_home_1:
            if karta[x][y - 1] == 'B':
                for i in range(len(possible_turns)):
                    if possible_turns[i] == 'RIGHT':
                        del possible_turns[i]
                        break
        if inky_leave_home_2:
            if karta[x + 1][y] == 'S':
                for i in range(len(possible_turns)):
                    if possible_turns[i] == 'DOWN':
                        del possible_turns[i]
                        break
        min_l = 999999999
        min_way = ''
        if len(possible_turns) < 2:
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
                m_y = int(m_y)
                m_x = int(m_x)
                coords[0] = int(coords[0])
                coords[1] = int(coords[1])
                l = (((m_x - coords[0]) ** 2) + (m_y - coords[1]) ** 2) ** 0.5
                if l < 0:
                    l += 2 * l
                coords.append(l)
                if l < min_l:
                    min_l = l
                    min_way = coords[2]
            return min_way


class Clyde(pygame.sprite.Sprite):                                            # TODO Клайд - Оранжевый призрак TODO
    def __init__(self, pos_x, pos_y, choord_x, choord_y, filename):
        super().__init__(spirits_group, all_sprites)
        self.mission = ('', '')
        self.image = filename
        self.choord_x = choord_x
        self.choord_y = choord_y
        self.rect = self.image.get_rect().move(tile_width * pos_x - 10, tile_height * pos_y - 10)

    def get_a_mission(self, choord_x, choord_y, clyde_choord_x, clyde_choord_y, orange_terror):
        if orange_terror:
            self.mission = (30, 0)
        else:
            min_m_x = int(choord_x) - 8
            if min_m_x < 3:
                min_m_x = 3
            max_m_x = int(choord_x) + 8
            if max_m_x > 31:
                max_m_x = 31
            min_m_y = int(choord_y) - 8
            if min_m_y < 1:
                min_m_y = 1
            max_m_y = int(choord_y) + 8
            if max_m_y > 26:
                max_m_y = 26
            clyde_choord_x = int(clyde_choord_x)
            clyde_choord_y = int(clyde_choord_y)
            if clyde_choord_x > min_m_x and clyde_choord_x < max_m_x and clyde_choord_y > min_m_y and clyde_choord_y < max_m_y:
                self.mission = (28, 6)
            else:
                self.mission = (choord_x, choord_y)

    def folow(self, karta, blinky_last_position, x, y, m_x, m_y, possible_turns, clyde_leave_home_1, clyde_leave_home_2):
        x = int(x)
        y = int(y)
        for i in range(len(possible_turns)):
            if possible_turns[i] == blinky_last_position:
                del possible_turns[i]
                break
        if karta[x + 1][y] == '1' or karta[x + 1][y] == 'x' or karta[x + 1][y] == 'B':
            for i in range(len(possible_turns)):
                if possible_turns[i] == 'DOWN':
                    del possible_turns[i]
                    break
        if karta[x - 1][y] == '1' or karta[x - 1][y] == 'x' or karta[x - 1][y] == 'B':
            for i in range(len(possible_turns)):
                if possible_turns[i] == 'UP':
                    del possible_turns[i]
                    break
        if karta[x][y + 1] == '1' or karta[x][y + 1] == 'x' or karta[x][y + 1] == 'B':
            for i in range(len(possible_turns)):
                if possible_turns[i] == 'RIGHT':
                    del possible_turns[i]
                    break
        if karta[x][y - 1] == '1' or karta[x][y - 1] == 'x' or karta[x][y - 1] == 'B':
            for i in range(len(possible_turns)):
                if possible_turns[i] == 'LEFT':
                    del possible_turns[i]
                    break
        if clyde_leave_home_1:
            if karta[x][y + 1] == 'O':
                for i in range(len(possible_turns)):
                    if possible_turns[i] == 'RIGHT':
                        del possible_turns[i]
                        break
        if clyde_leave_home_2:
            if karta[x + 1][y] == 'S':
                for i in range(len(possible_turns)):
                    if possible_turns[i] == 'DOWN':
                        del possible_turns[i]
                        break
        min_l = 999999999
        min_way = ''
        if len(possible_turns) < 2:
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
                m_y = int(m_y)
                m_x = int(m_x)
                coords[0] = int(coords[0])
                coords[1] = int(coords[1])
                l = (((m_x - coords[0]) ** 2) + (m_y - coords[1]) ** 2) ** 0.5
                if l < 0:
                    l += 2 * l
                coords.append(l)
                if l < min_l:
                    min_l = l
                    min_way = coords[2]
            return min_way