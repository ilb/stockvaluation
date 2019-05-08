#!/bin/sh
set -e
cp template.ods report.ods
unzip -qq -c report.ods content.xml > report.content.xml
#tidy -m -i -utf8 -xml -w 1000 template.content.xml
xsltproc -o content.xml patch-content.xsl report.content.xml
zip report.ods content.xml
rm report.content.xml content.xml data.xml
