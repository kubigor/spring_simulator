import random

import pyautogui
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Triangle
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget


class Spring(Widget):
    volume = ObjectProperty(None)
    ground_width = ObjectProperty(None)
    message = ObjectProperty(None)
    canvas_created = False
    brown = (0.6, 0.4, 0.3)
    green = (0, 1, 0)
    light_blue = (0, 0.7, 1)
    black = (0, 0, 0)

    # initialize window size
    def __init__(self, **kwargs):
        super(Spring, self).__init__(**kwargs)
        width = pyautogui.size().width // 2
        height = pyautogui.size().height // 2
        Window.size = (width, height)
        Window.left = (pyautogui.size().width - Window.width) // 2
        Window.minimum_width, Window.minimum_height = Window.size
        self.start_points = set()

    # clear window and proceed to canvas
    def take_input(self, volume, ground_width):
        if not self.check_input(volume, ground_width):
            print('Terminated')
            return

        print('Generating...')
        self.clear_widgets()
        self.volume = int(self.volume.text)
        self.generate_ground(int(self.ground_width.text))

    # input validation and error message
    def check_input(self, volume, ground_width):
        volume_check = volume.text.isdigit() and 1 <= int(volume.text) <= 100
        ground_width_check = ground_width.text.isdigit(
        ) and 10 <= int(ground_width.text) <= 50
        if not volume_check:
            self.message.text = "Provide correct volume between 1 and 100!"
        if not ground_width_check:
            self.message.text = "Provide correct ground size between 10 and 50!"
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
        self.temporary_label = (Label(text="Press on any green square.",
                                      font_size=18, size=(Window.width//4, Window.height//8), pos=(
                                           Window.width // 8 * 3, (Window.height // 6) * 5)))
        self.add_widget(self.temporary_label)
        with self.canvas:
            self.levels = self.build_heights(ground)
            self.build_ground(self.levels)
            Color(*self.light_blue)

    # determine the heights of blocks
    def build_heights(self, ground):
        levels = [12]
        for _ in range(1, ground):
            prev_level = levels[-1]
            level_change = random.randrange(-1, 2)
            new_level = max(0, prev_level + level_change)
            levels.append(new_level)

        return levels

    # build blocks
    def build_ground(self, levels):
        for column in range(len(levels)):
            Color(*self.brown)
            for height in range(levels[column]):
                if height == levels[column] - 1:
                    Color(*self.green)
                    self.start_points.add((column, height))
                self.add_cell(column, height)

    # override touch / create the spring source
    def on_touch_down(self, touch):
        if self.canvas_created:
            spring_x, spring_y = self.green_square_pressed(touch.pos)
            if spring_y:
                self.canvas_created = False
                self.remove_widget(self.temporary_label)
                self.canvas.add(
                    Rectangle(pos=(22*spring_x, 22*spring_y), size=(20, 20)))
                self.flow(spring_x, spring_y)
        return super(Spring, self).on_touch_down(touch)

    # check if spring source is valid
    def green_square_pressed(self, pos):
        x = int(pos[0] // 22)
        y = int(pos[1] // 22)

        if (x, y) in self.start_points:
            return (x, y)
        else:
            return (0, 0)

    # create river flow (main algorithm)
    def flow(self, source_x, source_y, volume_used=0):

        # check if left side is obstructed
        def move_left(source):
            x, y = source
            if x - 1 >= 0 and self.levels[x - 1] <= y:
                if self.levels[x - 1] < y:
                    left_stack.append([x, y])
                return True

            else:
                return False

        # check if right side is obstructed
        def move_right(source):
            x, y = source
            if x + 1 < limit and self.levels[x + 1] <= y:
                if self.levels[x + 1] < y:
                    right_stack.append([x, y])
                return True

            else:
                return False

        last_left_cell = None
        last_right_cell = None
        left_stack = []
        right_stack = []
        left_source = [source_x, source_y]
        right_source = [source_x, source_y]
        limit = len(self.levels)
        while volume_used <= self.volume:
            left_step_possibility = move_left(left_source)
            right_step_possibility = move_right(right_source)

            # if left and right obstructed the source moves up
            if not left_step_possibility and not right_step_possibility and not left_stack and not right_stack:
                source_y += 1
                volume_used += 1
                self.add_cell(source_x, source_y), 2
                left_source = [source_x, source_y]
                right_source = [source_x, source_y]

            if left_step_possibility:
                left_source[0] -= 1
                left_source[1] = self.levels[left_source[0]]
                self.add_cell(left_source[0], self.levels[left_source[0]])
                last_left_cell = [left_source[0], self.levels[left_source[0]]]
                self.levels[left_source[0]] += 1
                volume_used += 1
            else:
                if left_stack:
                    left_source = left_stack.pop()

            if volume_used == self.volume:
                break

            if right_step_possibility:
                right_source[0] += 1
                right_source[1] = self.levels[right_source[0]]
                self.add_cell(right_source[0], self.levels[right_source[0]])
                last_right_cell = [right_source[0],
                                   self.levels[right_source[0]]]
                self.levels[right_source[0]] += 1
                volume_used += 1
            else:
                if right_stack:
                    right_source = right_stack.pop()

        left_stack += [last_left_cell] if last_left_cell else []
        right_stack += [last_right_cell] if last_right_cell else []
        self.draw_triangles(left_stack, right_stack)
        self.restart_btn = Button(text="Restart", font_size=20, size=(Window.width//4, Window.height//8), pos=(
            Window.width // 8 * 3, (Window.height // 6) * 5), on_press=self.restart)
        self.add_widget(self.restart_btn)
        print('Finished')

    # adding slopes
    def draw_triangles(self, left_stack, right_stack):
        with self.canvas:
            while left_stack:
                Color(*self.black)
                x, y = left_stack.pop()
                self.add_cell(x, y)
                Color(*self.light_blue)
                x, y = x * 22, y * 22
                self.canvas.add(Triangle(points=(x, y, x+20, y, x+20, y+20)))

            while right_stack:
                Color(*self.black)
                x, y = right_stack.pop()
                self.add_cell(x, y)
                Color(*self.light_blue)
                x, y = x * 22, y * 22
                self.canvas.add(Triangle(points=(x, y, x+20, y, x, y+20)))

    def add_cell(self, x, y):
        self.rect = Rectangle(pos=(22*x, 22*y), size=(21, 21))
        self.canvas.add(self.rect)
        self.rect.size = (20, 20)
        return

    def restart(self, button):
        self.canvas.clear()
        MyApp().run()


class MyApp(App):
    def build(self):
        return Spring()


if __name__ == "__main__":
    MyApp().run()
