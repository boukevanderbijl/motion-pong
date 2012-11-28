# -*- coding: utf-8 -*-

from Box2D import *
import pygame

import random
import util


class Paddle(object):

    HEIGHT = 4.0
    WIDTH = 0.2

    def __init__(self, screen, x):
        self.screen = screen
        self.body = screen.world.CreateKinematicBody(position=(x, screen.HEIGHT/2 - self.HEIGHT/2))
        self.body.CreatePolygonFixture(box=(self.WIDTH/2, self.HEIGHT/2), friction=0.1, restitution=1.1, density=1.0)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 255), self.screen.translate_xy_width_height(self.body.position[0] - self.WIDTH/2, self.body.position[1] - self.HEIGHT/2, self.WIDTH, self.HEIGHT))


class Ball(object):

    # Official ping pong ball size 40 mm
    RADIUS = 0.5
    STARTING_VELOCITY = b2Vec2(10, 10)

    def __init__(self, screen, x, y):
        self.screen = screen
        self.body = screen.world.CreateDynamicBody(position=(x, y), bullet=True)
        self.body.CreateCircleFixture(radius=self.RADIUS, friction=0.1, restitution=1.0, density=2.0)
        self.body.ApplyLinearImpulse(self.STARTING_VELOCITY, self.body.worldCenter)

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), self.screen.translatexy(self.body.position[0], self.body.position[1]), self.screen.translate(self.RADIUS))

    def get_rect(self):
        return ((self.body.position[0] - self.RADIUS, self.body.position[1] - self.RADIUS), (self.RADIUS*2, self.RADIUS*2))

    def tick(self, time_passed):
        if self.body.position[0] - self.RADIUS > self.screen.WIDTH or self.body.position[0] + self.RADIUS < 0:
            self.body.transform = (b2Vec2(self.screen.WIDTH/2, self.screen.HEIGHT/2), 0)
            self.body.linearVelocity = b2Vec2(0, 0)
            self.body.ApplyLinearImpulse(self.STARTING_VELOCITY, self.body.worldCenter)