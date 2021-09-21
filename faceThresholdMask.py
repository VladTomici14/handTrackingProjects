import cv2
import numpy as np

camera = cv2.VideoCapture(0)
ret, testFrame = camera.read()
(height, width) = testFrame.shape[:2]

def main():
    while True:
        T, frame = camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.GaussianBlur(frame, (5, 5), 0)

        ostuThreshold, imageResult = cv2.threshold(frame, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # imageResult = cv2.bitwise_not(imageResult)

        cv2.imshow("frame", imageResult)

        if cv2.waitKey(1) == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()