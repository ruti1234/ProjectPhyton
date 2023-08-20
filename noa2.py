import numpy as np
import cv2
import os
import random

canvasPath = r'C:\Users\user\pyton\progect\image\Canvas.png'
piecePath = r'C:\Users\user\pyton\progect\image\dance1.png'
piecesRootFolder = r'C:\Users\user\pyton\progect\image'
fileNames = os.listdir(piecesRootFolder)
filePaths_example = [os.path.join(piecesRootFolder, f_name) for f_name in fileNames]

canvasImage_orig = cv2.imread(canvasPath)
canvasImage_orig = cv2.resize(canvasImage_orig, (1450, 705))
canvas_Fixed = canvasImage_orig.copy()

imgRnd = random.choice(filePaths_example)
pieceImage = cv2.imread(imgRnd)
# pieceImage = cv2.cvtColor(pieceImage, cv2.COLOR_BGR2BGRA)
height, width, channels = pieceImage.shape
pieceLocation = np.array([0, int(random.random() * canvasImage_orig.shape[1])])
pieceVelocity = np.array([1, 0])

isReachedEndOfCanvas = False
isOver = False
pieceImage = cv2.resize(pieceImage, (width, height))

while not isOver:
    canvasImage = canvasImage_orig.copy()

    if not np.array_equal(canvasImage[pieceLocation[0]:pieceLocation[0] + height,
                          pieceLocation[1]:pieceLocation[1] + width, :],
                          canvas_Fixed[pieceLocation[0]:pieceLocation[0] + height,
                          pieceLocation[1]:pieceLocation[1] + width, :]):
        isReachedEndOfCanvas = True
    pieceImage = cv2.resize(pieceImage, (width, height))
    # print(pieceImage)
    canvasImage[pieceLocation[0]:pieceLocation[0] + height,
    pieceLocation[1]:pieceLocation[1] + width, :] = pieceImage
    cv2.imshow('canvas', canvasImage)
    key = cv2.waitKey(1)
    pieceLocation = pieceLocation + pieceVelocity
    if key == ord('a'):
        pieceLocation[1] -= 10
    elif key == ord('d'):
        pieceLocation[1] += 10
    elif key == 27:
        isOver = True
    isReachedEndOfCanvas = pieceLocation[0] + height > canvasImage.shape[0] - 10

    if isReachedEndOfCanvas:
        canvasImage_orig = canvasImage.copy()
        imgRnd = random.choice(filePaths_example)
        pieceImage = cv2.imread(imgRnd)

        height, width, channels = pieceImage.shape
        pieceImage = cv2.resize(pieceImage, (width, height))
        pieceLocation = np.array([0, int(random.random() * canvasImage_orig.shape[1])])
cv2.waitKey()