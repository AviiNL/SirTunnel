#/bin/bash

chmod 755 /root/.ssh
chmod 644 /root/ssh/authorized_keys

/usr/sbin/sshd

./caddy run --config caddy_config.json
