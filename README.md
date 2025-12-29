docker-compose up -d
alembic revision --autogenerate -m "reinit_db"
alembic upgrade head
python -m app.db.seed
uvicorn app.main:app --reload