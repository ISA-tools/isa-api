#!/bin/sh
#
#ÊWrapper for User Add command
# 

ILBIN=$(dirname $0)
$ILBIN/lib/invoke.sh org.isatools.isatab.commandline.UserAddShellCommand ${1+"$@"}
