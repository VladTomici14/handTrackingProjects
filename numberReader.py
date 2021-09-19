from handTrackingModule import handsDetector
import time
import cv2
import os

# webcam variables
webcam = cv2.VideoCapture(0)
T, copyFrame = webcam.read()
(height, width) = copyFrame.shape[:2]

# hand variables
handDetector = handsDetector(staticImageModel = False,
                             maxNumHands = 1,
                             minDetectionConfidence = 0.5,
                             minTrackingConfidence = 0.5)

"""
# images reading
folderPath = "fingerImages"
imagePaths = os.listdir(folderPath)
imagesList = []
for imagePath in imagePaths:
    image = cv2.imread(f"{folderPath}/{imagePath}")
    imagesList.append(image)
"""

def verifyFinger()

def main():
    # time variables
    currentTime = 0
    previousTime = 0

    while True:
        ret, frame = webcam.read()

        frame = handDetector.findHands(frame = frame,
                                       draw = True)
        handlandmarks = handDetector.findPosition(frame = frame,
                                                  handNumber = 0,
                                                  draw = True)

        if len(handlandmarks) == 0:
            # declaring the list that contains a value which represents if the finger is up or no
            fingerTips = []
            for i in range(6):
                fingerTips.append(False)

            # verifying for each finger is it is up or not
            yCoord = [coord[1] for coord in handlandmarks]
            numberOfFingers = 0
            print(len(fingerTips))
            for i in range(6):
                i += 1
                theTip = i * 4
                theMid = (i * 4) - 2
                if yCoord[theTip] < yCoord[theMid]:
                    fingerTips[i] = True
                    numberOfFingers += 1
                else:
                    fingerTips[i] = False

            print(sum)

        """
        # putting the first fingers image in the left corner of the frame
        (hImage, wImage) = imageList[0].shape[:2]
        frame[0:hImage, 0:wImage] = imageList[0]
        """

        # calculate FPS
        currentTime = time.time()
        fps = 1 / (currentTime - previousTime)
        previousTime = currentTime

        cv2.putText(frame, str(int(fps)), (width // 2, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
        cv2.imshow("webcam", frame)

        if cv2.waitKey(1) == ord("q"):
            break

    webcam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
