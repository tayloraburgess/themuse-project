from flask import Flask, render_template, send_from_directory
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/companies')
def companies():
    return render_template('companies.html')

@app.route('/posts')
def posts():
    return render_template('posts.html')

@app.route('/coaches')
def coaches():
    return render_template('coaches.html')

@app.route('/css/<path:path>')
def serve_css(path):
    return send_from_directory('static/css', path)

app.run()
