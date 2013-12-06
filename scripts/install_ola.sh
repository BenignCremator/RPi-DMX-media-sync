#!/bin/bash

chmod 777 /etc/apt
echo "deb http://apt.openlighting.org/raspbian wheezy main" >> /etc/apt/sources.list
chmod 755 /etc/apt
apt-get update

#  Add ethtool for diagnostic use
apt-get install ethtool
apt-get install ola ola-python ola-rdm-tests

#  Add ola daemon user in case apt-get did not
#  Setting shell to /bin/bash for dev purposes
#  Change back to /bin/false for prod
if [ `grep -c olad /etc/passwd` ]
then
    adduser --system --home /home/olad --shell /bin/bash olad
fi

#  Make certain we have a place for the files
if [ ! -d /home/olad ]
then
    mkdir /home/olad
    chown olad:olad /home/olad
fi

/etc/init.d/olad start
/etc/init.d/olad status
/etc/init.d/rdm_test_server start
/etc/init.d/rdm_test_server status

ola_patch -d 1 -p 0 -u 0 -i
ola_dev_info
ola_dmxmonitor -u 0



