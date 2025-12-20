from http.server import BaseHTTPRequestHandler, HTTPServer
import os

METRICS_FILE = "/var/metrics/worker.prom"
PORT = 9101

class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/metrics":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; version=0.0.4")
            self.end_headers()
            if os.path.exists(METRICS_FILE):
                with open(METRICS_FILE, "r") as f:
                    self.wfile.write(f.read().encode())
            else:
                self.wfile.write(b"# No metrics yet\n")
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    server = HTTPServer(("", PORT), MetricsHandler)
    print(f"Prometheus metrics server running on port {PORT}")
    server.serve_forever()
