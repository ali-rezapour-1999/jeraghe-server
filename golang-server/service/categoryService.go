package service

import (
	"context"
	"encoding/json"
	"go-server/config"
	"go-server/middleware"
	"go-server/models"
	"net/http"
	"time"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func GetCategoryService(c *fiber.Ctx) error {
	db, ok := c.Locals("db").(*gorm.DB)
	if !ok || db == nil {
		err := fiber.NewError(http.StatusInternalServerError, "Database connection unavailable")
		middleware.LogSystemError(db, err, "Database connection unavailable in GetCategoryService")
		return err
	}

	ctx := context.Background()

	category, err := config.RedisClient.Get(ctx, "category").Result()
	if err == nil {
		var cachedData []models.Category
		if err := json.Unmarshal([]byte(category), &cachedData); err == nil {
			db.Logger.Info(ctx, "Retrieved categories from Redis: %d items", len(cachedData))
			return c.Status(fiber.StatusOK).JSON(fiber.Map{
				"status":  "success",
				"message": "اطلاعات دسته‌بندی با موفقیت دریافت شد",
				"data":    cachedData,
			})
		}
		db.Logger.Warn(ctx, "Failed to unmarshal Redis category data: %v", err)
	}

	var categories []models.Category
	if err := db.Find(&categories).Error; err != nil {
		middleware.LogSystemError(db, err, "Failed to fetch categories from database")
		return fiber.NewError(http.StatusInternalServerError, "خطا در دریافت داده‌های دسته‌بندی از پایگاه داده")
	}

	jsonData, err := json.Marshal(categories)
	if err != nil {
		middleware.LogSystemError(db, err, "Failed to marshal categories to JSON")
		return fiber.NewError(http.StatusInternalServerError, "خطا در تبدیل داده‌های دسته‌بندی به JSON")
	}

	if err := config.RedisClient.Set(ctx, "category", jsonData, 24*time.Hour).Err(); err != nil {
		db.Logger.Warn(ctx, "Failed to save categories to Redis: %v", err)
	}

	return c.Status(fiber.StatusOK).JSON(fiber.Map{
		"status":  "success",
		"message": "اطلاعات دسته‌بندی با موفقیت دریافت شد",
		"data":    categories,
	})
}
