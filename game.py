import pygame
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


    # заставочка

    def terminate():
        pygame.quit()
        sys.exit()


    def start_screen():
        intro_text = ["ЗАСТАВКА", "",
                      "ТЕСТОВЫЙ ПРОБЕГ",
                      "!№;:?*()_+,",
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

    # персонаж
    i = 0


    class Violet(pygame.sprite.Sprite):
        def __init__(self, *group):
            super().__init__(*group)

            self.walk_right_gg = [pygame.image.load('sprites walk 1.png'),
                                  pygame.image.load('sprites walk 2.png'), pygame.image.load('sprites walk 2-3.png'),
                                  pygame.image.load('sprites walk 3.png'), pygame.image.load('sprites walk 4.png'),
                                  pygame.image.load('sprites walk 5.png'), pygame.image.load('sprites walk 5.png'),
                                  pygame.image.load('sprites walk 4.png'), pygame.image.load('sprites walk 3.png'),
                                  pygame.image.load('sprites walk 2-3.png'),
                                  pygame.image.load('sprites walk 2.png')]
            self.walk_left_gg = [pygame.image.load('sp w left 1.png'), pygame.image.load('sp w left 2.png'),
                                 pygame.image.load('sp w left 2-3.png'), pygame.image.load('sp w left 3.png'),
                                 pygame.image.load('sp w left 4.png'),
                                 pygame.image.load('sp w left 5.png'), pygame.image.load('sp w left 5.png'),
                                 pygame.image.load('sp w left 4.png'), pygame.image.load('sp w left 3.png'),
                                 pygame.image.load('sp w left 2-3.png'),
                                 pygame.image.load('sp w left 2.png')]
            self.stand = [pygame.image.load('stand 1.png'), pygame.image.load('stand 2.png'),
                          pygame.image.load('stand 3.png'), pygame.image.load('stand 4.png')]
            self.image = self.stand[0]
            self.rect = self.image.get_rect()
            self.i = 0

        def update(self, status):

            if status == 'walk_right':
                self.image = self.walk_right_gg[self.i]
                self.i += 1
                if self.i == 11:
                    self.i = 0
                clock.tick(14)
            if status == 'walk_left':
                self.image = self.walk_left_gg[self.i]
                self.i += 1
                if self.i == 11:
                    self.i = 0
                clock.tick(14)
            if status == 'simple_stand':
                self.image = self.stand[0]
            screen.blit(self.image, [pers_x, pers_y])


    # левелы, они же уровни или локации, как хотите

    class Window():
        def __init__(self):
            self.win = pygame.image.load('win.png')
            self.tt = pygame.font.SysFont(None, 30)
            self.text_v = self.tt.render('', False, (250, 250, 250))

        def vi_talk(self, text=''):
            self.text_v = self.tt.render(text, False, (250, 250, 250))

        def uwu(self, poser):
            if poser == True:
                screen.blit(self.win, (0, 0))
                screen.blit(self.text_v, (280, 550))
            if poser == False:
                screen.blit(self.win, (0, 300))
                screen.blit(self.text_v, (280, 850))


class Levels():
    def __init__(self, *group):
        super().__init__(*group)
        self.background1 = pygame.image.load('test background 2.2.jpg')
        self.background3 = pygame.image.load('test background 2.jpg')
        self.background2 = pygame.image.load("background city 1.png").convert()
        self.platform_im = pygame.image.load('platform 1.png').convert()
        self.platform_im.set_colorkey(pygame.Color('white'))
        self.platform_im2 = pygame.image.load('platform 2.png')
        self.platform_im2.set_colorkey(pygame.Color('white'))
        self.phone = False
        #  self.image_phone = pygame.image.load('ph.png')
        self.wire = False
        # self.image_wire = pygame.image.load('')
        self.quest = False
        self.knife = False

    def lv1(self):
        screen.blit(self.background1, [0, 0])

    def lv2(self):
        screen.blit(self.background2, [0, 0])
        screen.blit(self.platform_im, [0, 0])
        screen.blit(self.platform_im2, [300, 150])

    def lv3(self):
        screen.blit(self.background3, [0, 0])


lv_li = 2
all_sprites = pygame.sprite.Group()
player = Violet()
all_sprites.add(player)

player_image = Violet()
pers_x = 25
pers_y = 320

loc = Levels()
di_win = Window()
k = -1
pose = ''
#  реплики 1
test_text = ['Если бы я только знал, чем это всё кончится...',
             'Я бы не брал ту шавуху',
             '']
# а тут совмещаем все картинки. ПОРЯДОК ВАЖЕН!!!

while running:
    # чек ивенты
    for event in pygame.event.get():
        # закрывашка
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_e]:
                pose = True
            elif event.key in [pygame.K_0]:
                pose = False
            if pose:
                if event.key in [pygame.K_l] and k != len(test_text) - 1:
                    k += 1
                elif event.key in [pygame.K_j] and k > 0:
                    k -= 1

    keys = pygame.key.get_pressed()

    # лево-право
    all_sprites.update('simple_stand')
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        pers_x += step if pers_x < 1500 else 0
        all_sprites.update('walk_right')
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        pers_x -= step if 0 < pers_x else 0
        all_sprites.update('walk_left')
    else:
        all_sprites.update('stand')

    if pers_x < 25 and lv_li > 1:
        lv_li -= 1
        pers_x = 1100
    elif pers_x > 1110 and lv_li < 3:
        lv_li += 1
        pers_x = 35

    if lv_li == 1:
        loc.lv1()
    if lv_li == 2:
        loc.lv2()
    if lv_li == 3:
        loc.lv3()
    screen.blit(player.image, [pers_x, pers_y])
    di_win.uwu(pose)
    if pose:
        di_win.vi_talk(test_text[k])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
