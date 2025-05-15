package models

import (
	"gorm.io/gorm"
)

type ProfileSkills struct {
	gorm.Model
	Title string `gorm:"type:varchar(255);not null" json:"title"`
}

func (*ProfileSkills) TableName() string {
	return "profiles_profileskill"
}
