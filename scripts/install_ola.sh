#!/bin/bash

chmod 777 /etc/apt
echo "deb http://apt.openlighting.org/raspbian wheezy main" >> /etc/apt/sources.list
chmod 755 /etc/apt
apt-get update
apt-get install ethtool
apt-get install ola ola-python ola-rdm-tests

if [ `grep -c olad /etc/passwd` ]
then
    adduser --system --home /home/olad --shell /bin/bash olad
fi

if [ ! -d /home/olad ]
then
    mkdir /home/olad
    chown olad:olad /home/olad
fi

/etc/init.d/olad start
/etc/init.d/olad status
/etc/init.d/rdm_test_server start
/etc/init.d/rdm_test_server status


