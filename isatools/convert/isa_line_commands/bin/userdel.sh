#!/bin/sh
#
#ÊWrapper for User Del command
# 

ILBIN=$(dirname $0)
$ILBIN/lib/invoke.sh org.isatools.isatab.commandline.UserDelShellCommand ${1+"$@"}
