import hashlib
import os
import random
import string
from datetime import datetime
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from db import get_conn, init_db, DB_URL

load_dotenv()
app = Flask(__name__)
init_db()


def ok(data=None):
  return jsonify({'ok': True, **(data or {})})

def err(message, code=400):
  return jsonify({'ok': False, 'error': message}), code

def sha(text):
  return hashlib.sha256(text.encode()).hexdigest()

def gen_req_id():
  return 'REQ-' + ''.join(random.choice(string.digits) for _ in range(8))

@app.post('/api/auth')
def auth():
  action = request.args.get('action')
  body = request.json or {}
  if not DB_URL:
    return err('NEON_DATABASE_URL missing', 500)
  with get_conn() as conn, conn.cursor() as cur:
    if action == 'signup':
      cur.execute('INSERT INTO users(first_name,last_name,email,phone,password_hash) VALUES (%s,%s,%s,%s,%s) ON CONFLICT (email) DO NOTHING RETURNING id',
                  (body.get('first_name'), body.get('last_name'), body.get('email'), body.get('phone'), sha(body.get('password', ''))))
      if cur.fetchone() is None:
        return err('Email already exists')
      return ok()
    if action == 'signin':
      cur.execute('SELECT id,first_name,last_name,email FROM users WHERE email=%s AND password_hash=%s AND status=%s',
                  (body.get('email'), sha(body.get('password', '')), 'active'))
      row = cur.fetchone()
      if not row:
        return err('Invalid credentials', 401)
      return ok({'user': {'id': row[0], 'first_name': row[1], 'last_name': row[2], 'email': row[3]}})
    if action == 'checkEmail':
      cur.execute('SELECT 1 FROM users WHERE email=%s', (body.get('email'),))
      return ok({'exists': cur.fetchone() is not None})
  return err('Unsupported action')

@app.post('/api/admin')
def admin():
  action = request.args.get('action')
  body = request.json or {}
  if action == 'login':
    user_ok = body.get('username') == os.getenv('ADMIN_USERNAME', 'admin')
    pass_ok = body.get('password') == os.getenv('ADMIN_PASSWORD', 'ifrh2026')
    return ok() if user_ok and pass_ok else err('Invalid credentials', 401)
  return ok()

@app.post('/api/requests')
def requests_api():
  action = request.args.get('action')
  body = request.json or {}
  if not DB_URL:
    return err('NEON_DATABASE_URL missing', 500)
  with get_conn() as conn, conn.cursor() as cur:
    if action == 'submit':
      req_id = gen_req_id()
      cur.execute('INSERT INTO research_requests(req_id,name,email,phone,type,priority,subject,message,status,date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                  (req_id, body.get('name'), body.get('email'), body.get('phone'), body.get('type'), body.get('priority'), body.get('subject'), body.get('message'), 'new', datetime.utcnow().date().isoformat()))
      return ok({'req_id': req_id})
    if action == 'list':
      cur.execute('SELECT req_id,name,email,type,priority,status,date FROM research_requests ORDER BY timestamp DESC LIMIT 200')
      return ok({'items': [dict(zip(['req_id','name','email','type','priority','status','date'], x)) for x in cur.fetchall()]})
  return err('Unsupported action')

@app.post('/api/reports')
def reports_api():
  return ok({'items': []})

@app.post('/api/settings')
def settings_api():
  return ok({'settings': {}})

@app.post('/api/sync')
def sync_api():
  action = request.args.get('action')
  body = request.json or {}
  if not DB_URL:
    return err('NEON_DATABASE_URL missing', 500)
  with get_conn() as conn, conn.cursor() as cur:
    if action == 'save':
      cur.execute("INSERT INTO site_data(key,value,updated_at) VALUES('site_state',%s::jsonb,NOW()) ON CONFLICT (key) DO UPDATE SET value=EXCLUDED.value, updated_at=NOW()", (str(body).replace("'", '"'),))
      return ok()
    if action == 'load':
      cur.execute("SELECT value FROM site_data WHERE key='site_state'")
      row = cur.fetchone()
      return ok({'data': row[0] if row else {}})
  return err('Unsupported action')

if __name__ == '__main__':
  app.run(port=3001, debug=True)
