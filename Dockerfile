# Production image, copy all the files and run next
FROM node:16.20-alpine AS runner

RUN apk add py3-setuptools py3-numpy py3-pandas
WORKDIR /app
COPY . .
RUN python setup.py install

CMD /bin/sh
