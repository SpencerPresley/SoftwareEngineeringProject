# Author: Jude Maggitti
# Last Modified: 3/17/24
# Summary: This is the basic framework that helps direct the web pages where to route certain paths 

from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

app.static_folder = 'static'

@app.route('/')
def home():
    return render_template('html/Version1/index.html')

@app.route('/html/Version1/<path:filename>')
def html(filename):
    html_folder = 'html/Version1'
    return render_template(f'{html_folder}/{filename}')

@app.route('/static/javaOldCopy/<path:filename>')
def static_files(filename):
    java_folder = 'javaOldCopy'
    return send_from_directory(app.static_folder, f'{java_folder}/{filename}')

@app.route('/static/json/<path:filename>')
def serve_json(filename):
    json_folder = 'json' 
    return send_from_directory(app.static_folder, f'{json_folder}/{filename}')

@app.route('/static/image/<path:filename>')
def img(filename):
    image_folder = 'image' 
    return send_from_directory(app.static_folder, f'{image_folder}/{filename}')

@app.route('/static/style/<path:filename>')
def css(filename):
    java_folder = 'style'
    return send_from_directory(app.static_folder, f'{java_folder}/{filename}')

if __name__ == '__main__':
    app.run(port=1111)
#port number we access