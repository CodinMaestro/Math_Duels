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


def training():
    pass


def story():
    pass


def two_players():
    fps = 60
    screen.fill("black")
    manager_tp = pygame_gui.UIManager((1200, 750))
    text_input = UITextEntryLine(relative_rect=Rect(0, 500, 1100, 250), manager=manager_tp)

    but_sqrt = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1100, 600), (100, 100)),
                                             text='Корень',
                                             manager=manager_tp)

    but_ready = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1100, 500), (100, 100)),
                                            text='Готово',
                                            manager=manager_tp)

    but_smth = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1100, 700), (100, 50)),
                                            text='Ответ',
                                            manager=manager_tp)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                pass
                # Можно вывести содержимое
                #print(text_input.get_text())

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
    font_renderer = pygame.font.Font(None, 90)
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
                pass
            if event.ui_element == story_button:
                pass
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