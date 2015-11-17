#ÊConfiguration options common to all tools go here.
COMMON_OPTS="-Xms256m -Xmx1024m -XX:PermSize=64m -XX:MaxPermSize=128m"

# Used for invoking a command in debug mode (end user doesn't usually need this)
#COMMON_OPTS="$COMMON_OPTS -Xdebug -Xnoagent"
#COMMON_OPTS="$COMMON_OPTS -Djava.compiler=NONE -Xrunjdwp:transport=dt_socket,server=y,suspend=y,address=5005"

# The Database driver. You need to set this to your driver, in case you don't use one of the provided ones
# 
#JDBCPATH=/path/to/jdbc_driver.jar
