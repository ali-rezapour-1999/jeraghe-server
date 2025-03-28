package routes

import (
	"fmt"
	"go-server/utils"

	"github.com/gofiber/fiber/v2"
)

func GetCategoryList(c *fiber.Ctx) error {
	token := ""
	data, err := utils.FetchFromDjango("base/", "category/", token, true)
	if err != nil {
		fmt.Println("Error fetching from Django => base/category", err)
		return fiber.NewError(fiber.ErrBadRequest.Code, "Error درخواست دیتا با خطا مواجه شده")
	}
	fmt.Println("get base/catgory")
	return c.JSON(data)
}

func BaseRoutes(app *fiber.App) {
	api := app.Group("/base")
	api.Get("/category", GetCategoryList)
}
