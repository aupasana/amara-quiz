# Instructions copied from - https://hub.docker.com/_/python/
FROM python:3-onbuild

# RUN pip install beautifulsoup4
RUN pip install indic_transliteration
RUN pip install flask-bootstrap

# tell the port number the container should expose
EXPOSE 5000

# run the command
CMD ["python", "./app.py"]
