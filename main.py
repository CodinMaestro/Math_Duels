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
background = pygame.Surface((1200, 750))
background.fill(pygame.Color('#000000'))

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

# text_input = UITextEntryLine(relative_rect=Rect(0, 0, 100, 100), manager=manager)


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


class Training:
    def __init__(self):
        pass


class Story:
    def __init__(self):
        pass


class TwoPlayers:
    def __init__(self):
        pass


class Lobby:
    def __init__(self):
        pass


class Settings:
    def __init__(self):
        pass


is_running = True
all_sprites = pygame.sprite.Group()
logo = pygame.transform.scale(load_img("logo.png"), (8000, 400))
dragon = AnimatedSprite(logo, 20, 1, 400, -50)
clock = pygame.time.Clock()
fps = 10

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == train_button:
                print('ОБУЧЕНИЕ!')
            if event.ui_element == story_button:
                print('СЮЖЕТ!')
            if event.ui_element == two_players_button:
                print('ИГРА НА ДВОИХ!')
            if event.ui_element == lobby_button:
                print('ЛОББИ!')
            if event.ui_element == settings_button:
                print('НАСТРОЙКИ!')

        '''if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            print(text_input.get_text())'''

        manager.process_events(event)
    all_sprites.draw(screen)
    all_sprites.update()
    manager.update(fps)
    pygame.display.flip()
    screen.blit(background, (0, 0))
    manager.draw_ui(screen)
    clock.tick(fps)