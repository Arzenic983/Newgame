import pygame
from pygame import *
import sys

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Игра.екзе')
    size = width, height = 1280, 720
    screen = pygame.display.set_mode(size)

    # все переменные писать в этот блок. Желательно.

    running = True
    fps = 144
    clock = pygame.time.Clock()
    step = 12
    PLATFORM_WIDTH = 30
    PLATFORM_HEIGHT = 30
    PLATFORM_COLOR = "#FFFFFF"

    # заставочка

    def terminate():
        pygame.quit()
        sys.exit()


    def start_screen():
        intro_text = ["ЗАСТАВКА", "",
                      "ТЕСТОВЫЙ ПРОБЕГ",
                      "Для продолжения нажмите любую клавишу"]
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 500
        for line in intro_text:
            string_rendered = font.render(line, True, pygame.Color('white'))
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
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return
            pygame.display.flip()
            clock.tick(fps)




    start_screen()

    # загрузочный блок 0:

    # бэкграунд

    background_image = pygame.image.load("test background 2.2.jpg").convert()

    # персонаж
    i = 0


    class Violet(pygame.sprite.Sprite):
        def __init__(self, *group):
            super().__init__(*group)

            self.walk_right_gg = [pygame.image.load('sprites walk 1.png'), pygame.image.load('sprites walk 2.png'),
                                  pygame.image.load('sprites walk 3.png'), pygame.image.load('sprites walk 4.png'),
                                  pygame.image.load('sprites walk 5.png'), pygame.image.load('sprites walk 5.png'),
                                  pygame.image.load('sprites walk 3.png'), pygame.image.load('sprites walk 2.png')]
            self.walk_left_gg = [pygame.image.load('sp w left 1.png'), pygame.image.load('sp w left 2.png'),
                                 pygame.image.load('sp w left 3.png'), pygame.image.load('sp w left 4.png'),
                                 pygame.image.load('sp w left 5.png'), pygame.image.load('sp w left 5.png'),
                                 pygame.image.load('sp w left 3.png'), pygame.image.load('sp w left 2.png')]
            self.stand = [pygame.image.load('stand 1.png'), pygame.image.load('stand 2.png'),
                          pygame.image.load('stand 3.png'), pygame.image.load('stand 4.png')]
            self.image = self.stand[0]
            self.rect = self.image.get_rect()
            self.rect.x = 25
            self.rect.y = 350
            self.i = 0
            self.start_velocity = 0
            self.jumped = False

        def update(self, status):

            if status == 'walk_right':
                self.image = self.walk_right_gg[self.i]
                self.i += 1
                if self.i == 8:
                    self.i = 0
                clock.tick(12)
            if status == 'walk_left':
                self.image = self.walk_left_gg[self.i]
                self.i += 1
                if self.i == 8:
                    self.i = 0
                clock.tick(12)
            if status == 'simple_stand':
                self.image = self.stand[0]
            screen.blit(self.image, self.rect)

        def gravity(self):
            self.start_velocity += 0.3
            if self.start_velocity > 20:
                self.start_velocity = 20

    all_sprites = pygame.sprite.Group()
    player = Violet()
    all_sprites.add(player)

    player_image = Violet()
    pers_x = 25
    pers_y = 320
    level = [
        "                          ",
        "                          ",
        "                          ",
        "                          ",
        "                          ",
        "                          ",
        "                          ",
        "                                     ---------",
        "                                     ---------",
        "                          ",
        "                          ",
        "                          ",
        "                          ",
        "                          ",
        "                          ",
        "                          ",
        "                          ",
        "                                    ",
        "                              ---   ",
        "                              ---   ",
        "---------------------------------   ",
        "---------------------------------   "]

    # а тут совмещаем все картинки. ПОРЯДОК ВАЖЕН!!!

    screen.blit(background_image, [0, 0])

    while running:
        # чек ивенты
        for event in pygame.event.get():
            # закрывашка
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # лево-право
        all_sprites.update('simple_stand')
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player.rect.x += step if pers_x < 1500 else 0
            all_sprites.update('walk_right')
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player.rect.x -= step if 0 < pers_x else 0
            all_sprites.update('walk_left')
        if keys[pygame.K_SPACE] and player.jumped == False:
            player.start_velocity = -8
            player.jumped = True
        if keys[pygame.K_SPACE]:
            player.jumped = False
        else:
            all_sprites.update('stand')


        pers_y += player.start_velocity
        player.gravity()

        if player.rect.bottom > height:
            player.rect.bottom = height


        screen.blit(background_image, [0, 0])

        x = y = 0  # координаты
        for row in level:  # вся строка
            for col in row:  # каждый символ
                if col == "-":
                    # создаем блок, заливаем его цветом и рисеум его
                    pf = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
                    pf.fill(Color(PLATFORM_COLOR))
                    screen.blit(pf, (x, y))

                x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
            y += PLATFORM_HEIGHT  # то же самое и с высотой
            x = 0  # на каждой новой строчке начинаем с нуля
        screen.blit(player.image, player.rect)
        pygame.display.flip()
        clock.tick(fps)

pygame.quit()
