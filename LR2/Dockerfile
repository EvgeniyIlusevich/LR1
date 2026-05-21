FROM golang:1.25.3-alpine AS builder
WORKDIR /src
RUN apk add --no-cache ca-certificates git

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o /out/taxiservice ./cmd

FROM alpine:3.21
WORKDIR /app
RUN apk add --no-cache ca-certificates

COPY --from=builder /out/taxiservice /app/taxiservice

EXPOSE 50051

CMD ["/app/taxiservice"]