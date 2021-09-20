from handTrackingModule import handsDetector
import time
import cv2

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

    # time variables
    currenTime = 0
    previousTime = 0

    while True:
        ret, frame = camera.read()

        frame = handdetector.findHands(frame = frame, draw = False)
        landmarksList = handdetector.findPosition(frame, draw = False)

        if len(landmarksList) != 0:
            numberOfFingers = 0
            for i in range(5):
                fingerTip = (i+1) * 4
                if i == 0:
                    fingerMid = 5
                else:
                    fingerMid = fingerTip - 2

                yCoord = [coord[1] for coord in landmarksList]
                if yCoord[fingerTip] < yCoord[fingerMid]:
                    numberOfFingers += 1
            print(numberOfFingers)
            cv2.putText(frame, f"Number of fingers: {str(int(numberOfFingers))}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # calculatint FPS
        currentTime = time.time()
        fps = 1 / (currentTime - previousTime)
        previousTime = currentTime

        cv2.putText(frame, f"FPS: {str(int(fps))}", (width // 2 + 100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
        cv2.imshow("frame", frame)

        if cv2.waitKey(1) == ord("q"):
            break

if __name__ == "__main__":
    main()
