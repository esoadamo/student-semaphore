from flask import Flask, redirect
from web import init_web_app
from os import environ

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = environ.get('SECRET_KEY', 'REPLACE_ME')

init_web_app(app, '/room')


@app.route('/')
def index():
    return redirect('/room/')


if __name__ == '__main__':
    app.run()
