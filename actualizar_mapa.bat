@echo off
setlocal EnableExtensions
cd /d "%~dp0"

title Actualizar mapas mentales - Markmap
echo.
echo ============================================
echo   Actualizacion local de mapas mentales
echo ============================================
echo.

where node >nul 2>nul
if errorlevel 1 (
  echo ERROR: Node.js no esta instalado o no esta en PATH.
  pause
  exit /b 1
)

if not exist "node_modules\markmap-cli" (
  echo Instalando dependencias de Markmap...
  call npm.cmd install
  if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias.
    pause
    exit /b 1
  )
)

echo Generando HTML desde mindmaps\...
call npm.cmd run build:maps
if errorlevel 1 (
  echo ERROR: La generacion del mapa fallo.
  pause
  exit /b 1
)

echo.
echo Mapa actualizado en docs\chapter-argument.html
start "" "%~dp0docs\index.html"
echo.
choice /c SN /n /m "Publicar tambien en GitHub Pages? [S/N]: "
if errorlevel 2 goto :local_done

set /p commit_message="Mensaje del commit (Enter = Actualizar mapas mentales): "
if "%commit_message%"=="" set "commit_message=Actualizar mapas mentales"

echo.
echo Guardando cambios y publicando...
git add mindmaps docs package.json package-lock.json scripts\build-markmaps.mjs actualizar_mapa.bat README.md .github\workflows\publish-mindmaps.yml
git commit -m "%commit_message%"
if errorlevel 1 (
  echo No se creo commit. Puede que no haya cambios nuevos.
  pause
  exit /b 1
)

git push
if errorlevel 1 (
  echo ERROR: Commit creado, pero git push fallo. Revisa credenciales o remoto.
  pause
  exit /b 1
)

echo Publicado. GitHub Actions compilara y desplegara GitHub Pages.
goto :finish

:local_done
echo Solo actualizacion local. No se hicieron cambios en GitHub.

:finish
echo.
pause
endlocal
