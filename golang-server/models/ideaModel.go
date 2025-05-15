package models

import (
	"encoding/json"
	"time"

	"gorm.io/gorm"
)

type IdeaPost struct {
	gorm.Model
	SlugID             string    `gorm:"type:varchar(100);unique;not null" json:"slug_id"`
	IsActive           bool      `gorm:"default:true" json:"is_active"`
	Title              string    `gorm:"type:varchar(255);not null" json:"title"`
	Image              string    `gorm:"type:varchar(255)" json:"image"`
	Description        string    `gorm:"type:text" json:"description"`
	Status             string    `gorm:"type:varchar(50)" json:"status"`
	NeedsCollaborators bool      `gorm:"default:false" json:"needs_collaborators"`
	CollaborationType  string    `gorm:"type:varchar(50)" json:"collaboration_type"`
	RelatedFiles       string    `gorm:"type:text" json:"related_files"`
	RepoURL            string    `gorm:"type:varchar(255)" json:"repo_url"`
	CustomCreatedAt    time.Time `gorm:"type:timestamp with time zone" json:"created_at"`
	UserID             uint      `gorm:"not null;index" json:"user_id"`

	CategoryID uint     `gorm:"not null;index" json:"-"`
	Category   Category `gorm:"foreignKey:CategoryID" json:"category"`

	ContactID uint    `gorm:"not null;index" json:"-"`
	Contact   Contact `gorm:"foreignKey:ContactID" json:"contact_info"`
}

func (i *IdeaPost) MarshalJSON() ([]byte, error) {
	type Alias IdeaPost
	return json.Marshal(&struct {
		*Alias
		CreatedAt string `json:"created_at"`
	}{
		Alias:     (*Alias)(i),
		CreatedAt: i.CustomCreatedAt.Format(time.RFC3339),
	})
}

func (IdeaPost) TableName() string {
	return "idea_idea"
}
