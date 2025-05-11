FROM python:3.11-slim

# 基本ツールと awslocal のインストール
RUN apt-get update && \
    apt-get install -y \
    git \
    curl \
    unzip \
    zip \
    locales && \
    locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 && \ 
    pip install --upgrade pip

# 環境変数のデフォルト値（LocalStack 開発用）
ENV AWS_ACCESS_KEY_ID=test \
    AWS_SECRET_ACCESS_KEY=test \
    AWS_DEFAULT_REGION=ap-northeast-1 \
    LANG en_US.UTF-8 \
    LANGUAGE en_US:en \
    LC_ALL en_US.UTF-8

WORKDIR /workspace
