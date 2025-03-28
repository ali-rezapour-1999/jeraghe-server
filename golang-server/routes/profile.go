package routes

import (
	"fmt"
	"go-server/middleware"
	"go-server/utils"
	"strings"

	"github.com/gofiber/fiber/v2"
)

func GetProfile(c *fiber.Ctx) error {
	authHeader := c.Get("Authorization")
	token := strings.TrimPrefix(authHeader, "Bearer ")
	verify, err := middleware.IsAuthontication(token)
	if verify && err == nil {
		data, err := utils.FetchFromDjango("profile/", "get/", token, true)
		if err != nil {
			fmt.Println("Error fetching from Django => profile", err)
			return fiber.NewError(fiber.ErrBadRequest.Code, "Error درخواست دیتا با خطا مواجه شده")
		}
		fmt.Println("get Profile info")
		return c.JSON(data)
	}
	return fiber.NewError(fiber.StatusUnauthorized, "Error : نیاز به احراض هویت داری")
}

func GetSocilaMedia(c *fiber.Ctx) error {
	authHeader := c.Get("Authorization")
	token := strings.TrimPrefix(authHeader, "Bearer ")
	verify, err := middleware.IsAuthontication(token)
	if verify && err == nil {
		data, err := utils.FetchFromDjango("profile/", "social-media/", token, true)
		if err != nil {
			fmt.Println("Error fetching from Django => profile", err)
			return fiber.NewError(fiber.ErrBadRequest.Code, "Error درخواست دیتا با خطا مواجه شده")
		}
		fmt.Println("get Profile info")
		return c.JSON(data)
	}
	return fiber.NewError(fiber.StatusUnauthorized, "Error : نیاز به احراض هویت داری")
}

func GetWorkHistory(c *fiber.Ctx) error {
	authHeader := c.Get("Authorization")
	token := strings.TrimPrefix(authHeader, "Bearer ")
	verify, err := middleware.IsAuthontication(token)
	if verify && err == nil {
		data, err := utils.FetchFromDjango("profile/", "work-history/", token, true)
		if err != nil {
			fmt.Println("Error fetching from Django => profile", err)
			return fiber.NewError(fiber.ErrBadRequest.Code, "Error درخواست دیتا با خطا مواجه شده")
		}
		fmt.Println("get Profile info")
		return c.JSON(data)
	}
	return fiber.NewError(fiber.StatusUnauthorized, "Error : نیاز به احراض هویت داری")
}
func GetUserSkill(c *fiber.Ctx) error {
	authHeader := c.Get("Authorization")
	token := strings.TrimPrefix(authHeader, "Bearer ")
	verify, err := middleware.IsAuthontication(token)
	if verify && err == nil {
		data, err := utils.FetchFromDjango("profile/", "user-skill/", token, true)
		if err != nil {
			fmt.Println("Error fetching from Django => profile", err)
			return fiber.NewError(fiber.ErrBadRequest.Code, "Error درخواست دیتا با خطا مواجه شده")
		}
		fmt.Println("get Profile info")
		return c.JSON(data)
	}
	return fiber.NewError(fiber.StatusUnauthorized, "Error : نیاز به احراض هویت داری")
}

func ProfileUserRoutes(app *fiber.App) {
	api := app.Group("/profile")
	api.Get("/get", GetProfile)
	api.Get("/social-media", GetSocilaMedia)
	api.Get("/work-history", GetWorkHistory)
	api.Get("/user-skill", GetUserSkill)
}
