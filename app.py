from flask import Flask, jsonify, Response, make_response, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
import os

from video_processing import VideoPlayer
import datetime

app = Flask(__name__)





app.config['UPLOAD_FOLDER'] = 'video'
vp = VideoPlayer(video_time=datetime.datetime(2024,5,1,17,57,41))
#vp.run_new_video('flask_test/video/test.mp4')

vid_ind = 0 
VIDEOS = [
    'C:\\Users\\master\\Downloads\\test1.mp4',
    'C:\\Users\\master\\Downloads\\test2.mp4'
]

vp.set_playlist(VIDEOS)



vp.add_line(284,49, 617,253, 781,439)
vp.add_line(161,170, 369,424, 781,439)
vp.add_line(276,432, 607,212, 781,439)
vp.add_line(1,272, 454,34, 781,439)

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

@app.route('/add_point', methods=['GET','POST'])
def add_point():
    if request.method == 'POST':
        data = request.json
        vp.add_point(data['x'],data['y'],data['width'], data['height'])
    return make_response(jsonify({'message':"OK"}),200)

@app.route('/count_table', methods=["GET"])
def count_table():
    return jsonify({'data': vp.get_stat().to_html()})

if __name__ == '__main__':
    app.run(debug=True)

#threading.Thread(target=app.run, kwargs={"use_reloader": False}).start()
