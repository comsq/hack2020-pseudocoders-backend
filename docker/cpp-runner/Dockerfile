FROM alpine:latest

RUN apk update && \
    apk upgrade && \
    apk --update add \
        bash \
        build-base \
        cmake \
        cppcheck \
        gcc \
        g++ \
        libstdc++ && \
    rm -rf /var/cache/apk/*

ADD entrypoint.sh /entrypoint.sh

CMD ["/entrypoint.sh"]

# docker run \
# -it --rm \
# -v "$PWD/source:/source" \
# -v "$PWD/tests:/tests" \
# dimastark/cpp-runner
