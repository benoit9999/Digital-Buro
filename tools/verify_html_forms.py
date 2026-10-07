"""Exercise real PHP + mail() against a localhost SMTP inbox, never external mail."""
import hashlib
import hmac
import http.cookiejar
import json
import os
import re
import socket
import socketserver
import subprocess
import tempfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from email import policy
from email.parser import Parser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHP = ROOT / '.deps/php/php.exe'
messages = []
results = []


class SMTP(socketserver.StreamRequestHandler):
    def handle(self):
        self.wfile.write(b'220 localhost test SMTP\r\n')
        envelope = []
        while True:
            line = self.rfile.readline()
            if not line:
                return
            command = line.decode('utf-8', errors='replace').strip()
            if command.upper() == 'DATA':
                self.wfile.write(b'354 Send message\r\n')
                body = []
                while True:
                    part = self.rfile.readline()
                    if part in (b'.\r\n', b''):
                        break
                    body.append(part)
                messages.append({'envelope':envelope[:], 'body':b''.join(body).decode('utf-8', errors='replace')})
                self.wfile.write(b'250 Accepted locally\r\n')
            elif command.upper() == 'QUIT':
                self.wfile.write(b'221 Bye\r\n')
                return
            else:
                envelope.append(command)
                self.wfile.write(b'250 OK\r\n')


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


