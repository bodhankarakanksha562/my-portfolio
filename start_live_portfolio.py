import http.server
import socketserver
import threading
import time
from pyngrok import ngrok

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

def start_server():
    try:
        # Use TCPServer and set allow_reuse_address to avoid "Address already in use" errors if restarted
        class ReusableTCPServer(socketserver.TCPServer):
            allow_reuse_address = True
            
        with ReusableTCPServer(("", PORT), Handler) as httpd:
            print(f"Local Server running on port {PORT}")
            httpd.serve_forever()
    except Exception as e:
        print(f"Failed to start server: {e}")

server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

# Give the server a moment to spin up
time.sleep(1)

print("Authenticating ngrok...")
ngrok.set_auth_token("3BIu06HLhQ9lwzI2E5PNr4lmtva_JDxwKdyNRKUnknc9ULgv")

print("Starting ngrok tunnel...")
# Create a tunnel to the local port
public_url = ngrok.connect(PORT)

print("\n" + "="*60)
print(f"YOUR PORTFOLIO IS LIVE AT: {public_url}")
print("="*60 + "\n")
print("Press Ctrl+C to stop the server and close the tunnel.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nShutting down...")
    ngrok.kill()
