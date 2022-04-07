import cv2
import numpy as np

def nothing(e):
    pass

# 窗口参数控制。
cv2.namedWindow("Color_Split_2APP")
cv2.resizeWindow("Color_Split_2APP", 400, 400)
# 创建控制滚动条。
cv2.createTrackbar("LowH", "Color_Split_2APP", 35, 255, nothing)
cv2.createTrackbar("LowS", "Color_Split_2APP", 43, 255, nothing)
cv2.createTrackbar("LowV", "Color_Split_2APP", 46, 255, nothing)
cv2.createTrackbar("HighH", "Color_Split_2APP", 77, 255, nothing)
cv2.createTrackbar("HighS", "Color_Split_2APP", 255, 255, nothing)
cv2.createTrackbar("HighV", "Color_Split_2APP", 255, 255, nothing)


# 图片更新。
while True:
    frame = cv2.imread('./images/img.jpg')
    frame = cv2.resize(frame,dsize=(200,200))

    #HSV模式。
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 获取滚动条值。
    l_h = cv2.getTrackbarPos("LowH", "Color_Split_2APP")
    l_s = cv2.getTrackbarPos("LowS", "Color_Split_2APP")
    l_v = cv2.getTrackbarPos("LowV", "Color_Split_2APP")
    u_h = cv2.getTrackbarPos("HighH", "Color_Split_2APP")
    u_s = cv2.getTrackbarPos("HighS", "Color_Split_2APP")
    u_v = cv2.getTrackbarPos("HighV", "Color_Split_2APP")

    l_g = np.array([l_h, l_s, l_v])
    u_g = np.array([u_h, u_s, u_v])

    #滤波处理。
    hsv = cv2.blur(hsv, (5, 5))
    hsv = cv2.medianBlur(hsv, 5)
    hsv = cv2.GaussianBlur(hsv, (5, 5), 0)
    hsv = cv2.bilateralFilter(hsv, 9, 75, 75)

    # 获取遮罩和处理后图片。
    mask = cv2.inRange(hsv, l_g, u_g)
    #遮罩图片。
    res = cv2.bitwise_and(frame, frame, mask=mask)

    imgs = np.hstack([frame, res])
    cv2.imshow("Color_Split_2App", imgs)
    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()