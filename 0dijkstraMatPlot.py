"""
@author Nick Waggoner
Date Created: 04-04-2022
Python Version 3.9
0dijkstraMatPlot.py
"""

import matplotlib.pyplot as plt
from heapq import heapify, heappop, heappush
import numpy as np

# wall coords - ((x1,x2), (y1,y2))
wall_coords = [
    ((+9.5750e+00, +9.5750e+00), (-1.1525e+01, +8.3250e+00)),   # right
    ((+9.5750e+00, +3.1250e+00), (+8.3250e+00, +8.3250e+00)),   # top
    ((+9.5750e+00, +3.1250e+00), (-1.1525e+01, -1.1525e+01)),   # bottom
    ((+3.1250e+00, +3.1250e+00), (-1.1525e+01, +8.3250e+00)),   # Left
    ((+5.5000e+00, +5.5000e+00), (-1.0175e+01, -1.1500e+01)),
    ((+8.3000e+00, +8.3000e+00), (-1.0100e+01, -1.1475e+01)),
    ((+4.4750e+00, +6.9000e+00), (-1.0150e+01, -1.0150e+01)),
    ((+6.8750e+00, +6.8750e+00), (-1.0125e+01, -8.7500e+00)),
    ((+5.7750e+00, +8.1000e+00), (-8.7500e+00, -8.7500e+00)),
    ((+4.4500e+00, +9.5500e+00), (-7.5000e+00, -7.5000e+00)),
    ((+4.4250e+00, +4.4250e+00), (-8.6250e+00, -6.1250e+00)),
    ((+5.6500e+00, +8.1000e+00), (-6.0751e+00, -6.0751e+00)),
    ((+5.6500e+00, +5.6500e+00), (-6.0750e+00, -4.9250e+00)),
    ((+5.6750e+00, +3.2000e+00), (-4.9251e+00, -4.9251e+00)),
    ((+8.2250e+00, +9.5750e+00), (-4.8750e+00, -4.8750e+00)),
    ((+6.9250e+00, +6.9250e+00), (-6.0250e+00, -2.2750e+00)),
    ((+6.9250e+00, +8.1250e+00), (-3.5000e+00, -3.5000e+00)),
    ((+4.4250e+00, +5.6250e+00), (-3.6000e+00, -3.6000e+00)),
    ((+3.1500e+00, +4.3500e+00), (-2.4251e+00, -2.4251e+00)),
    ((+4.3000e+00, +5.6000e+00), (-1.2251e+00, -1.2251e+00)),
    ((+5.6000e+00, +5.6000e+00), (+2.7500e-01, -3.5500e+00)),
    ((+6.9250e+00, +8.2250e+00), (-9.5000e-01, -9.5000e-01)),
    ((+8.2250e+00, +8.2250e+00), (-9.7500e-01, -2.1500e+00)),
    ((+8.2250e+00, +9.5250e+00), (-2.1750e+00, -2.1750e+00)),
    ((+3.1750e+00, +6.9500e+00), (+3.0001e-01, +3.0001e-01)),
    ((+8.3250e+00, +9.5750e+00), (+1.5000e-01, +1.5000e-01)),
    ((+8.3250e+00, +9.5750e+00), (+1.6000e+00, +1.6000e+00)),
    ((+6.9500e+00, +6.9500e+00), (+3.0000e-01, +2.8500e+00)),
    ((+3.1500e+00, +4.4500e+00), (+1.6000e+00, +1.6000e+00)),
    ((+4.4750e+00, +5.8250e+00), (+2.8000e+00, +2.8000e+00)),
    ((+4.4750e+00, +5.8250e+00), (+2.8000e+00, +2.8000e+00)),
    ((+6.9750e+00, +8.3000e+00), (+2.8499e+00, +2.8499e+00)),
    ((+5.8000e+00, +5.8000e+00), (+1.6750e+00, +4.1750e+00)),
    ((+5.8250e+00, +9.5500e+00), (+4.1750e+00, +4.1750e+00)),
    ((+8.3000e+00, +9.5750e+00), (+5.5500e+00, +5.5500e+00)),
    ((+4.4500e+00, +6.9500e+00), (+5.5250e+00, +5.5250e+00)),
    ((+4.4500e+00, +4.4500e+00), (+4.2500e+00, +6.8000e+00)),
    ((+5.6750e+00, +5.6750e+00), (+5.5500e+00, +6.7500e+00)),
    ((+5.6750e+00, +8.2750e+00), (+6.8002e+00, +6.8002e+00)),
    ((+3.1500e+00, +4.4500e+00), (+6.8000e+00, +6.8000e+00))
]

