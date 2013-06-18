Thibaut Colar - 2013.

This is a Frontend for raspberry PI that we use at work ([Rivet & Sway](http://www.rivetandsway.com)).

### Features:
  - Pianobar web frontend (Pandora music streaming)

### Planned Features:
  - "Network monitor" : share a comuter screen to the screen connected to the PI over the network.

### Requirements:
  - Python
  - Pianobar
  - Flask & Flask-bootstrap

### Installation:
  Install Pianobar & Flask + Flask-Bootstrap:

    sudo apt-get install pianobar python-pip
    sudo pip install flask flask-bootstrap

  Create the pianobar FIFO:

    mkfifo ~/.config/pianobar/ctl

### Configuration ############################################################
  Copy the confg files:

    cp config/config ~/.config/pianobar/
    cp config/eventcmd ~/.config/pianobar/
    chmod +x ~/.config/pianobar/eventcmd

  Edit the config file:
  Make sure to edit your pandora email and password and the event_command path

    vi ~/.config/pianobar/config

### Running ##################################################################
  Run:

    python music.py

  Head to http://host:5000/

