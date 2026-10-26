# FarmNova AI v2

FarmNova AI is a Flask agriculture assistant using Gemini and MongoDB Atlas.

## Database

This version is fully MongoDB-based. It uses PyMongo, not Flask-SQLAlchemy.

MongoDB database:
`farmnova`

Collections created/used by the application:
- `conversations`
- `messages`
- `users`
- `disease_history`
- `crop_recommendations`
- `weather_history`
- `reports`

## Setup

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Copy `.env.example` to `.env` and add your credentials:

```env
MONGO_URI=mongodb+srv://USERNAME:PASSWORD@CLUSTER.mongodb.net/?retryWrites=true&w=majority
MONGO_DB_NAME=farmnova
GEMINI_API_KEY=YOUR_KEY
GEMINI_MODEL=gemini-2.5-flash
```

Run:

```powershell
python app.py
```

Open `http://127.0.0.1:5000`.

## Important

Do not use `DATABASE_URL`, `SQLALCHEMY_DATABASE_URI`, or Flask-SQLAlchemy for this version.
Never commit `.env` or real API/database credentials to GitHub.
