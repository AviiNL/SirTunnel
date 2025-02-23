#/bin/bash

caddyVersion=2.4.4

echo Download Caddy
caddyGz=caddy_${caddyVersion}_linux_amd64.tar.gz
curl -s -O -L https://github.com/caddyserver/caddy/releases/download/v${caddyVersion}/${caddyGz}
tar xf ${caddyGz}

echo Clean up extra Caddy files
rm ${caddyGz}
rm LICENSE
rm README.md
