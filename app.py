import eventlet
from eventlet import wsgi
from flask import Flask, render_template
from flask_socketio import SocketIO

import modules.library
import modules.player

app = Flask(__name__, static_folder='templates')
socketio = SocketIO(app, debug=True, cors_allowed_origins='*', async_mode='eventlet')


@app.route("/")
def info_panel():
    return render_template('info_panel.html')


@app.route('/admin')
def admin_panel():
    return render_template('control_panel.html')


@socketio.on("play")
def play():
    # player.random_start()
    player.play(from_start=True)


@socketio.on("play_random")
def play_random():
    player.play(from_start=False)


@socketio.on("previous")
def previous():
    player.set_track(library.get_previous())
    serializable = {str(k): str(v) for k, v in library.track_data[library.currently_played].items()}
    socketio.emit("song_update", serializable)


@socketio.on("next")
def next():
    player.set_track(library.get_next())
    serializable = {str(k): str(v) for k, v in library.track_data[library.currently_played].items()}
    socketio.emit("song_update", serializable)


@socketio.on("pause")
def pause():
    player.pause_unpause()


@socketio.on("shuffle")
def shuffle():
    library.shuffle()


@socketio.on("set_library")
def set_library(args):
    library.set_library(args['path'])
    player.set_track(library.get_currently_played_path())
    serializable = {str(k): str(v) for k, v in library.track_data[library.currently_played].items()}
    socketio.emit("song_update", serializable)


if __name__ == "__main__":
    library = modules.library.LocalLibraryWithFile()
    player = modules.player.LocalPlayer()

    wsgi.server(eventlet.listen(("127.0.0.1", 8000)), app)
