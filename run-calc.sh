#!/bin/sh

 cat examples/input.json | env ru.bystrobank.apps.stockvaluation.securitiesrefurl=https://bystrobank.github.io/stockvaluation/securities.xhtml python fairpricecalc --response-representation application/xml > fairpriceorder/data.xml