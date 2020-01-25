import os
import sys
import pygame
import Spirits

pygame.init()
pygame.key.set_repeat(200, 70)
FPS = 60
WIDTH = 24 * 28
HEIGHT = 24 * 34
STEP = 24
karta = []
score = 0
pac = 'pacman.jpg'
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
player = None
pill = False
t = 0
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
dots_group = pygame.sprite.Group()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    global karta
    s = []
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('vert2', x, y)
                s.append('1')
            elif level[y][x] == '!':
                Tile('vert', x, y)
                s.append('1')
            elif level[y][x] == '_':
                Tile('hor2', x, y)
                s.append('1')
            elif level[y][x] == '-':
                Tile('hor', x, y)
                s.append('1')
            elif level[y][x] == '#':
                Tile('empty', x, y)
                s.append('.')
            elif level[y][x] == '1':
                Tile('left_up', x, y)
                s.append('1')
            elif level[y][x] == '2':
                Tile('right_up', x, y)
                s.append('1')
            elif level[y][x] == '3':
                Tile('left_down', x, y)
                s.append('1')
            elif level[y][x] == '4':
                Tile('right_down', x, y)
                s.append('1')
            elif level[y][x] == '@':
                new_player = Pacman(x, y, 25, 14)
                s.append('.')
            elif level[y][x] == 'd':
                Dot(x, y)
                s.append('.')
            elif level[y][x] == 'D':
                Big_Dot(x, y)
                s.append('.')
            if len(s) == 28:
                karta.append(s)
                s = []
    karta[16][22] = 'x'
    karta[16][5] = 'x'
    karta[14][14] = 'S'
    karta[15][15] = '1'
    karta[16][15] = 'O'
    karta[17][15] = '1'
    karta[16][13] = 'B'
    karta[17][13] = '1'
    karta[17][14] = '1'
    karta[15][11] = '1'
    karta[15][12] = '1'
    karta[15][13] = '1'
    karta[15][16] = '1'
    karta[17][11] = '1'
    karta[17][12] = '1'
    karta[17][16] = '1'
    karta[16][11] = '1'
    return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


tile_images = {'empty': load_image('black.jpg'), 'vert': load_image('vert.jpg'), 'hor': load_image('hor.jpg'),
               'left_up': load_image('left_up.jpg'), 'left_down': load_image('left_down.jpg'),
               'right_up': load_image('right_up.jpg'), 'right_down': load_image('right_down.jpg'),
               'vert2': load_image('vert2.jpg'), 'hor2': load_image('hor2.jpg')}
