@echo off
REM Invokes one of the tools

set CP=%ILHOME%\import_layer_deps.jar;%JDBCPATH%

java %COMMON_OPTS% -Dbioinvindex.config-path=%ILHOME%\config -cp %CP% %*
echo Finished.
