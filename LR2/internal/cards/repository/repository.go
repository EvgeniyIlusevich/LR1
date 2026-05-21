package repository

import (
	"context"
	"database/sql"
	"taxiservice1/internal/model"
)

type Repository struct {
	db *sql.DB
}

func NewRepository(db *sql.DB) *Repository {
	return &Repository{
		db: db,
	}
}

func (r *Repository) CreateOrder(ctx context.Context, order model.CreateOrderRequest) (model.CreatedOrder, error) {
	const query = `
		INSERT INTO orders (client_id, driver_id)
		VALUES ($1, $2)
		RETURNING id
	`

	var created model.CreatedOrder
	if err := r.db.QueryRowContext(ctx, query, order.ClientID, order.DriverID).Scan(&created.OrderID); err != nil {
		return model.CreatedOrder{}, err
	}

	return created, nil
}
