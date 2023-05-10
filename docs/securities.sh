set -e
curl -o securities.xhtml --cert ~/.certs/my.pem https://docs.ilb.ru/doc/treasurydocs/repo/data/issuancevolume.xhtml
git commit -a -m "update" && git  push
