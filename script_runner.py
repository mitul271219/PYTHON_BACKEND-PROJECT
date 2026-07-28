# import os
# import json

# from http.server import (
#     BaseHTTPRequestHandler,
#     HTTPServer
# )

# from google_sheets import (
#     patient_sheet,
#     bpm_sheet,
#     oxy_sheet
# )

# from scheduler import check_devices
# from dotenv import load_dotenv

# load_dotenv()


# # ============================================================
# # HTTP REQUEST HANDLER
# # ============================================================

# class CustomRequestHandler(
#     BaseHTTPRequestHandler
# ):

#     protocol_version = "HTTP/1.1"


#     # ========================================================
#     # CORS HEADERS
#     # ========================================================

#     def _send_cors_headers(self):

#         self.send_header(
#             "Access-Control-Allow-Origin",
#             "*"
#         )

#         self.send_header(
#             "Access-Control-Allow-Methods",
#             "POST, OPTIONS, GET"
#         )

#         self.send_header(
#             "Access-Control-Allow-Headers",
#             "X-API-KEY, Content-Type"
#         )


#     # ========================================================
#     # SEND JSON RESPONSE
#     # ========================================================

#     def _send_json_response(
#         self,
#         data,
#         status_code=200
#     ):

#         response_body = json.dumps(
#             data
#         ).encode(
#             "utf-8"
#         )


#         self.send_response(
#             status_code
#         )


#         self._send_cors_headers()


#         self.send_header(
#             "Content-Type",
#             "application/json"
#         )


#         self.send_header(
#             "Content-Length",
#             str(
#                 len(response_body)
#             )
#         )


#         self.end_headers()


#         self.wfile.write(
#             response_body
#         )


#     # ========================================================
#     # OPTIONS REQUEST
#     # ========================================================

#     def do_OPTIONS(self):

#         self.send_response(
#             200
#         )


#         self._send_cors_headers()


#         self.send_header(
#             "Content-Length",
#             "0"
#         )


#         self.end_headers()


#     # ========================================================
#     # GET REQUEST
#     # ========================================================

#     def do_GET(self):

#         try:

#             # ==================================================
#             # HOME
#             # ==================================================

#             if self.path == "/":

#                 response = {

#                     "success": True,

#                     "message":
#                     "Python Backend Running Successfully"

#                 }


#                 self._send_json_response(
#                     response
#                 )


#             # ==================================================
#             # PATIENTS
#             # ==================================================
#             elif self.path == "/patients":

#                 data = patient_sheet.get_all_records()


#                 response = {

#                     "success": True,

#                     "message":
#                     "Patients fetched successfully.",

#                     "count":
#                     len(data),

#                     "data":
#                     data

#                 }


#                 self._send_json_response(
#                     response
#                 )


#             # ==================================================
#             # BPM
#             # ==================================================

#             elif self.path == "/bpm":

#                 data = bpm_sheet.get_all_records()


#                 response = {

#                     "success": True,

#                     "message":
#                     "BPM data fetched successfully.",

#                     "count":
#                     len(data),

#                     "data":
#                     data

#                 }


#                 self._send_json_response(
#                     response
#                 )


#             # ==================================================
#             # OXY
#             # ==================================================

#             elif self.path == "/oxy":

#                 data = oxy_sheet.get_all_records()


#                 response = {

#                     "success": True,

#                     "message":
#                     "OXY data fetched successfully.",

#                     "count":
#                     len(data),

#                     "data":
#                     data

#                 }


#                 self._send_json_response(
#                     response
#                 )


#             # ==================================================
#             # UNKNOWN GET ROUTE
#             # ==================================================

#             else:

#                 response = {

#                     "success": False,

#                     "message":
#                     "GET endpoint not found"

#                 }


#                 self._send_json_response(
#                     response,
#                     404
#                 )


#         except Exception as e:

#             print(
#                 "GET ERROR:",
#                 e
#             )


#             response = {

#                 "success": False,

#                 "message":
#                 str(e)

#             }


#             self._send_json_response(
#                 response,
#                 500
#             )


#     # ========================================================
#     # POST REQUEST
#     # ========================================================

#     def do_POST(self):

#         try:

