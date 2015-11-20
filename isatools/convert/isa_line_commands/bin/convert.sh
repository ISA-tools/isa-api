#!/bin/sh
#
#ÊWrapper for the ISATAB Converter
# 

ILBIN=$(dirname $0)
$ILBIN/lib/invoke.sh org.isatools.isatab.commandline.ConverterShellCommand ${1+"$@"}
