import os
import sys
import pygame

pygame.init()
pygame.key.set_repeat(200, 70)


FPS = 50
WIDTH = 24 * 28
HEIGHT = 24 * 34
STEP = 24
karta = []

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


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
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))

def generate_level(level):
    global karta
    s = []
    new_player, x, y = None, None, None
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
                new_player = Player(x, y, 25, 14)
                s.append('.')
            if len(s) == 28:
                karta.append(s)
                s = []
    # вернем игрока, а также размер поля в клетках
    for elem in karta:
        print(elem)
    return new_player, x, y

def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('pacman.jpg'), (WIDTH, HEIGHT))
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
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)

tile_images = {'empty': load_image('black.jpg'), 'vert': load_image('vert.jpg'), 'hor': load_image('hor.jpg'),
               'left_up': load_image('left_up.jpg'), 'left_down': load_image('left_down.jpg'),
               'right_up': load_image('right_up.jpg'), 'right_down': load_image('right_down.jpg'),
               'vert2': load_image('vert2.jpg'), 'hor2': load_image('hor2.jpg')}
player_image = load_image('pacman.jpg')
tile_width = tile_height = 24


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, choord_x, choord_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.choord_x = choord_x
        self.choord_y = choord_y
        self.rect = self.image.get_rect().move(tile_width * pos_x - 10, tile_height * pos_y - 10)


start_screen()
player, level_x, level_y = generate_level(load_level('map2.txt'))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if player.choord_x == 16 and  player.choord_y == 27 and event.key == pygame.K_RIGHT:
                player.choord_y = 0
                player.rect.x -= STEP
            if event.key == pygame.K_LEFT and karta[player.choord_x][player.choord_y - 1] == '.':
                player.rect.x -= STEP
                player.choord_y = player.choord_y - 1
            if event.key == pygame.K_RIGHT and karta[player.choord_x][player.choord_y + 1] == '.':
                player.rect.x += STEP
                player.choord_y = player.choord_y + 1
            if event.key == pygame.K_UP and karta[player.choord_x - 1][player.choord_y] == '.':
                player.rect.y -= STEP
                player.choord_x = player.choord_x - 1
            if event.key == pygame.K_DOWN and karta[player.choord_x + 1][player.choord_y] == '.':
                player.rect.y += STEP
                player.choord_x = player.choord_x + 1
    screen.fill(pygame.Color(0, 0, 0))
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
terminate()