import math
import pygame
import pygame_gui
from pygame.rect import Rect
from pygame_gui.elements import UITextEntryLine
import sys
import os
import random
import sqlite3
con = sqlite3.connect("data/data_for_math_duels.db")
cur = con.cursor()


cursor_group = pygame.sprite.Group()


class Math_question:
    def __init__(self, line, dict=None):
        self.problem = line
        self.question = ''
        if dict is None:
            self.numbers = {}
        else:
            self.numbers = dict
        self.operations = {'**': 0, '*': 0, '+': 0, '-': 0, '/': 0, '!': 0, 'V‾': 0}

    def checking_for_correctness(self):
        if len(self.question) > 100:
            return False
        for i in range(len(self.sym[::-3])):
            if len(self.sym) > 3:
                if self.sym[i] == self.sym[i + 1] == self.sym[i + 2] == self.sym[i + 3]:
                    return False
        symbols = self.question.split()
        for si in range(len(symbols)):
            if symbols[si].isdigit():
                if symbols[si] not in self.numbers:
                    self.numbers[symbols[int(si)]] = 1
                else:
                    return False
            if '!' in symbols[si]:
                symbols[si] = factorial(symbols[si][1:-2], self.numbers)
            elif 'V‾' in symbols[si]:
                symbols[si] = root(symbols[si][3:-1], self.numbers)
        if len(symbols) > 0:
            if not None in symbols:
                self.question = ''.join(symbols)
                if '0/' not in self.question and '*0' not in self.question \
                        and '/0' not in self.question and '0*' not in self.question:
                    return True
                else:
                    return False

    def transformation(self):
        s = self.problem
        pr = ' '
        n = 0
        self.sym = []
        for i in range(len(self.problem)):
            if s[i].isdigit():
                self.question += s[i]
            elif not s[i].isalpha() or s[i] == 'V':
                if s[i] == '.':
                    self.question += s[i]
                elif s[i] == '*' and s[i + 1] == '*':
                    self.question += pr + '**' + pr
                    self.sym.append('**')
                    if s[i] in self.operations:
                        self.operations['**'] += 1
                elif s[i] in '+-/*':
                    self.question = self.question + pr + s[i] + pr
                    self.sym.append(s[i])
                    if s[i] in self.operations:
                        self.operations[s[i]] += 1
                elif s[i] == '!':
                    self.sym.append(s[i])
                    self.question = self.question[:-1] + s[i]
                    self.operations[s[i]] += 1
                elif s[i] == 'V' and s[i + 1] == '‾':
                    self.sym.append('V‾')
                    self.question += ' V‾'
                    self.operations['V‾'] += 1
                elif s[i] in '()':
                    if s[i] == '(':
                        n += 1
                        pr = ''
                        self.question += pr + s[i]
                    if s[i] == ')':
                        n -= 1
                        if i + 1 < len(self.problem) and n == 0:
                            if s[i + 1] != ')':
                                pr = ' '
                        self.question += s[i] + pr
        return self.question

    def answer(self):
        return eval(self.question)

    def print_summ(self):
        summ = 0
        summ += self.operations['+']
        summ += self.operations['-'] * 2
        summ += self.operations['*'] * 3
        summ += self.operations['/'] * 4
        summ += self.operations['V‾'] * 6
        summ += self.operations['**'] * 5
        summ += self.operations['!'] * 4
        return summ


def root(question, dict):
    p = Math_question(question, dict)
    np = p.transformation()
    if p.checking_for_correctness():
        return str(math.sqrt(eval(np)))


def factorial(question, dict):
    p = Math_question(question, dict)
    np = p.transformation()
    if p.checking_for_correctness():
        return str(math.factorial(eval(np)))


pygame.init()
pygame.display.set_caption('Math Duels')
screen = pygame.display.set_mode((1200, 750))
manager = pygame_gui.UIManager((1200, 750))
screen.fill("black")

train_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 215), (200, 40)),
                                             text='Обучение',
                                             manager=manager)

story_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 285), (200, 40)),
                                             text='Сюжет',
                                             manager=manager)

two_players_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 355), (200, 40)),
                                             text='Играть с другом',
                                             manager=manager)

lobby_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 425), (200, 40)),
                                             text='Лобби',
                                             manager=manager)

settings_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 495), (200, 40)),
                                             text='Настройки',
                                             manager=manager)


