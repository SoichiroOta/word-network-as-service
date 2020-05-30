FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
 && apt-get install -y \
      git \
      unzip \
 && rm -rf /var/lib/apt/lists/*

# フォントとして Ricty Diminished をインストールする。
WORKDIR /usr/share/fonts
ENV RICTY_DIMINISHED_VERSION 3.2.4
ADD https://github.com/mzyy94/RictyDiminished-for-Powerline/archive/$RICTY_DIMINISHED_VERSION-powerline-early-2016.zip .
RUN unzip -jo $RICTY_DIMINISHED_VERSION-powerline-early-2016.zip \
 && fc-cache -fv
COPY ./source-han-sans-2.001R /usr/share/fonts
RUN fc-cache -fv

# Matplotlib 用の設定ファイルを用意する。
WORKDIR /etc
RUN echo "backend : Agg" >> matplotlibrc \
 && echo "font.family : Ricty Diminished, Source Han Sans" >> matplotlibrc

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# add requirements
COPY ./requirements.txt /usr/src/app/requirements.txt

# install requirements
RUN pip install -r requirements.txt

# add app
COPY . /usr/src/app
