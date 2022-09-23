#!/bin/bash
cp /nfsshare/lsf10.1/conf/lsbatch/cjdx.cluster/configdir/lsb.users /nfsshare/lsf10.1/conf/lsbatch/cjdx.cluster/configdir/lsb.users.bak
cp /nfsshare/lsf10.1/conf/lsbatch/cjdx.cluster/configdir/lsb.queues /nfsshare/lsf10.1/conf/lsbatch/cjdx.cluster/configdir/lsb.queues.bak
cp /etc/passwd /etc/passwd.bak

USRPASS=""
for USR in $@
do
    PASS=`tr -dc A-Za-z0-9_ < /dev/urandom | head -c10`
    useradd -d /nfsshare/home/$USR -e 2023-08-01 -s /bin/bash -m $USR
    quotatool -u $USR -b -q 150G -l 150G /nfsshare
    echo "$USR:$PASS" | chpasswd
    USRPASS="$USRPASS\nUsername: $USR\nPassword: $PASS"
    sed -i '575s/$/'" $USR"'/' /nfsshare/lsf10.1/conf/lsbatch/cjdx.cluster/configdir/lsb.queues
    sed -i '586s/$/'" $USR"'/' /nfsshare/lsf10.1/conf/lsbatch/cjdx.cluster/configdir/lsb.queues
    sed -i '597s/$/'" $USR"'/' /nfsshare/lsf10.1/conf/lsbatch/cjdx.cluster/configdir/lsb.queues
    sed -i '85s/$/'"\n$USR  10  1"'/' /nfsshare/lsf10.1/conf/lsbatch/cjdx.cluster/configdir/lsb.users
done
make -C /var/yp
badmin reconfig

echo -e $USRPASS 
