package models

type Profile struct {
	ID          int     `json:"id"`
	SlugID      string  `json:"slug_id"`
	Gender      *string `json:"gender"`
	Age         *int    `json:"age"`
	State       *string `json:"state"`
	City        *string `json:"city"`
	Address     *string `json:"address"`
	Description *string `json:"description"`
}
