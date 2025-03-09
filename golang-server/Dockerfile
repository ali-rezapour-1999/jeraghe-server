FROM golang:1.22.2 AS builder

WORKDIR /go-app

COPY go.mod go.sum ./

ENV GOPROXY=https://goproxy.io,direct

RUN go mod download

COPY . .

RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app

FROM alpine:3.19

RUN apk --no-cache add ca-certificates

WORKDIR /app
COPY --from=builder /go-app .

EXPOSE 8080
CMD ["./app"]
