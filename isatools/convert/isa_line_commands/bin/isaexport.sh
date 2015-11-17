#!/bin/sh
#
#ÊWrapper for the ISATAB Exporter
# 

ILBIN=$(dirname $0)
$ILBIN/lib/invoke.sh org.isatools.isatab.commandline.ISATABExportShellCommand ${1+"$@"}

