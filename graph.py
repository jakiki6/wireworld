import pygame, random
from ww import *

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Roboto', 16)

height, width = pygame.display.Info().current_h, pygame.display.Info().current_w
tile_size = 5
colors = [
    (0, 0, 0),
    (255, 0, 0),
    (127, 127, 255),
    (255, 255, 0)
]

screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

for y in range(0, height):
    for x in range(0, width):
        screen.set_at((x, y), colors[get_at(x, y)])

pygame.display.flip()

clock = pygame.time.Clock()

paused = True
speed = False
stepping = False
gui = True

keys = {"e": False, "w": False, "s": False, "a": False, "d": False}
gx, gy = -100, -100
SPEED = 5
next_table = (2, 3, 1)
e_to = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_q:
                speed = not speed
            elif event.key == pygame.K_ESCAPE:
                exit(0)
            elif event.key == pygame.K_e:
                keys["e"] = True
            elif event.key == pygame.K_w:
                keys["w"] = True
            elif event.key == pygame.K_s:
                keys["s"] = True
            elif event.key == pygame.K_a:
                keys["a"] = True
            elif event.key == pygame.K_d:
                keys["d"] = True
            elif event.key == pygame.K_LSHIFT:
                SPEED *= 3
            elif event.key == pygame.K_c:
                save()
            elif event.key == pygame.K_r:
                undo()
            elif event.key == pygame.K_F1:
                gui = not gui
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_e:
                keys["e"] = False
            elif event.key == pygame.K_w:
                keys["w"] = False
            elif event.key == pygame.K_s:
                keys["s"] = False
            elif event.key == pygame.K_a:
                keys["a"] = False
            elif event.key == pygame.K_d:
                keys["d"] = False
            elif event.key == pygame.K_LSHIFT:
                SPEED //= 3
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                tile_size += 1
            elif event.button == 5:
                tile_size -= 1
            elif event.button == 1:
                mx, my = pygame.mouse.get_pos()
                x = (mx + gx) // tile_size
                y = (my + gy) // tile_size

                if get_at(x, y):
                    set_at(x, y, 0)
                else:
                    set_at(x, y, 3)
            elif event.button == 3:
                mx, my = pygame.mouse.get_pos()
                x = (mx + gx) // tile_size
                y = (my + gy) // tile_size

                if get_at(x, y) != 0:
                    set_at(x, y, next_table[get_at(x, y) - 1])

            if tile_size < 1:
                tile_size = 1
            elif tile_size > 100:
                tile_size = 100

    if keys["e"]:
        stepping = True
        paused = False
        speed = False
    elif e_to:
        stepping = False
        paused = True
        speed = False

    if keys["w"]:
        gy -= SPEED
    if keys["s"]:
        gy += SPEED
    if keys["a"]:
        gx -= SPEED
    if keys["d"]:
        gx += SPEED

    if stepping:
        e_to += 1

        if e_to == 1:
            paused = False
        elif e_to < 20:
            paused = True
        else:
            paused = False
    else:
        e_to = 0

    if not paused:
        tick()

    screen.fill((0, 0, 0))
    for pos, val in get_wmap().items():
        ex, ey = pos[0] * tile_size - gx, pos[1] * tile_size - gy

        if -tile_size < ex <= width and -tile_size < ey <= height:
            for oy in range(0, tile_size):
                for ox in range(0, tile_size):
                    screen.set_at((ex + ox, ey + oy), colors[val])

    if gui:
        screen.blit(font.render(f"FPS: {clock.get_fps() * 10 // 1 / 10}", True, (255, 255, 255)), (0, 0))
        screen.blit(font.render(f"Pos: {(gx + width // 2) // tile_size} {(gy + height // 2) // tile_size}", True, (255, 255, 255)), (0, 16))

        for y in range(height // 2 - 5, height // 2 + 6):
            screen.set_at((width // 2, y), (127, 127, 127))

        for x in range(width // 2 - 5, width // 2 + 6):
                screen.set_at((x, height // 2), (127, 127, 127))

    pygame.display.flip()

    if not speed:
        clock.tick(60)
