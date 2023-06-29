import cv2
import base64
from flask import Flask, Response

app = Flask(__name__)

@app.route('/')
def index():
    return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

def get_frame():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # 将帧编码为JPEG格式
        ret, jpeg = cv2.imencode('.jpg', frame)

        # 将JPEG编码的帧转换为Base64字符串
        b64 = base64.b64encode(jpeg.tobytes()).decode('utf-8')

        # 将Base64字符串作为MJPEG数据流发送给Web页面
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + b64.encode('utf-8') + b'\r\n')

    # 释放摄像头并关闭窗口
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    app.run(debug=True)
