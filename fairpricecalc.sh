#!/bin/bash
env python.net.ssl.trustStore=$HOME/.certs/ourCAbundle.crt python.net.ssl.keyStore=$HOME/.certs/stockvaluation.pem \
ru.bystrobank.apps.stockvaluation.securitiesrefurl=https://docs.ilb.ru/doc/treasurydocs/repo/data/issuancevolume.xhtml \
python fairpricecalc $*