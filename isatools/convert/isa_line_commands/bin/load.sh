#!/bin/sh
#
#ÊWrapper for the ISATAB Loader
# 

ILBIN=$(dirname $0)
$ILBIN/lib/invoke.sh org.isatools.isatab.commandline.PersistenceShellCommand ${1+"$@"}
