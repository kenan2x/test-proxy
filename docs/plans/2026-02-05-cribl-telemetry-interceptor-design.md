# Cribl Telemetry Interceptor & Mock Server Design

**Date:** 2026-02-05
**Status:** Approved
**Goal:** Capture Cribl telemetry traffic to `cdn.cribl.io/telemetry/`, analyze payload, and create a mock server for testing/analysis.

---

## Overview

This project intercepts and analyzes telemetry data sent by Cribl containers to understand what metrics/data are being collected, then creates a mock telemetry server for controlled testing environments.

## Architecture & Components

### 1. Cribl Container (Existing)
- **Image:** `cribl/cribl:latest`
- **Network:** `obs_net`
- **Configuration:** Modified to route traffic through proxy with CA certificate injection

### 2. mitmproxy Container (Phase 1 - Traffic Capture)
- **Image:** `mitmproxy/mitmproxy:latest`
- **Purpose:** Transparent HTTPS proxy to decrypt and capture telemetry traffic
- **Ports:**
  - 8080: Proxy port
  - 8081: Web UI for live traffic inspection
- **Volumes:**
  - `./captures`: Captured traffic in HAR/JSON format
  - `./certs`: Auto-generated CA certificates
- **Features:**
  - Live traffic monitoring via web interface
  - Export captured requests/responses
  - SSL/TLS decryption with custom CA

### 3. Telemetry Mock Server (Phase 2 - Mock)
- **Technology:** Python FastAPI
- **Port:** 8000
- **Purpose:** Replicate Cribl telemetry endpoints for controlled testing
- **Features:**
  - Dynamic endpoint generation from captured data
  - Smart response system (realistic timestamps, IDs)
  - Comprehensive request/response logging
  - Compatible with Cribl's telemetry client

### Network Flow

```
Phase 1 (Capture):
Cribl → HTTP_PROXY → mitmproxy:8080 → cdn.cribl.io
                           ↓
                   Capture & Export

Phase 2 (Mock):
Cribl → extra_hosts → telemetry-mock:8000 → Response
                           ↓
                    Log & Analyze
```

---

## Phase 1: Traffic Capture Setup

### mitmproxy Container Configuration

**docker-compose.yml addition:**
```yaml
mitmproxy:
  image: mitmproxy/mitmproxy:latest
  container_name: mitmproxy
  command: mitmweb --web-host 0.0.0.0 --set block_global=false
  ports:
    - "8080:8080"  # Proxy port
    - "8081:8081"  # Web UI
  volumes:
    - ./captures:/home/mitmproxy/captures
    - ./certs:/home/mitmproxy/.mitmproxy
  networks:
    - obs_net
```

### Cribl Container Proxy Configuration

**Modifications to Cribl service:**
```yaml
environment:
  - HTTP_PROXY=http://mitmproxy:8080
  - HTTPS_PROXY=http://mitmproxy:8080
  - SSL_CERT_FILE=/opt/cribl/mitmproxy-ca-cert.pem
volumes:
  - ./certs/mitmproxy-ca-cert.pem:/opt/cribl/mitmproxy-ca-cert.pem:ro
depends_on:
  - mitmproxy
```

### Capture Workflow

1. Start mitmproxy: `docker compose up mitmproxy`
2. CA certificate auto-generates in `./certs/`
3. Restart Cribl container with proxy configuration
4. Access Web UI at `http://localhost:8081` for live traffic
5. Export captured traffic as HAR/JSON to `./captures/`
6. Analyze captured data to identify endpoints, payloads, headers

---

## Phase 2: Mock Server Implementation

### Project Structure

```
telemetry-mock/
├── app/
│   ├── main.py           # FastAPI application, route definitions
│   ├── models.py         # Pydantic models (generated from captured data)
│   ├── responses.py      # Response templates based on real data
│   └── logger.py         # Request/response logging system
├── captured_data/        # HAR/JSON files from Phase 1
├── requirements.txt      # Python dependencies
└── Dockerfile           # Container image definition
```

### Mock Server Features

#### 1. Dynamic Endpoint Generation
- Parse captured HAR/JSON files
- Auto-generate FastAPI routes for each discovered endpoint
- Match path parameters, query parameters, and headers

