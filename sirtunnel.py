#!/usr/bin/env python3

import sys
import json
import time
from urllib import request
from urllib.error import HTTPError
import argparse
import logging

def delete(tunnel_id, caddy_api):
    delete_url = '{}/id/{}'.format(caddy_api, tunnel_id)
    req = request.Request(method='DELETE', url=delete_url)
    request.urlopen(req)

    # delete_error_url = '{}/id/{}'.format(caddy_api, tunnel_id + '-error')
    # error_req = request.Request(method='DELETE', url=delete_error_url)
    # request.urlopen(error_req)

if __name__ == '__main__':
    parser = argparse.ArgumentParser("SirTunnel", description="An easy way to securely expose a webserver running on one computer via a public URL")
    parser.add_argument("--debug", action="store_true", help="Additional logs")
    parser.add_argument("--caddy-api", default="http://127.0.0.1:2019", help="Caddy's admin api")
    parser.add_argument("domain", help="External domain name")
    parser.add_argument("tunnel_port", type=int, help="The tunnel port between your computer and the server per the command ssh -tr <tunnel_port>:localhost:8000")

    args = parser.parse_args()
    host = args.domain
    port = str(args.tunnel_port)
    debug = args.debug

    caddy_api = args.caddy_api

    logging.basicConfig(level="DEBUG" if debug else "INFO")

    LOGGER = logging.getLogger(__name__)
    LOGGER.debug("Log level set to debug")

    tunnel_id = host

    LOGGER.debug("Tunnel id build %s", tunnel_id)

    headers = {
        'Content-Type': 'application/json'
    }

    LOGGER.info("Checking domain and ports availability")
    req = request.Request(method='GET', url="{}/config/apps/http/servers/sirtunnel/routes".format(caddy_api), headers=headers)
    outcome = request.urlopen(req).read().decode('utf-8')
    routes = json.loads(outcome)
    for route in routes:
        if route['@id'] == host:
            delete(route['@id'], caddy_api)

    caddy_add_route_request = {
        "@id": tunnel_id,
        "match": [{
            "host": [host],
        }],
        "handle": [{
            "handler": "reverse_proxy",
            "upstreams":[{
                "dial": ':' + port
            }]
        }]
    }

    caddy_add_error_request = {
        "@id": tunnel_id + "-error",
        "match": [{
            "host": [host],
        }],
        "handle": [{
            "handler": "static_response",
            "body": "Tunnel " + host + " is unreachable."
        }]
    }

    route_body = json.dumps(caddy_add_route_request).encode('utf-8')
    error_body = json.dumps(caddy_add_error_request).encode('utf-8')
    
    create_route_url = '{}/config/apps/http/servers/sirtunnel/routes'.format(caddy_api)
    route_req = request.Request(method='POST', url=create_route_url, headers=headers)
    request.urlopen(route_req, route_body)

    create_error_url = '{}/config/apps/http/servers/sirtunnel/errors/routes'.format(caddy_api)
    error_req = request.Request(method='POST', url=create_error_url, headers=headers)
    request.urlopen(error_req, error_body)

    print("Tunnel created successfully")

    while True:
        try:
            time.sleep(10)
            # Quick check that the tunnel still exists
            req = request.Request(method='GET', url=caddy_api + '/id/' + tunnel_id)
            response = request.urlopen(req)
        except KeyboardInterrupt:
            print("Cleaning up tunnel")
            delete_url = caddy_api + '/id/' + tunnel_id
            req = request.Request(method='DELETE', url=delete_url)
            request.urlopen(req)
            break
        except HTTPError as ex:
            LOGGER.debug(str(ex))
            LOGGER.critical("Domain entry does not exist anymore. Aborting")
            break