smtp = socketserver.ThreadingTCPServer(('127.0.0.1', 0), SMTP)
threading.Thread(target=smtp.serve_forever, daemon=True).start()
smtp_stopped = False
with tempfile.TemporaryDirectory(prefix='db-html-form-test-', dir=ROOT / '.deps') as temporary:
    store = Path(temporary).resolve()
    assert store.is_relative_to((ROOT / '.deps').resolve())
    with socket.socket() as probe:
        probe.bind(('127.0.0.1', 0))
        port = probe.getsockname()[1]
    base = f'http://127.0.0.1:{port}'
    command = [str(PHP), '-n', '-d', 'SMTP=127.0.0.1', '-d', f'smtp_port={smtp.server_address[1]}',
               '-d', 'sendmail_from=site@digital-buro.be', '-d', f'session.save_path={store}',
               '-d', f'sys_temp_dir={store}', '-d', 'default_socket_timeout=2',
               '-S', f'127.0.0.1:{port}', '-t', str(ROOT / 'site-html')]
    process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    cookies = http.cookiejar.CookieJar()
    client = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookies), NoRedirect())

    def request(path, data=None, accept='application/json', method=None, extra=None):
        headers = {'Accept':accept, **(extra or {})}
        payload = urllib.parse.urlencode(data).encode() if data is not None else None
        req = urllib.request.Request(base + path, data=payload, headers=headers, method=method)
        try:
            with client.open(req, timeout=10) as response:
                return response.status, response.read().decode(), response.headers
        except urllib.error.HTTPError as response:
            return response.code, response.read().decode(), response.headers

    def check(label, data, status=422, **kwargs):
        count = len(messages)
        code, body, headers = request('/send_contact.php', data, **kwargs)
        assert code == status, (label, code, body)
        if status >= 400:
            assert len(messages) == count, label + ' sent mail despite rejection'
        results.append({'test':label, 'status':code})
        print(label + ': OK', flush=True)
        return body, headers

    def token(wait=True):
        code, body, headers = request('/send_contact.php?token=1')
        assert code == 200
        value = json.loads(body)
        assert re.fullmatch('[a-f0-9]{64}', value['token'])
        if wait:
            time.sleep(value['wait_ms'] / 1000 + 0.05)
        return value['token']

    def state_path():
        return next(store.glob('db_html_contact_v1_*.json'))

    def read_state():
        return json.loads(state_path().read_text())

    def write_state(state):
        state_path().write_text(json.dumps(state))

    def reset_limits():
        state = read_state()
        state['attempts'] = []
        write_state(state)

    def seed(count, age, ip='other-ip', phone='other-phone'):
        state = read_state()
        state['attempts'] = [{'t':int(time.time()) - age, 'ip':ip, 'phone':phone,
                              'fingerprint':'different-payload', 'sent':True} for _ in range(count)]
        write_state(state)

    def digest(value):
        return hmac.new(read_state()['secret'].encode(), value.encode(), hashlib.sha256).hexdigest()

    try:
        for _ in range(40):
            try:
                request('/contact.html')
                break
            except OSError:
                time.sleep(.1)
        valid = {'nom':'Élodie'+' D’Haene'*10, 'telephone':'02 534 47 02', 'email':'client@example.org',
                 'sujet':'reparation', 'appareil':'Imprimante', 'message':'Test local : <script>alert(1)</script> & caractères accentués.'}
        check('Direct POST without session', valid, 403)
        valid['form_token'] = token(wait=False)
        check('Server-side minimum filling time', valid, 429)
        time.sleep(2.1)
        for label, fields in [
            ('Name with digits', {'nom':'Jean123'}), ('Missing telephone', {'telephone':''}),
            ('Invalid telephone', {'telephone':'0000000000'}), ('Invalid email', {'email':'not-an-email'}),
            ('Header injection', {'email':'client@example.org\r\nBcc: attacker@example.org'}),
            ('Array instead of scalar', {'email[]':'attacker@example.org'}),
            ('Filled honeypot', {'site_web':'robot'}), ('Too many links', {'message':'https://a.test '*4}),
            ('Unknown subject', {'sujet':'inject'}), ('Message over 5000 characters', {'message':'a'*5001}),
            ('Device with header injection', {'appareil':'Printer\r\nBcc: x@example.org'}),
        ]:
            candidate = {**valid, **fields}
            if label == 'Array instead of scalar':
                candidate.pop('email')
            check(label, candidate)
        check('Oversized request', {**valid, 'message':'a'*25000}, 413)
        check('Foreign origin', valid, 403, extra={'Origin':'https://other.example'})
        check('Different origin port', valid, 403, extra={'Origin':'http://127.0.0.1:1'})
        check('Unsupported HTTP method', None, 405, method='PUT')
        check('Real PHP HTML mail accepted', {**valid, 'to':'attacker@example.org'}, 200)
        assert len(messages) == 1
        first = Parser(policy=policy.default).parsestr(messages[0]['body'])
        html = first.get_content()
        assert first.get_content_type() == 'text/html'
        assert str(first['Reply-To']) == 'client@example.org'
        assert '+3225344702' in html and '&lt;script&gt;' in html and '<script>' not in html
        assert 'Élodie' in str(first['Subject']) and 'Blackfriars' not in html
        assert str(first['Subject']).endswith(valid['nom'])
        encoded_words = re.findall(r'=\?UTF-8\?B\?[^?]+\?=', next(value for key, value in first.raw_items() if key.lower() == 'subject'))
        assert len(encoded_words) > 1 and all(len(word) <= 75 for word in encoded_words)
        (ROOT / 'artifacts/html-contact-email.html').write_text(html, encoding='utf-8')
        check('Consumed token replay', valid, 403)
        valid['form_token'] = token()
        state = read_state()
        state['attempts'][0]['ip'] = 'a-different-ip-bucket'
        write_state(state)
        check('Duplicate across IP buckets', valid, 409)
        reset_limits()
        seed(1, 0, ip=digest('127.0.0.1'))
        check('IP cooldown ignores forwarded IP headers', {**valid, 'message':'New request'}, 429,
              extra={'X-Forwarded-For':'203.0.113.1'})
        seed(5, 40, ip=digest('127.0.0.1'))
        check('Five attempts per IP per hour', {**valid, 'message':'New request'}, 429)
        seed(3, 40, phone=digest('+3225344702'))
        check('Repeated phone across IP buckets', {**valid, 'message':'New request'}, 429)
        seed(30, 40)
        check('Global hourly mailbox cap', {**valid, 'message':'New request'}, 429)
        seed(100, 7200)
        check('Global rolling daily mailbox cap', {**valid, 'message':'New request'}, 429)
        reset_limits()
        lock_code = '$f=fopen($argv[1],"c+");flock($f,LOCK_EX);echo "LOCKED\n";fflush(STDOUT);fgets(STDIN);flock($f,LOCK_UN);fclose($f);'
        locker = subprocess.Popen([str(PHP), '-r', lock_code, str(state_path())], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        try:
            assert locker.stdout.readline().strip() == 'LOCKED'
            check('Concurrent requests cannot bypass the shared lock', valid, 429)
        finally:
            locker.communicate('\n', timeout=5)
        previous = read_state()
        state_path().write_text('{invalid JSON')
        check('Broken anti-spam storage fails closed', valid, 503)
        write_state(previous)
        check('Callback without email', {**valid, 'sujet':'rappel', 'email':'', 'message':''}, 200)
        assert len(messages) == 2
        assert Parser(policy=policy.default).parsestr(messages[1]['body'])['Reply-To'] is None
        valid['form_token'] = token()
        cookie = next(c for c in cookies if c.name == 'db_html_form')
        session = store / ('sess_' + cookie.value)
        session.write_text(re.sub(r'form_time\|i:\d+;', 'form_time|i:'+str(int(time.time())-4000)+';', session.read_text()))
        check('Expired form token', valid, 403)
        valid['form_token'] = token()
        reset_limits()
        check('Native PHP success redirects to merci.html', {**valid, 'message':'Native POST'}, 303, accept='text/html')
        reset_limits()
        environment = {**os.environ, 'DB_TEST_BASE':base, 'DB_TEST_STORE':str(store)}
        subprocess.run(['node', str(ROOT / 'tools/check_html_forms_browser.cjs')], env=environment, check=True)
        assert len(messages) == 9, len(messages)
        results.append({'test':'Browser contact, four callbacks and native fallback', 'status':200})
        reset_limits()
        with socket.socket() as probe:
            probe.bind(('127.0.0.1', 0))
            mounted_port = probe.getsockname()[1]
        mounted_origin = f'http://127.0.0.1:{mounted_port}'
        mounted_command = command[:]
        mounted_command[mounted_command.index('-S') + 1] = f'127.0.0.1:{mounted_port}'
        mounted_command[-1] = str(ROOT)
        mounted_process = subprocess.Popen(mounted_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        mounted_client = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()), NoRedirect())
        try:
            for _ in range(40):
                try:
                    with mounted_client.open(mounted_origin+'/site-html/send_contact.php?token=1') as response:
                        challenge = json.loads(response.read())
                        assert 'path=/site-html/' in response.headers['Set-Cookie']
                    break
                except OSError:
                    time.sleep(.1)
            time.sleep(challenge['wait_ms']/1000 + .05)
            payload = urllib.parse.urlencode({**valid, 'form_token':challenge['token'], 'message':'Subdirectory installation'}).encode()
            req = urllib.request.Request(mounted_origin+'/site-html/send_contact.php', data=payload,
                headers={'Accept':'application/json', 'Origin':mounted_origin})
            with mounted_client.open(req) as response:
                assert response.status == 200 and json.loads(response.read())['ok']
            assert len(messages) == 10
            results.append({'test':'Subdirectory endpoint, scoped cookie and matching Origin', 'status':200})
            print('PHP form works under /site-html/ with a scoped session cookie: OK', flush=True)
        finally:
            mounted_process.terminate()
            mounted_process.wait(timeout=5)
        smtp.shutdown()
        smtp.server_close()
        smtp_stopped = True
        valid['form_token'] = token()
        reset_limits()
        check('Mail failure never returns success', {**valid, 'message':'SMTP down'}, 503)
        subprocess.run(['node', str(ROOT / 'tools/check_html_forms_browser.cjs')], env={**environment, 'DB_TEST_PHASE':'failure'}, check=True)
        assert len(messages) == 10
        for mail in messages:
            assert any(line.lower() == 'rcpt to:<digital-buro@skynet.be>' for line in mail['envelope']), mail['envelope']
        report = {'ok':True, 'checked_on':'2026-10-07', 'php':subprocess.check_output([str(PHP), '-v']).decode().splitlines()[0],
                  'transport':'Real PHP mail() to isolated localhost SMTP; no external mail',
                  'recipient':'digital-buro@skynet.be', 'captured_messages':len(messages), 'tests':results,
                  'limits':{'per_ip_hour':5, 'same_phone_hour':3, 'global_hour':30, 'global_day':100, 'duplicates_seconds':600}}
        (ROOT / 'artifacts/html-form-tests.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        print(json.dumps({'ok':True, 'tests':len(results), 'local_messages':len(messages)}, ensure_ascii=False), flush=True)
    finally:
        process.terminate()
        process.wait(timeout=5)
        if not smtp_stopped:
            smtp.shutdown()
            smtp.server_close()
