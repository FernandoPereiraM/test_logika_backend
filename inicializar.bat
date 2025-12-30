@echo off
TITLE FastAPI Dev Environment
set PYTHONUTF8=1

REM Ir siempre al directorio del proyecto
cd /d "%~dp0"

echo [1/6] Iniciando Docker...
docker-compose up -d

echo [2/6] Esperando a la BD...
timeout /t 10 /nobreak > NUL

echo [3/6] Limpiando rastro de versiones...
docker exec technical_test_db psql -U postgres -d technical_test -c "DROP TABLE IF EXISTS alembic_version CASCADE;"

echo [4/6] Aplicando esquema...
call env\Scripts\activate
alembic upgrade head

echo [5/6] Ejecutando Seed...
python -m app.db.seed

echo [6/6] Iniciando Servidor...
uvicorn app.main:app --reload

pause
