import numpy as np
import os
import cv2
import random
import sys
import pygame
import time

class Game:
    def __init__(self,canvas_path,folder_path,music_path,width,height):
        pygame.mixer.init()
        pygame.mixer.music.load(music_path)
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
        self.last_piece = self.canvasImage_orig.copy()
        cv2.rectangle(self.canvasImage_combined, (20, 10), (200, 60), (0, 0, 0), cv2.FILLED)
        cv2.putText(self.canvasImage_combined, f"Points: {self.points}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        self.matrix = np.zeros((self.height, self.width), dtype=int)
        self.game_over = False

    def check_validation_in_matrix(self, mat, height_start, height_end, width_start, width_end):
        if 1 in mat[height_start:height_end, width_start:width_end]:
            return False
        return True

    def play_music(self):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)

    def handle_piece_movement(self, pieceImage, pieceLocation, pieceVelocity):
        isReachedEndOfCanvas = False
        isCollisionDetected = False

        canvasImage = self.canvasImage_combined.copy()
        pieceHeight, pieceWidth, _ = pieceImage.shape
        canvasHeight, canvasWidth, _ = canvasImage.shape

        if 1 in self.matrix[pieceLocation[0]:pieceLocation[0] + pieceHeight, pieceLocation[1]:pieceLocation[1] + pieceWidth]:
            self.game_over = True
            return

        while not isReachedEndOfCanvas and not isCollisionDetected:
            canvasImage = self.canvasImage_combined.copy()

            pieceHeight, pieceWidth, _ = pieceImage.shape
            canvasHeight, canvasWidth, _ = canvasImage.shape
            targetHeight = pieceLocation[0] + pieceHeight
            targetWidth = pieceLocation[1] + pieceWidth

            targetArray = np.zeros((targetHeight - pieceLocation[0], targetWidth - pieceLocation[1], 3), dtype=np.uint8)
            targetArray[:pieceHeight, :pieceWidth] = pieceImage
            canvasImage[pieceLocation[0]:targetHeight, pieceLocation[1]:targetWidth] = targetArray
            cv2.imshow('canvas', canvasImage)
            key = cv2.waitKey(20)

            pieceLocation = pieceLocation + pieceVelocity

            if key == ord('a'):
                pieceLocation[1] -= 10
            elif key == ord('d'):
                pieceLocation[1] += 10
            elif key == ord('q'):
                sys.exit(0)

            if not self.check_validation_in_matrix(self.matrix, pieceLocation[0], targetHeight, pieceLocation[1], targetWidth):
                print("Collision!")
                isCollisionDetected = True

            isReachedEndOfCanvas = pieceLocation[0] + pieceHeight > canvasHeight - 10

        self.matrix[pieceLocation[0]:pieceLocation[0] + pieceHeight, pieceLocation[1]:pieceLocation[1] + pieceWidth] = 1

       # if isReachedEndOfCanvas or isCollisionDetected:
       #     if isReachedEndOf

# class Tetris:
#     def __init__(self, canvas_path, folder_path):
#         self.canvasPath = canvas_path
#         self.piecesRootFolder = folder_path
#         fileNames = os.listdir(self.piecesRootFolder)
#         if folder_path in self.canvasPath:
#             canvas_path.replace(folder_path, '')
#             fileNames.remove(canvas_path[len(folder_path)+1:])
#         points = 0
#         canvasImage_orig = cv2.imread(self.canvasPath)
#
#         width = 1500
#         height = 780
#         canvasImage_orig = cv2.resize(canvasImage_orig, (width, height))
#         canvasImage_combined = canvasImage_orig.copy()
#         last_piece = canvasImage_orig.copy()
#         cv2.rectangle(canvasImage_combined, (20, 10), (200, 60), (0, 0, 0), cv2.FILLED)
#         cv2.putText(canvasImage_combined, f"Points: {points}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255),2)
#
#         # Initialize the matrix with zeros
#         matrix = np.zeros((height, width), dtype=int)
#
#     #def theProgressOfTheGame(self):


#t1= Tetris(r'C:\L5\pic\dance4.png', r'C:\L5\pic')