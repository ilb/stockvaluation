# Production image, copy all the files and run next
FROM node:16.20-alpine AS runner

#RUN apk add py3-setuptools libxml2-dev libxslt-dev  libc-dev gcc python3-dev py3-numpy py3-pandas
RUN apk add py3-setuptools py3-numpy py3-pandas
WORKDIR /app
COPY . .
RUN python setup.py install
#RUN wget -qO - https://github.com/ilb/stockvaluation/archive/refs/heads/master.zip |busybox unzip -
#RUN apk add g++
#RUN cd stockvaluation-master/fairpricecalc && python3 -m venv .env && source .env/bin/activate && .env/bin/python -m pip install --&& .env/bin/python -m pip install install numpy && python setup.py install
#RUN cd stockvaluation-master/fairpricecalc && python setup.py install

#USER nextjs

CMD /bin/sh
