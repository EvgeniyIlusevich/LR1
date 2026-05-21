package service

import (
	"context"
	"taxiservice1/internal/model"
)

type OrderRepository interface {
	CreateOrder(ctx context.Context, order model.CreateOrderRequest) (model.CreatedOrder, error)
}

type Service struct {
	orderRepo OrderRepository
}

func NewService(orderRepo OrderRepository) *Service {
	return &Service{orderRepo: orderRepo}

}

func (s *Service) CreateOrder(ctx context.Context, order model.CreateOrderRequest) (model.CreatedOrder, error) {
	res, err := s.orderRepo.CreateOrder(ctx, order)
	if err != nil {
		return model.CreatedOrder{}, err
	}

	return res, nil
}
