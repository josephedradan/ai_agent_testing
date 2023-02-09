# graphicsDisplay.py
# ------------------
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

# Most code by Dan Klein and John Denero written or rewritten for cs188, UC Berkeley.
# Some code from a Pacman implementation by LiveWires, and used / modified with permission.

from __future__ import annotations

import math
import time
from typing import List
from typing import TYPE_CHECKING
from typing import Union

from common.graphics.gui import GUI
from common.graphics.gui_tkinter import GUITkinter
from common.graphics.gui_tkinter import colorToVector
from common.graphics.gui_tkinter import formatColor
from common.graphics.gui_tkinter import writePostscript
from pacman.agent import Agent
from pacman.agent.container_state import ContainerState
from pacman.game.directions import Directions
from pacman.game.layoutpacman import LayoutPacman
from pacman.game.player import Player
from pacman.game.type_player import TypePlayer
from pacman.graphics.graphics_pacman import GraphicsPacman

if TYPE_CHECKING:
    from common.state_data_pacman import StateDataPacman

###########################
#  GRAPHICS DISPLAY CODE  #
###########################


DEFAULT_GRID_SIZE = 30.0
INFO_PANE_HEIGHT = 35
BACKGROUND_COLOR = formatColor(0, 0, 0)
WALL_COLOR = formatColor(0.0 / 255.0, 51.0 / 255.0, 255.0 / 255.0)
INFO_PANE_COLOR = formatColor(.4, .4, 0)
SCORE_COLOR = formatColor(.9, .9, .9)
PACMAN_OUTLINE_WIDTH = 2
PACMAN_CAPTURE_OUTLINE_WIDTH = 4

GHOST_COLORS: List = []
GHOST_COLORS.append(formatColor(.9, 0, 0))  # Red
GHOST_COLORS.append(formatColor(0, .3, .9))  # Blue
GHOST_COLORS.append(formatColor(.98, .41, .07))  # Orange
GHOST_COLORS.append(formatColor(.1, .75, .7))  # Green
GHOST_COLORS.append(formatColor(1.0, 0.6, 0.0))  # Yellow
GHOST_COLORS.append(formatColor(.4, 0.13, 0.91))  # Purple

TEAM_COLORS = GHOST_COLORS[:2]

GHOST_SHAPE = [
    (0, 0.3),
    (0.25, 0.75),
    (0.5, 0.3),
    (0.75, 0.75),
    (0.75, -0.5),
    (0.5, -0.75),
    (-0.5, -0.75),
    (-0.75, -0.5),
    (-0.75, 0.75),
    (-0.5, 0.3),
    (-0.25, 0.75)
]
GHOST_SIZE = 0.65
SCARED_COLOR = formatColor(1, 1, 1)

GHOST_VEC_COLORS = list(map(colorToVector, GHOST_COLORS))

PACMAN_COLOR = formatColor(255.0 / 255.0, 255.0 / 255.0, 61.0 / 255)
PACMAN_SCALE = 0.5
# pacman_speed = 0.25

# Food
FOOD_COLOR = formatColor(1, 1, 1)
FOOD_SIZE = 0.1

# Laser
LASER_COLOR = formatColor(1, 0, 0)
LASER_SIZE = 0.02

# Capsule graphics
CAPSULE_COLOR = formatColor(1, 1, 1)
CAPSULE_SIZE = 0.25

# Drawing walls
WALL_RADIUS = 0.15


