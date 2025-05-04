# Math Battle Backend

FastAPI + MongoDB backend for Math Battle game.

## Setup

```bash
git clone <repo>
cd mathbattle-backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Edit **`.env`** to configure `MONGO_URL` and `JWT_SECRET_KEY`.
