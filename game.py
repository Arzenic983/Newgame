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
        screen.blit(self.image, self.rect)

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

        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            delta_x += 10
            signal = 'walk_right'
        elif key[pygame.K_a] or key[pygame.K_LEFT]:
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
        self.update(signal)
        if self.rect.left < -130:
            self.rect.left = -130
        if self.rect.right > width + 130:
            self.rect.right = width + 130
        self.rect.x += delta_x
        self.rect.y += delta_y
        #  screen.blit(self.image, self.rect)


class World:
    def __init__(self, *group):
        super().__init__(*group)
        self.background1 = pygame.image.load('backs0.png')
        self.background3 = pygame.image.load('backs 1.png')
        self.background2 = pygame.image.load("background city 1.png").convert()
        self.platform_im = pygame.image.load('platform 1.png').convert()
        self.platform_im.set_colorkey(pygame.Color('white'))
        self.platform_im2 = pygame.image.load('platform 2.png')
        self.platform_im2.set_colorkey(pygame.Color('white'))

        self.prep = pygame.image.load('prep.png')

    def lv0(self):
        screen.blit(self.background1, [0, 0])
        screen.blit(self.prep, [825, 484])

    def lv1(self):
        screen.blit(self.background2, [0, 0])
        screen.blit(self.platform_im, [0, 0])
        screen.blit(self.platform_im2, [300, 150])

    def lv2(self):
        screen.blit(self.background3, [0, 0])


class Items():
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
        if self.wire_it == False:
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
                return ['...', 'Как странно...Они должны защищать местных', 'Но получилось так, что они их убивают...',
                        'Подонки.', 'Легли под шишек свыше, которые нам все входы и выходы перекрыли...',
                        'И радуются...', 'Как и всегда это делали.', 'Не суть']
            if self.charley_rect.collidepoint(mouse_coordinates):
                if self.door_it:
                    return ['Держись, друг...', '...', 'Я доведу наше дело до конца...', 'end']
                else:
                    return ['...', 'Будь бы ты сейчас жив, Чарли....', 'хах', '.....']
            if self.wire_rect.collidepoint(mouse_coordinates):
                if self.wire_it == False:
                    self.wire_it = True
                    return ['Просто лежащий провод...', 'Думаю, его стоит подобрать...']
            else:
                return ['...']
        if location == 2:
            if self.door_rect.collidepoint(mouse_coordinates):
                if self.table_it and self.door_it == False:
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
                    return ['Панель состояния...', 'Судя по ней, сейчас всё в порядке, кроме одного блока...',
                            'Когда это всё закончится, стану электриком, хах']
                else:
                    return ['Тут рядом где-то энергоблок...Должно быть, это панель состояния всей системы',
                            'С ним всё в порядке, а вот с лифтом проблемы...',
                            'Ибо она ничего хорошего не показывает']
            if self.box_rect.collidepoint(mouse_coordinates):
                if self.oy_:
                    self.oy_ = False
                    return ['....']

                if self.box_it == False:
                    if self.wire_it:
                        self.box_it = True
                        self.table_it = True
                        return ['...', 'Я редко раньше работал с проводами...', 'Но я попробую...']

                    else:
                        return ['Разодранная панель для вызова лифта...', '''Надеюсь, они не додумались вывести сам лифт 
                    из строя''']
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
violett = Player(x=25, y=320)
all_sprites.add(violett)
dialog_window = DialogWindow()
items_text = False
defolt_text = ['...']
test_text = ['Как-то раз я невзначай',
             'Сунул... а впрочем...',
             '']
result = '...'
forbidden_words = ('...', 'Тут ничего нет, лол',
                   'Заче-...ладно')
end = False  # переменная, которая подводит к концу игры. Она объвит функцию с титрами (да и не только)
#  Появляется после выполнения всех заданий, когда Вайлет подходит к трупу
while running:
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
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_e]:
                flag_dialog = not flag_dialog  # == pose

            if flag_dialog:
                if event.key in [pygame.K_l] and replica_num < len(defolt_text):
                    replica_num += 1
                if event.key in [pygame.K_j] and replica_num > 0:
                    replica_num -= 1
                if replica_num == len(defolt_text):
                    replica_num = 0
                    flag_dialog = False
                if items_text:
                    items_text = False

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_position = pygame.mouse.get_pos()
            result = items.click(mouse_position, level_number)
            if result[-1] == 'end':
                result = result[:-1]
                end = True
            flag_dialog = True
            items_text = True
            defolt_text = result
            result = '...'

    if items_text == False and flag_dialog == 0:
        defolt_text = test_text
    violett.gravity_n_movement()

    dialog_window.unknown_func(flag_dialog)
    if flag_dialog:
        dialog_window.talk('Вайлет', defolt_text[replica_num])

    pygame.display.update()
    clock.tick(fps)
