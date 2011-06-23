#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Shpiler - simple cool game
'''

__author__ = 'Nikolay Blohin (nikolay@blohin.org)'
__version__ = '0.1.0'
__copyright__ = 'Copyright (c) 2011 Nikolay Blohin'
__license__ = 'GNU General Public License'


import random
import pyglet
from pyglet.window import key as KEYS
import cocos
from cocos.actions import *
from cocos.director import director


SCORE_FOR_LEVEL = 5
LEVEL = 1



class Game(cocos.layer.ColorLayer):

    is_event_handler = True

    def __init__(self):
        super(Game, self).__init__(250, 255, 250, 255)
        self.run_status = False # if false - stop, if true - run
        self.direction = 1      # 1 - Up, 2 - Right, 3 - Down, 4 - Left
        self.m_s = 3            # step for move
        self.m_d = 0.01         # duration for move
        self.score = 0          # player's score
        self.attackers = []     # list of all attacking
        self.life = 5           # life of player

        self.win_width, self.win_height = cocos.director.director.get_window_size()

        self.label_score = cocos.text.Label('Score: 0',
                          font_size=14,
                          color=(0, 0, 100, 200),
                          x=3,
                          y=self.win_height-22)
        self.label_level = cocos.text.Label('Level: 1',
                          font_size=14,
                          color=(0, 100, 0, 200),
                          x=3,
                          y=self.win_height-42)        
        self.label_life = cocos.text.Label('Life: 3',
                          font_size=14,
                          color=(100, 0, 0, 200),
                          x=3,
                          y=self.win_height-62)

        self.sprite_player = cocos.sprite.Sprite('cursor.png')
        self.sprite_target = cocos.sprite.Sprite('target.png')
        x = int(self.win_width/2)
        y = 8
        self.sprite_player.position = x, y

        x = random.randrange(10, self.win_width-10)
        y = random.randrange(30, self.win_height-10)
        self.sprite_target.position = x, y

        self.add(self.sprite_player)        
        self.add(self.sprite_target)
        self.add(self.label_score)
        self.add(self.label_level)
        self.add(self.label_life)
        
        self.schedule(self.update)
        self.schedule_interval(self.move_target, 3)
        self.schedule_interval(self.move_attackers, 2.4)
        

    def on_key_press(self, key, modifiers):
        """This function is called when a key is pressed."""
        repeat_left = Repeat(MoveBy((-1*self.m_s, 0), duration=self.m_d))
        repeat_up = Repeat(MoveBy((0, self.m_s), duration=self.m_d))
        repeat_right = Repeat(MoveBy((self.m_s, 0), duration=self.m_d))
        repeat_down = Repeat(MoveBy((0, -1*self.m_s), duration=self.m_d))
        if key==KEYS.LEFT:
            self.sprite_player.do(repeat_left)
            self.direction = 4
        elif key==KEYS.UP:
            self.sprite_player.do(repeat_up)
            self.direction = 1
        elif key==KEYS.RIGHT:
            self.sprite_player.do(repeat_right)
            self.direction = 2
        elif key==KEYS.DOWN:
            self.sprite_player.do(repeat_down)
            self.direction = 3
        elif key==KEYS.SPACE:
            self.sprite_player.stop()

    def move_target(self, *args, **kwargs):
        x = random.randrange(10, self.win_width-10)
        y = random.randrange(10, self.win_height-10)
        self.sprite_target.do(MoveTo((x, y), duration=3.5))


    def move_attackers(self, *args, **kwargs):
        for temp_sprite in self.attackers:
            x = random.randrange(10, self.win_width-10)
            y = random.randrange(10, self.win_height-10)
            temp_sprite.do(MoveTo((x, y), duration=2.5))
        

    def update(self, *args, **kwargs):
        # check borders
        x = self.sprite_player.x
        y = self.sprite_player.y
        if self.sprite_player.contains(1, y) and self.direction==4:
            self.sprite_player.stop()
        elif self.sprite_player.contains(self.win_width-1, y) and self.direction==2:
            self.sprite_player.stop()
        elif self.sprite_player.contains(x, 1) and self.direction==3:
            self.sprite_player.stop()
        elif self.sprite_player.contains(x, self.win_height-1) and self.direction==1:
            self.sprite_player.stop()

        # check target
        x = self.sprite_target.x
        y = self.sprite_target.y        
        if self.sprite_player.contains(x, y):
            self.score += 1
            self.label_score.element.text = 'Score: %s' % self.score
            if (self.score//SCORE_FOR_LEVEL)==len(self.attackers):
                # curent level
                self.sprite_target.stop()
                x = random.randrange(10, self.win_width-10)
                y = random.randrange(30, self.win_height-10)                
                self.sprite_target.do(Place((x, y)))
                #self.move_target()
            else:
                # go to next level
                global LEVEL
                LEVEL += 1
                self.label_level.element.text = 'Level: %s' % LEVEL
                self.sprite_player.stop()
                x = int(self.win_width/2)
                y = 8                
                self.sprite_player.do(Place((x, y)))                
                # add new attacker
                temp_sprite = cocos.sprite.Sprite('sport_8ball.png')
                x = random.randrange(10, self.win_width-10)
                y = random.randrange(30, self.win_height-10)                
                temp_sprite.position = x, y
                self.add(temp_sprite)
                self.attackers.append(temp_sprite)

                director.push(level_scene)

        # check attackers
        for temp_sprite in self.attackers:
            x = temp_sprite.x
            y = temp_sprite.y        
            if self.sprite_player.contains(x, y):
                # player dies
                self.life -= 1
                self.label_life.element.text = 'Life: %s' % self.life
                temp_sprite.stop()
                x = random.randrange(10, self.win_width-10)
                y = random.randrange(30, self.win_height-10)                
                temp_sprite.do(Place((x, y)))

                self.sprite_player.stop()
                x = int(self.win_width/2)
                y = 8                
                self.sprite_player.do(Place((x, y)))

                director.push(death_scene)

class NextLevel(cocos.layer.ColorLayer):

    is_event_handler = True    

    def __init__(self):
        super(NextLevel, self).__init__(100, 200, 100, 255)

        win_width, win_height = cocos.director.director.get_window_size()
        global LEVEL
        text = 'Level %s' % LEVEL
        self.label = cocos.text.Label(text,
                          font_size=32,
                          color=(0, 80, 0, 255),
                          x=win_width/2,
                          y=win_height/2,
                          anchor_x='center',
                          anchor_y='center')
        self.label_2 = cocos.text.Label('Press <spacebar> to continue',
                          font_size=14,
                          color=(0, 80, 0, 255),
                          x=win_width/2,
                          y=(win_height/2)-50,
                          anchor_x='center',
                          anchor_y='center')        
        self.add(self.label)
        self.add(self.label_2)

    def on_enter(self):
        super(NextLevel,self).on_enter()
        self.label.element.text = 'Level: %s' % LEVEL

    def on_key_press(self, key, modifiers):
        if key==KEYS.SPACE:
            director.pop()      


class Death(cocos.layer.ColorLayer):

    is_event_handler = True    

    def __init__(self):
        super(Death, self).__init__(200, 100, 100, 255)

        win_width, win_height = cocos.director.director.get_window_size()
        self.label = cocos.text.Label('You killed :(',
                          font_size=32,
                          color=(80, 0, 0, 255),
                          x=win_width/2,
                          y=win_height/2,
                          anchor_x='center',
                          anchor_y='center')
        self.label_2 = cocos.text.Label('Press <spacebar> to continue',
                          font_size=14,
                          color=(80, 0, 0, 255),
                          x=win_width/2,
                          y=(win_height/2)-50,
                          anchor_x='center',
                          anchor_y='center')
        self.add(self.label)
        self.add(self.label_2)

        
    def on_key_press(self, key, modifiers):
        if key==KEYS.SPACE:
            director.pop()
            

if __name__=="__main__":
    director.init(caption='Shpiler')
    main_scene = cocos.scene.Scene(Game())
    level_scene = cocos.scene.Scene(NextLevel())
    death_scene = cocos.scene.Scene(Death())
    director.run(main_scene)

