#!/usr/bin/env bash
# Setup the classpath
#

PWD="$(pwd)"
cd "$ILBIN/.."
ILHOME="$(pwd)"
cd "$PWD"

CP="$ILHOME/import_layer_deps.jar"
if [ "$JDBCPATH" != "" ]; then
  CP="$CP:$JDBCPATH"
fi

#CP=""
#for i in $(find $ILHOME/lib -type f -name '*.jar')
#do
#  CP=$CP$sep$i
#  sep=':'
#done
