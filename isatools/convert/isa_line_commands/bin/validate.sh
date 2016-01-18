#!/bin/sh
#
#ÊWrapper for the ISATAB Validator
# 

ILBIN=$(dirname $0)
$ILBIN/lib/invoke.sh org.isatools.isatab.commandline.ValidateShellCommand ${1+"$@"}
