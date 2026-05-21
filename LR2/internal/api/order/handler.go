package order

import (
	"context"
	"log/slog"
	"taxiservice1/internal/model"
)

type OrderService interface {
	CreateOrder(ctx context.Context, req model.CreateOrderRequest) (model.CreatedOrder, error)
}

type Handler struct {
	orderService OrderService
	log          *slog.Logger
}

func NewHandler(orderService OrderService, log *slog.Logger) *Handler {
	return &Handler{orderService: orderService, log: log}

}

func (h *Handler) CreateOrder(ctx context.Context, req model.CreateOrderRequest) (model.CreatedOrder, error) {
	createdOrder, err := h.orderService.CreateOrder(ctx, req)
	if err != nil {
		h.log.Error("handler.CreateOrder", "err", err, "client_id", req.ClientID)
	}

	h.log.Info("handler.CreateOrder", "createdOrder", createdOrder)

	return createdOrder, nil
}
