Thibaut Colar - 2013.

This is a Frontend for raspberry PI we use at the Rivet & Sway office.

h3. Features:
  - Pianobar web frontend (Pandora music streaming)

h3. Planned Features:
  - "Network monitor" : share a comuter screen to the screen connected to the PI over the network.

h3. Requirements:
  - Python
  - Pianobar
  - Flask & Flask-bootsrap

h3. Installation:
  Install Pianobar & Flask + Flask-Bootstrap:
    sudo apt-get install pianobar pip
    sudo pip install flask flask-bootstrap

  Create the Pianobar config file:
    mkdir ~/.config/pianobar
    echo "user = your_pandora_email@domain.com" >> ~/.config/pianobar/config
    echo "password = your_pandora_password" >> ~/.config/pianobar/config

  Create the pianobar FIFO:
      mkfifo ~/.config/pianobar/ctl

  Run "pianobar" to make sure it works ('q' to quit)

  Once that works we can run it:
    python music.py

  Head to http://host:5000/

