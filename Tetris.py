import numpy as np
import os
import cv2
import random
import sys
import time
import pygame
import playsound

class Tetris:
    def __init__(self, canvas_path, folder_path, music_path, width, height):
        # Initialize pygame
        pygame.mixer.init()
        # Load the music file
        self.music_file = music_path
        pygame.mixer.music.load(self.music_file)
        self.canvasPath = canvas_path
        self.piecesRootFolder = folder_path
        self.fileNames = os.listdir(self.piecesRootFolder)
        self.filePaths_example = [os.path.join(self.piecesRootFolder, f_name) for f_name in self.fileNames]
        self.points = 0
        self.canvasImage_orig = cv2.imread(self.canvasPath)
        self.width = width
        self.height = height
        self.canvasImage_orig = cv2.resize(self.canvasImage_orig, (self.width, self.height))
        self.canvasImage_combined = self.canvasImage_orig.copy()
        #self.last_piece = self.canvasImage_orig.copy()
        self.showPoints(self.canvasImage_combined)
        # Initialize the matrix with zeros
        self.matrix = np.zeros((self.height, self.width), dtype=int)

    def check_validation_in_matrix(self, mat, height_start, height_end, width_start, width_end):
        if 1 in mat[height_start:height_end, width_start:width_end]:
            return False
        return True

    def play_music(self):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)

    def showPoints(self,canvasImage_combined):
        cv2.rectangle(canvasImage_combined, (20, 10), (200, 60), (0, 0, 0), cv2.FILLED)
        cv2.putText(canvasImage_combined, f"Points: {self.points}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 255, 255), 2)

    def moreSound(self, sub_music):
        sound_effect_file = sub_music
        sound_effect = pygame.mixer.Sound(sound_effect_file)
        sound_effect.play()

    def play(self, sub_music):
        while True:
            pieceImage = cv2.imread(random.choice(self.filePaths_example))
            pieceLocation = np.array([0, int(self.canvasImage_orig.shape[1] / random.choice(range(2, 6)))])  # Top Left Corner
            pieceVelocity = np.array([1, 0])

            isReachedEndOfCanvas = False
            isCollisionDetected = False
            game_over = False

            self.play_music()

            canvasImage = self.canvasImage_combined.copy()

            pieceHeight, pieceWidth, _ = pieceImage.shape
            canvasHeight, canvasWidth, _ = canvasImage.shape

            if 1 in self.matrix[pieceLocation[0]:pieceLocation[0] + pieceHeight,
                    pieceLocation[1]:pieceLocation[1] + pieceWidth]:
                game_over = True
                break

            while not isReachedEndOfCanvas and not isCollisionDetected:
                canvasImage = self.canvasImage_combined.copy()
                pieceHeight, pieceWidth, _ = pieceImage.shape
                canvasHeight, canvasWidth, _ = canvasImage.shape
                targetHeight = pieceLocation[0] + pieceHeight
                targetWidth = pieceLocation[1] + pieceWidth

                targetArray = np.zeros((targetHeight - pieceLocation[0], targetWidth - pieceLocation[1], 3),
                                       dtype=np.uint8)
                targetArray[:pieceHeight, :pieceWidth] = pieceImage
                canvasImage[pieceLocation[0]:targetHeight, pieceLocation[1]:targetWidth] = targetArray

                cv2.imshow('canvas', canvasImage)
                key = cv2.waitKey(2)
                pieceLocation = pieceLocation + pieceVelocity

                if key == ord('a'):
                    pieceLocation[1] -= 10
                elif key == ord('d'):
                    pieceLocation[1] += 10
                elif key == ord('q'):
                    sys.exit(0)

                if not self.check_validation_in_matrix(self.matrix, pieceLocation[0], targetHeight,
                                                       pieceLocation[1], targetWidth):
                    print("Collision!")
                    isCollisionDetected = True

                isReachedEndOfCanvas = pieceLocation[0] + pieceHeight > canvasHeight - 10


            self.matrix[pieceLocation[0]:pieceLocation[0] + pieceHeight, pieceLocation[1]:pieceLocation[1] + pieceWidth] = 1


            if isReachedEndOfCanvas or isCollisionDetected:
                if isReachedEndOfCanvas:
                    # Prevent downloading pictures from the top of the canvas
                    invalid_x = pieceLocation[0] + pieceHeight - canvasHeight
                    invalid_y = pieceLocation[1] + pieceWidth // 2
                    self.matrix[invalid_x:, invalid_y] = 1

                self.moreSound(sub_music)

                self.canvasImage_combined[pieceLocation[0]:pieceLocation[0] + pieceHeight, pieceLocation[1]:pieceLocation[1] + pieceWidth] = pieceImage
                self.points += 1
                self.showPoints(self.canvasImage_combined)

                if pieceLocation[0] <= 10:
                    print("Image reached the top frame of the canvas. Game over.")
                    game_over = True
                    break

                key1 = cv2.waitKey(1)
                if key1 == ord('q'):
                    sys.exit(0)

        if game_over:
            self.showPoints(self.canvasImage_combined)

            # Display the updated canvas image with the points
            cv2.imshow('canvas', canvasImage)
            cv2.waitKey(1)
            self.moreSound(sub_music)
            time.sleep(2)  # Delay for 2 seconds before displaying "Game Over"

            # Add the "Game Over" text
            org = (canvasImage.shape[1] // 2 - 300, canvasImage.shape[0] // 2)
            fontScale = 3
            color = (0, 0, 255)
            thickness = 5
            canvasImage = cv2.putText(self.canvasImage_combined, 'Game Over', org, cv2.FONT_HERSHEY_SIMPLEX,
                                           fontScale, color, thickness, cv2.LINE_AA)

            cv2.imshow('canvas', canvasImage)
            cv2.waitKey(1)

            time.sleep(3)  # Delay for 1 second after displaying everything

            pygame.mixer.music.stop()  # Stop the music
            sys.exit(0)

game = Tetris(r'C:\L5\Canvas.png', r'C:\L5\pic', "C:\\L5\\Barnville.mp3", 1500, 780)
game.play("C:\\L5\\sound-effect-twinklesparkle-115095.mp3")

