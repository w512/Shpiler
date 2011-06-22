import sys
import os
import pyglet
import cocos
from cocos.actions import *


class Cursor():
    def __init__(self):
        self.run_status = False # if false - stop, if true - run
        self.direction = 1      # 1 - North, 2 - East, 3 - South, 4 - West


class HelloWorld(cocos.layer.ColorLayer):
    def __init__(self):
        super( HelloWorld, self ).__init__(128, 224, 128, 255)

        label = cocos.text.Label('Hello, World!',
            font_name='Times New Roman',
            font_size=32,
            anchor_x='center', anchor_y='center')

        label.position = 320,240
        self.add( label )


class KeyDisplay(cocos.layer.Layer):

    is_event_handler = True     #: enable pyglet's events

    def __init__(self):

        super( KeyDisplay, self ).__init__()

        self.text = cocos.text.Label("", x=100, y=280 )

        # To keep track of which keys are pressed:
        self.keys_pressed = set()
        self.update_text()
        self.add(self.text)

    def update_text(self):
        key_names = [pyglet.window.key.symbol_string(k) for k in self.keys_pressed]
        text = 'Keys: '+','.join(key_names)
        # Update self.text
        self.text.element.text = text

    def on_key_press(self, key, modifiers):
        """This function is called when a key is pressed.
        """
        self.keys_pressed.add(key)
        self.update_text()

    def on_key_release(self, key, modifiers):
        """This function is called when a key is released.
        """
        self.keys_pressed.remove(key)
        self.update_text()



        
        

if __name__ == "__main__":
    # director init takes the same arguments as pyglet.window
    cocos.director.director.init()

    # We create a new layer, an instance of HelloWorld
    hello_layer = HelloWorld()

    # A scene that contains the layer hello_layer
    main_scene = cocos.scene.Scene(hello_layer, KeyDisplay())
    #second_scene = cocos.scene.Scene(KeyDisplay())

    # And now, start the application, starting with main_scene
    #cocos.director.director.run(main_scene)
    cocos.director.director.run(main_scene)

