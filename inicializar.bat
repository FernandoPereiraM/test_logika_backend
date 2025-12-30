@echo off
TITLE FastAPI Initial Setup
set PYTHONUTF8=1

cd /d "%~dp0"

echo [1/7] Iniciando Docker...
docker-compose up -d

echo [2/7] Esperando a la BD...
timeout /t 10 /nobreak > NUL

echo [3/7] Verificando entorno virtual...
if not exist env\Scripts\activate.bat (
    echo Creando entorno virtual...
    python -m venv env
)

call env\Scripts\activate

echo [4/7] Instalando dependencias...
pip install -r requirements.txt

echo [5/7] Verificando estructura de migraciones...
if not exist app\db\migrations\versions (
    mkdir app\db\migrations\versions
)

echo [6/7] Verificando migraciones...
if not exist app\db\migrations\versions\*.py (
    echo Creando migracion inicial...
    alembic revision --autogenerate -m "initial_schema"
) else (
    echo Migraciones existentes detectadas.
)

echo [7/7] Aplicando esquema, seed y servidor...
alembic upgrade head
python -m app.db.seed
uvicorn app.main:app --reload

pause
