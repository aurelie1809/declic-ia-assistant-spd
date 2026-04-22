"""
Déclic IA — Proxy sécurisé pour l'assistant SPD
La clé API Anthropic reste côté serveur, jamais exposée au navigateur.
"""

import os
import json
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler

API_KEY  = os.environ.get("ANTHROPIC_API_KEY", "")
API_URL  = "https://api.anthropic.com/v1/messages"
PORT     = int(os.environ.get("PORT", 8080))


class Handler(BaseHTTPRequestHandler):

    # ── Silencieux dans les logs ──
    def log_message(self, fmt, *args):
        pass

    # ── CORS pour les appels depuis le navigateur ──
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    # ── Sert les fichiers statiques (HTML, CSS, JS) ──
    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/" or path == "/index.html":
            path = "/index.html"
        filepath = os.path.join(os.path.dirname(__file__), path.lstrip("/"))

        if os.path.isfile(filepath):
            ext = filepath.rsplit(".", 1)[-1].lower()
            types = {"html": "text/html", "css": "text/css",
                     "js": "application/javascript", "png": "image/png"}
            ctype = types.get(ext, "application/octet-stream")
            with open(filepath, "rb") as f:
                data = f.read()
            self.send_response(200)
            self.send_header("Content-Type", ctype + "; charset=utf-8")
            self.send_header("Content-Length", len(data))
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")

    # ── Proxy vers l'API Anthropic ──
    def do_POST(self):
        if self.path != "/api/generate":
            self.send_response(404)
            self.end_headers()
            return

        if not API_KEY:
            self._json_error(500, "Clé API non configurée sur le serveur.")
            return

        length = int(self.headers.get("Content-Length", 0))
        body   = self.rfile.read(length)

        try:
            payload = json.loads(body)
        except Exception:
            self._json_error(400, "Corps JSON invalide.")
            return

        # Sécurité : on force le modèle et on retire tout ce qui ne doit pas partir
        safe_payload = {
            "model":    "claude-haiku-4-5-20251001",
            "max_tokens": 3000,
            "system":   payload.get("system", ""),
            "messages": payload.get("messages", []),
        }

        req_body = json.dumps(safe_payload).encode("utf-8")
        req = urllib.request.Request(
            API_URL,
            data    = req_body,
            method  = "POST",
            headers = {
                "Content-Type":      "application/json",
                "x-api-key":         API_KEY,
                "anthropic-version": "2023-06-01",
            }
        )

        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = resp.read()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._cors()
            self.end_headers()
            self.wfile.write(result)

        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            try:
                msg = json.loads(err_body).get("error", {}).get("message", err_body)
            except Exception:
                msg = err_body
            self._json_error(e.code, msg)

        except Exception as e:
            self._json_error(500, str(e))

    def _json_error(self, code, message):
        body = json.dumps({"error": message}).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self._cors()
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    print(f"Déclic IA — Serveur démarré sur http://0.0.0.0:{PORT}")
    if not API_KEY:
        print("⚠️  ATTENTION : variable ANTHROPIC_API_KEY non définie.")
    httpd = HTTPServer(("0.0.0.0", PORT), Handler)
    httpd.serve_forever()
