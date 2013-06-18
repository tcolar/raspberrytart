#!/bin/sh

# Thibaut Clar - 2013
# Init script for RaspberryTart

### BEGIN INIT INFO
# Provides:          tart
# Required-Start:    $local_fs $remote_fs $network
# Required-Stop:     $local_fs $remote_fs $network
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Raspberry Tart
## END INIT INFO

# Rapsberry tart installatio dir
TART_HOME=/home/pi/raspberrytart/
# User running process
USER=pi
# Python path
PYTHON=/usr/bin/python

#. /lib/lsb/init-functions

case "$1" in
    start)
        echo -n "Starting RaspberryTart... "
        cd $TART_HOME
        sudo -u $USER -H sh -c "cd $TART_HOME; $PYTHON music.py" > "/tmp/tart.log" 2>&1 &
        PID=$!
        echo $PID > "/tmp/tart.pid"
        ;;
    stop)
        echo -n "Stopping RaspberryTart... "
        if [ ! -f "/tmp/tart.pid" ]
        then
            echo "Already stopped!"
            exit 1
        fi
        PID=`cat "/tmp/tart.pid"`
        kill $PID
        rm -f "/tmp/tart.pid"
        ;;
esac

exit 0