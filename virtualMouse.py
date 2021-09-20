from handTrackingModule import handsDetector
import numpy as np
import pyautogui
import autopy
import math
import time
import cv2

def main():
    # camera variables
    camera = cv2.VideoCapture(0)
    t, testFrame = camera.read()
    (height, width) = testFrame.shape[:2]

    # screen settings
    (screenWidth, screenHeight) = autopy.screen.size()

    # hand tracking variables
    handdetector = handsDetector(staticImageModel = False,
                                 maxNumHands = 1,
                                 minDetectionConfidence = 0.5,
                                 minTrackingConfidence = 0.5)

    # time variables
    currentTime = 0
    previousTime = 0

    while True:
        # 1. find handlandmarks
        ret, frame = camera.read()
        frame = handdetector.findHands(frame, False)
        landmarksList = handdetector.findPosition(frame, handNumber = 0, draw = False)

        # 2. get the tip of the index and of the middle finger
        if len(landmarksList) != 0:
            xCoord = [coord[0] for coord in landmarksList]
            yCoord = [coord[1] for coord in landmarksList]

            indexFinger = (xCoord[8], yCoord[8])
            middleFinger = (xCoord[12], yCoord[12])

            # 3. check which fingers are up
            fingersStatus = []
            for i in range(5):
                fingersStatus.append(False)

            for i in range(5):
                fingerIndexCoord = (i+1) * 4
                if i == 0:
                    if yCoord[fingerIndexCoord] < yCoord[5]:
                        fingersStatus[i] = True
                else:
                    if yCoord[fingerIndexCoord] < yCoord[fingerIndexCoord - 2]:
                        fingersStatus[i] = True

            indexFingerStatus = fingersStatus[1]
            middleFingerStatus = fingersStatus[2]

            # 4. index finger up => moving mode
            if indexFingerStatus == True and middleFingerStatus == False:
                # 5. convert coords ((height, width) -> (screenHeight, screenWidth))
                screenX = np.interp(xCoord[8], (0, width), (0, screenWidth))
                screenY = np.interp(yCoord[8], (0, height), (0, screenHeight))

                # 6. smoothening values

                # 7. move the cursor
                autopy.mouse.move(screenWidth - screenX, screenY)

                 # 8. check the clicking mode
            touchingState = False
            if indexFingerStatus == True and middleFingerStatus == True:
                distance = pow(xCoord[8] - xCoord[12], 2) + pow(yCoord[8] - yCoord[12], 2)
                distance = int(math.sqrt(distance))

                if distance <= 50:
                    touchingState = True
                    cv2.circle(frame, tuple(indexFinger), 10, (0, 255, 0), -1)
                    print("OK")

            if touchingState == False:
                cv2.circle(frame, tuple(indexFinger), 10, (0, 0, 255), -1)

        # calculating the fps
        currentTime = time.time()
        fps = 1 / (currentTime - previousTime)
        previousTime = currentTime
        cv2.putText(frame, f"FPS: {str(int(fps))}", (width // 2 + 150, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 70), 3)

        cv2.imshow("frame", frame)

        if cv2.waitKey(1) == ord("q"):
            break

if __name__ == "__main__":
    main()
