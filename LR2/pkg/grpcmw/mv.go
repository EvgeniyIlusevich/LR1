package grpcmw

import (
	"context"
	"google.golang.org/grpc"
	"google.golang.org/grpc/status"
	"log/slog"
	"time"
)

func UnaryServerLoggingInterceptor(log *slog.Logger) grpc.UnaryServerInterceptor {
	return func(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
		start := time.Now()
		resp, err := handler(ctx, req)
		code := status.Code(err)

		log.Info("grpc request",
			"method", info.FullMethod,
			"code", code,
			"duration",
			time.Since(start),
		)

		return resp, err
	}
}
