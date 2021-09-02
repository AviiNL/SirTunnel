#/bin/bash

mkdir -p /root/.ssh
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC7ZfowbYtqyGvnTCnLZcRlhC/7CxF9IjietfSJ0MSbQq0lbbl5rMfnYhDCEp0I/O1YR122yqnVJE83ljhk4z5FcSmc2jLgnYMOHTro5HwHuOUtRjcuChFmEE573UekuETbY1E0HHPzZ9JWh3yNHkf4g+8Jl+J/sixYGIbHUbNKfVpZ0uKrObbiej1Z1ray/70l72knUnVuHF/PrZLqRhn07WVt3JguBBUktv4IrZPi7SvM7OTjVKTKerVUUyCuEjt82P6X1peGENU5hjr6If9dGQDp0FUX850yV2UQLMqDal2AwGGXVo42NF60wqr7/0MKRXmyUYj37j5RTQfIkOTl AviiNL@DESKTOP-JPLAU3S" > /root/.ssh/authorized_keys
chmod 755 /root/.ssh
chmod 644 /root/ssh/authorized_keys

/usr/sbin/sshd

./caddy run --config caddy_config.json
