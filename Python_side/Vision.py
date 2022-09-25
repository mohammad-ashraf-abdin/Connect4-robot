import cv2
import numpy as np


M = 7
N = 6

#board = np.zeros((N, M))
Hight = 460
Width = 600
lower_red = np.array([110,100,100]) #120  100 100
upper_red = np.array([255,255,255])
kernel = np.ones((5,5), np.uint8)


# imge = cv2.imread('C:/Users/ashra/Pictures/Camera Roll/WIN_20190409_10_51_39_Pro.jpg')
cap = cv2.VideoCapture(1)

def BoardUpdate(board):
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # imge = cv2.pyrDown(frame)
        img = frame[60:520, 0:600]
        hav = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hav, lower_red, upper_red)
        fill = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        opening = cv2.morphologyEx(fill, cv2.MORPH_OPEN, kernel)

        dilation = cv2.dilate(opening, kernel, iterations=2)

        contours, hiercharchy = cv2.findContours(dilation, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            # cv2.drawContours(img, contour, -1, (0, 255, 0),3)
            con = contour
            if len(con) > 10:
                x, y, w, h = cv2.boundingRect(con)
                xcent = x + w / 2
                ycent = y + h / 2
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.circle(img, (int(xcent), int(ycent)), 1, (0, 255, 0), 3)
                cell_w = Width / 7
                cell_H = Hight / 6
                cellX = ((int(xcent / cell_w)))
                cellY = ((int(ycent / cell_H)))
                print(cellX + 1)
                print(cellY + 1)
                # print(cellX+(7*(cellY-1)))
                board[cellY][cellX] = 1
                print(board)
        cv2.imshow("img", img)
        cv2.imshow("edited", dilation)

        k = cv2.waitKey(5)
        if k == ord('q'):
            break
    return board


cap.release()
cv2.destroyAllWindows()
