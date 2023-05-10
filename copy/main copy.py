import random
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty


class StartWindow(Widget):
    Window.size = (1100, 800)
    volume = ObjectProperty(None)
    ground_width = ObjectProperty(None)
    message = ObjectProperty(None)

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

    def take_input(self, volume, ground_width):
        if not self.check_input(volume, ground_width):
            print('Terminated')
            return

        print('Generating...')
        self.canvas.clear()
        self.generate(int(self.ground_width.text))

    def generate(self, ground):
        print('generate !@')
        with self.canvas:
            levels = self.build_heights(ground)
            self.build_ground(levels)

    def build_heights(self, ground):
        levels = []
        for _ in range(ground):
            levels.append(random.randrange(17, 22))

        return levels

    def build_ground(self, levels):
        for column in range(len(levels)):
            Color(0.6, 0.4, 0.3, 1, mode="rgba")
            for height in range(levels[column]):
                if height == levels[column] - 1:
                    Color(0, 1, 0, 1, mode="rgba")
                    rect = Rectangle(
                        pos=(22 * column, 22 * height), size=(20, 20))
                else:
                    rect = Rectangle(
                        pos=(22 * column, 22 * height), size=(20, 20))
                self.canvas.add(rect)


class MyApp(App):
    def build(self):
        return StartWindow()


if __name__ == "__main__":
    MyApp().run()
