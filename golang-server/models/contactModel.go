package models

type Contact struct {
	ID         int    `json:"id"`
	UserID     int    `json:"user_id"`
	SlugID     string `json:"slug_id"`
	IsActive   bool   `json:"is_active"`
	Platform   string `json:"platform"`
	Link       string `json:"link"`
	IsVerified bool   `json:"is_verified"`
}
