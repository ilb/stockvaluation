#!/bin/sh

 cat examples/input.json | env ru.ilb.stockvaluation.securitiesrefurl=http://devel.net.ilb.ru/treasurytemp/issuancevolume.xhtml python fairpricecalc --response-representation application/xml > fairpriceorder/data.xml