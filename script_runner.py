



from http.server import BaseHTTPRequestHandler, HTTPServer

from scheduler import check_devices


class CustomRequestHandler(BaseHTTPRequestHandler):

    protocol_version = "HTTP/1.1"

    def do_GET(self):

        response = b"Python Backend Running Successfully"

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "text/plain"
        )

        self.send_header(
            "Content-Length",
            str(len(response))
        )

        self.end_headers()

        self.wfile.write(response)


if __name__ == "__main__":

    # ========================================================
    # CREATE LOCALHOST SERVER
    # ========================================================

    server = HTTPServer(
        ("localhost", 8000),
        CustomRequestHandler
    )

    print("========================================")
    print("LOCALHOST SERVER STARTED")
    print("http://localhost:8000")
    print("========================================")

    # ========================================================
    # SERVER START HONE KE BAAD check_devices()
    # CALL HOGA
    # ========================================================

    print("Starting device check...")

    result = check_devices()

    print("Device check result:")
    print(result)

    # ========================================================
    # KEEP SERVER RUNNING
    # ========================================================

    server.serve_forever()