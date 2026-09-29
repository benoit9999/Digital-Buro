"""Real PHP HTTP + mail() tests, isolated local SMTP inbox; no external mail."""
from pathlib import Path
import http.cookiejar, json, os, re, socket, socketserver, subprocess, tempfile, threading, time
import urllib.request, urllib.parse, urllib.error

ROOT = Path(__file__).resolve().parents[1]
PHP = ROOT / '.deps/php/php.exe'
messages = []
class SMTP(socketserver.StreamRequestHandler):
    def handle(self):
        self.wfile.write(b'220 localhost test SMTP\r\n')
        envelope=[]
        while True:
            line=self.rfile.readline()
            if not line:return
            cmd=line.decode('utf-8',errors='replace').strip()
            if cmd.upper()=='DATA':
                self.wfile.write(b'354 Send message\r\n');body=[]
                while True:
                    part=self.rfile.readline()
                    if part in (b'.\r\n',b''):break
                    body.append(part)
                messages.append({'envelope':envelope[:],'body':b''.join(body).decode('utf-8',errors='replace')})
                self.wfile.write(b'250 Accepted locally\r\n')
            elif cmd.upper()=='QUIT':self.wfile.write(b'221 Bye\r\n');return
            else:
                envelope.append(cmd);self.wfile.write(b'250 OK\r\n')
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):return None
smtp=socketserver.ThreadingTCPServer(('127.0.0.1',0),SMTP)
threading.Thread(target=smtp.serve_forever,daemon=True).start()
results=[]
with tempfile.TemporaryDirectory(prefix='db-contact-test-',dir=ROOT/'.deps') as tmp:
    with socket.socket() as probe:probe.bind(('127.0.0.1',0));port=probe.getsockname()[1]
    base=f'http://127.0.0.1:{port}'
    cmd=[str(PHP),'-n','-d','SMTP=127.0.0.1','-d',f'smtp_port={smtp.server_address[1]}',
         '-d','sendmail_from=site@digital-buro.be','-d',f'session.save_path={tmp}',
         '-d',f'sys_temp_dir={tmp}','-d','default_socket_timeout=2','-S',f'127.0.0.1:{port}','-t',str(ROOT/'public')]
    process=subprocess.Popen(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    client=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()),NoRedirect())
    def request(path,data=None,accept='application/json',origin=None):
        headers={'Accept':accept}
        if origin:headers['Origin']=origin
        req=urllib.request.Request(base+path,data=urllib.parse.urlencode(data).encode() if data is not None else None,headers=headers)
        try:
            with client.open(req,timeout=8) as res:return res.status,res.read().decode()
        except urllib.error.HTTPError as res:return res.code,res.read().decode()
    def check(label,data,status=422,**kwargs):
        code,body=request('/api/contact.php',data,**kwargs)
        assert code==status,(label,code,body)
        results.append({'test':label,'status':code})
        return body
    def token():
        code,body=request('/api/contact.php?token=1');assert code==200
        time.sleep(2.1)
        return json.loads(body)['token']
    def reset_limit():
        for file in Path(tmp).glob('dbcontact_v2_*'):file.write_text('{}')
    try:
        for i in range(40):
            try:request('/contact/');break
            except OSError:time.sleep(.1)
        valid={'nom':'Élodie D’Haene','telephone':'02 534 47 02','email':'client@example.org','sujet':'reparation','message':'Test local sans envoi externe.'}
        check('Direct POST without session rejected',valid,403)
        raw=json.loads(request('/api/contact.php?token=1')[1])['token']
        valid['form_token']=raw
        check('Server-side minimum time',valid,429)
        time.sleep(2.1)
        for label,fields in [
            ('Name containing digits',{'nom':'Jean123'}),('Name containing markup',{'nom':'<script>Jean</script>'}),
            ('Missing phone',{'telephone':''}),('Phone containing letters',{'telephone':'abcdefghi'}),
            ('Repeated fake number',{'telephone':'0000000000'}),('Too short phone',{'telephone':'02534'}),
            ('Invalid email',{'email':'not-an-email'}),('Header injection',{'email':'client@example.org\r\nBcc: spam@example.org'}),
            ('Honeypot',{'site_web':'bot'}),('Spam links',{'message':'https://a.test '*4}),('Unknown subject',{'sujet':'inject'})]:
            check(label,{**valid,**fields})
        check('Foreign origin',valid,403,origin='https://other.example')
        check('Contact accepted by real PHP mail()',valid,200)
        assert len(messages)==1
        mail=messages[0];assert any('digital-buro@skynet.be' in x.lower() for x in mail['envelope'])
        assert 'Reply-To: client@example.org' in mail['body'] and '+3225344702' in mail['body']
        check('Used token cannot be replayed',valid,403)
        valid['form_token']=token();check('IP cooldown',valid,429)
        reset_limit()
        check('Callback without email', {**valid,'sujet':'rappel','telephone':'+32 (0)476 25 38 49','email':''},200)
        assert len(messages)==2 and 'Reply-To:' not in messages[1]['body']
        valid['form_token']=token()
        for file in Path(tmp).glob('dbcontact_v2_*'):file.write_text(json.dumps({'attempt':0,'sent':[int(time.time())-40]*5}))
        check('Hourly volume limit',valid,429)
        reset_limit()
        code,html=request('/api/contact.php?form=1',accept='text/html');assert code==200
        fallback=re.search('name="form_token" value="([a-f0-9]+)"',html).group(1)
        check('No-JavaScript form submits through PHP',{**valid,'form_token':fallback},303,accept='text/html')
        assert len(messages)==3
        reset_limit()
        subprocess.run(['node',str(ROOT/'tools/check_contact_browser.cjs')],env={**os.environ,'DB_TEST_BASE':base},check=True)
        assert len(messages)==4
        results.append({'test':'Browser JavaScript through real PHP mail transport','status':200})
        valid['form_token']=token();reset_limit();smtp.shutdown();smtp.server_close()
        check('Mail transport failure never returns success',valid,503)
        report={'ok':True,'php':subprocess.check_output([str(PHP),'-v']).decode().splitlines()[0],
                'transport':'real PHP mail() to isolated localhost SMTP sink, no external delivery',
                'recipient':'digital-buro@skynet.be','captured_messages':len(messages),'tests':results}
        (ROOT/'artifacts/contact-tests.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
        print(json.dumps(report,ensure_ascii=False,indent=2))
    finally:
        process.terminate();process.wait(timeout=5)
        smtp.shutdown();smtp.server_close()
