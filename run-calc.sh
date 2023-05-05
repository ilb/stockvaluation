#!/bin/sh
cat examples/input.json | env ru.bystrobank.apps.stockvaluation.securitiesrefurl=https://ilb.github.io/stockvaluation/securities.xhtml python . --response-representation application/xml 
