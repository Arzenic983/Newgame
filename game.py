import pygame
import sys

# все переменные писать в этот блок. Желательно.

size = width, height = 1280, 720
running = True
fps = 60
clock = pygame.time.Clock()
replica_num = 0
level_number = 0
flag_dialog = 0

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Игра.екзе')
    screen = pygame.display.set_mode(size)


    def terminate():
        pygame.quit()
        sys.exit()


    def start_screen():
        intro_text = ["ЗАСТАВКА", "",
                      "ТЕСТОВЫЙ ПРОБЕГ",
                      "!№;:?*()_+,",
                      "Для продолжения нажмите Enter"]

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
            for eevent in pygame.event.get():
                if eevent.type == pygame.QUIT:
                    terminate()
                elif eevent.type == pygame.KEYDOWN or \
                        eevent.type == pygame.MOUSEBUTTONDOWN:
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
                              pygame.image.load('sprites walk 2.png')]
        self.walk_left_gg = [pygame.image.load('sp w left 1.png'), pygame.image.load('sp w left 2.png'),
                             pygame.image.load('sp w left 2-3.png'), pygame.image.load('sp w left 3.png'),
                             pygame.image.load('sp w left 4.png'),
                             pygame.image.load('sp w left 5.png'), pygame.image.load('sp w left 4.png'),
                             pygame.image.load('sp w left 3.png'), pygame.image.load('sp w left 2-3.png'),
                             pygame.image.load('sp w left 2.png')]
        self.stand = [pygame.image.load('stand 1.png'), pygame.image.load('stand 2.png'),
                      pygame.image.load('stand 3.png'), pygame.image.load('stand 4.png'),
                      pygame.image.load('stand 3.png'), pygame.image.load('stand 2.png')]
        self.image = self.stand[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.index_right = 0
        self.i = 0
        self.index_left = 0
        self.counter = 0
        self.speed_y = 0
        self.timer = 0
        self.step = 2.5
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.jumped = False

    def update(self):
        delta_x = 0
        delta_y = 0
        walk_cooldown = 6
        wait_cooldown = 15

        key = pygame.key.get_pressed()
        # jump
        if key[pygame.K_SPACE] and not self.jumped:
            self.speed_y = -20
            self.jumped = True
        if not key[pygame.K_SPACE]:
            self.jumped = False
        if self.jumped:
            self.step = 10
        else:
            self.step = 3
        # move & animate
        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            delta_x += self.step
            self.counter += 1
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index_right += 1
                if self.index_right >= len(self.walk_right_gg):
                    self.index_right = 0
                self.image = self.walk_right_gg[self.index_right]
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            delta_x -= self.step
            self.counter += 1
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index_left += 1
                if self.index_left >= len(self.walk_left_gg):
                    self.index_left = 0
                self.image = self.walk_left_gg[self.index_left]
        if not key[pygame.K_a] and not key[pygame.K_d]:
            self.timer += 1
            if self.timer > wait_cooldown:
                self.timer = 0
                self.i += 1
                if self.i >= len(self.stand):
                    self.i = 0
                self.image = self.stand[self.i]

        # phys
        self.speed_y += 1
        if self.speed_y > 10:
            self.speed_y = 10
        delta_y += self.speed_y

        # collision check

        for platform in level.platforms:
            # ycoord check
            if platform.colliderect(self.rect.x, self.rect.y + delta_y, self.width, self.height):
                # underground check - jumping
                if self.speed_y < 0:
                    delta_y = platform.bottom - self.rect.top
                # high ground check - falling
                elif self.speed_y >= 0:
                    delta_y = platform.top - self.rect.bottom

        # update coordinates


        if self.rect.left < -130:
            self.rect.left = -130
        if self.rect.right > width + 130:
            self.rect.right = width + 130
        self.rect.x += delta_x
        self.rect.y += delta_y

        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)


class World:
    def __init__(self, *group):
        super().__init__(*group)
        self.background1 = pygame.image.load('backs0.png')
        self.background3 = pygame.image.load('backs 1.png')
        self.background2 = pygame.image.load("background city 1.png")
        self.platform_im1 = pygame.image.load('plat1.png')
        self.platform_im2_1 = pygame.image.load('plat2.png')
        self.platform_im2_2 = pygame.image.load('plat2-2.png')
        self.platform_im3 = pygame.image.load('plat3.png')
        self.prep = pygame.image.load('prep.png')
        self.platforms = [self.platform_im1.get_rect(), self.platform_im2_1.get_rect(),
                          self.platform_im2_2.get_rect(), self.platform_im3.get_rect()]

    def lv0(self):
        screen.blit(self.background1, [0, 0])
        screen.blit(self.platform_im1, [0, 642])
        screen.blit(self.prep, [825, 484])

    def lv1(self):
        screen.blit(self.background2, [0, 0])
        screen.blit(self.platform_im2_1, [0, 660])
        screen.blit(self.platform_im2_2, [1051, 430])

    def lv2(self):
        screen.blit(self.background3, [0, 0])
        screen.blit(self.platform_im3, [0, 660])


