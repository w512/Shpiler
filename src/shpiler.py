import sys
import os
import pyglet
import cocos
from cocos.actions import *


class Cursor(cocos.layer.ColorLayer):

    is_event_handler = True

    def __init__(self):
        super(Cursor, self).__init__(128, 224, 128, 255)
        self.run_status = False # if false - stop, if true - run
        self.direction = 1      # 1 - North, 2 - East, 3 - South, 4 - West
        self.m_s = 5            # step for move
        self.m_d = 0.01         # duration for move

        self.sprite = cocos.sprite.Sprite('skynet.jpg')
        self.sprite.position = 320,40
        self.add(self.sprite)

    def on_key_press(self, key, modifiers):
        """This function is called when a key is pressed."""
        repeat_left = Repeat(MoveBy((-1*self.m_s, 0), duration=self.m_d))
        repeat_up = Repeat(MoveBy((0, self.m_s), duration=self.m_d))
        repeat_right = Repeat(MoveBy((self.m_s, 0), duration=self.m_d))
        repeat_down = Repeat(MoveBy((0, -1*self.m_s), duration=self.m_d))
        if key==65361:
            self.sprite.do(repeat_left)
        elif key==65362:
            self.sprite.do(repeat_up)
        elif key==65363:
            self.sprite.do(repeat_right)
        elif key==65364:
            self.sprite.do(repeat_down)
        elif key==32:
            self.sprite.stop()

    def update(self):
        pass
        

if __name__ == "__main__":
    cocos.director.director.init()
    main_scene = cocos.scene.Scene(Cursor())
    cocos.director.director.run(main_scene)

