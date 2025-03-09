package routes

import (
	"fmt"
	"go-server/utils"
	"strings"

	"github.com/gofiber/fiber/v2"
)

func GetProfile(c *fiber.Ctx) error {
	authHeader := c.Get("Authorization")
	token := strings.TrimPrefix(authHeader, "Bearer ")

	id := c.Params("id")
	data, err := utils.FetchFromDjango("profile", "profile-info"+"/"+id, token, id)
	if err != nil {
		fmt.Println("Error fetching from Django:", err)
		return fiber.NewError(fiber.StatusUnauthorized, "Error fetching users")
	}
	return c.JSON(data)
}

func ProfileUserRoutes(app *fiber.App) {
	api := app.Group("/profile-info/")
	api.Get("/:id", GetProfile)
}
