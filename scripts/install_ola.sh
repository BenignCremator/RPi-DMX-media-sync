#!/bin/bash

chmod 777 /etc/apt
echo "deb http://apt.openlighting.org/raspbian wheezy main" >> /etc/apt/sources.list
chmod 755 /etc/apt
apt-get update
apt-get install ola ola-python ola-rdm-tests
adduser pi olad


/etc/init.d/olad start
/etc/init.d/olad status
/etc/init.d/rdm_test_server start
/etc/init.d/rdm_test_server status


