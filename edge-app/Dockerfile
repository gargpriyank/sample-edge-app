FROM alpine:latest

COPY resources /

RUN apk update && apk add --no-cache \
    bash \
    alpine-sdk \
    python3 \
    cmake \
    curl-dev \
    bsd-compat-headers \
    perl \
    jq && \
    rm -fr /tmp/* && \
    ln -sf python3 /usr/bin/python && \
    python3 -m ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools && \
    pip3 install -r requirements.txt && \
    chmod +x /initialize.sh

RUN curl https://codeload.github.com/edenhill/kafkacat/tar.gz/master | tar xzf - && cd kafkacat-* && bash ./bootstrap.sh
RUN make -C /kafkacat-master bin-install

WORKDIR /

CMD ["/initialize.sh"]