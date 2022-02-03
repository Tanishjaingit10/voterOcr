import cv2
file_name = "page_36.jpg"

img = cv2.imread(file_name)
y = img.shape[0]
x = img.shape[0]
import math

h = math.floor((y * (0.9015151515151515 - 0.05948787446504993)) / 10)
w = math.floor((x * (0.6733646857631467 - 0.02838383838383838)) / 3)
import pytesseract

import time
for i in range(1,4):
    # row
    for k in range(1, 11):
        x1 = math.floor(x*0.02838383838383838) + w*(i-1)
        y1 = math.floor(y*0.05948787446504993) + h*(k-1)
        h1 = h
        w1 = w
        crop_img = img[y1:y1+h1, x1:x1+w1]
        cv2.imwrite(f"croped_img/col_{i}_row_{k}.jpg", crop_img)

        text = pytesseract.image_to_string(crop_img, lang='hin')
        print(text)

"""

19   41
0.03838383838383838   0.05848787446504993
471   41
0.9515151515151515   0.05848787446504993
20   626
0.04040404040404041   0.8930099857346647
471   627
0.9515151515151515   0.8944365192582026


"""