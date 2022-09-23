'''
For example:
    python add_user.py -n USER_test -date 2023-08-01
'''


import os, argparse

def parserArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-n',
        '--user_name',
        help = "usage: add_user -n username",
        type = str
    )
    parser.add_argument(
        '-date',
        '--expiration_date',
        help="for example: 2023-08-01",
        type = str
    )
    return parser.parse_args()


args = parserArgs()
username = args.username
expiration_date = args.expiration_date

shfile = '''
#!/bin/bash
cp /nfsshare/lsf10.1/conf/lsbatch/cjdx.cluster/configdir/lsb.users /nfsshare/lsf10.1/conf/lsbatch/cjdx.cluster/configdir/lsb.users.bak
cp /nfsshare/lsf10.1/conf/lsbatch/cjdx.cluster/configdir/lsb.queues /nfsshare/lsf10.1/conf/lsbatch/cjdx.cluster/configdir/lsb.queues.bak
cp /etc/passwd /etc/passwd.bak

USRPASS=""

PASS=`tr -dc A-Za-z0-9_ < /dev/urandom | head -c10`
useradd -d /nfsshare/home/{USR} -e {EXPIR} -s /bin/bash -m {USR}
quotatool -u {USR} -b -q 150G -l 150G /nfsshare
echo "{USR}:$PASS" | chpasswd
USRPASS="{USR}PASS\nUsername: {USR}\nPassword: $PASS"
sed -i '575s/$/'" {USR}"'/' /nfsshare/lsf10.1/conf/lsbatch/cjdx.cluster/configdir/lsb.queues
sed -i '586s/$/'" {USR}"'/' /nfsshare/lsf10.1/conf/lsbatch/cjdx.cluster/configdir/lsb.queues
sed -i '597s/$/'" {USR}"'/' /nfsshare/lsf10.1/conf/lsbatch/cjdx.cluster/configdir/lsb.queues
sed -i '85s/$/'"\n{USR}  10  1"'/' /nfsshare/lsf10.1/conf/lsbatch/cjdx.cluster/configdir/lsb.users

make -C /var/yp
badmin reconfig
'''.format(USR = username, EXPIR = expiration_date)


with open("./add_user.sh", 'w') as f:
    f.write(shfile)
    
os.system('./add_user.sh')

os.system('rm -f ./add_user.sh')
    
    