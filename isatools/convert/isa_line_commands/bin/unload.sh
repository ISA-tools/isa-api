#!/bin/sh
#
#ÊWrapper for the ISATAB Unloader
# 

ILBIN=$(dirname $0)
$ILBIN/lib/invoke.sh org.isatools.isatab.commandline.UnloadShellCommand ${1+"$@"}
