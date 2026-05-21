package app

import (
	"context"
	"database/sql"
	"errors"
	"fmt"
	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/jackc/pgx/v5/stdlib"
	"google.golang.org/grpc"
	"log/slog"
	"net"
	"os"
	"os/signal"
	"syscall"
	"taxiservice1/internal/migrations"
	"taxiservice1/pkg/closer"
	"taxiservice1/pkg/config"
	"taxiservice1/pkg/grpcmw"
	"taxiservice1/pkg/logger"
	"taxiservice1/pkg/migrator"
	"taxiservice1/pkg/postgres"
	"time"
)

type App struct {
	log        *slog.Logger
	pool       *pgxpool.Pool
	db         *sql.DB
	grpcServer *grpc.Server
	closer     *closer.Closer
}

func New(ctx context.Context) (*App, error) {
	if err := config.LoadDotEnv(".env"); err != nil {
		return nil, fmt.Errorf("app.New: %w", err)
	}

	env := config.Get("APP_ENV", "local")
	grpcAddr := config.MustGet("GRPC_ADDR")
	dsn := config.MustGet("DATABASE_URL")

	logger.Setup(env)
	log := logger.With("service", "order")
	log.Info("starting app order", "env", env, "grpc_addr", grpcAddr)

	pool, err := postgres.NewPool(ctx, dsn)
	if err != nil {
		return nil, fmt.Errorf("app.New: %w", err)
	}

	sqlDb := stdlib.OpenDBFromPool(pool)
	m, err := migrator.EmbedMigrations(sqlDb, migrations.FS, ".")
	if err != nil {
		return nil, fmt.Errorf("app.New: %w", err)
	}
	if err := m.Up(); err != nil {
		return nil, fmt.Errorf("app.New: %w", err)
	}

	shutdownCloser := closer.New(log.With("component", "shutdown"))
	shutdownCloser.AddFunc("postgres db", func() {
		_ = sqlDb.Close()
	})
	shutdownCloser.AddFunc("postgres pool", pool.Close)

	return &App{
		log:  log,
		pool: pool,
		db:   sqlDb,
		grpcServer: grpc.NewServer(
			grpc.UnaryInterceptor(grpcmw.UnaryServerLoggingInterceptor(log.With("component", "grpc"))),
		),
		closer: shutdownCloser,
	}, nil
}

func (a *App) Run() error {
	grpcAddr := config.MustGet("GRPC_ADDR")
	lis, err := net.Listen("tcp", grpcAddr)
	if err != nil {
		return fmt.Errorf("app.Run: %w", err)
	}

	a.closer.AddFunc("grpc listener", func() {
		_ = lis.Close()
	})
	a.closer.Add("grpc server", func(ctx context.Context) error {
		done := make(chan struct{})

		go func() {
			a.grpcServer.GracefulStop()
			close(done)
		}()

		select {
		case <-done:
			return nil
		case <-ctx.Done():
			a.grpcServer.Stop()
			<-done
			return ctx.Err()
		}
	})

	errCh := make(chan error, 1)
	go func() {
		if err := a.grpcServer.Serve(lis); err != nil && !errors.Is(err, grpc.ErrServerStopped) {
			errCh <- fmt.Errorf("app.Run: %w", err)
		}
	}()

	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, os.Interrupt, syscall.SIGTERM)

	select {
	case err := <-errCh:
		return err
	case sig := <-sigCh:
		a.log.Info("shutdown signal received", "signal", sig.String())
	}

	shutdownctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := a.closer.Close(shutdownctx); err != nil && !errors.Is(err, context.DeadlineExceeded) {
		return fmt.Errorf("app.Run: graceful shutdown %w", err)
	}

	a.log.Info("app stopped")

	return nil
}
