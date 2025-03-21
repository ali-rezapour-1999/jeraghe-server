package routes

import (
	"fmt"
	"go-server/middleware"
	"go-server/utils"
	"strings"

	"github.com/gofiber/fiber/v2"
)

func GetListPost(c *fiber.Ctx) error {
	data, err := utils.FetchFromDjango("blog", "posts", "")
	if err != nil {
		fmt.Println("Error fetching from Django =>get blog post list", err)
		return fiber.NewError(fiber.ErrBadRequest.Code, "Error fetching blog post list")
	}
	return c.JSON(data)
}

func GetUserPost(c *fiber.Ctx) error {
	authHeader := c.Get("Authorization")
	token := strings.TrimPrefix(authHeader, "Bearer ")
	userId := c.Params("id")

	verify, err := middleware.IsAuthontication(token)
	if verify && err == nil {
		data, err := utils.FetchFromDjango("blog", "posts"+"/"+userId, token)
		if err != nil {
			fmt.Println("Error fetching from Django => user blog post", err)
			return fiber.NewError(fiber.ErrBadRequest.Code, "Error fetching user blog post")
		}
		return c.JSON(data)
	}
	return fiber.NewError(fiber.StatusUnauthorized, "Error : you need Authorization")
}

func PostRoutes(app *fiber.App) {
	api := app.Group("/post/")
	api.Get("/list", GetListPost)
	api.Get("/user-post", GetUserPost)
}