#             # ==================================================
#             # SECURITY CHECK
#             # ==================================================

#             expected_secret = os.environ.get(
#                 "BACKEND_SECRET"
#             )


#             client_secret = self.headers.get(
#                 "X-API-KEY"
#             )


#             if (
#                 not expected_secret
#                 or client_secret != expected_secret
#             ):

#                 print(
#                     "Unauthorized: Invalid API Key"
#                 )


#                 response = {

#                     "success": False,

#                     "message":
#                     "Unauthorized. Invalid API Key."

#                 }


#                 self._send_json_response(
#                     response,
#                     401
#                 )


#                 return


#             # ==================================================
#             # CHECK DEVICE ENDPOINT
#             # ==================================================

#             if self.path == "/check-devices":

#                 print(
#                     "Device check request received"
#                 )


#                 result = check_devices()


#                 if result.get(
#                     "success"
#                 ):

#                     self._send_json_response(
#                         result,
#                         200
#                     )

#                 else:

#                     self._send_json_response(
#                         result,
#                         500
#                     )


#                 return


#             # ==================================================
#             # UNKNOWN POST ROUTE
#             # ==================================================

#             response = {

#                 "success": False,

#                 "message":
#                 "POST endpoint not found"

#             }


#             self._send_json_response(
#                 response,
#                 404
#             )


#         except Exception as e:

#             print(
#                 "POST ERROR:",
#                 e
#             )


#             response = {

#                 "success": False,

#                 "message":
#                 str(e)

#             }


#             self._send_json_response(
#                 response,
#                 500
#             )


# # ============================================================
# # START SERVER
# # ============================================================

# if __name__ == "__main__":

#     HOST = "0.0.0.0"

#     PORT = 8000


#     server = HTTPServer(

#         (
#             HOST,
#             PORT
#         ),

#         CustomRequestHandler

#     )


#     print(
#         "========================================"
#     )

#     print(
#         "PYTHON HTTP SERVER STARTED"
#     )

#     print(
#         "========================================"
#     )

#     print(
#         f"Server running on http://localhost:{PORT}"
#     )

#     print(
#         "========================================"
#     )


#     try:

#         server.serve_forever()


#     except KeyboardInterrupt:

#         print(
#             "\nServer stopped"
#         )


#         server.server_close()















# import os
# import importlib
# import json
# from http.server import BaseHTTPRequestHandler, HTTPServer

# from scheduler import check_devices


# class CustomRequestHandler(BaseHTTPRequestHandler):

#     protocol_version = 'HTTP/1.1'

#     def _send_cors_headers(self):
#         self.send_header(
#             'Access-Control-Allow-Origin',
#             '*'
#         )
#         self.send_header(
#             'Access-Control-Allow-Methods',
#             'POST, OPTIONS, GET'
#         )
#         self.send_header(
#             'Access-Control-Allow-Headers',
#             'X-API-KEY, Content-Type'
#         )


#     def do_OPTIONS(self):

#         self.send_response(200)
#         self._send_cors_headers()
#         self.send_header(
#             'Content-Length',
#             '0'
#         )
#         self.end_headers()


#     def do_GET(self):

#         print("GET request received")

#         response = {
#             "success": True,
#             "message": "Server running"
#         }

#         data = json.dumps(response).encode()

#         self.send_response(200)
#         self._send_cors_headers()
#         self.send_header(
#             'Content-Type',
#             'application/json'
#         )
#         self.send_header(
#             'Content-Length',
#             str(len(data))
#         )
#         self.end_headers()

#         self.wfile.write(data)



#     def do_POST(self):

#         expected_secret = os.environ.get(
#             'BACKEND_SECRET'
#         )

#         client_secret = self.headers.get(
#             'X-API-KEY'
#         )


#         if not expected_secret or client_secret != expected_secret:

#             msg = "Unauthorized"

#             self.send_response(401)
#             self._send_cors_headers()

#             self.send_header(
#                 'Content-Type',
#                 'text/plain'
#             )

#             self.send_header(
#                 'Content-Length',
#                 str(len(msg))
#             )

#             self.end_headers()

#             self.wfile.write(
#                 msg.encode()
#             )

#             return



#         try:

