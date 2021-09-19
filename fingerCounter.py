from handTrackingModule import handsDetector
import time
import cv2

# camera variables
camera = cv2.VideoCapture(0)
ret, testFrame = camera.read()
(height, width) = testFrame.shape[:2]

# time variables
currentTime = 0
previousTime = 0

handdetector = handsDetector(staticImageModel = False,
                             maxNumHands = 1,
                             minDetectionConfidence = 0.5,
                             minTrackingConfidence = 0.5)

def verifyFinger():

    return True

def main():
    while True:
        t, frame = camera.read()

        handlandmarks = handdetector.findHands(frame, draw = True)

        if len(handlandmarks) != 0:
            numberOfFingers = 0
            for i in range(6):
                fingerNumber = (i + 1) * 4
                if verifyFinger(fingerNumber) == True:
                    numberOfFingers += 1
            print(f"number of fingers: {int(numberOfFingers)}")

        # calculating the FPS
        currentTime = time.time()
        fps = 1 / (currentTime - previousTime)
        previousTime = currentTime

        if cv2.waitKey(1) == ord("q"):
            break

        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()