package main

import (
	"context"
	"log/slog"
	"os"
	"taxiservice1/internal/app"
)

func main() {
	ctx := context.Background()

	a, err := app.New(ctx)
	if err != nil {
		slog.Error("cmd.main", "err", err)

		os.Exit(1)
	}

	if err := a.Run(); err != nil {
		slog.Error("cmd.main", "err", err)

		os.Exit(1)
	}
}
