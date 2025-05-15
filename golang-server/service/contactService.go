package service

import (
	"context"
	"go-server/middleware"
	"go-server/models"
	"net/http"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func GetContactUserService(c *fiber.Ctx) error {
	db, ok := c.Locals("db").(*gorm.DB)
	if !ok || db == nil {
		middleware.LogSystemError(db, nil, "Database connection unavailable in GetContactUserService")
		return fiber.NewError(http.StatusInternalServerError, "خطا در دریافت داده‌های ارتباط از پایگاه داده")
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

	var contacts []models.Contact
	if err := db.WithContext(ctx).Where("is_verified = ? AND is_active = ? AND user_id = ?", true, true, userID).Find(&contacts).Error; err != nil {
		middleware.LogSystemError(db, err, "Failed to fetch contacts from database")
		return fiber.NewError(http.StatusInternalServerError, "خطا در دریافت داده‌های ارتباط از پایگاه داده")
	}

	return c.Status(fiber.StatusOK).JSON(fiber.Map{
		"status":  "success",
		"message": "اطلاعات ایده با موفقیت دریافت شد",
		"data":    contacts,
	})
}
