import http.server, socketserver

ROOT = "/tmp/claude-0/-home-claude/f96f6e27-f778-5af7-9888-3821977acd8e/scratchpad/vhostroot"

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        host = self.headers.get('Host','').split(':')[0]
        if host == 'blog.corp.local':
            body = open(f"{ROOT}/blog/index.html","rb").read()
        elif host == 'admin-panel.corp.local':
            body = open(f"{ROOT}/admin-panel/index.html","rb").read()
        else:
            body = open(f"{ROOT}/main/index.html","rb").read()
        self.send_response(200)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, fmt, *args):
        pass

with socketserver.TCPServer(("127.0.0.1", 8888), Handler) as httpd:
    httpd.serve_forever()
