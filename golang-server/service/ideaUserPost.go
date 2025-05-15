package service

import (
	"context"
	"go-server/middleware"
	"go-server/models"
	"net/http"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func GetIdeaUserService(c *fiber.Ctx) error {
	db, ok := c.Locals("db").(*gorm.DB)
	if !ok || db == nil {
		middleware.LogSystemError(db, nil, "Database connection unavailable in GetIdeaUserService")
		return fiber.NewError(http.StatusInternalServerError, "خطا در دریافت داده‌های ایده از پایگاه داده")
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

	var body models.IdeaPost
	if err := c.BodyParser(&body); err != nil {
		middleware.LogSystemError(db, err, "Failed to parse request body in GetIdeaUserService")
		return fiber.NewError(http.StatusInternalServerError, "خطا در تبدیل داده‌های درخواست به JSON")
	}

	if body.ID == 0 {
		middleware.LogSystemError(db, nil, "Invalid idea ID in GetIdeaUserService")
		return fiber.NewError(http.StatusBadRequest, "شناسه ایده نامعتبر است")
	}

	var idea models.IdeaPost
	if err := db.WithContext(ctx).
		Preload("Category").
		Preload("Contact").
		Where("id = ? AND user_id = ?", body.ID, userID).
		First(&idea).Error; err != nil {
		middleware.LogSystemError(db, err, "Failed to fetch idea from database")
		return fiber.NewError(http.StatusInternalServerError, "خطا در دریافت داده‌های ایده از پایگاه داده")
	}

	return c.Status(fiber.StatusOK).JSON(fiber.Map{
		"status":  "success",
		"message": "اطلاعات ایده با موفقیت دریافت شد",
		"data":    idea,
	})
}
