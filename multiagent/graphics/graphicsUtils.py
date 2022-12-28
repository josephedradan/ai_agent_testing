# graphicsUtils.py
# ----------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import os.path
import sys
import time
import tkinter

_Windows = sys.platform == 'win32'  # True if on Win95/98/NT


# _root_window = None      # The root window for graphics output
# _canvas = None      # The canvas which holds graphics
# _canvas_xs = None      # Size of canvas object
# _canvas_ys = None
# _canvas_x = None      # Current position on canvas
# _canvas_y = None
# _canvas_col = None      # Current colour (set to black below)
# _canvas_tsize = 12
# _canvas_tserifs = 0


def formatColor(r, g, b):
    return '#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255))


def colorToVector(color):
    return [int(x, 16) / 256.0 for x in [color[1:3], color[3:5], color[5:7]]]


if _Windows:
    _canvas_tfonts = ['times new roman', 'lucida console']
else:
    _canvas_tfonts = ['times', 'lucidasans-24']
    pass  # XXX need defaults here


class GraphicsActual:

    def __init__(self):
        self._root_window = None  # The root window for graphics output
        self._canvas = None  # The canvas which holds graphics
        self._canvas_xs = None  # Size of canvas object
        self._canvas_ys = None
        self._canvas_x = None  # Current position on canvas
        self._canvas_y = None
        self._canvas_col = None  # Current colour (set to black below)
        self._canvas_tsize = 12
        self._canvas_tserifs = 0

        self._bg_color = None

        self._leftclick_loc = None
        self._rightclick_loc = None
        self._ctrl_leftclick_loc = None

        # We bind to key-down and key-up events.

        self._keysdown = {}
        self._keyswaiting = {}
        # This holds an unprocessed key release.  We delay key releases by up to
        # one call to keys_pressed() to get round a problem with auto repeat.
        self._got_release = None

        self._mouse_enabled = 1

    def _draw_background(self):
        corners = [
            (0, 0), (0, self._canvas_ys),
            (self._canvas_xs, self._canvas_ys),
            (self._canvas_xs, 0)
        ]

        self.polygon(corners,
                self._bg_color,
                fillColor=self._bg_color,
                filled=True,
                smoothed=False)

    def begin_graphics(self, width=640, height=480, color=formatColor(0, 0, 0), title=None):

        # global _root_window, _canvas, _canvas_x, _canvas_y, _canvas_xs, _canvas_ys, _bg_color

        # Check for duplicate call
        if self._root_window is not None:
            # Lose the window.
            self._root_window.destroy()

        # Save the canvas size parameters
        self._canvas_xs = width - 1
        self._canvas_ys = height - 1
        self._canvas_x = 0
        self._canvas_y = self._canvas_ys
        self._bg_color = color

        def _destroy_window(event=None):
            sys.exit(0)

        # Create the root window
        self._root_window = tkinter.Tk()
        self._root_window.protocol('WM_DELETE_WINDOW', _destroy_window)
        self._root_window.title(title or 'Graphics Window')
        self._root_window.resizable(0, 0)

        # Create the canvas object
        try:
            self._canvas = tkinter.Canvas(self._root_window, width=width, height=height)
            self._canvas.pack()
            self._draw_background()
            self._canvas.update()
        except:
            self._root_window = None
            raise

        def _leftclick(event):
            nonlocal self
            self._leftclick_loc = (event.x, event.y)

        def _rightclick(event):
            nonlocal self
            self._rightclick_loc = (event.x, event.y)

        def _ctrl_leftclick(event):
            nonlocal self
            self._ctrl_leftclick_loc = (event.x, event.y)

        def wait_for_click():
            while True:
                nonlocal self

                # global _leftclick_loc
                # global _rightclick_loc
                # global _ctrl_leftclick_loc

                if self._leftclick_loc is not None:
                    val = self._leftclick_loc
                    self._leftclick_loc = None
                    return val, 'left'
                if self._rightclick_loc is not None:
                    val = self._rightclick_loc
                    self._rightclick_loc = None
                    return val, 'right'
                if self._ctrl_leftclick_loc is not None:
                    val = self._ctrl_leftclick_loc
                    _ctrl_leftclick_loc = None
                    return val, 'ctrl_left'
                self.sleep(0.05)

        def _keypress(event):
            nonlocal self
            # global _got_release

            # remap_arrows(event)
            self._keysdown[event.keysym] = 1
            self._keyswaiting[event.keysym] = 1
            #    print event.char, event.keycode
            self._got_release = None

        def _keyrelease(event):
            nonlocal self

            # global _got_release
            # remap_arrows(event)
            try:
                del self._keysdown[event.keysym]  # TODO INTERESTING CODE...
            except:
                pass
            self._got_release = 1

        def _clear_keys(event=None):
            nonlocal self

            # global _keysdown, _got_release, _keyswaiting
            # self._keysdown = {}
            # self._keyswaiting = {}
            # self._got_release = None

            self._clear_keys()

        # Bind to key-down and key-up events
        self._root_window.bind("<KeyPress>", _keypress)
        self._root_window.bind("<KeyRelease>", _keyrelease)
        self._root_window.bind("<FocusIn>", _clear_keys)
        self._root_window.bind("<FocusOut>", _clear_keys)
        self._root_window.bind("<Button-1>", _leftclick)
        self._root_window.bind("<Button-2>", _rightclick)
        self._root_window.bind("<Button-3>", _rightclick)
        self._root_window.bind("<Control-Button-1>", _ctrl_leftclick)
        _clear_keys()

    ##########################################
    ##########################################

    def remove_from_screen(self,
                           x,
                           # d_o_e=lambda arg: _root_window.dooneevent(arg),
                           # d_w=tkinter._tkinter.DONT_WAIT
                           ):

        self._canvas.delete(x)
        # d_o_e(d_w)
        self._root_window.dooneevent(tkinter._tkinter.DONT_WAIT)

    def move_to(self,
                object,
                x,
                y=None,
                # d_o_e=lambda arg: _root_window.dooneevent(arg),
                # d_w=tkinter._tkinter.DONT_WAIT
                ):

        if y is None:
            try:
                x, y = x
            except:
                raise Exception('incomprehensible coordinates')

        horiz = True
        newCoords = []
        current_x, current_y = self._canvas.coords(object)[0:2]  # first point
        for coord in self._canvas.coords(object):
            if horiz:
                inc = x - current_x
            else:
                inc = y - current_y
            horiz = not horiz

            newCoords.append(coord + inc)

        self._canvas.coords(object, *newCoords)
        # d_o_e(d_w)
        self._root_window.dooneevent(tkinter._tkinter.DONT_WAIT)

    def move_by(self,
                object,
                x,
                y=None,
                # d_o_e=lambda arg: _root_window.dooneevent(arg),
                # d_w=tkinter._tkinter.DONT_WAIT,
                lift=False
                ):
        if y is None:
            try:
                x, y = x
            except:
                raise Exception('incomprehensible coordinates')

        horiz = True
        newCoords = []
        for coord in self._canvas.coords(object):
            if horiz:
                inc = x
            else:
                inc = y
            horiz = not horiz

            newCoords.append(coord + inc)

        self._canvas.coords(object, *newCoords)

        # d_o_e(d_w)
        self._root_window.dooneevent(tkinter._tkinter.DONT_WAIT)

        if lift:
            self._canvas.tag_raise(object)

    #####

    def moveCircle(self, id, pos, r, endpoints=None):
        # global _canvas_x, _canvas_y

        x, y = pos
        #    x0, x1 = x - r, x + r + 1
        #    y0, y1 = y - r, y + r + 1
        x0, x1 = x - r - 1, x + r
        y0, y1 = y - r - 1, y + r
        if endpoints is None:
            e = [0, 359]
        else:
            e = list(endpoints)
        while e[0] > e[1]:
            e[1] = e[1] + 360

        if os.path.isfile('flag'):
            self.edit(id, ('extent', e[1] - e[0]))
        else:
            self.edit(id, ('start', e[0]), ('extent', e[1] - e[0]))
        self.move_to(id, x0, y0)

    #####

    def polygon(self, coords, outlineColor, fillColor=None, filled=1, smoothed=1, behind=0, width=1):
        c = []
        for coord in coords:
            c.append(coord[0])
            c.append(coord[1])
        if fillColor == None:
            fillColor = outlineColor
        if filled == 0:
            fillColor = ""
        poly = self._canvas.create_polygon(
            c, outline=outlineColor, fill=fillColor, smooth=smoothed, width=width)
        if behind > 0:
            self._canvas.tag_lower(poly, behind)  # Higher should be more visible
        return poly

    def square(self, pos, r, color, filled=1, behind=0):
        x, y = pos
        coords = [(x - r, y - r), (x + r, y - r), (x + r, y + r), (x - r, y + r)]
        return self.polygon(coords, color, color, filled, 0, behind=behind)

    def circle(self, pos, r, outlineColor, fillColor, endpoints=None, style='pieslice', width=2):
        x, y = pos
        x0, x1 = x - r - 1, x + r
        y0, y1 = y - r - 1, y + r
        if endpoints is None:
            e = [0, 359]
        else:
            e = list(endpoints)
        while e[0] > e[1]:
            e[1] = e[1] + 360

        return self._canvas.create_arc(x0, y0, x1, y1,
                                       outline=outlineColor,
                                       fill=fillColor,
                                       extent=e[1] - e[0],
                                       start=e[0],
                                       style=style,
                                       width=width)

    #####

    def edit(self, id, *args):
        self._canvas.itemconfigure(id, **dict(args))

    def text(self, pos, color, contents, font='Helvetica', size=12, style='normal', anchor="nw"):
        # global _canvas_x, _canvas_y

        x, y = pos
        font = (font, str(size), style)
        return self._canvas.create_text(x, y, fill=color, text=contents, font=font, anchor=anchor)

    def changeText(self, id, newText, font=None, size=12, style='normal'):
        self._canvas.itemconfigure(id, text=newText)
        if font is not None:
            self._canvas.itemconfigure(id, font=(font, '-%d' % size, style))

    def changeColor(self, id, newColor):
        self._canvas.itemconfigure(id, fill=newColor)

    def line(self, here, there, color=formatColor(0, 0, 0), width=2):
        x0, y0 = here[0], here[1]
        x1, y1 = there[0], there[1]

        return self._canvas.create_line(x0, y0, x1, y1, fill=color, width=width)

    ##########################################
    ##########################################

    ##########################################
    ##########################################

    def _clear_keys(self):
        self._keysdown = {}
        self._keyswaiting = {}
        self._got_release = None

    def get_keys_pressed(self,
                         # d_o_e=lambda arg: _root_window.dooneevent(arg),
                         # d_w=tkinter._tkinter.DONT_WAIT
                         ):
        # d_o_e(d_w)

        self._root_window.dooneevent(tkinter._tkinter.DONT_WAIT)

        if self._got_release:
            # d_o_e(d_w)
            self._root_window.dooneevent(tkinter._tkinter.DONT_WAIT)

        return list(self._keysdown.keys())

    def get_keys_waiting(self):
        # global _keyswaiting

        keys = list(self._keyswaiting.keys())
        self._keyswaiting = {}
        return keys

    # Block for a list of keys...

    def get_wait_for_keys(self):
        keys = []
        while not keys:
            keys = self.get_keys_pressed()
            self.sleep(0.05)
        return keys

    def refresh(self):
        self._canvas.update_idletasks()

    def sleep(self, secs):
        # global _root_window
        if self._root_window == None:
            time.sleep(secs)
        else:
            self._root_window.update_idletasks()
            self._root_window.after(int(1000 * secs), self._root_window.quit)
            self._root_window.mainloop()

    def end_graphics(self):
        # global _root_window, _canvas, _mouse_enabled

        try:
            try:
                self.sleep(1)
                if self._root_window is not None:
                    self._root_window.destroy()
            except SystemExit as e:
                print('Ending graphics raised an exception:', e)
        finally:
            self._root_window = None
            self._canvas = None
            self._mouse_enabled = 0
            self._clear_keys()


