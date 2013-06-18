This is a Frontend for raspberry PI that we use at work ([Rivet & Sway](http://www.rivetandsway.com)).

### Features:
  - Pianobar web frontend (Pandora music streaming)

### Planned Features:
  - "Network monitor" : share a comuter screen or document to the screen connected to the PI over the network.

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

### Configuration:
  Copy the confg files:

    cp config/config ~/.config/pianobar/
    cp config/eventcmd ~/.config/pianobar/
    chmod +x ~/.config/pianobar/eventcmd

  Edit the config file:
  Make sure to edit your pandora email and password and the event_command path

    vi ~/.config/pianobar/config

### Running:

    python music.py

  Head to http://host:5000/

  If you want to automatically run this when the server boots:
  **Edit init.d/tart.sh** and set the TART_HOME and USER vars correctly, then install it:

    sudo cp init.d/tart.sh /etc/init.d/
    sudo chmod +x /etc/init.d/tart.sh
    sudo update-rc.d tart.sh defaults

### Screenshot:

![Screenshot](https://raw.github.com/tcolar/raspberrytart/screenshot.png)

