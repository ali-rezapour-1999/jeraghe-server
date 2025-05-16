package service

import (
	"context"
	"errors"
	"go-server/middleware"
	"go-server/models"
	"net/http"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func GetProfileSkill(c *fiber.Ctx) error {
	db, ok := c.Locals("db").(*gorm.DB)
	if !ok || db == nil {
		middleware.LogSystemError(db, nil, "Database connection unavailable in GetProfileSkill")
		return fiber.NewError(http.StatusInternalServerError, "خطا در دریافت داده‌های پروفایل از پایگاه داده")
	}

	ctx := context.Background()

	authenticated, userID, err := middleware.IsAuthenticated(c)
	if !authenticated || err != nil {
		return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
			"status":  "error",
			"message": "احراز هویت ناموفق بود",
			"data":    nil,
			"error":   err.Error(),
		})
	}

	var profileSkill models.ProfileSkills
	if err := db.WithContext(ctx).
		Where("user_id = ?", userID).
		First(&profileSkill).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return c.JSON(fiber.Map{
				"status": "success",
				"data":   nil,
			})
		}
		middleware.LogSystemError(db, err, "Failed to fetch profile skills from database")
		return fiber.NewError(http.StatusInternalServerError, "خطا در دریافت داده‌های پروفایل از پایگاه داده")
	}

	return c.Status(fiber.StatusOK).JSON(fiber.Map{
		"status":  "success",
		"message": "اطلاعات پروفایل با موفقیت دریافت شد",
		"data":    profileSkill,
	})
}
