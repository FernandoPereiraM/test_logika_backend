@echo off
TITLE FastAPI Dev Environment
set PYTHONUTF8=1

echo [1/6] Iniciando Docker...
cd /d "%~dp0..\test_logika_backend"
docker-compose up -d

echo [2/6] Esperando a la BD...
timeout /t 10 /nobreak > NUL

echo [3/6] Limpiando rastro de versiones...
cd /d "%~dp0..\test_logika_backend"
docker exec technical_test_db psql -U postgres -d technical_test -c "DROP TABLE IF EXISTS alembic_version CASCADE;"

echo [4/6] Aplicando esquema...
cd /d "%~dp0..\test_logika_backend"
call env\Scripts\activate && alembic revision --autogenerate -m "tables"
call env\Scripts\activate && alembic upgrade head

echo [5/6] Ejecutando Seed...
cd /d "%~dp0..\test_logika_backend"
call env\Scripts\activate && python -m app.db.seed

echo [6/6] Iniciando Servidor...
cd /d "%~dp0..\test_logika_backend"
call env\Scripts\activate && uvicorn app.main:app --reload
pause