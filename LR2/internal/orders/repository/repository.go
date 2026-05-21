package repository

import (
	"context"
	"database/sql"

	sq "github.com/Masterminds/squirrel"
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
	query, args, err := sq.Insert("orders").
		Columns(
			"client_id",
			"driver_id",
			"price",
			"status",
			"from_lat",
		).
		Values(
			order.ClientID,
			order.DriverID,
			order.Price,
			order.Status,
			order.FromLat,
		).
		Suffix("RETURNING id").PlaceholderFormat(sq.Dollar).ToSql()

	if err != nil {
		return model.CreatedOrder{}, err
	}

	var res model.CreatedOrder
	if err := r.db.QueryRowContext(ctx, query, args...).Scan(&res.OrderID); err != nil {
		return model.CreatedOrder{}, err
	}

	return res, nil
}
