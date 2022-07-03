import os
import shutil
import flask
# from flask_socketio import SocketIO, emit
from flask import Flask, render_template, request, send_file, make_response, send_from_directory



# stream = None
app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
# socketIo = SocketIO(app)


# def gen():
#     while True:
#         # 读取
#         ret, frame = capture.read()
#         # 将获取到的框架，转格式、转码
#         frame = cv2.imencode(".jpg", frame)[1].tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# 视频喂流
# @app.route("/video_feed")
# def video_feed():
#     return Response(gen(),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def root():
    return render_template("index.html")


@app.route("/show")
def show():
    return render_template("show.html")


# 聊天
@app.route("/discuss")
def discuss():
    ip = request.remote_addr
    return render_template("discuss.html", ip=ip)


# 返回
@app.route("/shutdown")
def shutdown():
    # capture.release()
    return render_template("index.html")


# 视频测试
@app.route("/video")
def video():
    return render_template("video.html")


# 文件上传
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        try:
            f = request.files['file']
        except:
            return "上传错误"
        if f.filename == '':
            return '没有查询到文件'
        path = 'static/upload/'
        f.save(path + f.filename)
        return flask.redirect('/file')
    else:
        print('get')


# 文件下载
@app.route('/download/<string:file_name>')
def download(file_name):
    response = make_response(send_from_directory("static/upload", file_name, as_attachment=True))
    response.headers["Content-Disposition"] = f"attachment; filename={file_name.encode().decode('latin-1')}"
    return response


# 文件删除
@app.route('/delete/<string:file_name>')
def delete(file_name):
    try:
        shutil.move(f'static/upload/{file_name}', f'static/delete/{file_name}')
    finally:
        return flask.redirect('/file')


# 文件预览
@app.route('/static/<string:file_name>')
def preview(file_name):
    return send_file(f'static/upload/{file_name}')


# 文件界面
@app.route('/file')
def file():
    file_list = os.listdir('static/upload')
    return render_template('file.html', file_list=file_list)


@app.route('/test')
def index():
    return render_template('test.html')


# @socketIo.on('imessage', namespace='/test_conn')
# def test_message(message):
#     emit('message',
#          # 后端广播信息的事件名最好跟前端发送信息的事件名不一样
#          {'data': message['data']},
#          broadcast=True)


if __name__ == '__main__':
    # socketIo.run(app, debug=True)
    app.run(debug=True, host='0.0.0.0')
