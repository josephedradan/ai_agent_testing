# graphicsGridworldDisplay.py
# ---------------------------
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


from functools import reduce
from typing import Union

from common.display import Display
from common.display import formatColor
from common.display_tkinter import DisplayTkinter
from common import util

BACKGROUND_COLOR = formatColor(0, 0, 0)
EDGE_COLOR = formatColor(1, 1, 1)
OBSTACLE_COLOR = formatColor(0.5, 0.5, 0.5)
TEXT_COLOR = formatColor(1, 1, 1)
MUTED_TEXT_COLOR = formatColor(0.7, 0.7, 0.7)
LOCATION_COLOR = formatColor(0, 0, 1)

WINDOW_SIZE = -1
GRID_SIZE = -1
GRID_HEIGHT = -1
MARGIN = -1


class GraphicsGridworldDisplay:

    def __init__(self,
                 gridworld,
                 size=120,
                 speed=1.0,
                 display: Union[Display, None] = DisplayTkinter(),
                 ):

        print("INIT CALLED")
        # FIXME CHANGE LATER
        self.display: Union[DisplayTkinter, None] = DisplayTkinter()

        self.gridworld = gridworld
        self.size = size
        self.speed = speed

        self.count = 1

    def start(self):
        self.setup( size=self.size)

    def pause(self):
        self.display.get_wait_for_keys()

    # TODO: IMPORTANT
    def displayValues(self, agent, currentState=None, message='Agent Values'):
        values = util.Counter()
        policy = {}
        states = self.gridworld.getStates()

        for state in states:
            values[state] = agent.getValue(state)
            policy[state] = agent.getPolicy(state)
        self.drawValues(values, policy, currentState, message)
        # self.pause()  # TODO: WTF
        self.display.sleep(0.05 / self.speed)
        # self.display.sleep(0.1)

        # print(0.05 / self.speed)  # speed in 1 so 0.05
        # self.display.sleep(0.0125)

    def displayNullValues(self, currentState=None, message=''):
        values = util.Counter()
        # policy = {}
        states = self.gridworld.getStates()
        for state in states:
            values[state] = 0.0
            # policy[state] = agent.getPolicy(state)
        self.drawNullValues(self.gridworld, currentState, '')
        # drawValues(self.gridworld, values, policy, currentState, message)
        self.display.sleep(0.05 / self.speed)

    def displayQValues(self, agent, currentState=None, message='Agent Q-Values'):
        qValues = util.Counter()
        states = self.gridworld.getStates()
        for state in states:
            for action in self.gridworld.getPossibleActions(state):
                qValues[(state, action)] = agent.getQValue(state, action)
        self.drawQValues(qValues, currentState, message)
        self.display.sleep(0.05 / self.speed)

    def setup(self, title="Gridworld Display", size=120):
        global GRID_SIZE, MARGIN, SCREEN_WIDTH, SCREEN_HEIGHT, GRID_HEIGHT

        grid = self.gridworld.grid

        WINDOW_SIZE = size
        GRID_SIZE = size
        GRID_HEIGHT = grid.height
        MARGIN = GRID_SIZE * 0.75
        screen_width = (grid.width - 1) * GRID_SIZE + MARGIN * 2
        screen_height = (grid.height - 0.5) * GRID_SIZE + MARGIN * 2

        self.display.initialize_graphics(
            screen_width,
            screen_height,
            BACKGROUND_COLOR,
            name=title
        )

    def drawNullValues(self, currentState=None, message=''):

        grid = self.gridworld.grid

        self.blank()
        for x in range(grid.width):
            for y in range(grid.height):
                state = (x, y)
                gridType = grid[x][y]
                isExit = (str(gridType) != gridType)
                isCurrent = (currentState == state)
                if gridType == '#':
                    self.drawSquare(x, y, 0, 0, 0, None, None, True, False, isCurrent)
                else:
                    self.drawNullSquare(x, y, False, isExit, isCurrent)

        pos = to_screen(((grid.width - 1.0) / 2.0, - 0.8))
        self.display.draw_text(pos, TEXT_COLOR, message, "Courier", -32, "bold", "c")

    # TODO: IMPORTANT SHIT
    def drawValues(self, values, policy, currentState=None, message='State Values'):
        grid = self.gridworld.grid

        self.blank()
        valueList = [values[state] for state in self.gridworld.getStates()] + [0.0]
        minValue = min(valueList)
        maxValue = max(valueList)
        for x in range(grid.width):
            for y in range(grid.height):
                state = (x, y)
                gridType = grid[x][y]
                isExit = (str(gridType) != gridType)
                isCurrent = (currentState == state)
                if gridType == '#':
                    self.drawSquare(x, y, 0, 0, 0, None, None, True, False, isCurrent)
                else:
                    value = values[state]
                    action = None
                    if policy != None and state in policy:
                        action = policy[state]
                        actions = self.gridworld.getPossibleActions(state)
                    if action not in actions and 'exit' in actions:
                        action = 'exit'
                    valString = '%.2f' % value
                    self.drawSquare(x, y, value, minValue, maxValue, valString, action, False, isExit, isCurrent)

        pos = to_screen(((grid.width - 1.0) / 2.0, - 0.8))
        self.display.draw_text(pos, TEXT_COLOR, message, "Courier", -32, "bold", "c")
        # self.pause() # TODO: WTF

    def drawQValues(self, qValues, currentState=None, message='State-Action Q-Values'):
        grid = self.gridworld.grid

        self.blank()
        stateCrossActions = [[(state, action) for action in self.gridworld.getPossibleActions(state)] for state in
                             self.gridworld.getStates()]
        qStates = reduce(lambda x, y: x + y, stateCrossActions, [])
        qValueList = [qValues[(state, action)] for state, action in qStates] + [0.0]
        minValue = min(qValueList)
        maxValue = max(qValueList)
        for x in range(grid.width):
            for y in range(grid.height):
                state = (x, y)
                gridType = grid[x][y]
                isExit = (str(gridType) != gridType)
                isCurrent = (currentState == state)
                actions = self.gridworld.getPossibleActions(state)
                if actions == None or len(actions) == 0:
                    actions = [None]
                bestQ = max([qValues[(state, action)] for action in actions])
                bestActions = [action for action in actions if qValues[(state, action)] == bestQ]

                q = util.Counter()
                valStrings = {}
                for action in actions:
                    v = qValues[(state, action)]
                    q[action] += v
                    valStrings[action] = '%.2f' % v
                if gridType == '#':
                    self.drawSquare(x, y, 0, 0, 0, None, None, True, False, isCurrent)
                elif isExit:
                    action = 'exit'
                    value = q[action]
                    valString = '%.2f' % value
                    self.drawSquare(x, y, value, minValue, maxValue, valString, action, False, isExit, isCurrent)
                else:
                    self.drawSquareQ(x, y, q, minValue, maxValue, valStrings, actions, isCurrent)
        pos = to_screen(((grid.width - 1.0) / 2.0, - 0.8))
        self.display.draw_text(pos, TEXT_COLOR, message, "Courier", -32, "bold", "c")

    def blank(self):
        self.display.clear_screen()

    def drawNullSquare(self, grid, x, y, isObstacle, isTerminal, isCurrent):
        square_color = getColor(0, -1, 1)

        if isObstacle:
            square_color = OBSTACLE_COLOR

        (screen_x, screen_y) = to_screen((x, y))
        self.square((screen_x, screen_y),
                    0.5 * GRID_SIZE,
                    color=square_color,
                    filled=1,
                    width=1)

        self.square((screen_x, screen_y),
                    0.5 * GRID_SIZE,
                    color=EDGE_COLOR,
                    filled=0,
                    width=3)

        if isTerminal and not isObstacle:
            self.square((screen_x, screen_y),
                        0.4 * GRID_SIZE,
                        color=EDGE_COLOR,
                        filled=0,
                        width=2)
            self.display.draw_text((screen_x, screen_y),
                                   TEXT_COLOR,
                                   str(grid[x][y]),
                                   "Courier", -24, "bold", "c")

        text_color = TEXT_COLOR

        if not isObstacle and isCurrent:
            self.display.draw_circle((screen_x, screen_y), 0.1 * GRID_SIZE, LOCATION_COLOR,
                                     fillColor=LOCATION_COLOR)

        # if not isObstacle:
        #   self.display.draw_text( (screen_x, screen_y), text_color, valStr, "Courier", 24, "bold", "c")

    # TODO: IMPORTANT
    def drawSquare(self, x, y, val, min, max, valStr, action, isObstacle, isTerminal, isCurrent):
        square_color = getColor(val, min, max)

        if isObstacle:
            square_color = OBSTACLE_COLOR

        (screen_x, screen_y) = to_screen((x, y))
        self.square((screen_x, screen_y),
                    0.5 * GRID_SIZE,
                    color=square_color,
                    filled=1,
                    width=1)
        self.square((screen_x, screen_y),
                    0.5 * GRID_SIZE,
                    color=EDGE_COLOR,
                    filled=0,
                    width=3)
        if isTerminal and not isObstacle:
            self.square((screen_x, screen_y),
                        0.4 * GRID_SIZE,
                        color=EDGE_COLOR,
                        filled=0,
                        width=2)

        if action == 'north':
            self.display.draw_polygon(
                [(screen_x, screen_y - 0.45 * GRID_SIZE), (screen_x + 0.05 * GRID_SIZE, screen_y - 0.40 * GRID_SIZE),
                 (screen_x - 0.05 * GRID_SIZE, screen_y - 0.40 * GRID_SIZE)], EDGE_COLOR, filled=1, smoothed=False)
        if action == 'south':
            self.display.draw_polygon(
                [(screen_x, screen_y + 0.45 * GRID_SIZE), (screen_x + 0.05 * GRID_SIZE, screen_y + 0.40 * GRID_SIZE),
                 (screen_x - 0.05 * GRID_SIZE, screen_y + 0.40 * GRID_SIZE)], EDGE_COLOR, filled=1, smoothed=False)
        if action == 'west':
            self.display.draw_polygon(
                [(screen_x - 0.45 * GRID_SIZE, screen_y), (screen_x - 0.4 * GRID_SIZE, screen_y + 0.05 * GRID_SIZE),
                 (screen_x - 0.4 * GRID_SIZE, screen_y - 0.05 * GRID_SIZE)], EDGE_COLOR, filled=1, smoothed=False)
        if action == 'east':
            self.display.draw_polygon(
                [(screen_x + 0.45 * GRID_SIZE, screen_y), (screen_x + 0.4 * GRID_SIZE, screen_y + 0.05 * GRID_SIZE),
                 (screen_x + 0.4 * GRID_SIZE, screen_y - 0.05 * GRID_SIZE)], EDGE_COLOR, filled=1, smoothed=False)

        text_color = TEXT_COLOR

        if not isObstacle and isCurrent:
            print('FUCK YOU', (screen_x, screen_y), 0.1 * GRID_SIZE, LOCATION_COLOR)
            x = self.display.draw_circle(
                (screen_x, screen_y),
                0.1 * GRID_SIZE,
                outlineColor=LOCATION_COLOR,
                fillColor=LOCATION_COLOR
            )
            print(x)

        if not isObstacle:
            self.display.draw_text((screen_x, screen_y), text_color, valStr, "Courier", -30, "bold", "c")

    def drawSquareQ(self, x, y, qVals, minVal, maxVal, valStrs, bestActions, isCurrent):
        (screen_x, screen_y) = to_screen((x, y))

        center = (screen_x, screen_y)
        nw = (screen_x - 0.5 * GRID_SIZE, screen_y - 0.5 * GRID_SIZE)
        ne = (screen_x + 0.5 * GRID_SIZE, screen_y - 0.5 * GRID_SIZE)
        se = (screen_x + 0.5 * GRID_SIZE, screen_y + 0.5 * GRID_SIZE)
        sw = (screen_x - 0.5 * GRID_SIZE, screen_y + 0.5 * GRID_SIZE)
        n = (screen_x, screen_y - 0.5 * GRID_SIZE + 5)
        s = (screen_x, screen_y + 0.5 * GRID_SIZE - 5)
        w = (screen_x - 0.5 * GRID_SIZE + 5, screen_y)
        e = (screen_x + 0.5 * GRID_SIZE - 5, screen_y)

        actions = list(qVals.keys())
        for action in actions:

            wedge_color = getColor(qVals[action], minVal, maxVal)

            if action == 'north':
                self.display.draw_polygon((center, nw, ne), wedge_color, filled=1, smoothed=False)
                # self.display.draw_text((n, text_color, valStr, "Courier", 8, "bold", "n")
            if action == 'south':
                self.display.draw_polygon((center, sw, se), wedge_color, filled=1, smoothed=False)
                # self.display.draw_text((s, text_color, valStr, "Courier", 8, "bold", "s")
            if action == 'east':
                self.display.draw_polygon((center, ne, se), wedge_color, filled=1, smoothed=False)
                # self.display.draw_text((e, text_color, valStr, "Courier", 8, "bold", "e")
            if action == 'west':
                self.display.draw_polygon((center, nw, sw), wedge_color, filled=1, smoothed=False)
                # self.display.draw_text((w, text_color, valStr, "Courier", 8, "bold", "w")

        self.square(
            (screen_x, screen_y),
            0.5 * GRID_SIZE,
            color=EDGE_COLOR,
            filled=0,
            width=3
        )
        self.display.draw_line(ne, sw, color=EDGE_COLOR)
        self.display.draw_line(nw, se, color=EDGE_COLOR)

        if isCurrent:
            self.display.draw_circle((screen_x, screen_y), 0.1 * GRID_SIZE, LOCATION_COLOR, fillColor=LOCATION_COLOR)

        for action in actions:
            text_color = TEXT_COLOR
            if qVals[action] < max(qVals.values()): text_color = MUTED_TEXT_COLOR
            valStr = ""
            if action in valStrs:
                valStr = valStrs[action]
            h = -20
            if action == 'north':
                # self.display.draw_polygon( (center, nw, ne), wedge_color, filled = 1, smooth = 0)
                self.display.draw_text(n, text_color, valStr, "Courier", h, "bold", "n")
            if action == 'south':
                # self.display.draw_polygon( (center, sw, se), wedge_color, filled = 1, smooth = 0)
                self.display.draw_text(s, text_color, valStr, "Courier", h, "bold", "s")
            if action == 'east':
                # self.display.draw_polygon( (center, ne, se), wedge_color, filled = 1, smooth = 0)
                self.display.draw_text(e, text_color, valStr, "Courier", h, "bold", "e")
            if action == 'west':
                # self.display.draw_polygon( (center, nw, sw), wedge_color, filled = 1, smooth = 0)
                self.display.draw_text(w, text_color, valStr, "Courier", h, "bold", "w")

    # FIXME: TEST ME OUT YO WTF IS COING ON HERE
    def square(self, pos, size, color, filled, width):
        x, y = pos
        dx, dy = size, size

        coords = [(x - dx, y - dy), (x - dx, y + dy), (x + dx, y + dy), (x + dx, y - dy)]

        return self.display.draw_polygon(coords,
                                         outlineColor=color,
                                         fillColor=color, filled=filled, width=width, smoothed=False)



    def drawsss(self):
        self.count += 2
        print("#"* 10, "drawsss", "#"* 10)
        print(self.display._canvas)
        self.display.draw_circle(
            (262.5, 112.5),
            0.1 * GRID_SIZE,
            outlineColor=LOCATION_COLOR,
            fillColor=LOCATION_COLOR
        )



def getColor(val, minVal, max):
    r, g = 0.0, 0.0
    if val < 0 and minVal < 0:
        r = val * 0.65 / minVal
    if val > 0 and max > 0:
        g = val * 0.65 / max
    return formatColor(r, g, 0.0)


def to_screen(point):
    (gamex, gamey) = point
    x = gamex * GRID_SIZE + MARGIN
    y = (GRID_HEIGHT - gamey - 1) * GRID_SIZE + MARGIN
    return (x, y)


def to_grid(point):
    (x, y) = point
    x = int((y - MARGIN + GRID_SIZE * 0.5) / GRID_SIZE)
    y = int((x - MARGIN + GRID_SIZE * 0.5) / GRID_SIZE)
    print(point, "-->", (x, y))
    return (x, y)