class InfoPane:
    def __init__(self, gui: GUI, layout: LayoutPacman, gridSize: float):

        # TODO JOSEPH CUSTOM
        self.gui = gui

        #####

        self.gridSize: float = gridSize
        self.width = (layout.width) * gridSize
        self.base = (layout.height + 1) * gridSize
        self.height = INFO_PANE_HEIGHT
        self.fontSize = 24
        self.textColor = PACMAN_COLOR
        self._draw_pane()

    def _to_screen(self, pos, y=None):
        """
          Translates a point relative from the bottom left of the info pane.
        """
        if y == None:
            x, y = pos
        else:
            x = pos

        x = self.gridSize + x  # Margin
        y = self.base + y
        return x, y

    def _draw_pane(self):
        self.scoreText = self.gui.draw_text(
            self._to_screen(0, 0),
            self.textColor,
            "SCORE:    0",
            "Times",
            self.fontSize, "bold"
        )

    def _initialize_ghost_distances(self, distances):
        self.ghostDistanceText = []

        size = 20
        if self.width < 240:
            size = 12
        if self.width < 160:
            size = 10

        for i, d in enumerate(distances):
            t = self.gui.draw_text(
                self._to_screen(self.width / 2 + self.width / 8 * i, 0),
                GHOST_COLORS[i + 1],
                d,
                "Times",
                size,
                "bold"
            )

            self.ghostDistanceText.append(t)

    def updateScore(self, score):
        self.gui.change_text(self.scoreText, "SCORE: % 4d" % score)

    def setTeam(self, isBlue):  # FIXME: USE ME
        text = "RED TEAM"
        if isBlue:
            text = "BLUE TEAM"

        self.teamText = self.gui.draw_text(self._to_screen(
            300, 0), self.textColor, text, "Times", self.fontSize, "bold")

    def update_ghost_distances(self, distances):
        if len(distances) == 0:
            return
        if 'ghostDistanceText' not in dir(self):
            self._initialize_ghost_distances(distances)
        else:
            for i, d in enumerate(distances):
                self.gui.change_text(self.ghostDistanceText[i], d)

    def drawGhost(self):
        pass

    def drawPacman(self):
        pass

    def drawWarning(self):
        pass

    def clearIcon(self):
        pass

    def updateMessage(self, message):
        pass

    def clearMessage(self):
        pass


