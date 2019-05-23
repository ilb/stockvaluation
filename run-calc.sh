#!/bin/sh

 cat examples/input.json | env ru.bystrobank.apps.stockvaluation.securitiesrefurl=https://raw.githubusercontent.com/bystrobank/stockvaluation/master/fairpricecalc/test/volume.xhtml python fairpricecalc --response-representation application/xml > fairpriceorder/data.xml