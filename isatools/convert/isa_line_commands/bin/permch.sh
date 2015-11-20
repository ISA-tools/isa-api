#!/bin/sh
#
#ÊWrapper for PermMod command
# 

ILBIN=$(dirname $0)
$ILBIN/lib/invoke.sh org.isatools.isatab.commandline.PermModShellCommand ${1+"$@"}
