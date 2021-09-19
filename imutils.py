import mediapipe as mp
import time
import cv2

class allFunctionns:
    def __init__(self, frame):
        self.frame = frame
        (self.height, self.width) = frame.shape[:2]

    def calculateFPS(self, frame):
        global currentTime
        global previousTime

        currentTime = time.time()
        fps = 1 / (currentTime - previousTime)
        previousTime = currentTime

        cv2.putText(self.frame, str(int(fps)), (self.width // 2, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
