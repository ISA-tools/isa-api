#!/bin/sh
#
#ÊWrapper for Contents command
# 

ILBIN=$(dirname $0)
$ILBIN/lib/invoke.sh org.isatools.isatab.commandline.ReindexShellCommand ${1+"$@"}

