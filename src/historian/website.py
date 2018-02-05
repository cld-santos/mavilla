import uuid
from celery import Celery
from flask import (
    Flask,
    request,
    abort,
    redirect,
    url_for,
)
from flask_socketio import SocketIO, emit
from flask import render_template
from historian.tasks.investigate import investigate_it
from historian.tools.investigation import Investigation


def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


flask_app = Flask(__name__)
flask_app.config.update(
    CELERY_BROKER_URL='amqp://guest@localhost//',
    CELERY_RESULT_BACKEND='amqp://guest@localhost//'
)

celery = make_celery(flask_app)
socketio = SocketIO(flask_app)

@flask_app.route('/')
def index():
    return render_template('index.html')


@flask_app.route('/investigate/', methods=['POST', 'GET'])
def investigate_now():
    url = request.form.get('url', None)
    if not url:
        abort(401)
    process_key = uuid.uuid4()
    investigate_it.delay([url], collection=process_key)
    return redirect(url_for('investigation', process_key=process_key))

@flask_app.route('/investigation/<process_key>', methods=['POST', 'GET'])
def investigation(process_key):
    return render_template('investigation.html', process_key=process_key)

@flask_app.route('/investigation/<process_key>/cancel', methods=['POST', 'GET'])
def cancel_investigation(process_key):
    investigation = Investigation(collection=process_key)
    investigation.kill_them_all()
    return redirect(url_for('index'))

@socketio.on('sendMessage')
def send_message(data):
    print(data['data'])
    emit('vaiMensagem', data, broadcast=True)


if __name__ == '__main__':
    socketio.run(flask_app)
