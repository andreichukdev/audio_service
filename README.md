# Analyze audio service

## Stack

- Python;
- poetry;
- FastAPI;
- PostgreSQL;
- Docker;

## Steps for setup

### 1. Clone the repo

### 2. Install

```bash
cp .env.example .env
poetry install
poetry shell
alembic upgrade head
poetry run uvicorn src.app.main:app --reload
```

Run in Docker:

```bash
docker compose up --build
docker compose ps
docker compose down
```

If you wanna work local, you must change your .env and run App local and DB in Docker, so you can do this:

For example:

```bash
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/audio_prompts
```

And after that run command:

```bash
poetry shell
docker compose up -d db
docker compose ps
poetry run uvicorn src.app.main:app --reload
```

### 3. Test API in Postman

![Resgister User](media/user_auth.png)

![Login](media/user_login.png)

![Get User](media/get_user.png)

### 3. INFO about project

You run this url:

http://127.0.0.1:8000/docs#/

And see this and do all what you want, download audio from your local machine, CRUD tasks

![Project](media/info.png)
