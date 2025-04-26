package service

import (
	"github.com/gofiber/fiber/v2"
	"go-server/config"
	"go-server/middleware"
	"go-server/models"
)

func GetProfileData(c *fiber.Ctx) error {
	authenticated, userID, err := middleware.IsAuthenticated(c)
	if !authenticated || err != nil {
		return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
			"status":  "error",
			"message": "احراز هویت ناموفق بود",
			"data":    nil,
			"error":   err.Error(),
		})
	}

	query := `SELECT id , slug_id, gender, age, state, city, address, description FROM profiles_profile WHERE user_id = $1`
	rows, err := config.DB.Query(query, userID)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"status":  "error",
			"message": "خطا در دریافت اطلاعات پروفایل از پایگاه داده",
			"data":    nil,
			"error":   err.Error(),
		})
	}
	defer rows.Close()

	var profile models.Profile
	for rows.Next() {
		var profiles models.Profile
		err := rows.Scan(
			&profiles.ID,
			&profiles.SlugID,
			&profiles.Gender,
			&profiles.Age,
			&profiles.State,
			&profiles.City,
			&profiles.Address,
			&profiles.Description,
		)
		if err != nil {
			return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
				"status":  "error",
				"message": "خطا در خواندن داده‌های پروفایل",
				"data":    nil,
				"error":   err.Error(),
			})
		}
		profile = profiles
	}

	if err := rows.Err(); err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"status":  "error",
			"message": "خطا در پردازش نتایج پایگاه داده",
			"data":    nil,
			"error":   err.Error(),
		})
	}

	return c.Status(fiber.StatusOK).JSON(fiber.Map{
		"status":  "success",
		"message": "اطلاعات پروفایل با موفقیت دریافت شد",
		"data":    profile,
	})
}
