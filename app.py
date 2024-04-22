from flask import Flask, jsonify, Response, make_response, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
import os
import threading
import os 
import random
from video_processing import VideoPlayer
from pyngrok import ngrok, conf

app = Flask(__name__)
# conf.get_default().auth_token = '2fKNpAlhTcNYlDTyZDjVDuTd58t_4sJBcLPh84HbVQ1ZKLnCg'
# public_url = ngrok.connect(5000).public_url
# print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}/\"".format(public_url, 5000))

# app.config["BASE_URL"] = public_url

app.config['UPLOAD_FOLDER'] = 'video'
vp = VideoPlayer()
vp.run_new_video('flask_test\\video\\test.mp4')


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/video', methods=['GET','POST'])
def video():
    new_frame = vp.generate_frames()
    return Response(new_frame,
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
            return res


if __name__ == '__main__':
    app.run()

#threading.Thread(target=app.run, kwargs={"use_reloader": False}).start()
