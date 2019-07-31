FROM aupasana/amara-babylon as builder-babylon
FROM python:3.7-alpine

# install pip requirements and remove build tools
COPY requirements.txt /
RUN apk add --no-cache --virtual .build-deps gcc musl-dev && \
  pip install -r /requirements.txt && \
  apk del .build-deps gcc musl-dev

# copy files -- static files first
COPY --from=builder-babylon /data/babylon.db.gz .
COPY static/ /static/
COPY rupavali_shabda.db.gz /
COPY koshas_mulam.db.gz /
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
