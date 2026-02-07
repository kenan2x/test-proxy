#!/bin/sh
set -e

# Generate CA certificate if not exists
if [ ! -f /certs/mitmproxy-ca-cert.pem ]; then
    echo "[ENTRYPOINT] Generating CA certificate..."
    mkdir -p /certs
    mitmdump --set confdir=/certs -n 2>/dev/null || true
    echo "[ENTRYPOINT] CA certificate generated at /certs/mitmproxy-ca-cert.pem"
fi

# Start mitmproxy with addon
exec mitmdump -s /scripts/proxy-addon.py --set confdir=/certs --set block_global=false
