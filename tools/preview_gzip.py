"""Static audit preview with gzip/cache like .htaccess. Does not execute PHP."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from functools import partial
import gzip
import io

ROOT = Path(__file__).resolve().parents[1] / 'public'

class Preview(SimpleHTTPRequestHandler):
    def send_head(self):
        path = Path(self.translate_path(self.path))
        if path.suffix == '.php':
            self.send_error(503, 'PHP runtime required')
            return None
        if path.is_dir():
            if not self.path.split('?')[0].endswith('/'):
                return super().send_head()
            path = path / 'index.html'
        if not path.is_file() or path.name.startswith('.'):
            self.send_error(404)
            return None
        body = path.read_bytes()
        mime = self.guess_type(str(path))
        compressed = path.suffix in ('.html', '.css', '.js', '.svg', '.xml', '.webmanifest') and 'gzip' in self.headers.get('Accept-Encoding', '')
        if compressed:
            body = gzip.compress(body)
        self.send_response(200)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-cache' if path.suffix == '.html' else 'public, max-age=2592000')
        if compressed:
            self.send_header('Content-Encoding', 'gzip')
            self.send_header('Vary', 'Accept-Encoding')
        self.end_headers()
        return io.BytesIO(body)

if __name__ == '__main__':
    print('Audit preview http://127.0.0.1:8081 — static + gzip, no PHP', flush=True)
    ThreadingHTTPServer(('127.0.0.1', 8081), partial(Preview, directory=str(ROOT))).serve_forever()