def load_img(name, colorkey=None):
    fullname = os.path.join("data", name)
    if not os.path.isfile(fullname):
        print("No file here :(")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is None:
        image = image.convert_alpha()
    else:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


size = width, height = 1200, 750
FPS = 50
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
STEP = 50


tiles_images = {
            'tree': load_img('tree.png'),
            'dark_tree': load_img('dark_tree.png'),
            'empty': load_img('m22.png'),
            'shadow': load_img('shadow.png'),
            'place_for_a_duel': load_img('MD.png')}
tile_width = tile_height = 100


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = 'data/' + filename
    with open(filename, 'r') as file:
        map_level = list(map(str.strip, file.readlines()))
    max_width = max(map(len, map_level))
    return list(map(lambda x: x.ljust(max_width, '.'), map_level))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tile_group_map, all_sprites_map)
        if tile_type == 'tree' or tile_type == 'dark_tree':
            self.add(box_group_map)
        elif tile_type == 'place_for_a_duel':
            self.add(duels_map)
        self.image = tiles_images[tile_type]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('shadow', x, y)
                tree = random.choice(('tree', 'dark_tree'))
                Tile(tree, x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(load_img("photo/character_go1.png"), 4, 1, x, y)
            elif level[y][x] == 'M':
                Tile('empty', x, y)
                Tile('place_for_a_duel', x, y)
    return new_player, x, y


class Player(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(player_group_map, all_sprites_map)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(tile_width * x, tile_height * y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj, level_x, level_y):
        obj.rect.x += self.dx
        if obj.rect.x < -obj.rect.width:
            obj.rect.x += (level_x + 1) * obj.rect.width
        if obj.rect.x >= obj.rect.width * level_x:
            obj.rect.x -= (level_x + 1) * obj.rect.width
        obj.rect.y += self.dy
        if obj.rect.y < -obj.rect.height:
            obj.rect.y += (level_y + 1) * obj.rect.height
        if obj.rect.y >= obj.rect.height * level_y:
            obj.rect.y -= (level_y + 1) * obj.rect.height

    def update(self, target):
        self.dx = width // 2 - (target.rect.x + target.rect.w // 2)
        self.dy = height // 2 - (target.rect.y + target.rect.h // 2)


all_sprites_map = pygame.sprite.Group()
tile_group_map = pygame.sprite.Group()
player_group_map = pygame.sprite.Group()
box_group_map = pygame.sprite.Group()
duels_map = pygame.sprite.Group()
player = None


class Map:
    def __init__(self, level):
        running = True
        flag = True
        player, level_x, level_y = generate_level(load_level(level))
        camera = Camera()
        pygame.display.set_caption('Map')
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.update()
                        player.rect.x -= STEP
                        if pygame.sprite.spritecollideany(player, box_group_map):
                            player.rect.x += STEP
                    if event.key == pygame.K_RIGHT:
                        player.update()
                        player.rect.x += STEP
                        if pygame.sprite.spritecollideany(player, box_group_map):
                            player.rect.x -= STEP
                    if event.key == pygame.K_UP:
                        player.update()
                        player.rect.y -= STEP
                        if pygame.sprite.spritecollideany(player, box_group_map):
                            player.rect.y += STEP
                    if event.key == pygame.K_DOWN:
                        player.update()
                        player.rect.y += STEP
                        if pygame.sprite.spritecollideany(player, box_group_map):
                            player.rect.y -= STEP
                    if pygame.sprite.spritecollideany(player, duels_map):
                        flag = False
                if event.type == pygame.MOUSEMOTION:
                    if not game_cursor1 is None:
                        xy = event.pos
                        if pygame.mouse.get_focused():
                            cursor_group.update(xy)
                        else:
                            cursor_group.update(xy, False)
            camera.update(player)
            for sprite in all_sprites_map:
                camera.apply(sprite, level_x, level_y)
            screen.fill((0, 0, 0))
            all_sprites_map.draw(screen)
            tile_group_map.draw(screen)
            player_group_map.draw(screen)
            cursor_group.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)
            if flag is False:
                return


def draw(i, y, arr):
    height, width = 750, 1200
    text_coord = height
    font = pygame.font.Font("data/F77.ttf", 22)
    for line in arr:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 20
        intro_rect.top = text_coord - y * i
        intro_rect.x = width // 2 - intro_rect.width // 2
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def story(name):
    arr = []
    name = 'data/' + name
    with open(name, 'r', encoding="utf-8") as admin:
        result = admin.readlines()
        for line in result:
            arr.append(line.strip('\n'))
    return arr


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Training:
    def __init__(self):
        super().__init__()
        fps = 60
        screen.fill("black")
        self.manager_tr = pygame_gui.UIManager((1200, 750))
        self.tm = 0

        self.location = pygame.transform.scale(load_img("loc_for.png"), (1200, 500))
        screen.blit(self.location, self.location.get_rect())

        self.text_input = UITextEntryLine(relative_rect=Rect(0, 500, 1100, 250), manager=self.manager_tr,
                                     placeholder_text="1 + 2 = 3")
        self.text_input.disable()

        self.but_sqrt = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1100, 550), (100, 50)),
                                                text='Корень',
                                                manager=self.manager_tr)
        self.but_sqrt.disable()

        self.but_ready = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1100, 500), (100, 50)),
                                                 text='Готово',
                                                 manager=self.manager_tr)
        self.but_ready.disable()

        self.but_opponent_ans = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1100, 700), (100, 50)),
                                                        text='Ответ',
                                                        manager=self.manager_tr)

        self.but_opponent_ans.disable()
        self.text()
        self.text_input2 = UITextEntryLine(relative_rect=Rect(1100, 650, 100, 50), manager=self.manager_tr)
        self.text_input2.disable()

        while True:
            screen.fill((0, 0, 0))
            self.manager_tr.draw_ui(screen)
            screen.blit(self.location, self.location.get_rect())
            self.text()
            cursor_group.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    self.tm += 1
                    self.training_move()
                if event.type == pygame.MOUSEMOTION:
                    if not game_cursor1 is None:
                        xy = event.pos
                        if pygame.mouse.get_focused():
                            cursor_group.update(xy)
                        else:
                            cursor_group.update(xy, False)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                self.manager_tr.process_events(event)
            arrow = pygame.transform.scale(load_img("arrow.png"), (100, 100))
            if self.tm == 2:
                self.arrow1 = arrow.get_rect().move(1100, 460)
                screen.blit(arrow, self.arrow1)
            if self.tm == 3:
                self.arrow1 = arrow.get_rect().move(1100, 410)
                screen.blit(arrow, self.arrow1)
            if self.tm == 4:
                screen.blit(self.location, self.location.get_rect())
                self.arrow1 = arrow.get_rect().move(1100, 550)
                screen.blit(arrow, self.arrow1)
            if self.tm == 5:
                screen.fill('black', (1100, 598, 100, 50))
                self.text_input2.enable()
                self.text()
                self.arrow1 = arrow.get_rect().move(1100, 610)
                screen.blit(arrow, self.arrow1)
            if self.tm == 6:
                screen.fill('black', (1100, 598, 100, 53))
                self.text()
            pygame.display.flip()
            self.manager_tr.update(fps)
            clock.tick(fps)

    def training_move(self):
        if self.tm == 1:
            self.text_input.enable()
        if self.tm == 2:
            self.but_sqrt.enable()
        if self.tm == 3:
            self.but_ready.enable()
        if self.tm == 4:
            self.text_input2.enable()
        if self.tm == 5:
            self.but_opponent_ans.enable()
        if self.tm == 6:
            print("Congratulations!")

    def text(self):
        rules = ["Ответ", "", "Противника"]
        font = pygame.font.Font("data/F77.ttf", 13)
        text_coord = 620
        for line in rules:
            self.rendered = font.render(line, True, "white")
            self.linerect = self.rendered.get_rect()
            text_coord += -5
            self.linerect.top = text_coord
            self.linerect.x = 1100
            text_coord += self.linerect.height
            screen.blit(self.rendered, self.linerect)


