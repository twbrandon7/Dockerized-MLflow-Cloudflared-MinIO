FROM alpine:3.17.1

RUN apk add curl

RUN curl -o cloudflared -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64

RUN chmod +x cloudflared && \
    mv cloudflared /bin

ENTRYPOINT ["cloudflared", "--no-autoupdate"]
CMD ["version"]
