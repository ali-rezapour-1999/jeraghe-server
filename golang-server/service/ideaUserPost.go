package service

import (
	"go-server/config"
	"go-server/middleware"
	"go-server/models"

	"github.com/gofiber/fiber/v2"
)

func GetIdeaUserService(c *fiber.Ctx) error {
	authenticated, userID, err := middleware.IsAuthenticated(c)
	if !authenticated || err != nil {
		return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
			"status":  "error",
			"message": "احراز هویت ناموفق بود",
		})
	}

	var body models.IdeaPost
	if err := c.BodyParser(&body); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"status":  "error",
			"message": "خطا در تجزیه بدنه درخواست: " + err.Error(),
		})
	}

	if body.ID == 0 {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"status":  "error",
			"message": "شناسه ایده نامعتبر است",
		})
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
	WHERE  user_id = $2  and ii.id = $1
	`
	rows, err := config.DB.Query(query, body.ID, userID)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"status":  "error",
			"message": "خطا در دریافت اطلاعات ایده از پایگاه داده",
			"details": err.Error(),
		})
	}
	rows.Close()
	var ideaPosts []models.IdeaPost
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
			return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
				"status":  "error",
				"message": "خطا در خواندن داده‌های ایده",
			})
		}
		ideaPosts = append(ideaPosts, idea)
	}

	if err := rows.Err(); err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"status":  "error",
			"message": "خطا در پردازش نتایج پایگاه داده",
			"details": err.Error(),
		})
	}

	return c.Status(fiber.StatusOK).JSON(ideaPosts)
}
