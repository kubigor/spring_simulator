import kivy
import time
import random
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, RiseInTransition
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle, Color
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty


class First(Screen):
    multi = 0

    def __init__(self, **kw):
        super(First, self).__init__(**kw)

        with self.canvas:

            pass

    def gen(self):
        print('first')
        self.canvas.add(Rectangle(
            pos=(22 * self.multi, 22 * self.multi), size=(20, 20)))
        self.multi += 1
        # print(self.manager.chain(35))


class Second(Screen):
    def gen(self):
        # self.manager.volume = 35
        print('second')
        # print(self.manager.chain(35))
        First().gen()


class Manager(ScreenManager):

    def chain(self, number):
        self.volume = number
        print('manager', number)

    pass


kv = Builder.load_file("testing.kv")


class MyApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyApp().run()