class Story:
    def __init__(self, name):
        super().__init__()
        st1 = story(name)
        size = width, height = 1200, 750
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption('Story')
        screen.fill((0, 0, 0))
        clock = pygame.time.Clock()
        s = 0
        manager_st = pygame_gui.UIManager((1200, 750))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    self.chapters()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                manager_st.process_events(event)
            screen.fill((0, 0, 0))
            s += 1
            draw(s, 0.1, st1)
            clock.tick(10000000)
            pygame.display.flip()

    def chapters(self):
        fps = 60
        screen.fill("black")
        manager_ch = pygame_gui.UIManager((1200, 750))

        first_ch = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (400, 750)),
                                                text='<mega_image>',
                                                manager=manager_ch)
        second_ch = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 0), (400, 750)),
                                                text='<mega_image_2>',
                                                manager=manager_ch)

        third_ch = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((800, 0), (400, 750)),
                                                text='<mega_image_3>',
                                                manager=manager_ch)

        while True:
            screen.fill((0, 0, 0))
            manager_ch.draw_ui(screen)
            cursor_group.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == first_ch:
                        # Уровни для 1-й главы
                        #Map('level1.txt')
                        one_player()
                    if event.ui_element == second_ch:
                        # Уровни для 2-й главы
                        pass
                    if event.ui_element == third_ch:
                        # Уровни для 3-й главы
                        pass
                if event.type == pygame.MOUSEMOTION:
                    if not game_cursor1 is None:
                        xy = event.pos
                        if pygame.mouse.get_focused():
                            cursor_group.update(xy)
                        else:
                            cursor_group.update(xy, False)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                manager_ch.process_events(event)
            pygame.display.flip()

            manager_ch.update(fps)
            clock.tick(fps)


