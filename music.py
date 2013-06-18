
# History: Jun 14 13 Thibaut Colar Creation

from flask import Flask, redirect, url_for, render_template, g, jsonify
from flask.ext.bootstrap import Bootstrap
from datetime import datetime
from os.path import expanduser
import sys
import re
import os
import subprocess
import traceback
import fcntl
import time

app = Flask(__name__)

Bootstrap(app)

home = expanduser("~")
app.ctl = home + './.config/pianobar/ctl'
app.state = home + './.config/pianobar/state'
app.cur = home + './.config/pianobar/cur.txt'
app.cur_data = {}
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
def skip():
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

@app.route('/music/info')
def track_info():
    ts = os.path.getmtime(app.cur)
    if (not 'ts' in app.cur_data) or ts > app.cur_data['ts']:
        app.cur_data['ts'] = ts
        with open(app.cur) as f:
            lines = f.readlines()
            if 'songstart' in lines[0]:
                for line in lines:
                    if '=' in line:
                        (key, val) = line.split('=', 1)
                        if key in ['artist', 'title', 'album', 'coverArt',
                                   'detailUrl']:
                            app.cur_data[key] = val
    return jsonify(**app.cur_data)


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
        app.run(host='0.0.0.0', debug=False)
    except:
        traceback.print_exc()

    app.pb.terminate()

