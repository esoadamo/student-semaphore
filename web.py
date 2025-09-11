from flask import Flask, render_template, Blueprint
from pathlib import Path

DIR_ROOT = Path(__file__).parent.resolve()
DIR_STATIC = DIR_ROOT / 'static'
DIR_TEMPLATES = DIR_ROOT / 'templates'


def init_web_app(app_root: Flask, route_prefix: str = '/'):
    app = Blueprint(
        f'web_{route_prefix}',
        __name__,
        static_folder=DIR_STATIC,
        template_folder=DIR_TEMPLATES,
        url_prefix=route_prefix,
    )

    @app.route(f'/')
    def index():
        return render_template('room.html')

    app_root.register_blueprint(app)