class Items:
    def __init__(self, *group):
        super().__init__(*group)
        self.corpses = pygame.image.load('tr.png')
        self.corpses_rect = self.corpses.get_rect()
        self.corpses_rect = self.corpses_rect.move(0, 560)

        self.charley = pygame.image.load('charley.png')
        self.charley_rect = self.charley.get_rect()
        self.charley_rect = self.charley_rect.move(310, 645)

        self.wire_it = False
        self.wire = pygame.image.load('wire.png')
        self.wire_rect = self.wire.get_rect()
        self.wire_rect = self.wire_rect.move(745, 640)

        self.door = [pygame.image.load('door .png'), pygame.image.load('door open.png')]
        self.door_it = False
        self.door_rect = self.door[0].get_rect()
        self.door_rect = self.door_rect.move(887, 188)

        self.table_it = False
        self.table = [pygame.image.load('table error.png'), pygame.image.load('table complete.png')]
        self.table_rect = self.table[0].get_rect()
        self.table_rect = self.table_rect.move(588, 302)

        self.oy_ = True

        self.box_it = False
        self.box = [pygame.image.load('it is yep error.png'), pygame.image.load('it is yep complete.png')]
        self.box_rect = self.box[0].get_rect()
        self.box_rect = self.box_rect.move(810, 250)

    def location1(self):
        screen.blit(self.charley, [310, 645])
        screen.blit(self.corpses, [0, 560])
        if not self.wire_it:
            screen.blit(self.wire, [745, 640])

    def location2(self):
        pass

    def location3(self):
        if self.table_it:
            screen.blit(self.table[1], [588, 302])
        else:
            screen.blit(self.table[0], [588, 302])

        if self.box_it:
            screen.blit(self.box[1], [810, 250])
        else:
            screen.blit(self.box[0], [810, 250])

        if self.door_it:
            screen.blit(self.door[1], [887, 188])  # тут должна быть анимация, но её пока не будет
        else:
            screen.blit(self.door[0], [887, 188])

    def click(self, mouse_coordinates, location):  # то, где всё клацается
        if location == 0:
            if self.corpses_rect.collidepoint(mouse_coordinates):
                return ['хм...', 'Как странно...Они должны защищать местных',
                        'Но получилось так, что они защищают ОТ местных'
                        '...',
                        'Подонки.', 'Легли под пиджаков, которые нам все входы и выходы перекрыли...',
                        'А сами купаются в роскоши...', 'Как и всегда это делали.',
                        'Так что удивляться тут нечему, надо двигаться дальше']
            if self.charley_rect.collidepoint(mouse_coordinates):
                if self.door_it:
                    return ['Держись, дружище...', '...', 'Я доведу наше дело до конца...', 'end']
                else:
                    return ['Эх, Чарли-Чарли...', 'Будь бы ты сейчас жив, Чарли....', 'хах', '.....']
            if self.wire_rect.collidepoint(mouse_coordinates):
                if not self.wire_it:
                    self.wire_it = True
                    return ['Просто лежащий провод...',
                            'ПЭС-330ВвМ, "Фуджитсу Электроникс", тройная оплётка...',
                            'Думаю, его стоит подобрать...']
                else:
                    return ['...']
            else:
                return ['...']
        if location == 1:
            return ['...']
        if location == 2:
            if self.door_rect.collidepoint(mouse_coordinates):
                if self.table_it and not self.door_it:
                    self.door_it = True
                    return ['A что, если....']
                if self.door_it:
                    return ['Она открылась. Оттуда исходит свет...',
                            '''Забавно...За этот короткий промежуток времени я уже успел от него отвыкнуть''',
                            'Надо сходить к Чарли и сделать то, о чём он меня просил']
                else:
                    return ['Дверь, ведущая к выходу...', 'Но хотелось бы видеть её открытой']

            if self.table_rect.collidepoint(mouse_coordinates):
                if self.table_it:
                    return ['Генератор...', 'Судя по индикаторам, сейчас всё в порядке... ну кроме одного...',
                            'Когда это всё закончится, устроюсь в "Юнайтед Пауерс" электриком на радостях, хах']
                else:
                    return ['Тут точно рядом есть щиток... А это, должно быть, генератор',
                            'С ним всё в порядке, а вот с щитком лифта лифтом проблемы...',
                            'Ибо все индикаторы красные']
            if self.box_rect.collidepoint(mouse_coordinates):
                if self.oy_:
                    self.oy_ = False
                    return ['Надо рассмотреть это получше']

                if not self.box_it:
                    if self.wire_it:
                        self.box_it = True
                        self.table_it = True
                        return ['Проклятье', 'Щиток "Юнайтедов"... провод - "Фуджитсу"',
                                'Хуже я уже точно не сделаю...']

                    else:
                        return ['Панель управления лифтом. Разбита...',
                                '''Надеюсь, они не додумались вывести сам лифт из строя''']
                else:
                    return ['Отныне я электрик...', 'Довольно странно, что они выдрали провод, а не просто выстрелили',
                            'Мы так несколько пути этим мразям перекрыли...' 'Хах....']
            else:
                return ['Тут ничего нет, лол']