#    global _root_window
#    _root_window.destroy()
#    _root_window = None
# print "DESTROY"


def clear_screen(background=None):
    global _canvas_x, _canvas_y
    _canvas.delete('all')
    draw_background()
    _canvas_x, _canvas_y = 0, _canvas_ys


def image(pos, file="../../blueghost.gif"):
    x, y = pos
    # img = PhotoImage(file=file)
    return _canvas.create_image(x, y, image=tkinter.PhotoImage(file=file), anchor=tkinter.NW)


# def moveCircle(id, pos, r, endpoints=None):
#     global _canvas_x, _canvas_y
#
#     x, y = pos
#     #    x0, x1 = x - r, x + r + 1
#     #    y0, y1 = y - r, y + r + 1
#     x0, x1 = x - r - 1, x + r
#     y0, y1 = y - r - 1, y + r
#     if endpoints == None:
#         e = [0, 359]
#     else:
#         e = list(endpoints)
#     while e[0] > e[1]:
#         e[1] = e[1] + 360
#
#     if os.path.isfile('flag'):
#         edit(id, ('extent', e[1] - e[0]))
#     else:
#         edit(id, ('start', e[0]), ('extent', e[1] - e[0]))
#     move_to(id, x0, y0)


##############################################################################
### Keypress handling ########################################################
##############################################################################


