#!/bin/sh
set -e
cp template.ods order.ods
unzip -qq -c order.ods content.xml > order.content.xml
#tidy -m -i -utf8 -xml -w 1000 template.content.xml
xsltproc -o content.xml patch-content.xsl order.content.xml
zip order.ods content.xml
rm order.content.xml content.xml data.xml
