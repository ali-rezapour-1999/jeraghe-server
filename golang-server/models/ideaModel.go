package models

type IdeaPost struct {
	ID                 int    `json:"id"`
	SlugID             string `json:"slug_id"`
	IsActive           bool   `json:"is_active"`
	Title              string `json:"title"`
	Image              string `json:"image"`
	Description        string `json:"description"`
	Status             string `json:"status"`
	NeedsCollaborators bool   `json:"needs_collaborators"`
	CollaborationType  string `json:"collaboration_type"`
	RelatedFiles       string `json:"related_files"`
	RepoURL            string `json:"repo_url"`
	CreatedAt          string `json:"created_at"`
	UserID             int    `json:"user_id"`

	Category    Category `json:"category"`
	ContactInfo Contact  `json:"contact_info"`
}
