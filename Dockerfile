FROM python:3.8-alpine

RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libressl-dev libffi-dev
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/

RUN pip install -r requirements.txt
ADD . /app/

EXPOSE 8050
ENTRYPOINT [ "python" ]
CMD ["index.py"]