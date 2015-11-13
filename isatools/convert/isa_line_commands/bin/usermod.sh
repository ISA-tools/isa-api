#!/bin/sh
#
#ÊWrapper for User Mod command
# 

ILBIN=$(dirname $0)
$ILBIN/lib/invoke.sh org.isatools.isatab.commandline.UserModShellCommand ${1+"$@"}
