FROM ubuntu:18.04
FROM python:3.7


MAINTAINER Ivan Volodin <ivanwolodin@gmail.com>


ENV to_working_dir /home/web_app
ENV TZ=Europe/Moscow


WORKDIR                 ${to_working_dir}
# COPY .                /$to_working_dir
ADD hello.c             $to_working_dir 
ADD setup.py            $to_working_dir 
ADD getservertime.cpp   $to_working_dir 
#ADD check.py            $to_working_dir
ADD setup.py            $to_working_dir 
ADD server_w.py         $to_working_dir 
ADD client_w.py         $to_working_dir 


RUN apt-get update   && apt-get install nano
RUN apt-get update   && apt-get install build-essential
# RUN apt-get update && apt-get -y install python-dev
# RUN apt-get update && apt-get -y install python3-dev
RUN apt-get update   && apt-get -y install libpython3.7-dev

RUN python3 setup.py install
RUN python -m pip install psutil
RUN python -m pip install aiohttp


# create user to not work as a root
RUN groupadd -r ivan && useradd -r -g ivan ivan
RUN chown -R ivan:ivan /home/web_app 
USER ivan


CMD tail -f /dev/null # to prevent exiting
#ENTRYPOINT ["ping", "www.google.com"]
