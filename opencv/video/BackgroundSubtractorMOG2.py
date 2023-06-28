import cv2


cap = cv2.VideoCapture(0)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
model = cv2.createBackgroundSubtractorMOG2()

while(True):
    ret, frame = cap.read()
    if not ret:
        continue

    fgmk = model.apply(frame)
    fgmk = cv2.morphologyEx(fgmk, cv2.MORPH_OPEN, kernel)
    contours = cv2.findContours(fgmk, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    print(len(contours))
    # print(contours)
    for c in contours:
        length = cv2.arcLength(c, True)
        if length > 388:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow('fgmk', fgmk)
        # cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xff == 27:
            break

cap.release()
cv2.destroyAllWindows()