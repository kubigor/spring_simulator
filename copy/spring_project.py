import random
import pyautogui
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty


class Spring(Widget):
    volume = ObjectProperty(None)
    ground_width = ObjectProperty(None)
    message = ObjectProperty(None)
    canvas_created = False
    start_points = set()

    # initialize window size
    def __init__(self, **kwargs):
        super(Spring, self).__init__(**kwargs)
        width = pyautogui.size().width // 2
        height = pyautogui.size().height // 2
        Window.size = (width, height)
        Window.left = (pyautogui.size().width - Window.width) // 2
        Window.minimum_width, Window.minimum_height = Window.size

    # clear window and proceed to canvas
    def take_input(self, volume, ground_width):
        if not self.check_input(volume, ground_width):
            print('Terminated')
            return

        print('Generating...')
        self.ids.table.clear_widgets()
        self.volume = int(self.volume.text)
        self.generate_ground(int(self.ground_width.text))

    # input validation and error message

    def check_input(self, volume, ground_width):
        volume_check = volume.text.isdigit() and 1 <= int(volume.text) <= 100
        ground_width_check = ground_width.text.isdigit() and 5 <= int(ground_width.text) <= 50
        if not volume_check:
            self.message.text = "Provide correct volume between 1 and 100!"
        if not ground_width_check:
            self.message.text = "Provide correct ground size between 5 and 50!"
        if volume_check and ground_width_check:
            return True

        self.volume.text = ""
        self.ground_width.text = ""

    # canvas generation
    def generate_ground(self, ground):
        Window.size = (22 * (ground), 800)
        Window.left = (pyautogui.size().width - Window.width) // 2
        Window.minimum_width, Window.minimum_height = Window.size
        self.canvas_created = True

        with self.canvas:
            self.levels = self.build_heights(ground)
            self.build_ground(self.levels)
            Color(0, 0.7, 1)

    # determine the heights of blocks
    def build_heights(self, ground):
        levels = [20]
        for _ in range(1, ground):
            prev_level = levels[-1]
            level_change = random.randrange(-1, 2)
            new_level = prev_level + level_change
            levels.append(new_level)

        return levels

    # build blocks
    def build_ground(self, levels):
        for column in range(len(levels)):
            Color(0.6, 0.4, 0.3)
            for height in range(levels[column]):
                if height == levels[column] - 1:
                    Color(0, 1, 0)
                    self.start_points.add((column, height))
                rect = Rectangle(pos=(22 * column, 22 * height), size=(20, 20))
                self.canvas.add(rect)

    # create the spring source
    def on_touch_down(self, touch):
        if self.canvas_created:
            spring_x, spring_y = self.green_square_pressed(touch.pos)
            if spring_x:
                self.canvas.add(
                    Rectangle(pos=(22*spring_x, 22*spring_y), size=(20, 20)))
                self.flow(spring_x)
        return super(Spring, self).on_touch_down(touch)

    # check if spring source is valid
    def green_square_pressed(self, pos):
        x = int(pos[0] // 22)
        y = int(pos[1] // 22)
        if (x, y) in self.start_points:
            return (x, y)
        else:
            return (0, 0)

    # create river
    def flow(self, source_level):

        pass


class MyApp(App):
    def build(self):
        return Spring()


if __name__ == "__main__":
    MyApp().run()
