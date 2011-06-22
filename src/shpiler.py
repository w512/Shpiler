#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Shpiler - simple cool game
'''

__author__ = 'Nikolay Blohin (nikolay@blohin.org)'
__version__ = '0.0.2'
__copyright__ = 'Copyright (c) 2011 Nikolay Blohin'
__license__ = 'GNU General Public License'

# import sys
# import os
import random
import pyglet
import cocos
from cocos.actions import *


class Cursor(cocos.layer.ColorLayer):

    is_event_handler = True

    def __init__(self):
        super(Cursor, self).__init__(250, 255, 250, 255)
        self.run_status = False # if false - stop, if true - run
        self.direction = 1      # 1 - North, 2 - East, 3 - South, 4 - West
        self.m_s = 3            # step for move
        self.m_d = 0.01         # duration for move
        self.score = 0          # player's score

        self.win_width, self.win_height = cocos.director.director.get_window_size()

        self.label = cocos.text.Label('Score: 0',
                          font_name='Times New Roman',
                          font_size=16,
                          color=(0, 0, 0, 200),
                          x=3,
                          y=self.win_height-20)


        self.sprite = cocos.sprite.Sprite('cursor.png')
        self.sprite_2 = cocos.sprite.Sprite('target.png')
        self.enemy = cocos.sprite.Sprite('sport_8ball.png')

        x = int(self.win_width/2)
        y = 8
        self.sprite.position = x, y

        x = random.randrange(10, self.win_width-10)
        y = random.randrange(30, self.win_height-10)
        self.sprite_2.position = x, y

        x = random.randrange(10, self.win_width-10)
        y = random.randrange(10, self.win_height-10)
        self.enemy.position = x, y

        self.add(self.sprite)
        self.add(self.sprite_2)
        self.add(self.enemy)
        self.add(self.label)

        self.schedule(self.update)
        self.schedule_interval(self.move_target, 3)
        self.schedule_interval(self.move_enemy, 3)


    def on_key_press(self, key, modifiers):
        """This function is called when a key is pressed."""
        repeat_left = Repeat(MoveBy((-1*self.m_s, 0), duration=self.m_d))
        repeat_up = Repeat(MoveBy((0, self.m_s), duration=self.m_d))
        repeat_right = Repeat(MoveBy((self.m_s, 0), duration=self.m_d))
        repeat_down = Repeat(MoveBy((0, -1*self.m_s), duration=self.m_d))
        if key==65361:
            self.sprite.do(repeat_left)
            self.direction = 4
        elif key==65362:
            self.sprite.do(repeat_up)
            self.direction = 1
        elif key==65363:
            self.sprite.do(repeat_right)
            self.direction = 2
        elif key==65364:
            self.sprite.do(repeat_down)
            self.direction = 3
        elif key==32:
            self.sprite.stop()

    def move_target(self, *args, **kwargs):
        x = random.randrange(10, self.win_width-10)
        y = random.randrange(10, self.win_height-10)
        self.sprite_2.do(MoveTo((x, y), duration=3.5))

    def move_enemy(self, *args, **kwargs):
        x = random.randrange(10, self.win_width-10)
        y = random.randrange(10, self.win_height-10)
        self.enemy.do(MoveTo((x, y), duration=3.5))

    def update(self, *args, **kwargs):
        x = self.sprite.x
        y = self.sprite.y
        # check borders
        if self.sprite.contains(1, y) and self.direction==4:
            self.sprite.stop()
        elif self.sprite.contains(self.win_width-1, y) and self.direction==2:
            self.sprite.stop()
        elif self.sprite.contains(x, 1) and self.direction==3:
            self.sprite.stop()
        elif self.sprite.contains(x, self.win_height-1) and self.direction==1:
            self.sprite.stop()

        # check target
        x = self.sprite_2.x
        y = self.sprite_2.y
        if self.sprite.contains(x, y):
            self.score += 1
            self.label.element.text = 'Score: %s' % self.score
            self.move_target()

        x = self.enemy.x
        y = self.enemy.y
        if self.sprite.contains(x, y):
            self.score -= 1
            self.label.element.text = 'Score: %s' % self.score
            self.move_enemy()


if __name__=="__main__":
    cocos.director.director.init(caption='Shpiler')
    main_scene = cocos.scene.Scene(Cursor())
    cocos.director.director.run(main_scene)