# Display
for i in range(len(wall_coords)):
    plt.plot(wall_coords[i][0], wall_coords[i][1], "g")

# x coordinates for node locations
nodexlocs = [+3.8000e+00, +5.1000e+00, +6.3500e+00, +7.5500e+00, +8.9250e+00]
node_coords = {}

# Node creation and displaying, optional node number display
for i in range(15):
    for j in range(5):
        plt.plot(nodexlocs[j], 7.5 - (1.31 * i), '.r', markersize=5)
        node_coords[5*i+j] = (nodexlocs[j], 7.5 - (1.31 * i))
        print(node_coords[5 * i + j])
        plt.text(nodexlocs[j], 7.5 - (1.31 * i), 5*i+j)  # show node numbers


# lines are of form (x1x2),(y1y2)
# This function calculates whether two lines have a point of intersection or not (True or False)
def isIntersecting(l1, l2):
    s1_x = l1[0][1] - l1[0][0]
    s1_y = l1[1][1] - l1[1][0]
    s2_x = l2[0][1] - l2[0][0]
    s2_y = l2[1][1] - l2[1][0]

    try:
        s = (-s1_y * (l1[0][0] - l2[0][0]) + s1_x * (l1[1][0] - l2[1][0])) / (-s2_x * s1_y + s1_x * s2_y)
        t = (s2_x * (l1[1][0] - l2[1][0]) - s2_y * (l1[0][0] - l2[0][0])) / (-s2_x * s1_y + s1_x * s2_y)
    except ZeroDivisionError:
        return False  # returns false because l1 is parallel to l2 and therefore not intersecting
        # there are also no nodes inside of walls so no two lines are collinear

    if 0 <= s <= 1 and 0 <= t <= 1:
        # collision detected
        return True

    return False  # no collision


# This function checks if a given line (path) intersects with any other line (wall) in the list of walls
def wallcheck(path):
    for wall in wall_coords:
        if isIntersecting(path, wall):
            return True
    return False


# This function returns the distance between two points
def getDist(p1, p2):
    return np.sqrt(np.square(p2[0] - p1[0]) + np.square(p2[1] - p1[1]))


# Using Dijkstra's algorithm, return dictionary which reveals the path from any node to source_node
def dijkstraPath(source_node):
    # node_Q heap format: (dist, node_key)
    node_Q = []
    heapify(node_Q)
    MAX = 9999  # this is an initial condition to set unknown distances from source location to notional infinity
    previous = {}
    for node_key, node_coord in node_coords.items():
        if node_key != source_node:
            dist = MAX
            previous[node_key] = -1
        else:
            dist = 0
            previous[node_key] = -1
        heappush(node_Q, (dist, node_key))

    heapify(node_Q)
    while len(node_Q) > 0:
        u = heappop(node_Q)
        for v in range(len(node_Q)):
            alt = u[0] + getDist(node_coords[node_Q[v][1]], node_coords[u[1]])
            line = node_coords[node_Q[v][1]], node_coords[u[1]]
            # if new line does not intersect walls and is shorter than previously calculated path:
            if alt < node_Q[v][0] and not wallcheck(((line[0][0], line[1][0]), (line[0][1], line[1][1]))):
                plt.plot((line[0][0], line[1][0]), (line[0][1], line[1][1]), c="0.75", linewidth=0.5)
                node_Q[v] = alt, node_Q[v][1]
                previous[node_Q[v][1]] = u[1]
        heapify(node_Q)
    return previous


# This function uses the calculated path distances to pick the shortest path from start to finish
def showDijkstraPath(start, finish):
    previous = dijkstraPath(finish)
    print("From", start, "to", finish)
    prev = previous[start]
    node_order = []
    while start != finish:
        node_order.append(start)
        plt.plot((node_coords[start][0], node_coords[prev][0]), (node_coords[start][1], node_coords[prev][1]), "b")
        start = prev
        prev = previous[prev]
    node_order.append(start)
    return node_order

print(showDijkstraPath(31.53))

plt.show()
