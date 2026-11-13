# ==============================================================================
# MASTER PAPAN SKOR TIKTOK LIVE - STANDALONE DESKTOP APPLICATION
# Cyber HUD Edition - Powered by Microsoft Edge WebView2 & WebSocket Sync
# ==============================================================================
import sys
import os
import threading
import socket
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.request
import webview

def get_bundle_dir():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

def find_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 0))
    port = s.getsockname()[1]
    s.close()
    return port

def start_local_server(port, public_dir):
    class QuietHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=public_dir, **kwargs)
        def log_message(self, format, *args):
            pass

    try:
        server = HTTPServer(('127.0.0.1', port), QuietHandler)
        server.serve_forever()
    except Exception as e:
        print(f"[WARN] Local server error: {e}")

def is_online(url='https://papan-skor-tiktok.vercel.app/', timeout=3):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status == 200
    except Exception:
        return False

def main():
    bundle_dir = get_bundle_dir()
    public_dir = os.path.join(bundle_dir, 'public')
    if not os.path.exists(public_dir):
        public_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'public')

    local_port = find_free_port()
    t = threading.Thread(target=start_local_server, args=(local_port, public_dir), daemon=True)
    t.start()

    # Utamakan live vercel URL jika online agar pembaruan cloud otomatis aktif
    target_url = f'http://127.0.0.1:{local_port}/'
    if is_online():
        target_url = 'https://papan-skor-tiktok.vercel.app/'

    window = webview.create_window(
        title='Master Papan Skor TikTok LIVE - Cyber HUD Edition',
        url=target_url,
        width=1320,
        height=820,
        min_size=(960, 620),
        background_color='#070b14',
        text_select=True,
        confirm_close=False
    )
    webview.start(private_mode=False)

if __name__ == '__main__':
    main()