def remap_arrows(event):
    # TURN ARROW PRESSES INTO LETTERS (SHOULD BE IN KEYBOARD AGENT)
    if event.char in ['a', 's', 'd', 'w']:
        return
    if event.keycode in [37, 101]:  # LEFT ARROW (win / x)
        event.char = 'a'
    if event.keycode in [38, 99]:  # UP ARROW
        event.char = 'w'
    if event.keycode in [39, 102]:  # RIGHT ARROW
        event.char = 'd'
    if event.keycode in [40, 104]:  # DOWN ARROW
        event.char = 's'


###################
###################
###################
###################


def _adjust_coords(coord_list, x, y):
    for i in range(0, len(coord_list), 2):
        coord_list[i] = coord_list[i] + x
        coord_list[i + 1] = coord_list[i + 1] + y
    return coord_list


def writePostscript(filename):
    "Writes the current canvas to a postscript file."
    psfile = file(filename, 'w')
    psfile.write(_canvas.postscript(pageanchor='sw',
                                    y='0.c',
                                    x='0.c'))
    psfile.close()


ghost_shape = [
    (0, - 0.5),
    (0.25, - 0.75),
    (0.5, - 0.5),
    (0.75, - 0.75),
    (0.75, 0.5),
    (0.5, 0.75),
    (- 0.5, 0.75),
    (- 0.75, 0.5),
    (- 0.75, - 0.75),
    (- 0.5, - 0.5),
    (- 0.25, - 0.75)
]

if __name__ == '__main__':
    begin_graphics()
    clear_screen()
    ghost_shape = [(x * 10 + 20, y * 10 + 20) for x, y in ghost_shape]
    g = polygon(ghost_shape, formatColor(1, 1, 1))
    move_to(g, (50, 50))
    circle((150, 150), 20, formatColor(0.7, 0.3, 0.0), endpoints=[15, - 15])
    sleep(2)
