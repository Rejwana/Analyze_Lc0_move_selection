FROM nvidia/cuda:10.0-cudnn7-devel as builder

COPY . /

## Install Prerequisites

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y git wget unzip ninja-build python3.7 python3-pip gcc-8 g++-8 libeigen3-dev clang libopenblas-dev && \
    pip3 install meson==0.55.3
RUN apt-get install -y vim

RUN apt-get install -y mysql-client
RUN apt-get install -y mysql-server

# download and compile lc0
RUN     mkdir -p /lc0 && \
        wget -qO - https://github.com/LeelaChessZero/lc0/archive/master.tar.gz | \
            tar xzf - -C /lc0 --strip-components 1

RUN     wget -qO - https://github.com/LeelaChessZero/lczero-common/archive/master.tar.gz | \
            tar xzf - -C /lc0/libs/lczero-common --strip-components 1

RUN     CC=clang CXX=clang++ /lc0/build.sh


WORKDIR /Py
ENV LC_ALL=C.UTF-8 LANG=C.UTF-8
RUN pip3 install pipenv && pipenv install --system --deploy --ignore-pipfile

WORKDIR /
