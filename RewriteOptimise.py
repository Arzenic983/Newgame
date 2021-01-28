import pygame
import sys

# все переменные писать в этот блок. Желательно.

running = True
fps = 144
clock = pygame.time.Clock()
replica_num = 0
level_number = 0
flag_dialog = 0

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Игра.екзе')
    size = width, height = 1280, 720
    screen = pygame.display.set_mode(size)


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


class Player(pygame.sprite.Sprite):
    def __init__(self, *group, x, y):
        super().__init__(*group)

        self.walk_right_gg = [pygame.image.load('sprites walk 1.png'),
                              pygame.image.load('sprites walk 2.png'), pygame.image.load('sprites walk 2-3.png'),
                              pygame.image.load('sprites walk 3.png'), pygame.image.load('sprites walk 4.png'),
                              pygame.image.load('sprites walk 5.png'), pygame.image.load('sprites walk 4.png'),
                              pygame.image.load('sprites walk 3.png'), pygame.image.load('sprites walk 2-3.png'),
                              pygame.image.load('sprites walk 2.png'),
                              pygame.image.load('sprites walk 1.png')]
        self.walk_left_gg = [pygame.image.load('sp w left 1.png'), pygame.image.load('sp w left 2.png'),
                             pygame.image.load('sp w left 2-3.png'), pygame.image.load('sp w left 3.png'),
                             pygame.image.load('sp w left 4.png'),
                             pygame.image.load('sp w left 5.png'), pygame.image.load('sp w left 4.png'),
                             pygame.image.load('sp w left 3.png'), pygame.image.load('sp w left 2-3.png'),
                             pygame.image.load('sp w left 2.png'),
                             pygame.image.load('sp w left 1.png')]
        self.stand = [pygame.image.load('stand 1.png'), pygame.image.load('stand 2.png'),
                      pygame.image.load('stand 3.png'), pygame.image.load('stand 4.png'),
                      pygame.image.load('stand 3.png'), pygame.image.load('stand 2.png')]
        self.image = self.stand[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.i = 0
        self.dy = 0
        self.jumped = False

    def update(self, status):
        if not self.jumped:
            if status == 'walk_right':
                self.image = self.walk_right_gg[self.i]
                self.i += 1
                if self.i == len(self.walk_right_gg):
                    self.i = 0
                clock.tick(15)
            if status == 'walk_left':
                self.image = self.walk_left_gg[self.i]
                self.i += 1
                if self.i == len(self.walk_left_gg):
                    self.i = 0
                clock.tick(15)
            if status == 'simple_stand':
                if self.i >= len(self.stand):
                    self.i = 0
                self.image = self.stand[self.i]
                self.i += 1
                if self.i == len(self.stand):
                    self.i = 0
                clock.tick(4)
        if status == 'freeze':
            self.image = self.stand[0]
        # screen.blit(self.image, self.rect)

    def gravity_n_movement(self):

        delta_x = 0
        delta_y = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and not self.jumped:
            self.dy = -15
            signal = 'freeze'
            self.jumped = True
        elif key[pygame.K_SPACE]:
            self.jumped = False
            signal = 'freeze'

        if key[pygame.K_d]:
            delta_x += 10
            signal = "walk_right"
        if key[pygame.K_a]:
            delta_x -= 10
            signal = 'walk_left'
        else:
            signal = 'simple_stand'



        self.dy += 1
        if self.dy > 10:
            self.dy = 10
        delta_y += self.dy


        if self.rect.bottom > height:
            self.rect.bottom = height
        # self.update(signal)
        if self.rect.left < -130:
            self.rect.left = -130
        if self.rect.right > width + 130:
            self.rect.right = width + 130
        self.rect.x += delta_x
        self.rect.y += delta_y
        screen.blit(self.image, self.rect)


class World:
    def __init__(self, *group):
        super().__init__(*group)
        self.background1 = pygame.image.load('test background 2.2.jpg')
        self.background3 = pygame.image.load('test background 2.jpg')
        self.background2 = pygame.image.load("background city 1.png").convert()
        self.platform_im = pygame.image.load('platform 1.png').convert()
        self.platform_im.set_colorkey(pygame.Color('white'))
        self.platform_im2 = pygame.image.load('platform 2.png')
        self.platform_im2.set_colorkey(pygame.Color('white'))
        #  self.phone = False
        #  self.image_phone = pygame.image.load('ph.png')
        #  self.wire = False
        #  self.image_wire = pygame.image.load('')
        #  self.quest = False
        #  self.knife = False

    def lv0(self):
        screen.blit(self.background1, [0, 0])

    def lv1(self):
        screen.blit(self.background2, [0, 0])
        screen.blit(self.platform_im, [0, 0])
        screen.blit(self.platform_im2, [300, 150])

    def lv2(self):
        screen.blit(self.background3, [0, 0])


class DialogWindow:
    def __init__(self):
        self.window = pygame.image.load('win.png')
        self.font = pygame.font.SysFont(None, 30)
        self.replica = self.font.render('', False, (250, 250, 250))

    def talk(self, text=''):
        self.replica = self.font.render(text, False, (250, 250, 250))

    def unknown_func(self, poser):
        if poser:
            screen.blit(self.window, (0, 0))
            screen.blit(self.replica, (280, 550))
        if not poser:
            screen.blit(self.window, (0, 300))
            screen.blit(self.replica, (280, 850))


# заставка
# загрузка уровня
# загрузка спрайтов
# диалоговое окно
# реплики

start_screen()
level = World()
all_sprites = pygame.sprite.Group()
violett = Player(x=25, y=320)
all_sprites.add(violett)
dialog_window = DialogWindow()

test_text = ['Как-то раз я невзначай',
             'Сунул... а впрочем...',
             '']

while running:
    if violett.rect.x < 25 and level_number > 0:
        level_number -= 1
        violett.rect.x = 1100
    elif violett.rect.x > 1110 and level_number < 2:
        level_number += 1
        violett.rect.x = 35

    if level_number == 0:
        level.lv0()
    if level_number == 1:
        level.lv1()
    if level_number == 2:
        level.lv2()

    for event in pygame.event.get():
        # закрывашка
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_e]:
                flag_dialog = not flag_dialog  # == pose

            if not flag_dialog:
                if event.key in [pygame.K_l] and replica_num != len(test_text) - 1:
                    replica_num += 1
                if replica_num == len(test_text) - 1:
                    flag_dialog = False


    violett.gravity_n_movement()

    dialog_window.unknown_func(flag_dialog)
    if flag_dialog:
        dialog_window.talk(test_text[replica_num])
    pygame.display.update()
    clock.tick(fps)