class DialogWindow:
    def __init__(self):
        self.window = pygame.image.load('win.png')
        self.speaker_im = False
        self.font = pygame.font.SysFont(None, 30)
        self.font_name = pygame.font.SysFont(None, 33)
        self.replica = self.font.render('', False, (250, 250, 250))
        self.speaker = self.font_name.render(' ', False, (250, 250, 250))

    def talk(self, who=' ', text=''):
        self.speaker = self.font_name.render(who, False, ((201, 160, 220) if who == 'Вайлет' else (250, 250, 250)))
        if who == 'Вайлет':
            self.speaker_im = pygame.image.load('win_vi.png')
        self.replica = self.font.render(text, False, (250, 250, 250))

    def unknown_func(self, poser):
        if poser:
            screen.blit(self.window, (15, 495))
            screen.blit(self.speaker, (290, 550))
            if self.speaker_im:
                screen.blit(self.speaker_im, (96, 532))
            screen.blit(self.replica, (290, 585))
        if not poser:
            screen.blit(self.window, (15, 800))
            if self.speaker_im:
                screen.blit(self.speaker_im, (20, 800))
            screen.blit(self.speaker, (290, 850))
            screen.blit(self.replica, (280, 850))


# заставка
# загрузка уровня
# загрузка спрайтов
# диалоговое окно
# реплики
items = Items()
start_screen()
level = World()
all_sprites = pygame.sprite.Group()
violett = Player(x=25, y=height - 70)
all_sprites.add(violett)
dialog_window = DialogWindow()
items_text = False
default_text = ['...']
test_text = ['Как-то раз я невзначай',
             'Сунул... а впрочем...',
             '']
result = '...'
forbidden_words = ('...', 'Тут ничего нет, лол',
                   'Заче-...ладно')
end = False  # переменная, которая подводит к концу игры. Она объвит функцию с титрами (да и не только)
#  Появляется после выполнения всех заданий, когда Вайлет подходит к трупу
while running:
    clock.tick(fps)
    if violett.rect.x < 25 and level_number > 0:
        level_number -= 1
        violett.rect.x = 1100
    elif violett.rect.x > 1110 and level_number < 2:
        level_number += 1
        violett.rect.x = 35

    if level_number == 0:
        level.lv0()
        items.location1()
    if level_number == 1:
        level.lv1()
    if level_number == 2:
        level.lv2()
        items.location3()
    for event in pygame.event.get():
        # закрывашка
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if flag_dialog:
                if event.button == 3 and replica_num < len(default_text):
                    replica_num += 1
                if event.button == 2 and replica_num > 0:
                    replica_num -= 1
                if replica_num == len(default_text):
                    replica_num = 0
                    flag_dialog = False
                if items_text:
                    items_text = False

        elif event.type == pygame.MOUSEBUTTONUP and not flag_dialog and event.button == 1:
            mouse_position = pygame.mouse.get_pos()
            result = items.click(mouse_position, level_number)
            if result[-1] == 'end':
                result = result[:-1]
                end = True
            flag_dialog = True
            items_text = True
            default_text = result
            result = '...'

    if not items_text and flag_dialog == 0:
        default_text = test_text
    violett.update()

    dialog_window.unknown_func(flag_dialog)
    if flag_dialog:
        dialog_window.talk('Вайлет', default_text[replica_num])

    pygame.display.update()
