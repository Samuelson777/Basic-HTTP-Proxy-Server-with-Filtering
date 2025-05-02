# Basic HTTP Proxy Server with Filtering

## Overview
This project implements a simple HTTP proxy server in Python that listens for incoming HTTP requests, filters them based on a predefined blocklist of URL patterns, forwards allowed requests to the target servers, and returns the responses to the clients.

It is designed for educational purposes and allows users to understand proxy behavior, request routing, and basic URL filtering.

## Features
- Listens on localhost:8888 by default.
- Supports only HTTP protocol (no HTTPS).
- Filters requests whose URLs match blocklist patterns.
- Returns 403 Forbidden for blocked URLs with a custom message.
- Forwards allowed requests and returns the real response.
- Logs access and block attempts in the console.
- Simple to run and configure.

## Requirements
- Python 3.x  
- No external libraries needed (built using Python standard library).

## Usage
1. Run the proxy server
2. Configure your browser or HTTP client to use the proxy:  
- Host: `localhost`  
- Port: `8888`  
3. Visit websites as usual through the proxy.  
4. URLs contained in the blocklist will be blocked with a 403 response.

## Customizing Blocklist
To customize the blocklist, edit the `BLOCKLIST` list in the `basic_http_proxy_server.py` file. Add substrings to block URLs containing those patterns.

## Limitations
- Does **not** support HTTPS due to the complexity of SSL/TLS proxying.  
- Only GET requests are currently handled. Other HTTP methods are not supported.  
- Headers like Transfer-Encoding and Content-Encoding are not fully handled.  
- Intended for educational use and local testing.

## Conclusion
This basic HTTP proxy server offers a practical way to learn about HTTP proxies and request filtering. It demonstrates how requests can be intercepted, analyzed, and controlled before reaching their target servers. 

Running this proxy on your home PC allows you to experiment with request filtering and understand web traffic flow, forming a foundation for more advanced proxy or firewall projects.

## Restriction Warning
This proxy server is intended for educational and authorized testing purposes only. Do NOT use this proxy to intercept or alter traffic without the consent of involved parties. Unauthorized interception or tampering with network traffic may be illegal and unethical.

## Future Enhancements
- Support HTTPS proxying with SSL/TLS interception (requires certificate management).  
- Add support for other HTTP methods like POST, PUT, DELETE.  
- Implement more advanced filtering rules, e.g., regex matching or domain whitelisting.  
- Add a web-based dashboard for real-time monitoring and configuring filters.  
- Log requests and responses to files for audit purposes.  
- Add authentication for proxy use.  
- Support caching of responses to improve performance.

## License
This project is open source and available under the MIT License.
