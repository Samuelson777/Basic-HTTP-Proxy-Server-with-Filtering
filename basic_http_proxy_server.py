"""
Basic HTTP Proxy Server with URL Filtering

This script implements a simple HTTP proxy server in Python that listens for HTTP requests,
filters requests based on blocked URL patterns, forwards allowed requests to target servers,
and returns responses back to the client.

Usage:
    python basic_http_proxy_server.py

Default:
    Listens on localhost:8888
    Blocks URLs containing substrings defined in BLOCKLIST

Note:
    - Only supports HTTP, NOT HTTPS.
    - For HTTPS, complex SSL/TLS handling is required.
    - This proxy is for educational purposes only.

"""

import http.server
import socketserver
import urllib.request
from urllib.parse import urlparse
import sys
import threading

# Configuration
HOST = "localhost"
PORT = 8888

# List of URL substrings to block
BLOCKLIST = [
    "ads.example.com",
    "tracking.example",
    "malicious-site.com",
    "phishing-site.net",
]

class ProxyRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL
        url = self.path
        parsed_url = urlparse(url)

        # Handle relative URLs (in case browser sends paths only)
        if not parsed_url.scheme:
            # Convert relative path to absolute URL with http scheme and Host header
            host = self.headers.get('Host')
            if not host:
                self.send_error(400, "Bad Request: Host header missing")
                return
            url = "http://" + host + self.path
            parsed_url = urlparse(url)

        # Check blocklist
        if any(blocked_substring in url for blocked_substring in BLOCKLIST):
            self.send_response(403)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            message = f"<html><body><h1>403 Forbidden</h1><p>Access to {url} is blocked by proxy filter.</p></body></html>"
            self.wfile.write(message.encode('utf-8'))
            print(f"Blocked URL access attempt: {url}")
            return

        # Forward the request
        try:
            req = urllib.request.Request(url)
            # Copy headers except Host (urllib adds Host automatically)
            for key in self.headers:
                if key.lower() == 'host':
                    continue
                req.add_header(key, self.headers[key])

            with urllib.request.urlopen(req) as resp:
                self.send_response(resp.status)
                # Copy headers to the client
                for key, value in resp.getheaders():
                    # Some headers might not be safe or logical to forward
                    if key.lower() in ['transfer-encoding', 'content-encoding', 'content-length']:
                        # We'll set content-length manually
                        continue
                    self.send_header(key, value)
                content = resp.read()
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                print(f"Proxied request: {url}")
        except Exception as e:
            self.send_error(502, f"Bad Gateway: {e}")
            print(f"Error proxying {url}: {e}")

    def do_CONNECT(self):
        # HTTPS proxying is not supported by this simple proxy.
        self.send_error(501, "Not Implemented: HTTPS not supported by this proxy.")

    def log_message(self, format, *args):
        # Override to suppress default logging or customize
        sys.stdout.write("%s - - [%s] %s\n"
                         % (self.client_address[0],
                            self.log_date_time_string(),
                            format%args))


def run_server():
    print(f"Starting proxy server on {HOST}:{PORT}")
    with socketserver.ThreadingTCPServer((HOST, PORT), ProxyRequestHandler) as httpd:
        print("Proxy server running. Configure your browser to use this proxy.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nProxy server stopped.")


if __name__ == "__main__":
    run_server()