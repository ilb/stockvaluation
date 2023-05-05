# Production image, copy all the files and run next
FROM node:16.20-alpine AS runner

RUN apk add py3-setuptools py3-pandas py3-lxml py3-dicttoxml
WORKDIR /app
COPY . .
RUN cd fairpricecalc && python setup.py install
ENV ru.bystrobank.apps.stockvaluation.securitiesrefurl=https://ilb.github.io/stockvaluation/securities.xhtml

CMD python fairpricecalc