def one_player():
    arr = []
    fps = 60
    screen.fill("black")
    manager_tp = pygame_gui.UIManager((1200, 750))
    location = pygame.transform.scale(load_img("loc_for.png"), (1200, 500))
    screen.blit(location, location.get_rect())
    text_input = UITextEntryLine(relative_rect=Rect(0, 500, 1100, 200), manager=manager_tp,
                                 placeholder_text="")
    but_sqrt = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1100, 550), (100, 50)),
                                            text='Корень',
                                            manager=manager_tp)

    but_ready = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1100, 500), (100, 50)),
                                             text='Готово',
                                             manager=manager_tp)

    but_opponent_ans = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1100, 700),
                                                                              (100, 50)),
                                                    text='Ответ',
                                                    manager=manager_tp)

    def text():
        rules = ["Ответ", "", "на пример"]
        font = pygame.font.Font("data/F77.ttf", 13)
        text_coord = 620
        for line in rules:
            rendered = font.render(line, True, "white")
            linerect = rendered.get_rect()
            text_coord += -5
            linerect.top = text_coord
            linerect.x = 1100
            text_coord += linerect.height
            screen.blit(rendered, linerect)

    text()
    text_input2 = UITextEntryLine(relative_rect=Rect(1100, 650, 100, 50), manager=manager_tp)
    font = pygame.font.Font("data/F77.ttf", 15)
    question = ''
    text_pr = font.render(question, True, "white")
    while True:
        manager_tp.draw_ui(screen)
        screen.fill((0, 0, 0))
        screen.blit(location, location.get_rect())
        manager_tp.draw_ui(screen)
        text()
        screen.blit(text_pr, (0, 715, 0, 0))
        cursor_group.draw(screen)
        for event in pygame.event.get():
            if text_input.get_text() != question:
                question = text_input.get_text()
            text_pr = font.render(question, True, "white")
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                pass
                # Можно вывести содержимое
                # print(text_input.get_text())
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == but_ready:
                    WHOSETURN = 1
                    text_input.clear()
                    print(arr)
                    arr.clear()
                if event.ui_element == but_sqrt:
                    question = 'v‾'
                    text_input.set_text(text_input.get_text() + 'v')
                    print(question)
                if event.ui_element == but_opponent_ans:
                    pass
            if event.type == pygame.MOUSEMOTION:
                if not game_cursor1 is None:
                    xy = event.pos
                    if pygame.mouse.get_focused():
                        cursor_group.update(xy)
                    else:
                        cursor_group.update(xy, False)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            manager_tp.process_events(event)
        pygame.display.flip()
        manager_tp.update(fps)
        clock.tick(fps)

WHOSETURN = 0


