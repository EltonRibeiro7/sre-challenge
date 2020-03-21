FROM python:3.7.7-alpine3.11
LABEL MAINTAINER=eltonribeiro@outlook.com
LABEL app=api
WORKDIR /app
COPY ./api/ ./api/
COPY ./shared/ ./shared/
COPY requirements.txt . 
RUN apk add --update --no-cache mariadb-connector-c-dev \
	&& apk add --no-cache --virtual .build-deps \
		mariadb-dev \
		gcc \
		musl-dev \
	&& pip install mysqlclient==1.4.6 \
	&& apk del .build-deps
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /app/api
CMD [ "python", "./app.py" ]