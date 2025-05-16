package models

import (
	"gorm.io/gorm"
)

type Profile struct {
	gorm.Model
	SlugID      string `gorm:"type:varchar(100);unique;not null" json:"slug_id"`
	Gender      string `gorm:"type:varchar(50)" json:"gender"`
	Age         string `gorm:"type:varchar(10)" json:"age"`
	State       string `gorm:"type:varchar(100)" json:"state"`
	City        string `gorm:"type:varchar(100)" json:"city"`
	Address     string `gorm:"type:text" json:"address"`
	Description string `gorm:"type:text" json:"description"`
}

func (*Profile) TableName() string {
	return "profiles_profile"
}