#### 2. Smart Response System
- Use captured responses as templates
- Generate dynamic values:
  - Timestamps (current time)
  - Random IDs (UUIDs)
  - Request-specific data echoing
- Maintain original HTTP status codes

#### 3. Comprehensive Logging
**Request logging:**
- Timestamp
- HTTP method & path
- Headers (full set)
- Query parameters
- Request body (JSON parsed)

**Response logging:**
- Status code
- Response body
- Latency (processing time)

**Output formats:**
- JSON files in `/logs` directory (one per request)
- Pretty-printed console output for real-time monitoring

#### 4. Host File Redirection
Cribl container's `/etc/hosts` override:
```yaml
extra_hosts:
  - "cdn.cribl.io:telemetry-mock"
```

This redirects all `cdn.cribl.io` DNS lookups to the mock server within Docker network.

---

## Testing & Deployment Strategy

### Phase 1 Validation

**Success Criteria:**
- ✅ At least 1 telemetry request captured in mitmproxy Web UI
- ✅ HAR export successful and parseable
- ✅ Request endpoints, headers, and payloads clearly visible
- ✅ SSL/TLS decryption working (HTTPS content readable)

**Verification Steps:**
1. Monitor mitmproxy Web UI during Cribl startup
2. Wait for telemetry heartbeat (usually within 5 minutes)
3. Inspect captured request details
4. Export to HAR and validate JSON structure

### Mock Server Unit Tests

**Test Coverage:**
- Endpoint routing (correct handlers for captured URLs)
- Response accuracy (matches captured response structure)
- Request logging (all fields captured correctly)
- Error handling (400/404/500 for invalid requests)

**Test Framework:** pytest
```python
def test_telemetry_endpoint():
    response = client.post("/telemetry/v1/metrics", json=sample_payload)
    assert response.status_code == 200
    assert "timestamp" in response.json()
```

### Integration Testing

**Test Scenario:**
1. Start mock server: `docker compose up telemetry-mock`
2. Modify Cribl service to use `extra_hosts` for DNS override
3. Restart Cribl container
4. Monitor mock server logs for incoming requests
5. Verify Cribl shows no errors in UI/logs
6. Confirm telemetry data appears in mock server logs

**Success Criteria:**
- ✅ Cribl successfully sends telemetry to mock server
- ✅ Mock server logs show complete request details
- ✅ No connection errors in Cribl logs
- ✅ Mock server responds with valid HTTP 200/201

### Final Container Deployment

**Complete docker-compose.yml structure:**
```yaml
version: '3.8'

services:
  cribl:
    image: cribl/cribl:latest
    container_name: cribl
    restart: unless-stopped
    environment:
      - CRIB_DIST_MODE=single
    extra_hosts:
      - "cdn.cribl.io:telemetry-mock"  # DNS override
    volumes:
      - cribl_config:/opt/cribl/config-volume
      - cribl_local:/opt/cribl/local
    ports:
      - "9000:9000"
      - "10001:10001"
      - "9514:9514/tcp"
      - "9514:9514/udp"
    networks:
      - obs_net
    depends_on:
      - telemetry-mock

  telemetry-mock:
    build: ./telemetry-mock
    container_name: telemetry-mock
    restart: unless-stopped
    ports:
      - "8000:8000"
    volumes:
      - ./logs:/app/logs
    networks:
      - obs_net

networks:
  obs_net:
    driver: bridge

volumes:
  cribl_config:
  cribl_local:
```

---

## Success Criteria (Final)

- ✅ Cribl telemetry requests redirect to mock server
- ✅ Mock server logs capture complete telemetry payload
- ✅ Cribl operates normally without errors
- ✅ All components running in Docker containers
- ✅ Mock server responses compatible with Cribl client
- ✅ Complete audit trail of telemetry data collected

---

## Security & Privacy Considerations

- Captured telemetry data may contain sensitive system information
- Store captures in `.gitignore`d directories
- Mock server should only run in isolated test environments
- CA certificates should not be shared or committed to version control

---

## Future Enhancements

- Metrics dashboard (visualize captured telemetry)
- Telemetry data filtering (privacy-preserving mock)
- Performance testing (load testing with mock server)
- Multi-environment support (dev/staging/prod configs)