class GraphicsPacmanGUI(GraphicsPacman):
    def __init__(self,
                 gui: Union[GUI, None] = GUITkinter(),
                 time_frame: float = 0.0,
                 zoom: float = 1.0,
                 capture=False,
                 ):
        super().__init__(gui, time_frame, zoom)
        self.have_window = 0
        self.currentGhostImages = {}
        self.pacmanImage = None
        self.zoom = zoom
        self.gridSize = DEFAULT_GRID_SIZE * zoom
        self.capture = capture

        #####

        self.layout: Union[LayoutPacman, None] = None
        self.width: Union[int, None] = None
        self.height: Union[int, None] = None
        #####

        # TODO JOSEPH CUSTOM
        # self.gui= None

    def get_display(self) -> GUI:
        return self.gui

    def checkNullDisplay(self):
        return False

    def initialize(self, state_data: StateDataPacman, isBlue=False):
        self.isBlue = isBlue
        self._startGraphics(state_data)

        # self.drawDistributions(state_pacman)
        self.distributionImages = None  # Initialized lazily
        self.drawStaticObjects(state_data)
        self._drawAgentObjects(state_data)

        # Information
        self.previousState = state_data

    def _startGraphics(self, state):
        self.layout = state.layout
        layout = self.layout

        self.width = layout.width
        self.height = layout.height
        self._make_window(self.width, self.height)
        self.infoPane = InfoPane(self.gui, layout, self.gridSize)
        self.currentState = layout

    def drawDistributions(self, state):
        walls = state.layout.walls
        dist = []
        for x in range(walls.width):
            distx = []
            dist.append(distx)
            for y in range(walls.height):
                (screen_x, screen_y) = self.to_screen((x, y))
                block = self.gui.draw_square((screen_x, screen_y),
                                             0.5 * self.gridSize,
                                             color=BACKGROUND_COLOR,
                                             filled=1, behind=2)
                distx.append(block)
        self.distributionImages = dist

    def drawStaticObjects(self, state):
        layout: LayoutPacman = self.layout
        self.drawWalls(layout.walls)
        self.food = self.drawFood(layout.food)
        self.capsules = self.drawCapsules(layout.list_capsule)
        self.gui.refresh()

    def _drawAgentObjects(self, state):
        self.dict_k_agent_v_tuple__container_state__image = {}  # (container_state, image)
        for index, tuple__player__container_state in enumerate(state.dict_k_player_v_container_state.items()):

            player = tuple__player__container_state[0]
            agent = player.get_agent()
            container_state = tuple__player__container_state[1]

            if player.get_type_player() == TypePlayer.PACMAN:
                image = self._draw_pacman(container_state, index)
            else:
                image = self._draw_ghost(container_state, index)

            self.dict_k_agent_v_tuple__container_state__image[agent] = (container_state, image)

        self.gui.refresh()

    def _swap_images(self, agent: Agent, container_state_new: ContainerState):
        """
        Changes an image from a ghost to a pacman or vis versa (for capture)

        JOSEPH NOTES:
            LIKE TAG????????????????????????

        """
        container_state_previous, image_previous = self.dict_k_agent_v_tuple__container_state__image.get(agent)

        for item in image_previous:
            self.gui.remove_from_screen(item)

        if container_state_new.is_pacman:
            image = self._draw_pacman(container_state_new, agentIndex)
            self.dict_k_agent_v_tuple__container_state__image[agentIndex] = (container_state_new, image)
        else:
            image = self._draw_ghost(container_state_new, agentIndex)
            self.dict_k_agent_v_tuple__container_state__image[agentIndex] = (container_state_new, image)

        self.gui.refresh()

    def update(self, state_data_pacman: StateDataPacman):

        agent: Agent = state_data_pacman._agentMoved
        player: Player = state_data_pacman.get_player_from_agent(agent)

        container_state: ContainerState = state_data_pacman.dict_k_player_v_container_state.get(agent)

        # TODO: THIS FUNCTION IS UNNEEDED BECAUSE JOSEPH USE DICT
        # if self.dict_k_agent_v_tuple__container_state__image[agent][0].is_pacman != container_state.is_pacman:
        #     self._swap_images(agent, container_state)

        container_state_previous, image_previous = self.dict_k_agent_v_tuple__container_state__image.get(agent)

        if player.get_type_player() == TypePlayer.PACMAN:
            self.animatePacman(container_state, container_state_previous, image_previous)
        else:
            self.moveGhost(container_state, player, container_state_previous, image_previous)

        self.dict_k_agent_v_tuple__container_state__image[agent] = (container_state, image_previous)

        if state_data_pacman._foodEaten != None:
            self.removeFood(state_data_pacman._foodEaten, self.food)
        if state_data_pacman._capsuleEaten != None:
            self.removeCapsule(state_data_pacman._capsuleEaten, self.capsules)
        self.infoPane.updateScore(state_data_pacman.score)

        if 'ghostDistances' in dir(state_data_pacman):
            print(state_data_pacman)
            print(type(state_data_pacman))

            raise Exception("FUCK ME WTF WE GOT HERE")
            self.infoPane.update_ghost_distances(state_data_pacman.ghostDistances)

    def _make_window(self, width, height):
        grid_width = (width - 1) * self.gridSize
        grid_height = (height - 1) * self.gridSize
        screen_width = 2 * self.gridSize + grid_width
        screen_height = 2 * self.gridSize + grid_height + INFO_PANE_HEIGHT

        # TODO: HERE JOSEPH
        self.gui.initialize_graphics(
            screen_width,
            screen_height,
            BACKGROUND_COLOR,
            "CS188 Pacman")

    def _draw_pacman(self, container_state: ContainerState, index) -> List:

        position = self.getPosition(container_state)
        screen_point = self.to_screen(position)
        endpoints = self.getEndpoints(self.getDirection(container_state))

        width = PACMAN_OUTLINE_WIDTH
        outlineColor = PACMAN_COLOR
        fillColor = PACMAN_COLOR

        if self.capture:
            outlineColor = TEAM_COLORS[index % 2]
            fillColor = GHOST_COLORS[index]
            width = PACMAN_CAPTURE_OUTLINE_WIDTH

        return [self.gui.draw_circle(screen_point,
                                     PACMAN_SCALE * self.gridSize,
                                     fillColor=fillColor, outlineColor=outlineColor,
                                     endpoints=endpoints,
                                     width=width)
                ]

    def _draw_ghost(self, container_state: ContainerState, agentIndex) -> List:

        pos = self.getPosition(container_state)
        dir = self.getDirection(container_state)

        (screen_x, screen_y) = (self.to_screen(pos))
        coords = []
        for (x, y) in GHOST_SHAPE:
            coords.append((x * self.gridSize * GHOST_SIZE + screen_x,
                           y * self.gridSize * GHOST_SIZE + screen_y))

        colour = self.getGhostColor(container_state, agentIndex)
        body = self.gui.draw_polygon(coords, colour, filled=1)
        WHITE = formatColor(1.0, 1.0, 1.0)
        BLACK = formatColor(0.0, 0.0, 0.0)

        dx = 0
        dy = 0
        if dir == 'North':
            dy = -0.2
        if dir == 'South':
            dy = 0.2
        if dir == 'East':
            dx = 0.2
        if dir == 'West':
            dx = -0.2
        leftEye = self.gui.draw_circle((screen_x + self.gridSize * GHOST_SIZE * (-0.3 + dx / 1.5), screen_y -
                                        self.gridSize * GHOST_SIZE * (0.3 - dy / 1.5)),
                                       self.gridSize * GHOST_SIZE * 0.2, WHITE,
                                       WHITE)
        rightEye = self.gui.draw_circle((screen_x + self.gridSize * GHOST_SIZE * (0.3 + dx / 1.5), screen_y -
                                         self.gridSize * GHOST_SIZE * (0.3 - dy / 1.5)),
                                        self.gridSize * GHOST_SIZE * 0.2, WHITE,
                                        WHITE)
        leftPupil = self.gui.draw_circle((screen_x + self.gridSize * GHOST_SIZE * (-0.3 + dx), screen_y -
                                          self.gridSize * GHOST_SIZE * (0.3 - dy)),
                                         self.gridSize * GHOST_SIZE * 0.08, BLACK, BLACK)
        rightPupil = self.gui.draw_circle((screen_x + self.gridSize * GHOST_SIZE * (0.3 + dx), screen_y -
                                           self.gridSize * GHOST_SIZE * (0.3 - dy)),
                                          self.gridSize * GHOST_SIZE * 0.08, BLACK, BLACK)
        ghostImageParts = []
        ghostImageParts.append(body)
        ghostImageParts.append(leftEye)
        ghostImageParts.append(rightEye)
        ghostImageParts.append(leftPupil)
        ghostImageParts.append(rightPupil)

        return ghostImageParts

    def getEndpoints(self, direction, position=(0, 0)):
        x, y = position
        pos = x - int(x) + y - int(y)
        width = 30 + 80 * math.sin(math.pi * pos)

        delta = width / 2
        if (direction == 'West'):
            endpoints = (180 + delta, 180 - delta)
        elif (direction == 'North'):
            endpoints = (90 + delta, 90 - delta)
        elif (direction == 'South'):
            endpoints = (270 + delta, 270 - delta)
        else:
            endpoints = (0 + delta, 0 - delta)
        return endpoints

    def movePacman(self, position, direction, image):
        screenPosition = self.to_screen(position)
        endpoints = self.getEndpoints(direction, position)
        r = PACMAN_SCALE * self.gridSize
        self.gui.move_circle(image[0], screenPosition, r, endpoints)
        self.gui.refresh()

    def animatePacman(self, pacman, prevPacman, image):
        if self.time_frame < 0:
            print('Press any key to step forward, "q" to play')
            keys = self.gui.get_wait_for_keys()
            if 'q' in keys:
                self.time_frame = 0.1
        if self.time_frame > 0.01 or self.time_frame < 0:
            start = time.time()
            fx, fy = self.getPosition(prevPacman)
            px, py = self.getPosition(pacman)
            frames = 4.0
            for i in range(1, int(frames) + 1):
                pos = px * i / frames + fx * \
                      (frames - i) / frames, py * i / frames + fy * (frames - i) / frames
                self.movePacman(pos, self.getDirection(pacman), image)
                self.gui.refresh()
                self.gui.sleep(abs(self.time_frame) / frames)
        else:
            self.movePacman(self.getPosition(pacman),
                            self.getDirection(pacman), image)
        self.gui.refresh()

    def getGhostColor(self, ghost, ghostIndex):
        if ghost.scaredTimer > 0:
            return SCARED_COLOR
        else:
            return GHOST_COLORS[ghostIndex]

    def moveEyes(self, pos, dir, eyes):
        (screen_x, screen_y) = (self.to_screen(pos))
        dx = 0
        dy = 0
        if dir == 'North':
            dy = -0.2
        if dir == 'South':
            dy = 0.2
        if dir == 'East':
            dx = 0.2
        if dir == 'West':
            dx = -0.2
        self.gui.move_circle(eyes[0], (screen_x + self.gridSize * GHOST_SIZE * (-0.3 + dx / 1.5), screen_y -
                                       self.gridSize * GHOST_SIZE * (0.3 - dy / 1.5)),
                             self.gridSize * GHOST_SIZE * 0.2)
        self.gui.move_circle(eyes[1], (screen_x + self.gridSize * GHOST_SIZE * (0.3 + dx / 1.5), screen_y -
                                       self.gridSize * GHOST_SIZE * (0.3 - dy / 1.5)),
                             self.gridSize * GHOST_SIZE * 0.2)
        self.gui.move_circle(eyes[2], (screen_x + self.gridSize * GHOST_SIZE * (-0.3 + dx), screen_y -
                                       self.gridSize * GHOST_SIZE * (0.3 - dy)),
                             self.gridSize * GHOST_SIZE * 0.08)
        self.gui.move_circle(eyes[3], (screen_x + self.gridSize * GHOST_SIZE * (0.3 + dx), screen_y -
                                       self.gridSize * GHOST_SIZE * (0.3 - dy)),
                             self.gridSize * GHOST_SIZE * 0.08)

    def moveGhost(self, container_state, player: Player, container_state_previous, image_previous):
        old_x, old_y = self.to_screen(self.getPosition(container_state_previous))
        new_x, new_y = self.to_screen(self.getPosition(container_state))
        delta = new_x - old_x, new_y - old_y

        for ghostImagePart in image_previous:
            self.gui.move_by(ghostImagePart, delta)
        self.gui.refresh()

        if container_state.scaredTimer > 0:
            color = SCARED_COLOR
        else:
            color = GHOST_COLORS[player.index]

        self.gui.edit(image_previous[0], ('fill', color), ('outline', color))
        self.moveEyes(self.getPosition(container_state),
                      self.getDirection(container_state), image_previous[-4:])
        self.gui.refresh()

    def getPosition(self, agentState):
        if agentState.container_position_vector == None:
            return (-1000, -1000)
        return agentState.get_position()

    def getDirection(self, agentState):
        if agentState.container_position_vector == None:
            return Directions.STOP
        return agentState.container_position_vector.get_direction()

    def finish(self):
        self.gui.end_graphics()

    def to_screen(self, point):
        (x, y) = point
        # y = self.height - y
        x = (x + 1) * self.gridSize
        y = (self.height - y) * self.gridSize
        return (x, y)

    # Fixes some TK issue with off-center circles
    def to_screen2(self, point):
        (x, y) = point
        # y = self.height - y
        x = (x + 1) * self.gridSize
        y = (self.height - y) * self.gridSize
        return (x, y)

    def drawWalls(self, wallMatrix):
        wallColor = WALL_COLOR
        for xNum, x in enumerate(wallMatrix):
            if self.capture and (xNum * 2) < wallMatrix.width:
                wallColor = TEAM_COLORS[0]
            if self.capture and (xNum * 2) >= wallMatrix.width:
                wallColor = TEAM_COLORS[1]

            for yNum, cell in enumerate(x):
                if cell:  # There's a wall here
                    pos = (xNum, yNum)
                    screen = self.to_screen(pos)
                    screen2 = self.to_screen2(pos)

                    # draw each quadrant of the square based on adjacent walls
                    wIsWall = self.isWall(xNum - 1, yNum, wallMatrix)
                    eIsWall = self.isWall(xNum + 1, yNum, wallMatrix)
                    nIsWall = self.isWall(xNum, yNum + 1, wallMatrix)
                    sIsWall = self.isWall(xNum, yNum - 1, wallMatrix)
                    nwIsWall = self.isWall(xNum - 1, yNum + 1, wallMatrix)
                    swIsWall = self.isWall(xNum - 1, yNum - 1, wallMatrix)
                    neIsWall = self.isWall(xNum + 1, yNum + 1, wallMatrix)
                    seIsWall = self.isWall(xNum + 1, yNum - 1, wallMatrix)

                    # NE quadrant
                    if (not nIsWall) and (not eIsWall):
                        # inner circle
                        self.gui.draw_circle(screen2, WALL_RADIUS * self.gridSize,
                                             wallColor, wallColor, (0, 91), 'arc')
                    if (nIsWall) and (not eIsWall):
                        # vertical line
                        self.gui.draw_line(add(screen, (self.gridSize * WALL_RADIUS, 0)), add(screen,
                                                                                              (
                                                                                                  self.gridSize * WALL_RADIUS,
                                                                                                  self.gridSize * (
                                                                                                      -0.5) - 1)),
                                           wallColor)
                    if (not nIsWall) and (eIsWall):
                        # horizontal line
                        self.gui.draw_line(add(screen, (0, self.gridSize * (-1) * WALL_RADIUS)), add(screen,
                                                                                                     (
                                                                                                         self.gridSize * 0.5 + 1,
                                                                                                         self.gridSize * (
                                                                                                             -1) * WALL_RADIUS)),
                                           wallColor)
                    if (nIsWall) and (eIsWall) and (not neIsWall):
                        # outer circle
                        self.gui.draw_circle(
                            add(screen2, (self.gridSize * 2 * WALL_RADIUS, self.gridSize * (-2) * WALL_RADIUS)),
                            WALL_RADIUS * self.gridSize - 1, wallColor, wallColor, (180, 271), 'arc')
                        self.gui.draw_line(
                            add(screen, (self.gridSize * 2 * WALL_RADIUS - 1, self.gridSize * (-1) * WALL_RADIUS)),
                            add(screen, (self.gridSize * 0.5 + 1, self.gridSize * (-1) * WALL_RADIUS)), wallColor)
                        self.gui.draw_line(
                            add(screen, (self.gridSize * WALL_RADIUS, self.gridSize * (-2) * WALL_RADIUS + 1)),
                            add(screen, (self.gridSize * WALL_RADIUS, self.gridSize * (-0.5))), wallColor)

                    # NW quadrant
                    if (not nIsWall) and (not wIsWall):
                        # inner circle
                        self.gui.draw_circle(screen2, WALL_RADIUS * self.gridSize,
                                             wallColor, wallColor, (90, 181), 'arc')
                    if (nIsWall) and (not wIsWall):
                        # vertical line
                        self.gui.draw_line(add(screen, (self.gridSize * (-1) * WALL_RADIUS, 0)), add(screen,
                                                                                                     (
                                                                                                         self.gridSize * (
                                                                                                             -1) * WALL_RADIUS,
                                                                                                         self.gridSize * (
                                                                                                             -0.5) - 1)),
                                           wallColor)
                    if (not nIsWall) and (wIsWall):
                        # horizontal line
                        self.gui.draw_line(add(screen, (0, self.gridSize * (-1) * WALL_RADIUS)), add(screen,
                                                                                                     (
                                                                                                         self.gridSize * (
                                                                                                             -0.5) - 1,
                                                                                                         self.gridSize * (
                                                                                                             -1) * WALL_RADIUS)),
                                           wallColor)
                    if (nIsWall) and (wIsWall) and (not nwIsWall):
                        # outer circle
                        self.gui.draw_circle(
                            add(screen2, (self.gridSize * (-2) * WALL_RADIUS, self.gridSize * (-2) * WALL_RADIUS)),
                            WALL_RADIUS * self.gridSize - 1, wallColor, wallColor, (270, 361), 'arc')
                        self.gui.draw_line(
                            add(screen, (self.gridSize * (-2) * WALL_RADIUS + 1, self.gridSize * (-1) * WALL_RADIUS)),
                            add(screen, (self.gridSize * (-0.5), self.gridSize * (-1) * WALL_RADIUS)), wallColor)
                        self.gui.draw_line(
                            add(screen, (self.gridSize * (-1) * WALL_RADIUS, self.gridSize * (-2) * WALL_RADIUS + 1)),
                            add(screen, (self.gridSize * (-1) * WALL_RADIUS, self.gridSize * (-0.5))), wallColor)

                    # SE quadrant
                    if (not sIsWall) and (not eIsWall):
                        # inner circle
                        self.gui.draw_circle(screen2, WALL_RADIUS * self.gridSize,
                                             wallColor, wallColor, (270, 361), 'arc')
                    if (sIsWall) and (not eIsWall):
                        # vertical line
                        self.gui.draw_line(add(screen, (self.gridSize * WALL_RADIUS, 0)), add(screen,
                                                                                              (
                                                                                                  self.gridSize * WALL_RADIUS,
                                                                                                  self.gridSize * (
                                                                                                      0.5) + 1)),
                                           wallColor)
                    if (not sIsWall) and (eIsWall):
                        # horizontal line
                        self.gui.draw_line(add(screen, (0, self.gridSize * (1) * WALL_RADIUS)), add(screen,
                                                                                                    (
                                                                                                        self.gridSize * 0.5 + 1,
                                                                                                        self.gridSize * (
                                                                                                            1) * WALL_RADIUS)),
                                           wallColor)
                    if (sIsWall) and (eIsWall) and (not seIsWall):
                        # outer circle
                        self.gui.draw_circle(
                            add(screen2, (self.gridSize * 2 * WALL_RADIUS, self.gridSize * (2) * WALL_RADIUS)),
                            WALL_RADIUS * self.gridSize - 1, wallColor, wallColor, (90, 181), 'arc')
                        self.gui.draw_line(
                            add(screen, (self.gridSize * 2 * WALL_RADIUS - 1, self.gridSize * (1) * WALL_RADIUS)),
                            add(screen, (self.gridSize * 0.5, self.gridSize * (1) * WALL_RADIUS)), wallColor)
                        self.gui.draw_line(
                            add(screen, (self.gridSize * WALL_RADIUS, self.gridSize * (2) * WALL_RADIUS - 1)),
                            add(screen, (self.gridSize * WALL_RADIUS, self.gridSize * (0.5))), wallColor)

                    # SW quadrant
                    if (not sIsWall) and (not wIsWall):
                        # inner circle
                        self.gui.draw_circle(screen2, WALL_RADIUS * self.gridSize,
                                             wallColor, wallColor, (180, 271), 'arc')
                    if (sIsWall) and (not wIsWall):
                        # vertical line
                        self.gui.draw_line(add(screen, (self.gridSize * (-1) * WALL_RADIUS, 0)), add(screen,
                                                                                                     (
                                                                                                         self.gridSize * (
                                                                                                             -1) * WALL_RADIUS,
                                                                                                         self.gridSize * (
                                                                                                             0.5) + 1)),
                                           wallColor)
                    if (not sIsWall) and (wIsWall):
                        # horizontal line
                        self.gui.draw_line(add(screen, (0, self.gridSize * (1) * WALL_RADIUS)), add(screen,
                                                                                                    (
                                                                                                        self.gridSize * (
                                                                                                            -0.5) - 1,
                                                                                                        self.gridSize * (
                                                                                                            1) * WALL_RADIUS)),
                                           wallColor)
                    if (sIsWall) and (wIsWall) and (not swIsWall):
                        # outer circle
                        self.gui.draw_circle(
                            add(screen2, (self.gridSize * (-2) * WALL_RADIUS, self.gridSize * (2) * WALL_RADIUS)),
                            WALL_RADIUS * self.gridSize - 1, wallColor, wallColor, (0, 91), 'arc')
                        self.gui.draw_line(
                            add(screen, (self.gridSize * (-2) * WALL_RADIUS + 1, self.gridSize * (1) * WALL_RADIUS)),
                            add(screen, (self.gridSize * (-0.5), self.gridSize * (1) * WALL_RADIUS)), wallColor)
                        self.gui.draw_line(
                            add(screen, (self.gridSize * (-1) * WALL_RADIUS, self.gridSize * (2) * WALL_RADIUS - 1)),
                            add(screen, (self.gridSize * (-1) * WALL_RADIUS, self.gridSize * (0.5))), wallColor)

    def isWall(self, x, y, walls):
        if x < 0 or y < 0:
            return False
        if x >= walls.width or y >= walls.height:
            return False
        return walls[x][y]

    def drawFood(self, foodMatrix):
        foodImages = []
        color = FOOD_COLOR
        for xNum, x in enumerate(foodMatrix):
            if self.capture and (xNum * 2) <= foodMatrix.width:
                color = TEAM_COLORS[0]
            if self.capture and (xNum * 2) > foodMatrix.width:
                color = TEAM_COLORS[1]
            imageRow = []
            foodImages.append(imageRow)
            for yNum, cell in enumerate(x):
                if cell:  # There's food here
                    screen = self.to_screen((xNum, yNum))
                    dot = self.gui.draw_circle(screen,
                                               FOOD_SIZE * self.gridSize,
                                               outlineColor=color, fillColor=color,
                                               width=1)
                    imageRow.append(dot)
                else:
                    imageRow.append(None)
        return foodImages

    def drawCapsules(self, capsules):
        capsuleImages = {}
        for capsule in capsules:
            (screen_x, screen_y) = self.to_screen(capsule)
            dot = self.gui.draw_circle((screen_x, screen_y),
                                       CAPSULE_SIZE * self.gridSize,
                                       outlineColor=CAPSULE_COLOR,
                                       fillColor=CAPSULE_COLOR,
                                       width=1)
            capsuleImages[capsule] = dot
        return capsuleImages

    def removeFood(self, cell, foodImages):
        x, y = cell
        self.gui.remove_from_screen(foodImages[x][y])

    def removeCapsule(self, cell, capsuleImages):
        x, y = cell
        self.gui.remove_from_screen(capsuleImages[(x, y)])

    def drawExpandedCells(self, cells):
        """
        Draws an overlay of expanded grid positions for search agents
        """
        n = float(len(cells))
        baseColor = [1.0, 0.0, 0.0]
        self.clearExpandedCells()
        self.expandedCells = []
        for k, cell in enumerate(cells):
            screenPos = self.to_screen(cell)
            cellColor = formatColor(
                *[(n - k) * c * .5 / n + .25 for c in baseColor])
            block = self.gui.draw_square(screenPos,
                                         0.5 * self.gridSize,
                                         color=cellColor,
                                         filled=1, behind=2)
            self.expandedCells.append(block)
            if self.time_frame < 0:
                self.gui.refresh()

    def clearExpandedCells(self):
        if 'expandedCells' in dir(self) and len(self.expandedCells) > 0:
            for cell in self.expandedCells:
                self.gui.remove_from_screen(cell)

    def updateDistributions(self, distributions):
        "Draws an player's belief distributions"
        # copy all distributions so we don't change their state_pacman
        distributions = [x.copy() for x in distributions]
        if self.distributionImages == None:
            self.drawDistributions(self.previousState)
        for x in range(len(self.distributionImages)):
            for y in range(len(self.distributionImages[0])):
                image = self.distributionImages[x][y]
                weights = [dist[(x, y)] for dist in distributions]

                if sum(weights) != 0:
                    pass
                # Fog of war
                color = [0.0, 0.0, 0.0]
                colors = GHOST_VEC_COLORS[1:]  # With Pacman
                if self.capture:
                    colors = GHOST_VEC_COLORS
                for weight, gcolor in zip(weights, colors):
                    color = [min(1.0, c + 0.95 * g * weight ** .3)
                             for c, g in zip(color, gcolor)]
                self.gui.change_color(image, formatColor(*color))
        self.gui.refresh()


