import winsound
import cv2
camera = cv2.VideoCapture(0)
while camera.isOpened():
    ret, frame1 = camera.read()
    ret, frame2 = camera.read()
    diff_frame = cv2.absdiff(frame1, frame2) # steady position-> full blackout if not steady -> whitespot => if whitespot then alarm,detect...
    color_grey = cv2.cvtColor(diff_frame, cv2.COLOR_RGB2GRAY) #convert rgb iinto grey
    blur = cv2.GaussianBlur(color_grey, (5, 5), 0)
    _, thresh_hold = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh_hold, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i in contours:
        if cv2.contourArea(i) < 4000:
            continue
        x, y, w, h = cv2.boundingRect(i)
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 215, 0), 2) # just detect bigger things moving.not small thing
        winsound.PlaySound('alert.wav', winsound.SND_ASYNC)
    if cv2.waitKey(10) == ord('e'):
        break
    cv2.imshow("Security Camera", frame1)
