@echo off
setlocal
if defined TOOLS_C_PYTHON (
  "%TOOLS_C_PYTHON%" "%~dp0tools\check.py" %*
) else (
  python "%~dp0tools\check.py" %*
)
exit /b %errorlevel%
