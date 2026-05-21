package model

import "time"

type CreateOrderRequest struct {
	ClientID  int64
	DriverID  int64
	Price     float64
	Status    string
	FromLat   float64
	FromLon   float64
	ToLat     float64
	ToLon     float64
	CreatedAt time.Time
	UpdateAt  time.Time
}

type CreatedOrder struct {
	OrderID int64
}
