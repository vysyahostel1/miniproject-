# IFRH (Indian Financial Research Hub)

A Vite + React frontend with a Python Flask backend for research requests, auth, admin login, and Neon PostgreSQL persistence.

## Run locally

```bash
cd ifrh-react
npm install
cp .env.example .env.local
cd backend && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
python app.py
# in another terminal:
cd ifrh-react
npm run dev
```

Frontend: http://localhost:5173  
Backend: http://localhost:3001
