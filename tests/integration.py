"""End-to-end API checks against an isolated temporary H2 database. Python 3 stdlib only."""
import concurrent.futures, http.cookiejar, json, os, pathlib, socket, subprocess, tempfile, time, unittest, urllib.request, urllib.parse, urllib.error
ROOT=pathlib.Path(__file__).resolve().parents[1]
class Client:
 def __init__(self,base):
  self.base=base;self.csrf=None;self.opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
 def call(self,path,data=None,csrf=True,origin=None):
  headers={}
  if data is not None:
   headers['Content-Type']='application/x-www-form-urlencoded'
   if csrf and self.csrf:headers['X-CSRF-Token']=self.csrf
  if origin:headers['Origin']=origin
  req=urllib.request.Request(self.base+'/api/'+path,None if data is None else urllib.parse.urlencode(data).encode(),headers)
  try:
   with self.opener.open(req,timeout=15) as r:return r.status,json.load(r)
  except urllib.error.HTTPError as e:return e.code,json.load(e)
 def me(self):
  code,body=self.call('me');self.csrf=body['csrf'];return body['user']
class Flow(unittest.TestCase):
 def test_complete_flow(self):
  with tempfile.TemporaryDirectory() as d:
   with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
   base=f'http://127.0.0.1:{port}'
   env=dict(os.environ,DATA_DIR=d,PORT=str(port),ADMIN_EMAIL='admin@example.edu',ADMIN_PASSWORD='Admin-test-478!')
   def start():
    proc=subprocess.Popen(['java','-cp',os.pathsep.join(['campusloop.jar','lib/*']),'campusloop.App'],cwd=ROOT,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    for _ in range(100):
     if proc.poll() is not None:raise RuntimeError(proc.stderr.read().decode())
     try:
      if Client(base).call('events')[0]==200:return proc
     except OSError:pass
     time.sleep(.1)
    proc.terminate();raise RuntimeError('Server did not start')
   def stop(proc):proc.terminate();proc.wait(timeout=10);proc.stderr.close()
   proc=start()
   try:
    anon=Client(base);self.assertEqual(anon.call('admin/participants?eventId=1')[0],401)
    with urllib.request.urlopen(base) as r:
     self.assertEqual(r.status,200);self.assertIn("frame-ancestors 'none'",r.headers['Content-Security-Policy'])
     html=r.read().decode();self.assertIn("Sheikh Sameer Ali",html);self.assertIn('/logo.png',html)
    with urllib.request.urlopen(base+'/logo.png') as r:
     self.assertEqual(r.headers['Content-Type'],'image/png');self.assertEqual(r.read(),(ROOT/'web/logo.png').read_bytes())
    self.assertEqual(anon.call('signup',dict(name='Invalid',email='bad',studentId='B1',department='CS',password='short'))[0],400)
    a,b,admin=Client(base),Client(base),Client(base)
    for client,name,sid in [(a,'Asha','CS001'),(b,'Rahul','CS002')]:
     self.assertEqual(client.call('signup',dict(name=name,email=name.lower()+'@example.edu',studentId=sid,department='Computer Science',password='Student-pass-123'))[0],201)
     self.assertEqual(client.me()['role'],'STUDENT')
    self.assertEqual(anon.call('signup',dict(name='Duplicate',email='asha@example.edu',studentId='CS099',department='CS',password='Student-pass-123'))[0],409)
    self.assertEqual(anon.call('signup',dict(name='Duplicate',email='other@example.edu',studentId='CS001',department='CS',password='Student-pass-123'))[0],409)
    self.assertEqual(a.call('admin/save-event',{})[0],403)
    self.assertEqual(admin.call('login',dict(email='admin@example.edu',password='wrong'))[0],401)
    self.assertEqual(admin.call('login',dict(email='admin@example.edu',password='Admin-test-478!'))[0],200);self.assertEqual(admin.me()['role'],'ADMIN')
    def create(name,capacity):
     from datetime import datetime,timedelta
     fields=dict(name=name,category='Technical',description='Integration test description.',venue='Seminar Hall',capacity=capacity,startsAt=(datetime.now()+timedelta(days=4)).isoformat(timespec='minutes'))
     self.assertEqual(admin.call('admin/save-event',fields)[0],200)
     event=next(e for e in admin.call('events')[1]['events'] if e['name']==name)
     return event['id'],fields
    event,fields=create('Last seat test',1)
    self.assertEqual(a.call('register',dict(eventId=event),csrf=False)[0],403)
    self.assertEqual(a.call('register',dict(eventId=event),origin='https://evil.example')[0],403)
    with concurrent.futures.ThreadPoolExecutor() as pool:
     results=list(pool.map(lambda c:c.call('register',dict(eventId=event)),[a,b]))
    self.assertEqual(sorted(r[0] for r in results),[200,409])
    winner=a if results[0][0]==200 else b;loser=b if winner is a else a
    self.assertEqual(winner.call('register',dict(eventId=event))[0],409)
    self.assertEqual(loser.call('unregister',dict(eventId=event))[0],404)
    self.assertEqual(len(admin.call('admin/participants?eventId='+str(event))[1]['participants']),1)
    self.assertEqual(winner.call('unregister',dict(eventId=event))[0],200)
    self.assertEqual(loser.call('register',dict(eventId=event))[0],200)
    event2,fields2=create('Capacity and attendance',2)
    self.assertEqual(a.call('register',dict(eventId=event2))[0],200);self.assertEqual(b.call('register',dict(eventId=event2))[0],200)
    self.assertEqual(admin.call('admin/save-event',dict(fields2,id=event2,capacity=1))[0],409)
    self.assertEqual(admin.call('admin/delete-event',dict(eventId=event2))[0],409)
    ps=admin.call('admin/participants?eventId='+str(event2))[1]['participants'];reg=ps[0]
    self.assertEqual(admin.call('admin/attendance',dict(registrationId=reg['id'],attended='true'))[0],200)
    self.assertEqual(admin.call('admin/participants?eventId='+str(event2))[1]['participants'][0]['attended'],True)
    self.assertEqual(admin.call('admin/cancel-event',dict(eventId=event2))[0],200)
    self.assertEqual(a.call('unregister',dict(eventId=event2))[0],409)
    self.assertEqual(admin.call('admin/attendance',dict(registrationId=reg['id'],attended='false'))[0],409)
    self.assertEqual(admin.call('admin/save-event',dict(fields2,id=event2))[0],409)
    self.assertTrue(any(r['status']=='CANCELLED' for r in a.call('registrations')[1]['registrations']))
    tmp,_=create('Delete empty test',5);self.assertEqual(admin.call('admin/delete-event',dict(eventId=tmp))[0],200)
    # User input remains data, not SQL, and output is JSON escaped.
    injection,inj=create("SQL ' OR 1=1 -- <script>",5);self.assertIsInstance(injection,int)
    self.assertEqual(admin.call('admin/save-event',dict(inj,id=injection,startsAt='2000-01-01T00:00'))[0],400)
    self.assertEqual(admin.call('admin/save-event',dict(inj,id=injection,capacity=0))[0],400)
    self.assertEqual(a.call('logout',{})[0],200);self.assertIsNone(a.me())
    # Restart persistence, account persistence, and invalidation of old sessions.
    before=len(admin.call('events')[1]['events']);stop(proc);proc=start()
    self.assertIsNone(admin.me());self.assertEqual(admin.call('login',dict(email='admin@example.edu',password='Admin-test-478!'))[0],200);admin.me()
    self.assertEqual(len(admin.call('events')[1]['events']),before)
    self.assertEqual(len(admin.call('admin/participants?eventId='+str(event2))[1]['participants']),2)
    self.assertEqual(a.call('login',dict(email='asha@example.edu',password='Student-pass-123'))[0],200);a.me()
    self.assertTrue(any(r['status']=='CANCELLED' for r in a.call('registrations')[1]['registrations']))
    # No password hashes or other users' contact details in event output.
    self.assertNotIn('password_hash',json.dumps(a.call('events')[1]));self.assertNotIn('password_hash',json.dumps(a.call('me')[1]))
   finally:stop(proc)
if __name__=='__main__':unittest.main(verbosity=2)
