# Cribl Telemetry Interceptor Proxy
# All-in-one: mitmproxy + addon + CA certificate

FROM mitmproxy/mitmproxy:latest

# Switch to root for setup
USER root

# Copy addon script and entrypoint
COPY proxy-addon.py /scripts/proxy-addon.py
COPY entrypoint.sh /scripts/entrypoint.sh
RUN chmod +x /scripts/entrypoint.sh

# Create directories
RUN mkdir -p /certs /logs && chmod 777 /certs /logs

# Switch back to mitmproxy user
USER mitmproxy

# Expose ports
EXPOSE 8080

# Set environment
ENV MITMPROXY_CONFDIR=/certs

# Use entrypoint to generate certs at runtime
ENTRYPOINT ["/scripts/entrypoint.sh"]
