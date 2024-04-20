from flask import Flask, jsonify, Response, make_response, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from flask_ngrok import run_with_ngrok

import os 
import random
from video_processing import VideoPlayer

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'video'
#run_with_ngrok(app)

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
            res = make_response(jsonify({'message':f"{file.filename} uploaded"}),200)
            redirect(url_for('index'))
            return res


@app.route('/upload_video', methods=["GET","POST"])
def upload_video():
    if request.method == 'POST':
        filesize = request.cookies.get('filesize')
        file = request.files['file']

        print(f"Filesize {filesize}")
        print(file)

        res = make_response(jsonify({'message':f"{file.filename} uploaded"}),200)
        return res 


if __name__ == '__main__':
    app.run(debug=True)