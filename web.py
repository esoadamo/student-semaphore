import json

from flask import Flask, render_template, Blueprint, session, abort, redirect, url_for, request, send_from_directory
from pathlib import Path
from typing import NotRequired, TypedDict


DIR_ROOT = Path(__file__).parent.resolve()
DIR_STATIC = DIR_ROOT / 'static'
DIR_TEMPLATES = DIR_ROOT / 'templates'
DIR_MODULES = DIR_ROOT / 'modules'

ROOM = [
    [{'name': '', 'hostname': None, 'status': None}, {'name': '', 'hostname': None, 'status': None}, {'name': '', 'hostname': None, 'status': None}, {'name': '', 'hostname': None, 'status': None}],
    [{'name': '', 'hostname': None, 'status': None}, {'name': '', 'hostname': None, 'status': None}, {'name': '', 'hostname': None, 'status': None}, {'name': '', 'hostname': None, 'status': None}],
    [{'name': '', 'hostname': None, 'status': None}, None, None, {'name': '', 'hostname': None, 'status': None}],
    [{'name': '', 'hostname': None, 'status': None}, None, None, {'name': '', 'hostname': None, 'status': None}],
    [{'name': '', 'hostname': None, 'status': None}, None, None, {'name': '', 'hostname': None, 'status': None}],
    [{'name': '', 'hostname': None, 'status': None}, None, None, {'name': '', 'hostname': None, 'status': None}],
    [{'name': '', 'hostname': None, 'status': None}, None, None, None],
]


class LoginSession(TypedDict):
    hostname: str
    room_id: str
    username: NotRequired[str]
    is_admin: NotRequired[bool]


def get_session() -> LoginSession:
    if 'student-semaphore::login' not in session:
        abort(401)
    return json.loads(session['student-semaphore::login'])


def init_web_app(app_root: Flask, route_prefix: str = '/'):
    app = Blueprint(
        f'web_{route_prefix}',
        __name__,
        static_folder=DIR_STATIC,
        template_folder=DIR_TEMPLATES,
        url_prefix=route_prefix,
    )

    @app.route('/')
    def app_index():
        login = get_session()
        return render_template('room.html', login=login)

    @app.errorhandler(401)
    def app_error_unauthorized(_):
        return redirect(url_for('.app_login'))

    @app.route('/login', methods=['POST', 'GET'])
    def app_login():
        if request.method == 'POST':
            hostname = request.form.get('hostname')
            room_id = request.form.get('room_id')
            username = request.form.get('username', '')
            if not hostname or not room_id:
                abort(401)
            # TODO secret validation
            session['student-semaphore::login'] = json.dumps(LoginSession(hostname=hostname, room_id=room_id, username=username, is_admin=False))
            return redirect(url_for('.app_index'))
        return render_template('login.html')

    @app.route('/api/room')
    def app_api_get_room():
        get_session()
        return ROOM

    @app.route('/api/room/assign', methods=['POST'])
    def app_api_room_assign():
        login = get_session()
        hostname = login['hostname']
        target_row = int(request.json.get('row', -1))
        target_col = int(request.json.get('col', -1))
        if target_row < 0 or target_row >= len(ROOM) or target_col < 0 or target_col >= len(ROOM[0]):
            abort(400)
        if ROOM[target_row][target_col] is None or ROOM[target_row][target_col]['hostname'] is not None:
            abort(403)
        # Clear previous assignment
        current_status = None
        for r in range(len(ROOM)):
            for c in range(len(ROOM[r])):
                if ROOM[r][c] is not None and ROOM[r][c]['hostname'] == hostname:
                    current_status = ROOM[r][c]['status']
                    ROOM[r][c] = {'name': '', 'hostname': None, 'status': None}
        # Assign new seat
        ROOM[target_row][target_col] = {'name': login.get('username', ''), 'hostname': hostname, 'status': current_status}
        return {'success': True}

    @app.route('/api/room/status', methods=['POST'])
    def app_api_room_status():
        login = get_session()
        hostname = login['hostname']
        status = request.json.get('status')
        for r in range(len(ROOM)):
            for c in range(len(ROOM[r])):
                if ROOM[r][c] is not None and ROOM[r][c]['hostname'] == hostname:
                    ROOM[r][c]['status'] = status
                    return {'success': True}
        abort(403)

    @app.route('/api/room/name', methods=['POST'])
    def app_api_room_name():
        login = get_session()
        hostname = login['hostname']
        name = request.json.get('name')
        for r in range(len(ROOM)):
            for c in range(len(ROOM[r])):
                if ROOM[r][c] is not None and ROOM[r][c]['hostname'] == hostname:
                    ROOM[r][c]['name'] = name
                    return {'success': True}
        abort(403)

    @app.route('/api/module')
    def app_api_get_module():
        login = get_session()
        file_module = DIR_MODULES / f"{login['room_id']}.py"
        if not file_module.exists():
            file_module = DIR_MODULES / 'default.py'
        return send_from_directory(DIR_MODULES, file_module.relative_to(DIR_MODULES))

    app_root.register_blueprint(app)
