from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Function to access the webcam
def webcam_stream():
    camera = cv2.VideoCapture(0)  # Use 0 for the first webcam
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route for streaming the webcam
@app.route('/video_feed')
def video_feed():
    return Response(webcam_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)  # Run the app on all available network interfaces
