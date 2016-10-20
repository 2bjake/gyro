from collections import namedtuple
Point = namedtuple('Point', 'x y')

def point_left(point):
    return Point(point.x - 1, point.y)

def point_right(point):
    return Point(point.x + 1, point.y)

def point_up(point):
    return Point(point.x, point.y + 1)

def point_down(point):
    return Point(point.x, point.y - 1)