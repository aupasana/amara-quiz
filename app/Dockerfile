FROM aupasana/amara-babylon as builder-babylon
FROM python:3.7-alpine

# install pip requirements and remove build tools
RUN apk add --no-cache --virtual .build-deps gcc musl-dev
COPY requirements.txt /
RUN pip install -r /requirements.txt
RUN apk del .build-deps gcc musl-dev

# copy files -- static files first
COPY --from=builder-babylon /data/babylon.db.gz .
COPY static/ /static/
COPY amara.db.gz /
COPY templates/ /templates/
COPY app.py /

COPY init.sh /usr/local/bin/
RUN ln -s usr/local/bin/init.sh /
ENTRYPOINT ["init.sh"]

# tell the port number the container should expose
EXPOSE 5000

CMD ["python", "./app.py"]
#CMD ["python", "-u", "./app.py"]
