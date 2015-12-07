@echo off

REM Configuration options common to all tools go here.

SET COMMON_OPTS=-Xms256m -Xmx1024m -XX:PermSize=64m -XX:MaxPermSize=128m



REM The Database driver. You need to set this to your driver, in case you don't use one of the provided ones

REM JDBCPATH=/path/to/jdbc_driver.jar

REM SET JDBCPATH=c:\tmp\ojdbc5.jar



