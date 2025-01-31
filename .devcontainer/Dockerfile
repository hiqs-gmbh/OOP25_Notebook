FROM mcr.microsoft.com/devcontainers/python:1-3.12

RUN apt-get update && apt-get install -y \
ffmpeg \
git-lfs 

COPY ./requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

