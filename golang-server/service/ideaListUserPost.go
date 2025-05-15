package service

import (
	"context"
	"go-server/middleware"
	"go-server/models"
	"net/http"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func GetUserIdeaListService(c *fiber.Ctx) error {
	db, ok := c.Locals("db").(*gorm.DB)
	if !ok || db == nil {
		middleware.LogSystemError(db, nil, "Database connection unavailable in GetUserIdeaListService")
		return fiber.NewError(http.StatusInternalServerError, "خطا در دریافت داده‌های ایده هام از پایگاه داده")
	}

	ctx := context.Background()

	authenticated, userID, err := middleware.IsAuthenticated(c)
	if !authenticated || err != nil {
		return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
			"status":  "error",
			"message": "احراز هویت ناموفق بود",
		})
	}

	var ideas []models.IdeaPost
	if err := db.WithContext(ctx).
		Preload("Category").
		Preload("Contact").
		Where("is_active = ? AND user_id = ?", true, userID).
		Find(&ideas).Error; err != nil {
		middleware.LogSystemError(db, err, "Failed to fetch ideas from database")
		return fiber.NewError(http.StatusInternalServerError, "خطا در دریافت داده‌های ایده هام از پایگاه داده")
	}

	return c.Status(fiber.StatusOK).JSON(fiber.Map{
		"status":  "success",
		"message": "اطلاعات ایده با موفقیت دریافت شد",
		"data":    ideas,
	})
}