player_image = load_image('pacman.jpg')
blinky_image = load_image('blinky_1.jpg')
pinky_image = load_image('pinky_1.jpg')
clyde_image = load_image('clyde_1.jpg')
inky_image = load_image('inky_1.jpg')
dot_image = load_image('dot.jpg')
big_dot_image = load_image('big_dot.jpg')
tile_width = tile_height = 24


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Pacman(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, choord_x, choord_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.choord_x = choord_x
        self.choord_y = choord_y
        self.im = 0
        self.rect = self.image.get_rect().move(tile_width * pos_x - 8, tile_height * pos_y - 8)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        global pac
        global pill
        if (self.im // 10) % 2 == 0:
            self.image = load_image(pac)
            self.im += 1
        else:
            self.image = load_image('pacman2.jpg')
            self.im += 1
        if pygame.sprite.collide_mask(self, blinky_red_spirit):
            if pill:
                blinky_red_spirit.kill()
            else:
                self.kill()
                terminate()
        if pygame.sprite.collide_mask(self, pinky_pink_spirit):
            if pill:
                pinky_pink_spirit.kill()
            else:
                self.kill()
                terminate()
        if pygame.sprite.collide_mask(self, clyde_orange_spirit):
            if pill:
                clyde_orange_spirit.kill()
            else:
                self.kill()
                terminate()
        if pygame.sprite.collide_mask(self, inky_blue_spirit):
            if pill:
                inky_blue_spirit.kill()
            else:
                self.kill()
                terminate()


class Dot(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(dots_group, all_sprites)
        self.image = dot_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        global score
        if pygame.sprite.collide_mask(self, player):
            score += 1
            self.kill()
            if score == 244:
                generate_level('map2.txt')


class Big_Dot(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(dots_group, all_sprites)
        self.image = big_dot_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        global score
        global pill
        if pygame.sprite.collide_mask(self, player):
            pygame.mixer.music.load('salo.mp3')
            pygame.mixer.music.play()
            pill = True
            score += 1
            self.kill()
            if score == 244:
                generate_level('map2.txt')
        if pill:
            global t
            if t < 1500:
                t += 1
            else:
                t = 0
                pill = False


blinky_red_spirit = Spirits.Blinky(14, 13, 13, 14, blinky_image)
blinky_last_position = 'LEFT'
min_way_red = 'RIGHT'
k_red = 0
pinky_pink_spirit = Spirits.Pinky(14, 16, 16, 14, pinky_image)
pinky_last_position = 'DOWN'
min_way_pink = 'UP'
pinky_leave_home = False
k_pink = 0
inky_blue_spirit = Spirits.Inky(11, 16, 16, 11, inky_image)
inky_last_position = 'LEFT'
min_way_blue = 'RIGHT'
inky_leave_home_1 = False
inky_leave_home_2 = False
k_blue = 0
clyde_orange_spirit = Spirits.Clyde(16, 16, 16, 16, clyde_image)
clyde_last_position = 'RIGHT'
min_way_orange = 'LEFT'
clyde_leave_home_1 = False
clyde_leave_home_2 = False
k_orange = 0
start_screen()
player, level_x, level_y = generate_level(load_level('map2.txt'))
running = True
run_left = False
run_right = False
run_up = False
run_down = False
k = 0
k_red = 0
while running:
    if pill:
        blinky_red_spirit.image = load_image('dead_1.jpg')
        pinky_pink_spirit_image = load_image('dead_1.jpg')
        clyde_orange_spirit.image = load_image('dead_1.jpg')
        inky_blue_spirit.image = load_image('dead_1.jpg')
    else:
        blinky_red_spirit.image = load_image('blinky_1.jpg')
        pinky_pink_spirit.image = load_image('pinky_1.jpg')
        clyde_orange_spirit.image = load_image('clyde_1.jpg')
        inky_blue_spirit.image = load_image('inky_1.jpg')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and karta[player.choord_x][player.choord_y - 1] != '1' and not run_left:
                if run_down:
                    player.rect.y -= k
                elif run_up:
                    player.rect.y += k
                elif run_right:
                    player.rect.x -= k
                k = 0
                run_left = True
                run_right = False
                run_up = False
                run_down = False
            if event.key == pygame.K_RIGHT and karta[player.choord_x][player.choord_y + 1] != '1' and not run_right:
                if run_down:
                    player.rect.y -= k
                elif run_up:
                    player.rect.y += k
                elif run_left:
                    player.rect.x += k
                k = 0
                run_right = True
                run_left = False
                run_up = False
                run_down = False
            if event.key == pygame.K_UP and karta[player.choord_x - 1][player.choord_y] != '1' and not run_up:
                if run_down:
                    player.rect.y -= k
                elif run_left:
                    player.rect.x += k
                elif run_right:
                    player.rect.x -= k
                k = 0
                run_up = True
                run_right = False
                run_left = False
                run_down = False
            if event.key == pygame.K_DOWN and karta[player.choord_x + 1][player.choord_y] != '1' and not run_down:
                if run_left:
                    player.rect.x += k
                elif run_up:
                    player.rect.y += k
                elif run_right:
                    player.rect.x -= k
                k = 0
                run_down = True
                run_right = False
                run_up = False
                run_left = False
    if run_down and karta[player.choord_x + 1][player.choord_y] != '1':
        player.rect.y += 1
        pac = 'pacman4.jpg'
        k += 1
        if k == 24:
            player.choord_x = player.choord_x + 1
            k = 0
    elif run_up and karta[player.choord_x - 1][player.choord_y] != '1':
        player.rect.y -= 1
        pac = 'pacman3.jpg'
        k += 1
        if k == 24:
            player.choord_x = player.choord_x - 1
            k = 0
    elif run_left and karta[player.choord_x][player.choord_y - 1] != '1':
        player.rect.x -= 1
        pac = 'pacman5.jpg'
        k += 1
        if k == 24:
            player.choord_y = player.choord_y - 1
            k = 0
    elif run_right and karta[player.choord_x][player.choord_y + 1] != '1':
        player.rect.x += 1
        pac = 'pacman.jpg'
        k += 1
        if k == 24:
            player.choord_y = player.choord_y + 1
            k = 0

    # Движение Блинки (красный)

    blinky_red_spirit.get_a_mission(player.choord_x, player.choord_y)
    if min_way_red == 'UP':
        blinky_last_position = 'DOWN'
        blinky_red_spirit.rect.y -= 1
        k_red += 1
        if k_red == 24:
            blinky_red_spirit.choord_x = blinky_red_spirit.choord_x - 1
            if karta[blinky_red_spirit.choord_x][blinky_red_spirit.choord_y] == '.':
                possible_turns = ['UP', 'DOWN', 'LEFT', 'RIGHT']
                min_way_red = blinky_red_spirit.folow(karta, blinky_last_position,
                                                      blinky_red_spirit.choord_x, blinky_red_spirit.choord_y,
                                                      blinky_red_spirit.mission[0], blinky_red_spirit.mission[1],
                                                      possible_turns)
            k_red = 0
    elif min_way_red == 'DOWN':
        blinky_last_position = 'UP'
        blinky_red_spirit.rect.y += 1
        k_red += 1
        if k_red == 24:
            blinky_red_spirit.choord_x = blinky_red_spirit.choord_x + 1
            if karta[blinky_red_spirit.choord_x][blinky_red_spirit.choord_y] == '.':
                possible_turns = ['UP', 'DOWN', 'LEFT', 'RIGHT']
                min_way_red = blinky_red_spirit.folow(karta, blinky_last_position,
                                                      blinky_red_spirit.choord_x, blinky_red_spirit.choord_y,
                                                      blinky_red_spirit.mission[0], blinky_red_spirit.mission[1],
                                                      possible_turns)
            k_red = 0
    elif min_way_red == 'LEFT':
        blinky_last_position = 'RIGHT'
        blinky_red_spirit.rect.x -= 1
        k_red += 1
        if k_red == 24:
            blinky_red_spirit.choord_y = blinky_red_spirit.choord_y - 1
            if karta[blinky_red_spirit.choord_x][blinky_red_spirit.choord_y] == '.':
                possible_turns = ['UP', 'DOWN', 'LEFT', 'RIGHT']
                min_way_red = blinky_red_spirit.folow(karta, blinky_last_position,
                                                      blinky_red_spirit.choord_x, blinky_red_spirit.choord_y,
                                                      blinky_red_spirit.mission[0], blinky_red_spirit.mission[1],
                                                      possible_turns)
            k_red = 0
    elif min_way_red == 'RIGHT':
        blinky_last_position = 'LEFT'
        blinky_red_spirit.rect.x += 1
        k_red += 1
        if k_red == 24:
            blinky_red_spirit.choord_y = blinky_red_spirit.choord_y + 1
            if karta[blinky_red_spirit.choord_x][blinky_red_spirit.choord_y] == '.':
                possible_turns = ['UP', 'DOWN', 'LEFT', 'RIGHT']
                min_way_red = blinky_red_spirit.folow(karta, blinky_last_position,
                                                      blinky_red_spirit.choord_x, blinky_red_spirit.choord_y,
                                                      blinky_red_spirit.mission[0], blinky_red_spirit.mission[1],
                                                      possible_turns)
            k_red = 0

    # Движение Пинки (розовый)

    if pinky_pink_spirit.choord_x == 13 and pinky_pink_spirit.choord_y == 14:
        pinky_leave_home = True

    pinky_pink_spirit.get_a_mission(player.choord_x, player.choord_y, karta)
    if min_way_pink == 'UP':
        pinky_last_position = 'DOWN'
        pinky_pink_spirit.rect.y -= 1
        k_pink += 1
        if k_pink == 24:
            pinky_pink_spirit.choord_x = pinky_pink_spirit.choord_x - 1
            if karta[pinky_pink_spirit.choord_x][pinky_pink_spirit.choord_y] == '.':
                possible_turns_pink = ['UP', 'DOWN', 'LEFT', 'RIGHT']
                min_way_pink = pinky_pink_spirit.folow(karta, pinky_last_position,
                                                       pinky_pink_spirit.choord_x, pinky_pink_spirit.choord_y,
                                                       pinky_pink_spirit.mission[0], pinky_pink_spirit.mission[1],
                                                       possible_turns_pink, pinky_leave_home)
            k_pink = 0
    elif min_way_pink == 'DOWN':
        pinky_last_position = 'UP'
        pinky_pink_spirit.rect.y += 1
        k_pink += 1
        if k_pink == 24:
            pinky_pink_spirit.choord_x = pinky_pink_spirit.choord_x + 1
            if karta[pinky_pink_spirit.choord_x][pinky_pink_spirit.choord_y] == '.':
                possible_turns_pink = ['UP', 'DOWN', 'LEFT', 'RIGHT']
                min_way_pink = pinky_pink_spirit.folow(karta, pinky_last_position,
                                                       pinky_pink_spirit.choord_x, pinky_pink_spirit.choord_y,
                                                       pinky_pink_spirit.mission[0], pinky_pink_spirit.mission[1],
                                                       possible_turns_pink, pinky_leave_home)
            k_pink = 0
    elif min_way_pink == 'LEFT':
        pinky_last_position = 'RIGHT'
        pinky_pink_spirit.rect.x -= 1
        k_pink += 1
        if k_pink == 24:
            pinky_pink_spirit.choord_y = pinky_pink_spirit.choord_y - 1
            if karta[pinky_pink_spirit.choord_x][pinky_pink_spirit.choord_y] == '.':
                possible_turns_pink = ['UP', 'DOWN', 'LEFT', 'RIGHT']
                min_way_pink = pinky_pink_spirit.folow(karta, pinky_last_position,
                                                       pinky_pink_spirit.choord_x, pinky_pink_spirit.choord_y,
                                                       pinky_pink_spirit.mission[0], pinky_pink_spirit.mission[1],
                                                       possible_turns_pink, pinky_leave_home)
            k_pink = 0
    elif min_way_pink == 'RIGHT':
        pinky_last_position = 'LEFT'
        pinky_pink_spirit.rect.x += 1
        k_pink += 1
        if k_pink == 24:
            pinky_pink_spirit.choord_y = pinky_pink_spirit.choord_y + 1
            if karta[pinky_pink_spirit.choord_x][pinky_pink_spirit.choord_y] == '.':
                possible_turns_pink = ['UP', 'DOWN', 'LEFT', 'RIGHT']
                min_way_pink = pinky_pink_spirit.folow(karta, pinky_last_position,
                                                       pinky_pink_spirit.choord_x, pinky_pink_spirit.choord_y,
                                                       pinky_pink_spirit.mission[0], pinky_pink_spirit.mission[1],
                                                       possible_turns_pink, pinky_leave_home)
            k_pink = 0

    # Движение Клайда (Оранжевый)

    if clyde_orange_spirit.choord_x == 16 and clyde_orange_spirit.choord_y == 14:
        clyde_leave_home_1 = True
    if clyde_orange_spirit.choord_x == 13 and clyde_orange_spirit.choord_y == 14:
        clyde_leave_home_2 = True

    clyde_orange_spirit.get_a_mission(player.choord_x, player.choord_y,
                                      clyde_orange_spirit.choord_x, clyde_orange_spirit.choord_y)
    if min_way_orange == 'UP':
        clyde_last_position = 'DOWN'
        clyde_orange_spirit.rect.y -= 1
        k_orange += 1
        if k_orange == 24:
            clyde_orange_spirit.choord_x = clyde_orange_spirit.choord_x - 1
            if karta[clyde_orange_spirit.choord_x][clyde_orange_spirit.choord_y] == '.':
                possible_turns_orange = ['UP', 'DOWN', 'LEFT', 'RIGHT']
                min_way_orange = clyde_orange_spirit.folow(karta, clyde_last_position,
                                                           clyde_orange_spirit.choord_x, clyde_orange_spirit.choord_y,
                                                           clyde_orange_spirit.mission[0],
                                                           clyde_orange_spirit.mission[1],
                                                           possible_turns_orange, clyde_leave_home_1,
                                                           clyde_leave_home_2)
            k_orange = 0
    elif min_way_orange == 'DOWN':
        clyde_last_position = 'UP'
        clyde_orange_spirit.rect.y += 1
        k_orange += 1
        if k_orange == 24:
            clyde_orange_spirit.choord_x = clyde_orange_spirit.choord_x + 1
            if karta[clyde_orange_spirit.choord_x][clyde_orange_spirit.choord_y] == '.':
                possible_turns_orange = ['UP', 'DOWN', 'LEFT', 'RIGHT']
                min_way_orange = clyde_orange_spirit.folow(karta, clyde_last_position,
                                                           clyde_orange_spirit.choord_x, clyde_orange_spirit.choord_y,
                                                           clyde_orange_spirit.mission[0],
                                                           clyde_orange_spirit.mission[1],
                                                           possible_turns_orange, clyde_leave_home_1,
                                                           clyde_leave_home_2)
            k_orange = 0
    elif min_way_orange == 'LEFT':
        clyde_last_position = 'RIGHT'
        clyde_orange_spirit.rect.x -= 1
        k_orange += 1
        if k_orange == 24:
            clyde_orange_spirit.choord_y = clyde_orange_spirit.choord_y - 1
            if karta[clyde_orange_spirit.choord_x][clyde_orange_spirit.choord_y] == '.':
                possible_turns_orange = ['UP', 'DOWN', 'LEFT', 'RIGHT']
                min_way_orange = clyde_orange_spirit.folow(karta, clyde_last_position,
                                                           clyde_orange_spirit.choord_x, clyde_orange_spirit.choord_y,
                                                           clyde_orange_spirit.mission[0],
                                                           clyde_orange_spirit.mission[1],
                                                           possible_turns_orange, clyde_leave_home_1,
                                                           clyde_leave_home_2)
            k_orange = 0
    elif min_way_orange == 'RIGHT':
        clyde_last_position = 'LEFT'
        clyde_orange_spirit.rect.x += 1
        k_orange += 1
        if k_orange == 24:
            clyde_orange_spirit.choord_y = clyde_orange_spirit.choord_y + 1
            if karta[clyde_orange_spirit.choord_x][clyde_orange_spirit.choord_y] == '.':
                possible_turns_orange = ['UP', 'DOWN', 'LEFT', 'RIGHT']
                min_way_orange = clyde_orange_spirit.folow(karta, clyde_last_position,
                                                           clyde_orange_spirit.choord_x, clyde_orange_spirit.choord_y,
                                                           clyde_orange_spirit.mission[0],
                                                           clyde_orange_spirit.mission[1],
                                                           possible_turns_orange, clyde_leave_home_1,
                                                           clyde_leave_home_2)
            k_orange = 0

    # Движение Инки (синий)

    inky_blue_spirit.get_a_mission(player.choord_x, player.choord_y,
                                   blinky_red_spirit.choord_x, blinky_red_spirit.choord_y)
    if min_way_blue == 'UP':
        inky_last_position = 'DOWN'
        inky_blue_spirit.rect.y -= 1
        k_blue += 1
        if k_blue == 24:
            inky_blue_spirit.choord_x = inky_blue_spirit.choord_x - 1
            if karta[inky_blue_spirit.choord_x][inky_blue_spirit.choord_y] == '.':
                possible_turns_blue = ['UP', 'DOWN', 'LEFT', 'RIGHT']
                min_way_blue = inky_blue_spirit.folow(karta, inky_last_position,
                                                      inky_blue_spirit.choord_x, inky_blue_spirit.choord_y,
                                                      inky_blue_spirit.mission[0], inky_blue_spirit.mission[1],
                                                      possible_turns_blue, inky_leave_home_1, inky_leave_home_2)
            k_blue = 0
    elif min_way_blue == 'DOWN':
        inky_last_position = 'UP'
        inky_blue_spirit.rect.y += 1
        k_blue += 1
        if k_blue == 24:
            inky_blue_spirit.choord_x = inky_blue_spirit.choord_x + 1
            if karta[inky_blue_spirit.choord_x][inky_blue_spirit.choord_y] == '.':
                possible_turns_blue = ['UP', 'DOWN', 'LEFT', 'RIGHT']
                min_way_blue = inky_blue_spirit.folow(karta, inky_last_position,
                                                      inky_blue_spirit.choord_x, inky_blue_spirit.choord_y,
                                                      inky_blue_spirit.mission[0], inky_blue_spirit.mission[1],
                                                      possible_turns_blue, inky_leave_home_1, inky_leave_home_2)
            k_blue = 0
    elif min_way_blue == 'LEFT':
        inky_last_position = 'RIGHT'
        inky_blue_spirit.rect.x -= 1
        k_blue += 1
        if k_blue == 24:
            inky_blue_spirit.choord_y = inky_blue_spirit.choord_y - 1
            if karta[inky_blue_spirit.choord_x][inky_blue_spirit.choord_y] == '.':
                possible_turns_blue = ['UP', 'DOWN', 'LEFT', 'RIGHT']
                min_way_blue = inky_blue_spirit.folow(karta, inky_last_position,
                                                      inky_blue_spirit.choord_x, inky_blue_spirit.choord_y,
                                                      inky_blue_spirit.mission[0], inky_blue_spirit.mission[1],
                                                      possible_turns_blue, inky_leave_home_1, inky_leave_home_2)
            k_blue = 0
    elif min_way_blue == 'RIGHT':
        inky_last_position = 'LEFT'
        inky_blue_spirit.rect.x += 1
        k_blue += 1
        if k_blue == 24:
            inky_blue_spirit.choord_y = inky_blue_spirit.choord_y + 1
            if karta[inky_blue_spirit.choord_x][inky_blue_spirit.choord_y] == '.':
                possible_turns_blue = ['UP', 'DOWN', 'LEFT', 'RIGHT']
                min_way_blue = inky_blue_spirit.folow(karta, inky_last_position,
                                                      inky_blue_spirit.choord_x, inky_blue_spirit.choord_y,
                                                      inky_blue_spirit.mission[0], inky_blue_spirit.mission[1],
                                                      possible_turns_blue, inky_leave_home_1, inky_leave_home_2)
            k_blue = 0
    screen.fill(pygame.Color(0, 0, 0))
    tiles_group.draw(screen)
    dots_group.draw(screen)
    player_group.draw(screen)
    Spirits.spirits_group.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(FPS)
terminate()