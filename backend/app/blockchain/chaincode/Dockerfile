FROM golang:1.21-alpine AS builder

WORKDIR /go/src/github.com/chaincode
COPY . .

RUN go mod init foodtrace && \
    go mod tidy && \
    CGO_ENABLED=0 GOOS=linux go build -o chaincode

FROM alpine:3.18
RUN apk add --no-cache bash
WORKDIR /root/
COPY --from=builder /go/src/github.com/chaincode/chaincode .

ENV CORE_PEER_TLS_ENABLED=false \
    CORE_CHAINCODE_LOGGING_LEVEL=DEBUG \
    CORE_CHAINCODE_LOGGING_SHIM=DEBUG

EXPOSE 7052
ENTRYPOINT ["./chaincode"] 