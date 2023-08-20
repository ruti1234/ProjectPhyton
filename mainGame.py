import numpy as np
import os
import cv2
import random
import sys
canvasPath = r'C:\L5\Canvas.png'
piecesRootFolder = r'C:\L5\pic'
fileNames = os.listdir(piecesRootFolder)
filePaths_example = [os.path.join(piecesRootFolder, f_name) for f_name in fileNames]

canvasImage_orig = cv2.imread(canvasPath)

width = 800
height = 700
canvasImage_orig = cv2.resize(canvasImage_orig, (width, height))
while True:
    pieceImage = cv2.imread(random.choice(filePaths_example))
    height, width, channels = pieceImage.shape
    pieceLocation = np.array([0, int(canvasImage_orig.shape[1]/random.choice(range(1,3)))]) # Top Left Corner
    pieceVelocity = np.array([1, 0])

    isReachedEndOfCanvas = False

    while not isReachedEndOfCanvas:
        canvasImage = canvasImage_orig.copy()
        canvasImage[pieceLocation[0]:pieceLocation[0] + height,
                    pieceLocation[1]:pieceLocation[1] + width] = pieceImage

        cv2.imshow('canvas', canvasImage)
        key = cv2.waitKey(20)
        pieceLocation = pieceLocation + pieceVelocity
        if key == ord('a'):
            pieceLocation[1] -= 10
        elif key == ord('d'):
            pieceLocation[1] += 10
        elif  key == 87:
            sys.exit(0)
        isReachedEndOfCanvas = pieceLocation[0] + height > canvasImage.shape[0] - 10

    key1=cv2.waitKey()
    if key1==87:
        sys.exit(0)


