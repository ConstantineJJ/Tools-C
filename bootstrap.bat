@echo off
setlocal
if defined TOOLS_C_PYTHON (
  "%TOOLS_C_PYTHON%" "%~dp0tools\bootstrap.py" %*
) else (
  python "%~dp0tools\bootstrap.py" %*
)
exit /b %errorlevel%
