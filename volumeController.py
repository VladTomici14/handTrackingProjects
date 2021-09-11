from handTrackingModule import handsDetector
from subprocess import call
import time
import math
import cv2

def main():
    # webcam variables
    webcam = cv2.VideoCapture(0)
    T, aux = webcam.read()
    (height, width) = aux.shape[:2]
    (centerX, centerY) = (int(width // 2), int(height // 2))

    # time variables
    currentTime = 0
    previousTime = 0

    # importing our class
    detector = handsDetector(staticImageModel = False,
                             maxNumHands = 1,
                             minDetectionConfidence = 0.5,
                             minTrackingConfidence = 0.5)

    firstTime = True

    while True:
        ret, frame = webcam.read()

        frame = detector.findHands(frame, True)
        landmarksList = detector.findPosition(frame)

        if len(landmarksList) != 0:
            distance = detector.calculateDistance(landmarksList, frame)
            volume = distance // 2
            if volume <= 100 and volume >= 0:
                call(["amixer", "-D", "pulse", "sset", "Master", str(volume)+"%"])
                cv2.putText(frame, f"Volume: {str(int(volume))}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            if firstTime == True:
                initialValue = distance
                firstTime = False
            print(initialValue)
        if len(landmarksList) == 0:
            cv2.putText(frame, "Volume: 0", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            firstTime = True

        # calculating the fps
        currentTime = time.time()
        fps = 1 / (currentTime - previousTime)
        previousTime = currentTime

        cv2.putText(frame, f"FPS: {str(int(fps))}", (width // 2 - 30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("webcam", frame)

        if cv2.waitKey(1) == ord("q"):
            break

if __name__ == "__main__":
    main()