# container in which to dev/test this app
# meant for interactive use only

FROM python:3.7

RUN apt-get update && \
  apt-get -y install less sqlite3 vim && \
  apt-get -y install libxml-libxml-perl

RUN pip3 install Flask-Bootstrap
RUN pip3 install indic_transliteration

EXPOSE 5000
WORKDIR /data/src/amara-quiz

# docker build -t amara-dev -f amara-dev.dockerfile ~/src/containers/empty_context
# docker run -p 8888:5000 -it --rm -v ~:/data amara-dev bash
