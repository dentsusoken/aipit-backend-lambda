FROM python:3.11-slim

# 基本ツールとロケール設定
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    curl \
    unzip \
    zip \
    locales && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen && \
    echo 'LANG=en_US.UTF-8' > /etc/default/locale && \
    pip install --upgrade pip

# 環境変数のデフォルト値（LocalStack 開発用）
ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en

WORKDIR /workspace
