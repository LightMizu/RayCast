import pygame.event
import shutil
from pygame.locals import *
import os
from pygame import gfxdraw
from service import *


def add_vector(vec1, vec2):
    return vec1[0] + vec2[0], vec1[1] + vec2[1]


def update(camera: Camera, objects: list[Rectangle]) -> list[tuple[Point, int, float]]:
    pygame.event.set_grab(True)
    points = camera.get_intersection(objects)
    points.sort(key=lambda x: x[1])
    for event in pg.event.get():
        if event.type == MOUSEMOTION:
            rel = pg.mouse.get_rel()
            pygame.mouse.set_pos((640 // 2, 480 // 2))
            sens = 2.1
            camera.set_yaw(camera.yaw - rel[0] / 10 * sens)
        if event.type == QUIT:
            pg.quit()
            exit()
    speed = 500
    direction = (cos(camera.yaw), sin(camera.yaw))
    keys = pg.key.get_pressed()
    move = (0, 0)
    if keys[pg.K_w]:
        move = add_vector(move, (direction[0], direction[1]))
    if keys[pg.K_s]:
        move = add_vector(move, (-direction[0], -direction[1]))
    if keys[pg.K_d]:
        move = add_vector(move, (direction[1], -direction[0]))
    if keys[pg.K_a]:
        move = add_vector(move, (-direction[1], direction[0]))
    if keys[pg.K_ESCAPE]:
        pg.quit()
        exit()
    leng = (move[0] ** 2 + move[1] ** 2) ** 0.5
    if leng != 0:
        move = (move[0]*speed / (leng*100), move[1]*speed / (leng*100))
        camera.add_vector(move)
    print()

    return points


def draw(screen: pg.Surface, points: list[tuple[Point, float, tuple[int, int, int]]]) -> None:
    screen.fill((0, 0, 0))
    points.sort(key=lambda x: x[2][0])
    for point in points:
        pg.draw.rect(screen, point[2], pg.Rect(point[0].x - 5, point[0].y - point[1] // 2, 5, point[1]))
    pg.display.flip()


def runGame() -> None:
    pg.init()
    pygame.mouse.set_visible(False)

    fps = 0
    fpsClock = pg.time.Clock()
    width, height = 640, 480
    fov = 70
    screen_height = int((width / 2) / math.tan(math.radians(fov // 2)))
    screen = pg.display.set_mode((width, height))

    camera: Camera = Camera(width // 2, height // 2, render_distance=255, fov=fov)
    rect: Rectangle = Rectangle(Point(90, 90), 90, 90)
    rect1: Rectangle = Rectangle(Point(180, 180), 90, 90)
    objects = [rect, rect1]
    os.system("cls")
    fpss = 0
    n = 1
    while True:
        points = update(camera, objects)
        new_points = []
        for point in points:
            angle = point[2]
            dist = point[1]
            pos = point[0]
            pg.draw.circle(screen, (255, 0, 0), (pos.x, pos.y), 2)
            angle = fov // 2 - angle
            line = math.tan(math.radians(angle)) * screen_height
            x = (width / 2 + line)
            sat = int(-1.275 * dist + 255)
            sat = min(sat, 255)
            sat = max(0, sat)
            color = (1 * sat, 1 * sat, 1 * sat)
            try:
                project_height = (screen_height * 100) / dist
            except ZeroDivisionError:
                camera.pos = Point(0, 0)
                text = "Death"
                os.system("cls")
                print(text.center(shutil.get_terminal_size().columns, '-'))
                break

            new_points.append((Point(x, height / 2), project_height, color))

        draw(screen, new_points)
        ms = fpsClock.tick(fps)
        try:
            pg.display.set_caption(f"FPS: {1000/ms:.1f}, AVG FPS: {fpss/n:.1f}")
            fpss += 1000/ms
            n += 1
        except ZeroDivisionError:
            pg.display.set_caption(f"FPS: inf")


if __name__ == "__main__":
    runGame()
