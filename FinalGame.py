import numpy as np
import os
import cv2
import random
import sys
import FunctionCv as f
import time
import pygame
import playsound
def check_validation_in_matrix(mat, height_start, height_end, width_start, width_end):
    if 1 in mat[height_start:height_end, width_start:width_end]:
        return False
    return True
# Initialize pygame
pygame.mixer.init()
# Load the music file
music_file = "C:\\L5\\AT.mp3"
pygame.mixer.music.load(music_file)
canvasPath = r'C:\L5\Canvas.png'
piecesRootFolder = r'C:\L5\pic'
fileNames = os.listdir(piecesRootFolder)
filePaths_example = [os.path.join(piecesRootFolder, f_name) for f_name in fileNames]
points=0
canvasImage_orig = cv2.imread(canvasPath)

width = 800
height = 700
canvasImage_orig = cv2.resize(canvasImage_orig, (width, height))
canvasImage_combined = canvasImage_orig.copy()
last_piece = canvasImage_orig.copy()
cv2.rectangle(canvasImage_combined, (20, 10), (200, 60), (0, 0, 0), cv2.FILLED)
cv2.putText(canvasImage_combined, f"Points: {points}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

# Initialize the matrix with zeros
matrix = np.zeros((height, width), dtype=int)

while True:
    pieceImage = cv2.imread(random.choice(filePaths_example))
   # pieceImage = f.makeBackgroundTransfer(pieceImage)
    pieceLocation = np.array([0, int(canvasImage_orig.shape[1] / random.choice(range(2, 6)))])  # Top Left Corner
    pieceVelocity = np.array([1, 0])
    isReachedEndOfCanvas = False
    isCollisionDetected = False
    game_over = False
    if not pygame.mixer.music.get_busy():
     pygame.mixer.music.play(-1)

    while not isReachedEndOfCanvas and not isCollisionDetected:
        canvasImage = canvasImage_combined.copy()

        pieceHeight, pieceWidth, _ = pieceImage.shape
        canvasHeight, canvasWidth, _ = canvasImage.shape

        targetHeight = pieceLocation[0] + pieceHeight
        targetWidth = pieceLocation[1] + pieceWidth

        targetArray = np.zeros((targetHeight - pieceLocation[0], targetWidth - pieceLocation[1], 3), dtype=np.uint8)
        pieceImage = pieceImage[:, :, :3]  # Remove alpha channel
        targetArray[:pieceHeight, :pieceWidth] = pieceImage
        canvasImage[pieceLocation[0]:targetHeight, pieceLocation[1]:targetWidth] = targetArray
        if 1 in matrix[pieceLocation[0]:pieceLocation[0] + height,
               pieceLocation[1]:pieceLocation[1] + width]:
            game_over = True
            # voice
            break
        cv2.imshow('canvas', canvasImage)
        key = cv2.waitKey(20)
        pieceLocation = pieceLocation + pieceVelocity
        if key == ord('a'):
            pieceLocation[1] -= 10
        elif key == ord('d'):
            pieceLocation[1] += 10
        elif key == ord('q'):
            sys.exit(0)

        if not check_validation_in_matrix(matrix, pieceLocation[0], targetHeight, pieceLocation[1], targetWidth):
            print("Collision!")
            isCollisionDetected = True

        isReachedEndOfCanvas = pieceLocation[0] + pieceHeight > canvasHeight - 10

    matrix[pieceLocation[0]:pieceLocation[0] + pieceHeight, pieceLocation[1]:pieceLocation[1] + pieceWidth] = 1

    # Check if isReachedEndOfCanvas is true or collision is detected
    if isReachedEndOfCanvas or isCollisionDetected:
        if isReachedEndOfCanvas:
            # Prevent downloading picture from the top of the canvas
            invalid_x = pieceLocation[0] + pieceHeight - canvasHeight
            invalid_y = pieceLocation[1] + pieceWidth // 2
            matrix[invalid_x:, invalid_y] = 1
        # Add the piece image to the combined canvas image
        sound_effect_file = "C:\\L5\\sound-effect-twinklesparkle-115095.mp3"
        sound_effect = pygame.mixer.Sound(sound_effect_file)
        sound_effect.play()
        canvasImage_combined[pieceLocation[0]:pieceLocation[0] + pieceHeight, pieceLocation[1]:pieceLocation[1] + pieceWidth] = pieceImage
        points += 1
        # Display the player's points in the upper corner of the screen
        # Clear the previous points text
        cv2.rectangle(canvasImage_combined, (20, 10), (200, 60), (0, 0, 0), cv2.FILLED)
        cv2.putText(canvasImage_combined, f"Points: {points}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255),2, cv2.LINE_AA)

        if pieceLocation[0] <= 10:
            print("Image reached the top frame of the canvas. Game over.")
            game_over = True
            time.sleep(3)
            break

        if game_over:
            # Add the piece image to the combined canvas image
            sound_effect_file = "C:\\L5\\sound-effect-twinklesparkle-115095.mp3"
            sound_effect = pygame.mixer.Sound(sound_effect_file)
            sound_effect.play()
            canvasImage_combined[pieceLocation[0]:pieceLocation[0] + pieceHeight,
            pieceLocation[1]:pieceLocation[1] + pieceWidth] = pieceImage
            points += 1
            # Display the player's points in the upper corner of the screen
            # Clear the previous points text
            cv2.rectangle(canvasImage_combined, (20, 10), (200, 60), (0, 0, 0), cv2.FILLED)
            cv2.putText(canvasImage_combined, f"Points: {points}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 255, 255), 2, cv2.LINE_AA)
            org = (300, 400)
            fontScale = 5
            color = (0, 0, 255)
            thickness = 15
            canvasImage = cv2.putText(canvasImage_combined, 'Game Over', org, cv2.FONT_HERSHEY_SIMPLEX,
                                      fontScale, color, thickness, cv2.LINE_AA)
            cv2.imshow('canvas', canvasImage)
            time.sleep(3)
            pygame.mixer.music.stop()  # Stop the music
            cv2.waitKey(2000)
            sys.exit(0)
        key1 = cv2.waitKey(10)
        if key1 == ord('q'):
            sys.exit(0)