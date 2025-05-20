FROM python:3.13-slim

# 環境変数のデフォルト値（LocalStack 開発用）
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en

# プロキシ設定
# ENV http_proxy="http://your-proxy"
# ENV HTTP_PROXY="http://your-proxy"
# ENV https_proxy="http://your-proxy"
# ENV HTTPS_PROXY="http://your-proxy"
# ENV no_proxy="localhost,localhost.localstack.cloud,127.0.0.1,[::1],localstack"
# ENV NO_PROXY="localhost,localhost.localstack.cloud,127.0.0.1,[::1],localstack"

# 基本ツールとロケール設定
RUN apt-get update
RUN apt-get install -y --no-install-recommends git curl unzip zip locales less
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen
RUN locale-gen
RUN echo 'LANG=en_US.UTF-8' > /etc/default/locale
RUN pip install --upgrade pip

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip"
RUN unzip /tmp/awscliv2.zip -d /tmp
RUN /tmp/aws/install

RUN curl -L -o /tmp/aws-sam-cli-linux.zip https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip
RUN unzip /tmp/aws-sam-cli-linux.zip -d /tmp/aws-sam-cli-linux
RUN /tmp/aws-sam-cli-linux/install

WORKDIR /workspace
