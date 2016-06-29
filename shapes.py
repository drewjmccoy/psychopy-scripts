# @author Drew McCoy <drewm@alleninstitute.org>
# defines Rectangle, SkeletonNode, SkeletonStim

from psychopy import visual
import math

# a node of a skeleton data structure
# SkeletonNode(position, connections)
class SkeletonNode(object):

    # initializes node
    def __init__(self, position=(0, 0), connections=[]):
        self.position = position
        self.connections = connections


# a shape stimulus
# SkeletonStim(window, root, thickness)
class SkeletonStim(object):

    # class that defines a Rectangle ShapeStim, given two end points
    # Rectangle(window, p0, p1, thickness=20)
    class _Rectangle(object):

        # initializes the Rectangle
        def __init__(self, window, p0=(-100, 0), p1=(100, 0), thickness=20):
            self._rectangle = visual.Rect(win=window,
                                          units="pix",
                                          fillColor="white",
                                          width=self._getWidth(p0, p1),
                                          height=thickness,
                                          pos=self._getPosition(p0, p1),
                                          ori=self._getOrientation(p0, p1))
            self.opacity = 1.0

        def draw(self):
            self._rectangle.draw()

        def setOpacity(self, newOpacity):
            self._rectangle.setOpacity(newOpacity=newOpacity)
            self.opacity = newOpacity

        # returns the width of the Rectangle
        def _getWidth(self, p0, p1):
            result = math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)
            return result

        # returns the position (midpoint) of the Rectangle
        def _getPosition(self, p0, p1):
            # use midpoint formula
            x = (p1[0] + p0[0]) / 2
            y = (p1[1] + p0[1]) / 2
            return (x, y)

        # returns the orientation of the Rectangle in degrees. 0 is up, increasing
        # clockwise
        def _getOrientation(self, p0, p1):
            # get change y and x
            dy = p1[1] - p0[1]
            dx = p1[0] - p0[0]

            # if slope is undefined
            if dx is 0:
                if dy < 0:
                    return 90
                else:
                    return 270

            # get temp radians of orientation (neg b/c psychopy is weird)
            rad = -math.atan2(dy, dx)

            # to degrees
            deg = math.degrees(rad)

            return deg

    # initializes stimulus
    def __init__(self, window, root, stimulus_id, thickness=20):
        self.window = window # window to be drawn on
        self.root = root # root SkeletonNode
        self.stimulus_id = stimulus_id # id of the
        self.thickness = thickness # thickness of the lines
        self.stimulus_type = "shape"

        # list of circles and rectangles that make up the shape
        self._shape_list = []

        # build up shape list
        self._build_shape_list(window=window)

    # draws the SkeletonStim on the window
    def draw(self):
        for i in range(len(self._shape_list)):
            self._shape_list[i].draw()

    def changeOpacity(self, change):
        for shape in self._shape_list:
            shape.setOpacity(shape.opacity + change)

    def setOpacity(self, newOpacity):
        for shape in self._shape_list:
            shape.setOpacity(newOpacity)

    # builds up the shape list with circles and squares
    def _build_shape_list(self, window):
        self._build_shape_list_helper(window, self.root)

    # helps build up shape list with recursion
    def _build_shape_list_helper(self, window, current):
        circle = visual.Circle(win=window,
                               units="pix",
                               radius=(self.thickness / 2),
                               edges=32,
                               fillColor="white",
                               pos=current.position)
        self._shape_list.append(circle)

        for i in range(len(current.connections)):
            rectangle = self._Rectangle(window=window,
                                  p0=current.position,
                                  p1=current.connections[i].position,
                                  thickness=self.thickness)
            self._shape_list.append(rectangle)
            self._build_shape_list_helper(window, current.connections[i])

# a motion stimulus
# MotionStim(self, window, units, coherence, fieldSize, color, dotSize, dotLife,
#            noiseDots, signalDots, speed, nDots, fieldShape, dir, stimulus_id)
class MotionStim:

    def __init__(self, window, units, coherence, fieldSize, color, dotSize, dotLife,
                 noiseDots, signalDots, speed, nDots, fieldShape, dir, stimulus_id):
        self.dots = visual.DotStim(win=window,
                                   units=units,
                                   coherence=coherence,
                                   fieldSize=fieldSize,
                                   color=color,
                                   dotSize=dotSize,
                                   dotLife=dotLife,
                                   noiseDots=noiseDots,
                                   signalDots=signalDots,
                                   speed=speed,
                                   nDots=nDots,
                                   fieldShape=fieldShape,
                                   dir=dir)
        self.stimulus_id = stimulus_id
        self.stimulus_type = "motion"

    def draw(self):
        self.dots.draw()


class MotionStimTemp:

    class _Dot:

        def __init__(self, window, radius, position, direction, speed, field_size):
            self.window = window
            self.radius = radius
            self.position = position
            self.direction = direction
            self.speed = speed
            self.dot = visual.Circle(win=window,
                                     units="pix",
                                     radius=self.radius,
                                     edges=32,
                                     fillColor="white",
                                     pos=self.position)

        def draw(self):
            self.dot.draw()
            self._update_position()

        def _update_position(self):
            pass

    def __init__(self, window, n_dots, coherence, field_size, dot_size, speed):
        self.window = window
        self.n_dots = n_dots
        self.coherence = coherence
        self.field_size = field_size
        self.dot_size = dot_size
        self.speed = speed

        self.dots = self._get_dots(window=self.window,
                                   n_dots=self.n_dots,
                                   field_size=self.field_size,
                                   dot_size=self.dot_size,
                                   speed=self.speed)

    def draw(self):
        for dot in self.dots:
            dot.draw()

    def _get_dots(self, window, n_dots, field_size, dot_size, speed):
        result = []
        for i in range(n_dots):
            dot = self._Dot(window=window,
                      radius=dot_size/2,
                      position=(0,0), # randomize
                      direction=0, # randomize
                      speed=speed,
                      field_size=field_size)
            result.append(dot)

        return result
