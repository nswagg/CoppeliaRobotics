# Retrieve all obstacles from the coppelia scene
EXCLUDED_OBJECTS = ["Floor", "box", "visible", "element", "visibleElement"]
FLOOR = "/Floor/element"
ROBOT = "/PioneerP3DX"

import math
VERBOCITY = 1
ROBOTS = ["Pioneer_p3dx"]

def getAllSceneShapes(sim, estimatedSceneShapes=2000):
    outputFile = open("walls.txt", "a")
    floorHandle = sim.getObject(FLOOR)
    i = 0
    sceneObjects = []

    while i < estimatedSceneShapes:
        objectHandle = sim.getObjects(i, sim.object_shape_type)

        if objectHandle == -1:
            break

        if sim.getObjectAlias(objectHandle, -1) not in EXCLUDED_OBJECTS and objectHandle != -1:
            orientation = round(math.degrees(sim.getObjectOrientation(objectHandle, floorHandle)[2]))
            print(f"Retrieving Obstacle: {objectHandle}")
            shapePosition = sim.getObjectPosition(objectHandle, floorHandle)
            shapeBoundingBox = sim.getShapeBB(objectHandle)
            if VERBOCITY == 1:
                print("POS: ", shapePosition)

            # Scale the object orientation based on horizontal alignment
            if orientation == 90 or orientation == -90:
                shapeWidth = shapeBoundingBox[1]
                shapeHeight = shapeBoundingBox[0]
                if VERBOCITY == 1:
                    print("A", shapeWidth, shapeHeight)
                x1 = shapePosition[0] - (.5 * shapeWidth)
                y1 = shapePosition[1]
                x2 = shapePosition[0] + (.5 * shapeWidth)
                y2 = shapePosition[1]

                sceneObjects.append(((x1, x2), (y1, y2)))

            # Object is on the vertical plane
            elif orientation == 0 or orientation == -180 or orientation == 180:
                shapeWidth = shapeBoundingBox[0]
                shapeHeight = shapeBoundingBox[1]
                if VERBOCITY == 1:
                    print("BB: ", shapeWidth, shapeHeight)
                x1 = shapePosition[0]
                y1 = shapePosition[1] - (.5 * shapeHeight)
                x2 = shapePosition[0]
                y2 = shapePosition[1] + (.5 * shapeHeight)

                sceneObjects.append(((x1, x2), (y1, y2)))

        i += 1

    for i in sceneObjects:
        outputFile.write(str(i) + ",\n")

    return sceneObjects

def getRobotHandles(sim, robots=ROBOT):
    """Returns list of robot handles. Provides Pioneer handle by default, but can take in list of handles"""
    robotObjs = []