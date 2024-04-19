from flask import Flask, jsonify, Response, make_response, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from flask_ngrok import run_with_ngrok

import os 
import random
from video_processing import VideoPlayer

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'video'

@app.route('/')
def index():
    return render_template('index.html')

vp = VideoPlayer()

@app.route('/video', methods=['GET','POST'])
def video():
    return Response(vp.generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/upload',methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            path =  os.path.join(app.config['UPLOAD_FOLDER'],filename)
            file.save(path)
            vp.run_new_video(path)
            return redirect(url_for('index'))




if __name__ == '__main__':
    app.run(debug=True)