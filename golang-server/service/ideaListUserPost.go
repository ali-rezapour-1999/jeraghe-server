package service

import (
	"go-server/config"
	"go-server/middleware"
	"go-server/models"
	"net/http"

	"github.com/gofiber/fiber/v2"
)

func GetUserIdeaListService(c *fiber.Ctx) error {
	validate, userID, err := middleware.IsAuthenticated(c)
	if !validate || err != nil {
		return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{"error": "Unauthorized"})
	}

	query := `
SELECT ii.id,
       ii.title,
       ii.slug_id,
       ii.is_active,
       ii.image,
       ii.description,
       ii.status,
       ii.needs_collaborators,
       ii.collaboration_type,
       ii.related_files,
       ii.repo_url,
       ii.created_at,
       bc.title,
       bc2.link,
       bc2.platform
	FROM idea_idea ii
         left join public.base_category bc on ii.category_id = bc.id
         left join public.base_contact bc2 on ii.contact_info_id = bc2.id
	WHERE ii.is_active = true
  	AND ii.user_id = $1
	`

	rows, err := config.DB.Query(query, userID)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"status":  "error",
			"message": "خطا در دریافت اطلاعات ایده از پایگاه داده",
			"details": err.Error(),
		})
	}

	var ideaPost []models.IdeaPost
	for rows.Next() {
		var idea models.IdeaPost
		err := rows.Scan(
			&idea.ID,
			&idea.Title,
			&idea.SlugID,
			&idea.IsActive,
			&idea.Image,
			&idea.Description,
			&idea.Status,
			&idea.NeedsCollaborators,
			&idea.CollaborationType,
			&idea.RelatedFiles,
			&idea.RepoURL,
			&idea.CreatedAt,
			&idea.Category.Title,
			&idea.ContactInfo.Link,
			&idea.ContactInfo.Platform,
		)
		if err != nil {
			return c.Status(http.StatusInternalServerError).JSON(fiber.Map{
				"error": "Error scanning contact data",
			})
		}
		ideaPost = append(ideaPost, idea)
	}

	return c.Status(http.StatusOK).JSON(ideaPost)
}
