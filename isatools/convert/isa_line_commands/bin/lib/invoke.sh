#!/bin/sh
#
# Invokes one of the tools
# 

# TODO: .bat version, see:
#   http://weblogs.asp.net/whaggard/archive/2005/01/28/get-directory-path-of-an-executing-batch-file.aspx
#   http://www.google.co.uk/url?sa=t&source=web&ct=res&cd=1&ved=0CAYQFjAA&url=http%3A%2F%2Fblogs.msdn.com%2Foldnewthing%2Farchive%2F2005%2F01%2F28%2F362565.aspx&ei=XFenS7KmH4Pw0gTwrv3CAQ&usg=AFQjCNGFcH4Ejyin5J2riZhgeDL93v5rMw&sig2=i_7TmYuXg7lQz5nWC1dbBg
#
ILLIB=$(dirname $0)
ILBIN=$ILLIB/..
. $ILBIN/config.sh
. $ILLIB/init.sh

CLASSNAME=$1
shift

java -version

# See here for an explaination about ${1+"$@"} :
# http://stackoverflow.com/questions/743454/space-in-java-command-line-arguments 

java \
  $COMMON_OPTS \
  -Dbioinvindex.config-path=$ILHOME/config \
  -cp $CP $CLASSNAME \
  ${1+"$@"}

RES=$?

echo ${RES}
echo Finished.
exit ${RES}