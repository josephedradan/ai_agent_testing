"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 1/9/2023

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""
from abc import ABC
from abc import abstractmethod

def formatColor(r, g, b):
    return '#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255))

class GUI(ABC):

    @abstractmethod
    def initialize_graphics(self, width=640, height=480, color=formatColor(0, 0, 0), name=None):
        pass

    @abstractmethod
    def draw_square(self, pos, r, color, filled=1, behind=0):
        pass

    @abstractmethod
    def draw_circle(self, pos, r, outlineColor, fillColor, endpoints=None, style='pieslice', width=2):
        pass

    @abstractmethod
    def draw_polygon(self, coords, outlineColor, fillColor=None, filled=1, smoothed=1, behind=0, width=1):
        pass

    @abstractmethod
    def draw_text(self, pos, color, contents, font='Helvetica', size=12, style='normal', anchor="nw"):
        pass

    @abstractmethod
    def draw_line(self, here, there, color=formatColor(0, 0, 0), width=2):
        pass

    @abstractmethod
    def change_text(self, id, newText, font=None, size=12, style='normal'):
        pass

    @abstractmethod
    def edit(self, id, *args):
        pass

    @abstractmethod
    def change_color(self, id, newColor):
        pass


    @abstractmethod
    def get_keys_pressed(self):
        pass

    @abstractmethod
    def get_keys_waiting(self):
        pass

    @abstractmethod
    def get_wait_for_keys(self):
        pass

    @abstractmethod
    def refresh(self):
        pass

    @abstractmethod
    def sleep(self, secs):
        pass

    @abstractmethod
    def end_graphics(self):
        pass

    @abstractmethod
    def remove_from_screen(self,x):
        pass

    @abstractmethod
    def move_by(self, object, x, y=None, lift=False):
        pass
    @abstractmethod
    def move_circle(self, id, pos, r, endpoints=None):
        pass

    @abstractmethod
    def clear_screen(self):
        pass