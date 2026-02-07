#!/bin/sh
set -e

# Generate CA certificate if not exists
if [ ! -f /certs/mitmproxy-ca-cert.pem ]; then
    echo "[ENTRYPOINT] Generating CA certificate..."
    mkdir -p /certs
    # Run mitmdump briefly just to generate certs, then kill it
    timeout 5 mitmdump --set confdir=/certs -n 2>/dev/null || true
    echo "[ENTRYPOINT] CA certificate generated at /certs/mitmproxy-ca-cert.pem"
fi

echo "[ENTRYPOINT] Starting mitmproxy on port 8081..."
# Start mitmproxy with addon
exec mitmdump -s /scripts/proxy-addon.py --set confdir=/certs --set block_global=false --set connection_strategy=lazy --listen-port 8081
