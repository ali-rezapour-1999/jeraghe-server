package models

import (
	"database/sql"

	"gorm.io/gorm"
)

type Profile struct {
	gorm.Model
	SlugID      string         `gorm:"type:varchar(100);unique;not null" json:"slug_id"`
	Gender      sql.NullString `gorm:"type:varchar(50)" json:"gender"`
	Age         sql.NullString `gorm:"type:varchar(10)" json:"age"`
	State       sql.NullString `gorm:"type:varchar(100)" json:"state"`
	City        sql.NullString `gorm:"type:varchar(100)" json:"city"`
	Address     sql.NullString `gorm:"type:text" json:"address"`
	Description sql.NullString `gorm:"type:text" json:"description"`
}
