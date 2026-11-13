# ==============================================================================
# MASTER PAPAN SKOR TIKTOK LIVE - STANDALONE DESKTOP APPLICATION
# Cyber HUD Edition - Powered by Microsoft Edge WebView2 & WebSocket Sync
# ==============================================================================
import sys
import os
import time
import socket
import threading
import tempfile
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Setup safe diagnostic logging
log_path = os.path.join(tempfile.gettempdir(), 'MasterPapanSkor.log')
try:
    log_file = open(log_path, 'a', encoding='utf-8', buffering=1)
    sys.stdout = log_file
    sys.stderr = log_file
except Exception:
    pass

print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Launching Master Papan Skor...")

def get_bundle_dir():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

# Configure PATH for WebView2 and Python.NET binaries in frozen package
bundle_dir = get_bundle_dir()
if getattr(sys, 'frozen', False):
    extra_paths = [
        bundle_dir,
        os.path.join(bundle_dir, 'webview', 'lib'),
        os.path.join(bundle_dir, 'webview', 'lib', 'runtimes', 'win-x64', 'native'),
        os.path.join(bundle_dir, 'webview', 'lib', 'runtimes', 'win-x86', 'native')
    ]
    for p in extra_paths:
        if os.path.exists(p) and p not in os.environ.get('PATH', ''):
            os.environ['PATH'] = p + ';' + os.environ.get('PATH', '')

def get_public_dir():
    b_dir = get_bundle_dir()
    candidates = [
        os.path.join(b_dir, 'public'),
        b_dir,
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'public'),
        r'D:\galatamaapp\papan-skor-tiktok\public'
    ]
    for c in candidates:
        if os.path.exists(os.path.join(c, 'index.html')):
            return c
    return candidates[0]

def find_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 0))
    port = s.getsockname()[1]
    s.close()
    return port

def start_local_server(port, public_dir):
    class CyberHUDHTTPHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=public_dir, **kwargs)
        def log_message(self, format, *args):
            pass

    CyberHUDHTTPHandler.extensions_map.update({
        '.js': 'application/javascript',
        '.mjs': 'application/javascript',
        '.json': 'application/json',
        '.css': 'text/css',
        '.html': 'text/html',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.svg': 'image/svg+xml',
        '.ico': 'image/x-icon',
        '.mp3': 'audio/mpeg',
        '.wav': 'audio/wav',
        '.ogg': 'audio/ogg',
        '.woff2': 'font/woff2',
        '.woff': 'font/woff',
        '.ttf': 'font/ttf'
    })

    try:
        server = HTTPServer(('127.0.0.1', port), CyberHUDHTTPHandler)
        print(f"[INFO] Server listening on http://127.0.0.1:{port}/ serving {public_dir}")
        server.serve_forever()
    except Exception as e:
        print(f"[WARN] Local server error: {e}")

def wait_for_server(port, timeout=2.5):
    start_t = time.time()
    while time.time() - start_t < timeout:
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=0.1):
                return True
        except (OSError, ConnectionRefusedError):
            time.sleep(0.05)
    return False

def main():
    public_dir = get_public_dir()
    print(f"[INFO] Public directory detected: {public_dir}")

    local_port = find_free_port()
    t = threading.Thread(target=start_local_server, args=(local_port, public_dir), daemon=True)
    t.start()

    is_ready = wait_for_server(local_port, timeout=2.5)
    if is_ready:
        target_url = f'http://127.0.0.1:{local_port}/'
        print(f"[INFO] Local server verified ready: {target_url}")
    else:
        # Fallback instan ke deployment cloud jika local server delay
        target_url = 'https://papan-skor-tiktok-pi.vercel.app/'
        print(f"[WARN] Local server timed out, falling back to Vercel: {target_url}")

    try:
        import webview
        print("[INFO] Initializing WebView2 window...")
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
        print("[INFO] WebView window closed normally.")
    except Exception as e:
        print(f"[FATAL] WebView error: {e}")
        import traceback
        traceback.print_exc()
        # Fallback buka di default browser jika engine webview bermasalah
        webbrowser.open(target_url)

if __name__ == '__main__':
    main()
