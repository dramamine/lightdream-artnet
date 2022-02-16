from ctypes import sizeof
import cv2
import os

path = "..\\video\\rotate_gradient_red2red_12unis.mp4"

vid = cv2.VideoCapture(path)
width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = vid.get(cv2.CAP_PROP_FPS)

currentframe = 0
  
while(True):
      
  # reading from frame
  ret,frame = vid.read()
  if ret:
    whites = 0
    blacks = 0
    # print("got stuff:", ret)
    # print(len(frame))
    # print(len(frame[0]))
    for col in range(0, width):
      for row in range(0, height):
        # print(frame[row][col])
        if (frame[row][col][0]) == 0:
          blacks += 1
        else:
          whites += 1

    print(whites, blacks)
    # print(frame)
    # one frame is fine for now
    break
  else:
    break

vid.release()
cv2.destroyAllWindows()
