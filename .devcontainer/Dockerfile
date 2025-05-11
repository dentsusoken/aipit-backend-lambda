FROM python:3.11-slim

# 基本ツールと awslocal のインストール
RUN apt-get update && \
    apt-get install -y \
    git \
    curl \
    unzip \
    zip \
    && pip install --upgrade pip

# 環境変数のデフォルト値（LocalStack 開発用）
ENV AWS_ACCESS_KEY_ID=test \
    AWS_SECRET_ACCESS_KEY=test \
    AWS_DEFAULT_REGION=ap-northeast-1

WORKDIR /workspace
