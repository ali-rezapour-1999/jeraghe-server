package service

import (
	"go-server/config"
	"go-server/middleware"
	"go-server/models"
	"net/http"

	"github.com/gofiber/fiber/v2"
)

func GetContactUserSerivce(c *fiber.Ctx) error {
	validate, userID, err := middleware.IsAuthenticated(c)
	if !validate || err != nil {
		return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{"error": "Unauthorized"})
	}

	query := `
		SELECT id, user_id, slug_id, is_active, platform, link, is_verified
		FROM base_contact
		WHERE is_verified = true AND is_active = true AND user_id = $1
	`

	rows, err := config.DB.Query(query, userID)
	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(fiber.Map{
			"error": "Error fetching contacts from database",
		})
	}
	defer rows.Close()

	var contacts []models.Contact
	for rows.Next() {
		var contact models.Contact
		err := rows.Scan(
			&contact.ID,
			&contact.UserID,
			&contact.SlugID,
			&contact.IsActive,
			&contact.Platform,
			&contact.Link,
			&contact.IsVerified,
		)
		if err != nil {
			return c.Status(http.StatusInternalServerError).JSON(fiber.Map{
				"error": "Error scanning contact data",
			})
		}
		contacts = append(contacts, contact)
	}

	return c.Status(http.StatusOK).JSON(contacts)
}