def two_players():
    global WHOSETURN
    arr = []
    fps = 60
    screen.fill("black")
    manager_tp = pygame_gui.UIManager((1200, 750))

    location = pygame.transform.scale(load_img("loc_for.png"), (1200, 500))
    screen.blit(location, location.get_rect())

    text_input = UITextEntryLine(relative_rect=Rect(0, 500, 1100, 250), manager=manager_tp,
                                 placeholder_text="1 + 2 = 3")

    but_sqrt = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1100, 550), (100, 50)),
                                             text='Корень',
                                             manager=manager_tp)

    but_ready = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1100, 500), (100, 50)),
                                            text='Готово',
                                            manager=manager_tp)

    but_opponent_ans = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1100, 700), (100, 50)),
                                            text='Ответ',
                                            manager=manager_tp)

    def text():
        rules = ["Ответ", "", "Противника"]
        font = pygame.font.Font("data/F77.ttf", 13)
        text_coord = 620
        for line in rules:
            rendered = font.render(line, True, "white")
            linerect = rendered.get_rect()
            text_coord += -5
            linerect.top = text_coord
            linerect.x = 1100
            text_coord += linerect.height
            screen.blit(rendered, linerect)

    text()
    text_input2 = UITextEntryLine(relative_rect=Rect(1100, 650, 100, 50), manager=manager_tp)

    while True:
        screen.fill((0, 0, 0))
        screen.blit(location, location.get_rect())
        manager_tp.draw_ui(screen)
        text()
        cursor_group.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                pass
                # Можно вывести содержимое
                # print(text_input.get_text())
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == but_ready:
                    arr.append(text_input.get_text())
                    WHOSETURN = 1
                    print(arr)
                    arr.clear()
                if event.ui_element == but_sqrt:
                    pass
                if event.ui_element == but_opponent_ans:
                    pass
            if event.type == pygame.MOUSEMOTION:
                if not game_cursor1 is None:
                    xy = event.pos
                    if pygame.mouse.get_focused():
                        cursor_group.update(xy)
                    else:
                        cursor_group.update(xy, False)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            manager_tp.process_events(event)
        pygame.display.flip()
        manager_tp.update(fps)
        clock.tick(fps)


