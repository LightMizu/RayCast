from typing import List, Tuple

import pygame as pg
from dataclasses import dataclass, field
import math


@dataclass
class Point:
    x: float
    y: float


@dataclass
class Rectangle:
    pos: Point = field(init=True)
    h: int = field(init=True)
    w: int = field(init=True)
    rect: pg.Rect = field(init=False)

    def __post_init__(self):
        self.rect = pg.Rect(self.pos.x, self.pos.y, self.w, self.h)


class Camera:
    pos: Point
    yaw: float
    fov: int
    renderDistance: int

    def __init__(self, x: int = 0, y: int = 0, fov: int = 100, render_distance: int = 200) -> None:
        self.pos = Point(x, y)
        self.fov = fov
        self.renderDistance = render_distance
        self.yaw = 0

    def __str__(self) -> str:
        return f"Camera {self.pos.x} {self.pos.y} {self.yaw}"

    def get_intersection(self, objects: list[Rectangle]) -> list[tuple[Point, int, float]]:
        answer: list[tuple[Point, int, float]] = []
        x = 0
        start_angle = self.yaw - self.fov // 2
        end_angle = self.yaw + self.fov // 2
        angle = start_angle
        while angle <= end_angle:
            if x == 1:
                x = 0
                continue
            for distance in range(0, self.renderDistance):
                if x == 1:
                    break
                x = cos(angle) * distance + self.pos.x
                y = sin(angle) * distance + self.pos.y
                for object in objects:
                    if object.rect.collidepoint(x, y):
                        if angle < 0:
                            angle = 360 + angle
                        distance *= cos(self.yaw - angle)
                        answer.append((Point(x, y), distance, angle - self.yaw + self.fov // 2))
                        x = 1
                        break
            angle += 70/200

        return answer

    def set_yaw(self, angle: float):
        if angle < 0:
            self.yaw = 360 + angle
        else:
            self.yaw = angle
        if self.yaw == 360:
            self.yaw = 0

    def add_vector(self, vector: Tuple[float, float]):
        self.pos = Point(self.pos.x + vector[0], self.pos.y + vector[1])


def cos(angle: float) -> float:
    return math.cos(math.radians(angle))


def sin(angle: float) -> float:
    return math.sin(math.radians(angle))


def get_angle(point: Point) -> int:
    pos: tuple[int, int] = pg.mouse.get_pos()
    return round(math.degrees(math.atan2(point.x - pos[0], pos[1] - point.y))) + 90
