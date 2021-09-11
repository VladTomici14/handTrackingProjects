import mediapipe as mp
import math
import cv2

class handsDetector():
    def __init__(self,
                 staticImageModel = False,
                 maxNumHands = 1,
                 minDetectionConfidence = 0.5,
                 minTrackingConfidence = 0.5):
        # mediapipe hands variables
        self.staticImageModel = staticImageModel
        self.maxNumHands = maxNumHands
        self.minDetectionConfidence = minDetectionConfidence
        self.minTrackingConfidence = minTrackingConfidence

        # hand variables
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode = self.staticImageModel,
                                        max_num_hands = self.maxNumHands,
                                        min_detection_confidence = self.minDetectionConfidence,
                                        min_tracking_confidence = self.minTrackingConfidence)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, frame, draw = False):
        (h, w) = frame.shape[:2]
        RGBFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(RGBFrame)

        if self.results.multi_hand_landmarks:
            for handLandmarks in self.results.multi_hand_landmarks:
                if draw == True:
                    self.mpDraw.draw_landmarks(frame, handLandmarks, self.mpHands.HAND_CONNECTIONS)

        return frame

    def findPosition(self, frame, handNumber = 0, draw = True):
        (height, width) = frame.shape[:2]
        landmarksList = []

        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[handNumber]
            for id, landmark in enumerate(myhand.landmark):
                (x, y) = (int(width * landmark.x), int(height * landmark.y))
                landmarksList.append((x, y))
                if draw == True:
                    if (id == 4 or id == 8) and id != 0:
                        cv2.circle(frame, (x, y), 15, (0, 0, 255), -1) # aka replacing -1 with cv2.FILLED

        return landmarksList

    def calculateDistance(self, landmarksList, frame):
        xCoords = [item[0] for item in landmarksList]
        yCoords = [item[1] for item in landmarksList]

        distance = pow(xCoords[8] - xCoords[4], 2) + pow(yCoords[8] - yCoords[4], 2)
        distance = int(math.sqrt(distance))

        cv2.line(frame, (xCoords[8], yCoords[8]), (xCoords[4], yCoords[4]), (0, 153, 24), 2)

        return distance

