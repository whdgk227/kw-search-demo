from app import app

from flask import make_response, render_template, request, send_file


@app.route('/')
@app.route('/index')
def index():
    return "Hello, Keyword!"


@app.route('/search')
def search():
    headers = {'Content-Type': 'text/html'}
    templates = render_template("search.html")
    return make_response(templates, 200, headers)
