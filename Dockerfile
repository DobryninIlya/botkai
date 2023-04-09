FROM alpine:3.12

WORKDIR /usr/src/app


#FROM python:3.8-alpine
#FROM python:3.8-slim
COPY requirements.txt .
#RUN apk add --no-cache python g++ make
RUN apk add py3-pip python3 g++ make
RUN apk add libxml2 libxslt libxml2-dev libxslt-dev
RUN pip install tld --ignore-installed six --user
RUN apk add python3-dev py3-setuptools
RUN apk add tiff-dev jpeg-dev openjpeg-dev zlib-dev freetype-dev lcms2-dev \
    libwebp-dev tcl-dev tk-dev harfbuzz-dev fribidi-dev libimagequant-dev \
    libxcb-dev libpng-dev
RUN pip3 install tld --ignore-installed six --user
RUN \
 apk add --no-cache python3 postgresql-libs py3-pip && \
 apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
 pip install -r requirements.txt && \
 apk --purge del .build-deps
#FROM python:3.8-alpine
COPY . .
RUN pip install tld --ignore-installed six
RUN pip install -r requirements.txt

#ENV PATH_TO_ENV=./EnvironmentPath.txt
#RUN while read line; do export $line; done < $PATH_TO_ENV
#RUN chmod +x ./EnvironmentPath
#RUN source ./EnvironmentPath
#CMD source ./EnvironmentPath
#ENTRYPOINT ["./EnvironmentPath"]
EXPOSE 5432 5432
EXPOSE 80 80
RUN printenv
CMD ["python3", "run_bot.py"]
#CMD source ./EnvironmentPath && python3 run_bot.py