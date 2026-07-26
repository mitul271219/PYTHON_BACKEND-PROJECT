import os
import json

from http.server import (
    BaseHTTPRequestHandler,
    HTTPServer
)

from google_sheets import (
    patient_sheet,
    bpm_sheet,
    oxy_sheet
)

from scheduler import check_devices
from dotenv import load_dotenv

load_dotenv()


# ============================================================
# HTTP REQUEST HANDLER
# ============================================================

class CustomRequestHandler(
    BaseHTTPRequestHandler
):

    protocol_version = "HTTP/1.1"


    # ========================================================
    # CORS HEADERS
    # ========================================================

    def _send_cors_headers(self):

        self.send_header(
            "Access-Control-Allow-Origin",
            "*"
        )

        self.send_header(
            "Access-Control-Allow-Methods",
            "POST, OPTIONS, GET"
        )

        self.send_header(
            "Access-Control-Allow-Headers",
            "X-API-KEY, Content-Type"
        )


    # ========================================================
    # SEND JSON RESPONSE
    # ========================================================

    def _send_json_response(
        self,
        data,
        status_code=200
    ):

        response_body = json.dumps(
            data
        ).encode(
            "utf-8"
        )


        self.send_response(
            status_code
        )


        self._send_cors_headers()


        self.send_header(
            "Content-Type",
            "application/json"
        )


        self.send_header(
            "Content-Length",
            str(
                len(response_body)
            )
        )


        self.end_headers()


        self.wfile.write(
            response_body
        )


    # ========================================================
    # OPTIONS REQUEST
    # ========================================================

    def do_OPTIONS(self):

        self.send_response(
            200
        )


        self._send_cors_headers()


        self.send_header(
            "Content-Length",
            "0"
        )


        self.end_headers()


    # ========================================================
    # GET REQUEST
    # ========================================================

    def do_GET(self):

        try:

            # ==================================================
            # HOME
            # ==================================================

            if self.path == "/":

                response = {

                    "success": True,

                    "message":
                    "Python Backend Running Successfully"

                }


                self._send_json_response(
                    response
                )


            # ==================================================
            # PATIENTS
            # ==================================================
            elif self.path == "/patients":

                data = patient_sheet.get_all_records()


                response = {

                    "success": True,

                    "message":
                    "Patients fetched successfully.",

                    "count":
                    len(data),

                    "data":
                    data

                }


                self._send_json_response(
                    response
                )


            # ==================================================
            # BPM
            # ==================================================

            elif self.path == "/bpm":

                data = bpm_sheet.get_all_records()


                response = {

                    "success": True,

                    "message":
                    "BPM data fetched successfully.",

                    "count":
                    len(data),

                    "data":
                    data

                }


                self._send_json_response(
                    response
                )


            # ==================================================
            # OXY
            # ==================================================

            elif self.path == "/oxy":

                data = oxy_sheet.get_all_records()


                response = {

                    "success": True,

                    "message":
                    "OXY data fetched successfully.",

                    "count":
                    len(data),

                    "data":
                    data

                }


                self._send_json_response(
                    response
                )


            # ==================================================
            # UNKNOWN GET ROUTE
            # ==================================================

            else:

                response = {

                    "success": False,

                    "message":
                    "GET endpoint not found"

                }


                self._send_json_response(
                    response,
                    404
                )


        except Exception as e:

            print(
                "GET ERROR:",
                e
            )


            response = {

                "success": False,

                "message":
                str(e)

            }


            self._send_json_response(
                response,
                500
            )


    # ========================================================
    # POST REQUEST
    # ========================================================

    def do_POST(self):

        try:

            # ==================================================
            # SECURITY CHECK
            # ==================================================

            expected_secret = os.environ.get(
                "BACKEND_SECRET"
            )


            client_secret = self.headers.get(
                "X-API-KEY"
            )


            if (
                not expected_secret
                or client_secret != expected_secret
            ):

                print(
                    "Unauthorized: Invalid API Key"
                )


                response = {

                    "success": False,

                    "message":
                    "Unauthorized. Invalid API Key."

                }


                self._send_json_response(
                    response,
                    401
                )


                return


            # ==================================================
            # CHECK DEVICE ENDPOINT
            # ==================================================

            if self.path == "/check-devices":

                print(
                    "Device check request received"
                )


                result = check_devices()


                if result.get(
                    "success"
                ):

                    self._send_json_response(
                        result,
                        200
                    )

                else:

                    self._send_json_response(
                        result,
                        500
                    )


                return


            # ==================================================
            # UNKNOWN POST ROUTE
            # ==================================================

            response = {

                "success": False,

                "message":
                "POST endpoint not found"

            }


            self._send_json_response(
                response,
                404
            )


        except Exception as e:

            print(
                "POST ERROR:",
                e
            )


            response = {

                "success": False,

                "message":
                str(e)

            }


            self._send_json_response(
                response,
                500
            )


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    HOST = "0.0.0.0"

    PORT = 8000


    server = HTTPServer(

        (
            HOST,
            PORT
        ),

        CustomRequestHandler

    )


    print(
        "========================================"
    )

    print(
        "PYTHON HTTP SERVER STARTED"
    )

    print(
        "========================================"
    )

    print(
        f"Server running on http://localhost:{PORT}"
    )

    print(
        "========================================"
    )


    try:

        server.serve_forever()


    except KeyboardInterrupt:

        print(
            "\nServer stopped"
        )


        server.server_close()