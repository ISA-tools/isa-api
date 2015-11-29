@echo off
REM Wrapper for the ISATAB Reindex Command

call config.bat

set ILBIN=%~dp0

set ILHOME=%ILBIN%\..

call %ILBIN%\invoke.bat org.isatools.isatab.commandline.ReindexShellCommand %*



