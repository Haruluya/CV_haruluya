import json
import requests
import cv2


# 微信公众号发送消息请求。
# 获取access_token。
def get_access_token():
    app_id = 'wxxxxxxxxxxxxxx'
    app_secret = 'axxxxxxxxx'
    url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}'
    resp = requests.get(url).json()
    return resp.get('access_token')

#请求发送消息。
def set_wechat_message(message):
    access_token = get_access_token()
    url = f'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={access_token}'
    open_id = "xxxxxxxxxxxxxxxx"
    req_data = {
        "touser": open_id,
        "msgtype": "text",
        "text":
            {
                "content": f"{message}"
            }
    }
    requests.post(url, data=json.dumps(req_data, ensure_ascii=False).encode('utf-8'))

# 利用差分法实现动态捕捉。

camera = cv2.VideoCapture(0)
# 差分对比背景。
init_background = None
es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 4))
is_send_msg = False


while True:
    grabbed, frame = camera.read()

    # 转换为灰度图后进行高斯滤波。
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gaussian_gray_frame = cv2.GaussianBlur(gray_frame, (25, 25), 3)

    #赋值初始背景。
    if init_background is None:
        init_background = gaussian_gray_frame
        continue

    #求差分。
    diff = cv2.absdiff(init_background, gray_frame)
    # 去噪。
    diff = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)[1]
    # 腐蚀。
    diff = cv2.dilate(diff, es, iterations=3)
    # 获取轮廓。
    contours, hierarchy = cv2.findContours(diff.copy(), cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)
    is_find_object = False
    # 遍历判断差分大小。
    for c in contours:
        if cv2.contourArea(c) < 2000:
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        is_find_object = True
        if not is_send_msg:
            is_send_msg = True
            set_wechat_message('FORBIDDEN！！！')

    # 窗口视图部分。
    if is_find_object:
        show_text = "Motion: You are detected!"
        show_color = (0, 0, 255)
    else:
        show_text = "Motion: Nothing is detected"
        show_color = (0, 255, 0)

    cv2.putText(frame, show_text, (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, show_color, 2)

    cv2.imshow('init_frame', frame)
    cv2.imshow('diff_frame', diff)

    key = cv2.waitKey(1) & 0xFFf
    if key == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()