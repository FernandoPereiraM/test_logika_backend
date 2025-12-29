@echo off
TITLE FastAPI Environment Setup
set PYTHONUTF8=1

:: 1. Gestión del Entorno Virtual (VENV)
if not exist "env\" (
    echo [!] Creando entorno virtual...
    python -m venv env
    if %errorlevel% neq 0 (echo Error al crear venv && pause && exit /b)
    
    echo [+] Actualizando pip dentro del entorno...
    :: Usamos 'call' para mantener el proceso vivo tras activar el venv
    call env\Scripts\activate && python.exe -m pip install --upgrade pip
    
    echo [+] Instalando dependencias desde requirements.txt...
    call env\Scripts\activate && pip install -r requirements.txt
) else (
    echo [OK] Entorno virtual detectado.
)

:: 2. Ejecución con el Entorno Activo
echo [+] Iniciando servicios...
docker-compose up -d

:: Sincronizar Base de Datos usando el entorno
call env\Scripts\activate && alembic upgrade head

:: Ejecutar el servidor usando el entorno
echo ====================================================
echo   ENTORNO ACTIVO - INICIANDO FASTAPI
echo ====================================================
call env\Scripts\activate && uvicorn app.main:app --reload

pause