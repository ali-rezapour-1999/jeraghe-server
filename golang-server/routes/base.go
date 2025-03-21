package routes

import (
	"fmt"
	"go-server/utils"

	"github.com/gofiber/fiber/v2"
)

func GetCategoryList(c *fiber.Ctx) error {
	data, err := utils.FetchFromDjango("base", "categroy-list", "")
	if err != nil {
		fmt.Println("Error fetching from Django =>get blog post list", err)
		return fiber.NewError(fiber.ErrBadRequest.Code, "Error fetching blog post list")
	}
	fmt.Println("get Category List from Django")
	return c.JSON(data)
}

func BaseRoutes(app *fiber.App) {
	api := app.Group("/base/")
	api.Get("/category-list", GetCategoryList)
}
