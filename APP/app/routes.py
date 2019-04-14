from app import app, cursor, connection
from flask import render_template, flash, redirect, url_for, request, session


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')



@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404