#             content_length = int(
#                 self.headers['Content-Length']
#             )

#             body = self.rfile.read(
#                 content_length
#             )


#             json_data = json.loads(
#                 body.decode('utf-8')
#             )


#             result = run_script(
#                 json_data
#             )


#             response = {

#                 "success":
#                     True
#                     if isinstance(result, dict)
#                     and result.get("success") == True
#                     else False,

#                 "content":
#                     result

#             }


#             response_body = json.dumps(
#                 response
#             ).encode()



#             self.send_response(200)

#             self._send_cors_headers()

#             self.send_header(
#                 'Content-Type',
#                 'application/json'
#             )

#             self.send_header(
#                 'Content-Length',
#                 str(len(response_body))
#             )

#             self.end_headers()


#             self.wfile.write(
#                 response_body
#             )



#         except Exception as e:


#             error = {
#                 "success": False,
#                 "message": str(e)
#             }


#             data = json.dumps(
#                 error
#             ).encode()


#             self.send_response(500)

#             self._send_cors_headers()

#             self.send_header(
#                 'Content-Type',
#                 'application/json'
#             )

#             self.send_header(
#                 'Content-Length',
#                 str(len(data))
#             )

#             self.end_headers()


#             self.wfile.write(
#                 data
#             )





# def run_script(json_data):

#     try:

#         print(
#             "JSON DATA:",
#             json_data
#         )


#         script_module = importlib.import_module(
#             json_data['script_name']
#         )


#         if (
#             'argv' in json_data
#             and len(json_data['argv']) > 0
#         ):

#             result = script_module.main(
#                 json_data['argv']
#             )

#         else:

#             result = script_module.main()



#         return result if result else {

#             "success": True,
#             "message": "Script executed"

#         }



#     except Exception as e:


#         return {

#             "success": False,
#             "message": str(e)

#         }





# # ==========================================================
# # START SCRIPT RUNNER
# # ==========================================================

# if __name__ == "__main__":


#     print(
#         "\n================================="
#     )

#     print(
#         "RUNNING DEVICE CHECK"
#     )

#     print(
#         "================================="
#     )


#     # CALL scheduler.py FUNCTION

#     device_result = check_devices()



#     if device_result.get("success"):


#         print(
#             "\nDEVICE CHECK SUCCESS"
#         )

#         print(
#             device_result.get("message")
#         )


#         print(
#             "\nSTARTING SERVER ON PORT 8000..."
#         )


#         HTTPServer(
#             ('0.0.0.0', 8000),
#             CustomRequestHandler
#         ).serve_forever()



#     else:


#         print(
#             "\nDEVICE CHECK FAILED"
#         )

#         print(
#             device_result.get("message")
#         )

#         print(
#             "SERVER NOT STARTED"
#         )












# from http.server import BaseHTTPRequestHandler, HTTPServer

# from scheduler import check_devices


# # ============================================================
# # HTTP REQUEST HANDLER
# # ============================================================

# class CustomRequestHandler(BaseHTTPRequestHandler):

#     protocol_version = "HTTP/1.1"

#     def do_GET(self):

#         # Simple response for browser GET request
#         response = b"Python Backend Running Successfully"

#         self.send_response(200)

#         self.send_header(
#             "Content-Type",
#             "text/plain"
#         )

#         self.send_header(
#             "Content-Length",
#             str(len(response))
#         )

#         self.end_headers()

#         self.wfile.write(response)


# # ============================================================
# # START SERVER
# # ============================================================

# if __name__ == "__main__":

#     print("========================================")
#     print("STARTING PYTHON BACKEND")
#     print("========================================")

#     # --------------------------------------------------------
#     # CHECK DEVICES AUTOMATICALLY
#     # --------------------------------------------------------

#     print("Calling check_devices()...")

#     result = check_devices()

#     print("check_devices() result:")
#     print(result)

#     print("========================================")
#     print("STARTING LOCALHOST SERVER")
#     print("http://localhost:8000")
#     print("========================================")

#     # --------------------------------------------------------
#     # START LOCALHOST SERVER
#     # --------------------------------------------------------

#     server = HTTPServer(
#         ("localhost", 8000),
#         CustomRequestHandler
#     )

#     server.serve_forever()








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