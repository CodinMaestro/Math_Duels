import pygame
import pygame_gui
from pygame.rect import Rect
from pygame_gui.elements import UITextEntryLine

pygame.init()

pygame.display.set_caption('Math Duels')
window_surface = pygame.display.set_mode((1200, 750))
manager = pygame_gui.UIManager((1200, 750))
background = pygame.Surface((1200, 750))
background.fill(pygame.Color('#000000'))

train_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 275), (200, 40)),
                                             text='Обучение',
                                             manager=manager)

story_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 335), (200, 40)),
                                             text='Сюжет',
                                             manager=manager)

two_players_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 395), (200, 40)),
                                             text='Играть с другом',
                                             manager=manager)

lobby_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 455), (200, 40)),
                                             text='Лобби',
                                             manager=manager)

settings_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 515), (200, 40)),
                                             text='Настройки',
                                             manager=manager)

#text_input = UITextEntryLine(relative_rect=Rect(0, 0, 100, 100), manager=manager)



is_running = True

clock = pygame.time.Clock()
fps = 60

while is_running:
    time_delta = clock.tick(60) / 1000.0
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
    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)
    pygame.display.update()