def lobby():
    fps = 60
    screen.fill("black")
    font_renderer = pygame.font.Font("data/F77.ttf", 40)
    manager_lob = pygame_gui.UIManager((1200, 750))

    but_red_skin = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((600, 0), (295, 290)),
                                                text='',
                                                manager=manager_lob)

    but_blue_skin = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((905, 0), (295, 290)),
                                                 text='',
                                                 manager=manager_lob)

    but_green_skin = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((600, 295), (295, 290)),
                                                  text='',
                                                  manager=manager_lob)

    but_hood_skin = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((905, 295), (295, 290)),
                                                 text='',
                                                 manager=manager_lob)

    but_goose = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((833, 590), (128, 160)),
                                             text='',
                                             manager=manager_lob)

    ###############################################################################################
    but_red_skin_purch = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 0), (50, 50)),
                                                text='',
                                                manager=manager_lob)

    but_blue_skin_purch = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((70, 0), (50, 50)),
                                                 text='',
                                                 manager=manager_lob)

    but_green_skin_purch = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((130, 0), (50, 50)),
                                                  text='',
                                                  manager=manager_lob)

    but_hood_skin_purch = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((190, 0), (50, 50)),
                                                 text='',
                                                 manager=manager_lob)

    but_goose_purch = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 0), (50, 50)),
                                             text='',
                                             manager=manager_lob)
    # ВАЖНО!
    but_green_skin_purch.disable()
    but_red_skin_purch.disable()
    but_hood_skin_purch.disable()
    but_blue_skin_purch.disable()
    but_goose_purch.disable()

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    red_skin_purch = pygame.transform.scale(load_img("photo/R_character.png"), (50, 50))
    red_skins_purch = red_skin_purch.get_rect().move(10, 0)

    blue_skin_purch = pygame.transform.scale(load_img("photo/B_character.png"), (50, 50))
    blue_skins_purch = blue_skin_purch.get_rect().move(70, 0)

    green_skin_purch = pygame.transform.scale(load_img("photo/G_character.png"), (50, 50))
    green_skins_purch = green_skin_purch.get_rect().move(130, 0)

    hood_skin_purch = pygame.transform.scale(load_img("photo/NY_character.png"), (50, 50))
    hood_skins_purch = hood_skin_purch.get_rect().move(190, 0)

    goose_purch = pygame.transform.scale(load_img("photo/goose.png"), (50, 50))
    goose_s_purch = goose_purch.get_rect().move(250, -5)
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    ###############################################################################################

    label_red = font_renderer.render(f"20", True, "white")
    label_rect_red = label_red.get_rect()
    label_rect_red = label_rect_red.move((720, 220))

    label_blue = font_renderer.render(f"40", True, "white")
    label_rect_blue = label_blue.get_rect()
    label_rect_blue = label_rect_blue.move((1020, 220))

    label_green = font_renderer.render(f"60", True, "white")
    label_rect_green = label_green.get_rect()
    label_rect_green = label_rect_green.move((720, 510))

    label_hood = font_renderer.render(f"100", True, "white")
    label_rect_hood = label_hood.get_rect()
    label_rect_hood = label_rect_hood.move((1020, 510))

    label_goose = font_renderer.render(f"150", True, "white")
    label_rect_goose = label_goose.get_rect()
    label_rect_goose = label_rect_goose.move((833, 590))

    location = pygame.transform.scale(load_img("loc_for.png"), (1200, 750))
    screen.blit(location, location.get_rect())

    red_skin = pygame.transform.scale(load_img("photo/R_character.png"), (295, 290))
    red_skins = red_skin.get_rect().move(600, 0)

    blue_skin = pygame.transform.scale(load_img("photo/B_character.png"), (295, 290))
    blue_skins = blue_skin.get_rect().move(905, 0)

    green_skin = pygame.transform.scale(load_img("photo/G_character.png"), (295, 290))
    green_skins = green_skin.get_rect().move(600, 295)

    hood_skin = pygame.transform.scale(load_img("photo/NY_character.png"), (295, 290))
    hood_skins = hood_skin.get_rect().move(905, 295)

    goose = pygame.transform.scale(load_img("photo/goose.png"), (128, 160))
    goose_s = goose.get_rect().move(833, 590)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            '''Проверка на двойное нажатие для совершения покупки
            if event.type == pygame.KEYDOWN and event.key == pygame.MOUSEBUTTONDOWN:
                purchased = True'''
            manager_lob.process_events(event)

        screen.blit(red_skin, red_skins)
        screen.blit(blue_skin, blue_skins)
        screen.blit(green_skin, green_skins)
        screen.blit(hood_skin, hood_skins)
        screen.blit(goose, goose_s)

        ################################################
        # Ставим условие, что если в БД есть купленный скин, то кнопки делаем .enable()
        screen.blit(red_skin_purch, red_skins_purch)
        screen.blit(blue_skin_purch, blue_skins_purch)
        screen.blit(green_skin_purch, green_skins_purch)
        screen.blit(hood_skin_purch, hood_skins_purch)
        screen.blit(goose_purch, goose_s_purch)
        ################################################

        screen.blit(label_red, label_rect_red)
        screen.blit(label_blue, label_rect_blue)
        screen.blit(label_green, label_rect_green)
        screen.blit(label_hood, label_rect_hood)
        screen.blit(label_goose, label_rect_goose)

        pygame.display.flip()
        manager_lob.draw_ui(screen)
        manager_lob.update(fps)
        clock.tick(fps)


class Cursors(pygame.sprite.Sprite):
    def __init__(self, image, group):
        group.empty()
        super().__init__(group)
        self.image = load_img(image)
        self.rect = self.image.get_rect()
        self.rect.x = width + 100
        self.rect.y = height + 100

    def update(self, xy, key=True):
        event = xy
        if key:
            self.rect.x = event[0]
            self.rect.y = event[1]
        else:
            self.rect.x = width + 100
            self.rect.y = height + 100


