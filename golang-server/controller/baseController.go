package controller

import (
	"context"
	"encoding/json"
	"fmt"
	"go-server/config"
	"net/http"
	"time"

	"github.com/gofiber/fiber/v2"
)

func GetCategroyController(c *fiber.Ctx) error {
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

	var data []map[string]interface{ any }
	for rows.Next() {
		var id int
		var title string
		if err := rows.Scan(&id, &title); err != nil {
			return c.Status(http.StatusInternalServerError).JSON(fiber.Map{"error": "Error in processing category data"})
		}
		data = append(data, map[string]interface{ any }{"id": id, "title": title})
	}

	jsonData, err := json.Marshal(data)
	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(fiber.Map{"error": "Error in convert category Data to JSON"})
	}

	err = config.RedisClient.Set(ctx, "category", jsonData, 24*time.Hour).Err()
	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(fiber.Map{"error": "Error in save category data to Redis"})
	}
	fmt.Println("Category from database", data)

	return c.JSON(data)
}
