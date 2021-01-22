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
    while running:
        # бэкграунд

        background_image = pygame.image.load("test background 2.jpg").convert()

        # прикрепляем перса

        player_position = pygame.mouse.get_pos()
        x = player_position[0]
        y = player_position[1]
        player_image = pygame.image.load("player.png").convert()
        player_image.set_colorkey(pygame.Color('white'))

        # а тут совмещаем все холсты. ПОРЯДОК ВАЖЕН!!!

        screen.blit(background_image, [0, 0])
        screen.blit(player_image, [x, y])

        # чек ивенты
        for event in pygame.event.get():
            # закрывашка
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(fps)

pygame.quit()
