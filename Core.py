import pygame
import sys

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Игра.екзе')
    size = width, height = 1600, 900
    screen = pygame.display.set_mode(size)

    # все переменные писать в этот блок. Желательно.

    running = True
    fps = 144
    clock = pygame.time.Clock()
    step = 2

    # заставочка

    def terminate():
        pygame.quit()
        sys.exit()


    def start_screen():
        intro_text = ["ЗАСТАВКА", "",
                      "ТЕСТОВЫЙ ПРОБЕГ",
                      "!№;:?*()_+,",
                      "Для продолжения нажмите любую клавишу"]

        screen.fill((0, 0, 255))
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

    background_image = pygame.image.load("test background 2.jpg").convert()

    # персонаж

    player_image = pygame.image.load("player.png").convert()
    player_image.set_colorkey(pygame.Color('white'))
    pers_x = 25
    pers_y = 820

    # а тут совмещаем все картинки. ПОРЯДОК ВАЖЕН!!!

    screen.blit(background_image, [0, 0])
    screen.blit(player_image, [pers_x, pers_y])

    while running:
        # чек ивенты
        for event in pygame.event.get():
            # закрывашка
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # лево-право

        if keys[pygame.K_d]:
            pers_x += step if pers_x < 1500 else 0
        if keys[pygame.K_a]:
            pers_x -= step if 0 < pers_x else 0
        screen.blit(background_image, [0, 0])
        screen.blit(player_image, [pers_x, pers_y])

        pygame.display.flip()
        clock.tick(fps)

pygame.quit()
