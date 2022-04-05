import os

import cv2
import face_recognition

target_face_name = ['haruluya']
person_face_name_list = []
person_face_data_list = []

#读取图片并提取脸部特征。
image_files = os.listdir('images')
for image_file in  image_files:
    # 提取照片人名。
    person_name,format = os.path.splitext(image_file)
    person_face_name_list.append(person_name)

    # 提取人脸特征并保存。
    image_url = os.path.join('images', image_file)
    image_data = face_recognition.load_image_file(image_url,'RGB')
    person_face_data = face_recognition.face_encodings(image_data)[0]
    person_face_data_list.append(person_face_data)

# 人脸识别。
video_capture = cv2.VideoCapture(0)
while True:
    ret, frame = video_capture.read()
    # 提取人脸并提取脸部特征。
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # 遍历匹配人脸特征。
    matched_person_name_list = []
    person_name = "DISMATCH"
    for face_encoding in face_encodings:
        result = face_recognition.compare_faces(person_face_data_list, face_encoding)

        for index, _match in enumerate(result):
            if _match:
                person_name = person_face_name_list[index]
                break
        matched_person_name_list.append(person_name)

# view部分。
    for (top, right, bottom, left), name in zip(face_locations, matched_person_name_list):

        color = (255, 0, 0)
        if name in target_face_name:
            color = (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left, top - 10), font, 0.5, color, 1)
    cv2.imshow("face_location_haruluya", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


video_capture.release()
cv2.destroyAllWindows()
