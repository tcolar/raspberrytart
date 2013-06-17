
# History: Jun 14 13 Thibaut Colar Creation

from flask import Flask, redirect, url_for, render_template, g
from flask.ext.bootstrap import Bootstrap
import sys
import re
import os
import subprocess
import traceback
import fcntl
import time

app = Flask(__name__)

Bootstrap(app)

app.ctl = os.getenv("HOME") + '/.config/pianobar/ctl'
app.state = state = os.getenv("HOME") + '/.config/pianobar/state'
app.pb = None
app.cur_station = None
app.station_list = {}
app.pending_station = False

@app.route('/')
def index():
    return redirect(url_for('music'))

@app.route('/music/')
def music():
    if not app.station_list:
        return redirect(url_for('stations_refresh'))
    return render_template('music.html', stations = app.station_list)
#    if not app.cur_station:
#        return redirect(url_for('stations'))
#    return 'Cur Station: ' + app.cur_station

@app.route('/music/stations_refresh')
def stations_refresh():
    out = ''
    if not app.pending_station:
        out = send('s', 4)
    else:
        out = app.pb.stdout.read()

    # parse stations
    for line in out.split('\n'):
        match = re.search(r".*(\d+)\)\s([qQ]\s)?(.*)", line.strip())
        if match:
            app.station_list[match.group(1)] = match.group(3)
    if not app.station_list:
        app.station_list["?"] = "Error: No Stations found !!"
    return redirect(url_for('music'))

### Called via Ajax ##########################################################
@app.route('/music/skip')
def pause():
  if app.pending_station:
      return ''
  send("n")
  return "ok"

@app.route('/music/pause')
def pause():
  if app.pending_station:
      return ''
  send("p")
  return "ok"

@app.route('/music/volume/<action>')
def volume(action):
  if app.pending_station:
      return ''
  if action == 'up':
    send("(((((")
  elif action == 'down':
    send(")))))")
  return "ok"

@app.route('/music/station/<id>')
def station(id):
    app.cur_station = id
    if not app.pending_station:
        send('s')
    send(id + "\n")
    app.pending_station = False
    return 'ok'

@app.route('/music/reset_pianobar')
def reset():
    do_reset()
    return 'ok'

### Internals ################################################################

def do_reset():
    if os.path.exists(app.state):
      os.remove(app.state) # Necessary so we don't get autoplay
    if app.pb:
        if app.pending_station:
            send("0\n")
            send('q')
        app.pb.kill()
    app.pb = subprocess.Popen('pianobar', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    fcntl.fcntl(app.pb.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
    app.pending_station = True
    app.cur_station = None

def send(cmd, wait = 0):
    with open(app.ctl, 'a') as fifo:
        fifo.write(cmd)
        fifo.flush()
    out = ''
    time.sleep(wait)
    try:
        out = app.pb.stdout.read()
    except:
        print "error"
    print out
    return out


def get_lines(until):
    app.pb.expect(until)
    return app.pb.before

##### Main ###################################################################

if __name__ == '__main__':
    try:
        do_reset()
        app.run(debug=False)
    except:
        traceback.print_exc()

    app.pb.terminate()

