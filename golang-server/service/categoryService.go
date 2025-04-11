package service

import (
	"context"
	"encoding/json"
	"fmt"
	"go-server/config"
	"go-server/models"
	"net/http"
	"time"

	"github.com/gofiber/fiber/v2"
)

func GetCategroyService(c *fiber.Ctx) error {
	ctx := context.Background()

	category, err := config.RedisClient.Get(ctx, "category").Result()
	if err == nil {
		var cachedData []map[string]interface{ any }
		if json.Unmarshal([]byte(category), &cachedData) == nil {
			fmt.Println("Category from redis", cachedData)
			return c.JSON(cachedData)
		}
	}

	rows, err := config.DB.Query("SELECT id, title FROM base_category")
	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(fiber.Map{"error": "Error Failed get category data from database with query"})
	}
	defer rows.Close()

	var categoreis []models.Category
	for rows.Next() {
		var category models.Category
		err := rows.Scan(
			&category.ID,
			&category.Title,
		)
		if err != nil {
			return c.Status(http.StatusInternalServerError).JSON(fiber.Map{
				"error": "Error scanning contact data",
			})
		}
		categoreis = append(categoreis, category)
	}
	jsonData, err := json.Marshal(categoreis)
	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(fiber.Map{"error": "Error in convert category Data to JSON"})
	}

	err = config.RedisClient.Set(ctx, "category", jsonData, 24*time.Hour).Err()
	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(fiber.Map{"error": "Error in save category data to Redis"})
	}
	fmt.Println("Category from database", categoreis)

	return c.JSON(categoreis)
}