# TODO: WTF IS THIS SHIT
class FirstPersonGraphicsPacman(GraphicsPacmanGUI):
    # def __init__(self, zoom=1.0, showGhosts=True, capture=False, frameTime=0):
    #     GraphicsPacmanDisplay.__init__(self, zoom, time_frame=frameTime)
    #     self.showGhosts = showGhosts
    #     self.capture = capture

    def initialize(self, state_data: StateDataPacman, isBlue=False):

        # TODO: CHECK SOLUTION
        self.showGhosts = True

        ####

        self.isBlue = isBlue
        GraphicsPacmanGUI._startGraphics(self, state_data)
        # Initialize distribution images
        walls = state_data.layout.walls
        dist = []
        self.layout = state_data.layout

        # Draw the rest
        self.distributionImages = None  # initialize lazily
        self.drawStaticObjects(state_data)
        self._drawAgentObjects(state_data)

        # Information
        self.previousState = state_data

    def lookAhead(self, config, state):
        if config.get_direction() == 'Stop':
            return
        else:
            pass
            # Draw relevant ghosts
            allGhosts = state.get_list_container_state_ghost()
            visibleGhosts = state.getVisibleGhosts()
            for i, ghost in enumerate(allGhosts):
                if ghost in visibleGhosts:
                    self._draw_ghost(ghost, i)
                else:
                    self.currentGhostImages[i] = None

    def getGhostColor(self, ghost, ghostIndex):
        return GHOST_COLORS[ghostIndex]

    def getPosition(self, ghostState):
        if not self.showGhosts and not ghostState.is_pacman and ghostState.get_position()[1] > 1:
            return (-1000, -1000)
        else:
            return GraphicsPacmanGUI.getPosition(self, ghostState)


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


# Saving graphical output
# -----------------------
# Note: to make an animated gif from this postscript output, try the command:
# convert -delay 7 -loop 1 -compress lzw -layers optimize frame* out.gif
# convert is part of imagemagick (freeware)

SAVE_POSTSCRIPT = False
POSTSCRIPT_OUTPUT_DIR = 'frames'
FRAME_NUMBER = 0
import os


def saveFrame():
    "Saves the current graphical output as a postscript file"
    global SAVE_POSTSCRIPT, FRAME_NUMBER, POSTSCRIPT_OUTPUT_DIR
    if not SAVE_POSTSCRIPT:
        return
    if not os.path.exists(POSTSCRIPT_OUTPUT_DIR):
        os.mkdir(POSTSCRIPT_OUTPUT_DIR)
    name = os.path.join(POSTSCRIPT_OUTPUT_DIR, 'frame_%08d.ps' % FRAME_NUMBER)
    FRAME_NUMBER += 1
    writePostscript(name)  # writes the current canvas
