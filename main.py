import math


class Math_question:
    def __init__(self, line, dict=None):
        self.problem = line
        self.question = ''
        if dict is None:
            self.numbers = {}
        else:
            self.numbers = dict
        self.numbers['1'] = 1
        self.numbers['0'] = 1
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
                return True

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
                elif s[i] in '+-/':
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
    
import pygame
import pygame_gui
from pygame.rect import Rect
from pygame_gui.elements import UITextEntryLine
import sys
import os

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


class Training():
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

        self.text_input2 = UITextEntryLine(relative_rect=Rect(1100, 650, 100, 50), manager=self.manager_tr)
        self.text_input2.disable()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    self.tm += 1
                    self.training_move()
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
                self.arrow1 = arrow.get_rect().move(1100, 610)
                screen.blit(arrow, self.arrow1)
            pygame.display.flip()
            self.manager_tr.draw_ui(screen)
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


class Story:
    def __init__(self):
        super().__init__()
        fps = 60
        screen.fill("black")
        manager_st = pygame_gui.UIManager((1200, 750))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    self.chapters()

                manager_st.process_events(event)
            pygame.display.flip()
            manager_st.draw_ui(screen)
            manager_st.update(fps)
            clock.tick(fps)

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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == first_ch:
                        # Уровни для 1-й главы
                        pass
                    if event.ui_element == second_ch:
                        # Уровни для 2-й главы
                        pass
                    if event.ui_element == third_ch:
                        # Уровни для 3-й главы
                        pass
                manager_ch.process_events(event)
            pygame.display.flip()
            manager_ch.draw_ui(screen)
            manager_ch.update(fps)
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

    text_input = UITextEntryLine(relative_rect=Rect(0, 500, 1100, 250), manager=manager_tp, placeholder_text="1 + 2 = 3")

    but_sqrt = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1100, 550), (100, 50)),
                                             text='Корень',
                                             manager=manager_tp)

    but_ready = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1100, 500), (100, 50)),
                                            text='Готово',
                                            manager=manager_tp)

    but_opponent_ans = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1100, 700), (100, 50)),
                                            text='Ответ',
                                            manager=manager_tp)
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

    text_input2 = UITextEntryLine(relative_rect=Rect(1100, 650, 100, 50), manager=manager_tp)

    while True:
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
                if event.ui_element == but_sqrt:
                    pass
                if event.ui_element == but_opponent_ans:
                    pass

            manager_tp.process_events(event)
        pygame.display.flip()
        manager_tp.draw_ui(screen)
        manager_tp.update(fps)
        clock.tick(fps)


def lobby():
    pass


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

    slider = pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(relative_rect=pygame.Rect((480, 208), (600, 30)),
                                                                manager=manager_sett, start_value=0, value_range=(0, 100))

    arr = ["Такой курсор", "Вот такой курсор", "И этот"]
    drop_menu = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(options_list=arr, starting_option=arr[0],
                                                                     relative_rect=pygame.Rect((480, 400), (200, 60)),
                                                                     manager=manager_sett)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                pass
            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == drop_menu:
                    return
            manager_sett.process_events(event)
        pygame.display.flip()
        manager_sett.draw_ui(screen)
        manager_sett.update(fps)
        clock.tick(fps)


is_running = True
all_sprites = pygame.sprite.Group()
logo = pygame.transform.scale(load_img("logo_2.png"), (8000, 400))
logo_go = AnimatedSprite(logo, 20, 1, 400, -50)
clock = pygame.time.Clock()
fps = 10
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == train_button:
                Training()
            if event.ui_element == story_button:
                Story()
            if event.ui_element == two_players_button:
                pass
                two_players()
            if event.ui_element == lobby_button:
                pass
            if event.ui_element == settings_button:
                settings()
        manager.process_events(event)
    all_sprites.draw(screen)
    all_sprites.update()
    manager.update(fps)
    pygame.display.flip()
    screen.fill("black")
    manager.draw_ui(screen)
    clock.tick(fps)
pygame.quit()


n = input()
p = Math_question(n)
np = p.transformation()
s = p.checking_for_correctness()
if s:
    print(p.answer())
    print(p.print_summ())
else:
    print('Ошибка')
