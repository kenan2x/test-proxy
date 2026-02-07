# Telemetry Mock Server

A comprehensive telemetry interception and analysis system built with FastAPI and mitmproxy. This project captures, logs, and serves mock telemetry data for Cribl Stream applications.

## Overview

This system intercepts telemetry requests from Cribl Stream and serves mock responses while logging all traffic for analysis. It's designed to help understand what telemetry data is collected and transmitted by Cribl applications.

## Architecture

```
Client Application (Cribl Stream)
        |
        v
   mitmproxy (Interceptor)
        |
        v
   Mock Server (FastAPI)
        |
        v
   Logs & Analysis
```

### Components

1. **Mock Server (FastAPI)**
   - Serves telemetry endpoints (`/telemetry/*`)
   - Provides health checks and metrics
   - Logs all requests and responses
   - Returns realistic mock data

2. **mitmproxy (Traffic Interceptor)**
   - Intercepts HTTPS traffic
   - Redirects telemetry requests to mock server
   - Transparent proxy for other traffic
   - SSL/TLS certificate management

3. **Logging System**
   - Structured JSON logs for all requests
   - Separate log files for different components
   - Request/response payload capture
   - Timestamp-based analysis

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.9+ (for local development)

### Running with Docker Compose

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down
```

The mock server will be available at:
- HTTP: `http://localhost:8000`
- Health check: `http://localhost:8000/health`
- Metrics: `http://localhost:8000/metrics`

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Run server locally
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Testing

### Unit Tests
```bash
pytest tests/unit/ -v
```

### Integration Tests
```bash
# Ensure services are running first
docker compose up -d

# Run integration tests
pytest tests/integration/ -v
```

### All Tests
```bash
pytest tests/ -v --cov=app
```

## Telemetry Data Captured

The system captures and logs the following telemetry information:

### Request Data
- **Timestamp**: When the request was made
- **URL**: Full request URL including query parameters
- **Method**: HTTP method (GET, POST, etc.)
- **Headers**: All request headers
- **Query Parameters**: Version info, environment, session IDs
- **User Agent**: Client application information
- **IP Address**: Source IP of the request

### Response Data
- **Status Code**: HTTP response status
- **Response Time**: Processing duration
- **Content Type**: Type of content served
- **Payload**: Mock telemetry data returned

### Common Query Parameters
- `v` or `version`: Application version
- `env`: Environment (prod, dev, staging)
- `session_id`: User session identifier
- `user_id`: User identifier
- `timestamp`: Client timestamp

## Log Files

Logs are stored in the `logs/` directory:

```
logs/
├── telemetry_requests.log    # All telemetry requests
├── mock_server.log            # Server operational logs
├── mitmproxy.log              # Proxy logs
└── analysis/                  # Analysis reports
    ├── summary.json           # Request statistics
    └── final-report.md        # Comprehensive analysis
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Server Configuration
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO

# mitmproxy Configuration
MITM_PORT=8080
MITM_HOST=0.0.0.0
```

### Docker Compose

The `docker-compose.yml` file configures:
- Network settings
- Volume mounts for logs
- Port mappings
- Service dependencies

## API Endpoints

### Health Check
```bash
GET /health
```
Returns server status and uptime.

### Metrics
```bash
GET /metrics
```
Returns request counts, response times, and error rates.

### Telemetry Endpoints
```bash
GET /telemetry/index.html
GET /telemetry/cribl.js
POST /telemetry/events
GET /telemetry/config
```

## Analysis

### View Request Summary
```bash
# Generate summary report
python -m app.analysis.summarize

# View in logs/analysis/summary.json
cat logs/analysis/summary.json
```

### Search Logs
```bash
# Find all requests with specific version
grep "version=1.2.3" logs/telemetry_requests.log

# Count requests by endpoint
jq -r '.url' logs/telemetry_requests.log | sort | uniq -c
```

## Security Considerations

This is a development/testing tool. For production use:

1. Enable authentication on endpoints
2. Encrypt log files containing sensitive data
3. Use secure certificate management
4. Implement rate limiting
5. Add input validation and sanitization

## Troubleshooting

### Services won't start
```bash
# Check if ports are in use
lsof -i :8000
lsof -i :8080

# View detailed logs
docker compose logs mock-server
docker compose logs mitmproxy
```

### No telemetry data captured
1. Verify client is configured to use proxy
2. Check mitmproxy certificate is trusted
3. Ensure firewall allows traffic
4. Review `logs/mitmproxy.log` for errors

### Tests failing
```bash
# Rebuild containers
docker compose down
docker compose build --no-cache
docker compose up -d

# Wait for services to be ready
sleep 5

# Run tests again
pytest tests/
```

## Development Roadmap

- [ ] Add database storage for telemetry data
- [ ] Build web UI for log analysis
- [ ] Implement data visualization dashboard
- [ ] Add support for WebSocket telemetry
- [ ] Create CLI for common operations
- [ ] Add export to CSV/Excel functionality

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Contact

For questions or issues, please open an issue on the project repository.
