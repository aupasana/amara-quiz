# Instructions copied from - https://hub.docker.com/_/python/
FROM aupasana/amara-babylon as builder-babylon

FROM python:3-onbuild
COPY --from=builder-babylon /data/babylon.db.gz .

# tell the port number the container should expose
EXPOSE 5000

# run the command
COPY init.sh /usr/local/bin/
RUN ln -s usr/local/bin/init.sh /
ENTRYPOINT ["init.sh"]

CMD ["python", "./app.py"]

#CMD ["python", "-u", "./app.py"]