def settings():
    fps = 60
    screen.fill("black")
    font_renderer = pygame.font.Font("data/F77.ttf", 40)
    manager_sett = pygame_gui.UIManager((1200, 750))
    label_vol = font_renderer.render("Звук", True, "white")
    label_rect_vol = label_vol.get_rect()
    label_rect_vol = label_rect_vol.move((200, 187))

    screen.blit(label_vol, label_rect_vol)

    label_cur = font_renderer.render("Курсор", True, "white")
    label_rect_cur = label_cur.get_rect()
    label_rect_cur = label_rect_cur.move((200, 374))

    screen.blit(label_cur, label_rect_cur)
    x = int(cur.execute("""SELECT quantity_of_coins FROM 'primary' 
            WHERE object = 'sound volume'""").fetchall()[0][0])
    slider = pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(
        relative_rect=pygame.Rect((480, 208), (600, 30)),
        manager=manager_sett, start_value=x, value_range=(0, 100))

    arr = ["Обычный", "Карандаш", "Кастомный"]
    y = arr.index(cur.execute("""SELECT photo_gif FROM 'primary' 
            WHERE object = 'cursor'""").fetchall()[0][0])
    drop_menu = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
        options_list=arr, starting_option=arr[y],  relative_rect=pygame.Rect((480, 400), (200, 60)),
        manager=manager_sett)

    game_cursor = cur.execute("""SELECT photo FROM 'primary'
     WHERE object = 'cursor'""").fetchall()[0][0]
    if game_cursor == 'common':
        game_cursor = None
    while True:
        screen.fill((0, 0, 0))
        manager_sett.draw_ui(screen)
        screen.blit(label_vol, label_rect_vol)
        screen.blit(label_cur, label_rect_cur)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                if not game_cursor is None:
                    xy = event.pos
                    if pygame.mouse.get_focused():
                        cursor_group.update(xy)
                    else:
                        cursor_group.update(xy, False)
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                pass
            elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                x = event.value
                queue = f"UPDATE 'primary' SET quantity_of_coins = {x}" \
                        f" WHERE object = 'sound volume'"
                cur.execute(queue)
                con.commit()
            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == drop_menu:
                    values = drop_menu.selected_option
                    queue1 = f"UPDATE 'primary' SET photo_gif = '{values}' WHERE object = 'cursor'"
                    if values == 'Карандаш':
                        cursor = 'cur1.png'
                        pygame.mouse.set_visible(False)
                    elif values == 'Кастомный':
                        cursor = 'cur2.png'
                        pygame.mouse.set_visible(False)
                    else:
                        cursor = 'common'
                        pygame.mouse.set_visible(True)
                    queue2 = f"UPDATE 'primary' SET photo = '{cursor}' WHERE object = 'cursor'"
                    cur.execute(queue1)
                    cur.execute(queue2)
                    con.commit()
                    screen.fill((0, 0, 0), (480, 459, 200, 100))
                    if cursor != 'common':
                        game_cursor = Cursors(cursor, cursor_group)
                    else:
                        game_cursor = None
                        cursor_group.empty()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            manager_sett.process_events(event)
        cursor_group.draw(screen)
        pygame.display.flip()
        manager_sett.update(fps)
        clock.tick(fps)


is_running = True
all_sprites = pygame.sprite.Group()
logo = pygame.transform.scale(load_img("logo_2.png"), (8000, 400))
logo_go = AnimatedSprite(logo, 20, 1, 400, -50)
clock = pygame.time.Clock()
fps = 15
game_cursor1 = cur.execute("""SELECT photo FROM 'primary'
 WHERE object = 'cursor'""").fetchall()[0][0]
if game_cursor1 == 'common':
    game_cursor1 = None
    pygame.mouse.set_visible(True)
else:
    game_cursor1 = Cursors(game_cursor1, cursor_group)
    pygame.mouse.set_visible(False)
while is_running:
    screen.fill((0, 0, 0))
    manager.draw_ui(screen)
    cursor_group.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == train_button:
                Training()
            if event.ui_element == story_button:
                Story('story1.txt')
            if event.ui_element == two_players_button:
                two_players()
            if event.ui_element == lobby_button:
                pass
            if event.ui_element == settings_button:
                settings()
                game_cursor1 = cur.execute("""SELECT photo FROM 'primary'
                                 WHERE object = 'cursor'""").fetchall()[0][0]
                if game_cursor1 == 'common':
                    game_cursor1 = None
                    pygame.mouse.set_visible(True)
                else:
                    game_cursor1 = Cursors(game_cursor1, cursor_group)
                    pygame.mouse.set_visible(False)
        if event.type == pygame.MOUSEMOTION:
            if not game_cursor1 is None:
                xy = event.pos
                if pygame.mouse.get_focused():
                    cursor_group.update(xy)
                else:
                    cursor_group.update(xy, False)
        manager.process_events(event)
    all_sprites.draw(screen)
    all_sprites.update()
    manager.update(fps)
    pygame.display.flip()
    screen.fill("black")
    clock.tick(fps)
pygame.quit()
