from handTrackingModule import handsDetector
import time
import cv2
import os

def main():
    # camera variables
    camera = cv2.VideoCapture(0)
    t, testFrame = camera.read()
    (height, width) = testFrame.shape[:2]

    # hand variables
    handdetector = handsDetector(staticImageModel = False,
                                 maxNumHands = 1,
                                 minDetectionConfidence = 0.5,
                                 minTrackingConfidence = 0.5)

    while True:
        ret, frame = camera.read()

        frame = handdetector.findHands(frame, draw = True)
        landmarksList = handdetector.findPosition(frame)

        cv2.imshow("frame", frame)

        if cv2.waitKey(1) == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()