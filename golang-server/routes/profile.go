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
	userId := c.Params("id")

	verify, err := middleware.IsAuthontication(token)
	if verify && err == nil {
		data, err := utils.FetchFromDjango("profile", "profile-info"+"/"+userId, token)
		if err != nil {
			fmt.Println("Error fetching from Django => profile", err)
			return fiber.NewError(fiber.ErrBadRequest.Code, "Error fetching users")
		}
		fmt.Println("get Profile info")
		return c.JSON(data)
	}
	return fiber.NewError(fiber.StatusUnauthorized, "Error : you need Authorization")
}

func GetSocialMedia(c *fiber.Ctx) error {
	authHeader := c.Get("Authorization")
	token := strings.TrimPrefix(authHeader, "Bearer ")

	verify, err := middleware.IsAuthontication(token)
	if verify && err == nil {
		data, err := utils.FetchFromDjango("profile", "social-media", token)
		if err != nil {
			fmt.Println("Error fetching from Django => social-media:", err)
			return fiber.NewError(fiber.ErrBadRequest.Code, "Error fetching users")
		}
		fmt.Println("get Profile social-media")
		return c.JSON(data)
	}
	return fiber.NewError(fiber.StatusUnauthorized, "Error : you need Authorization")
}

func GetWorkHistory(c *fiber.Ctx) error {
	authHeader := c.Get("Authorization")
	token := strings.TrimPrefix(authHeader, "Bearer ")

	verify, err := middleware.IsAuthontication(token)
	if verify && err == nil {
		data, err := utils.FetchFromDjango("profile", "work-histroy", token)
		if err != nil {
			fmt.Println("Error fetching from Django => work-histroy:", err)
			return fiber.NewError(fiber.ErrBadRequest.Code, "Error fetching users")
		}
		return c.JSON(data)
	}
	return fiber.NewError(fiber.StatusUnauthorized, "Error : you need Authorization")
}

func GetUserSkills(c *fiber.Ctx) error {
	authHeader := c.Get("Authorization")
	token := strings.TrimPrefix(authHeader, "Bearer ")

	verify, err := middleware.IsAuthontication(token)
	if verify && err == nil {
		data, err := utils.FetchFromDjango("profile", "user-skills", token)
		if err != nil {
			fmt.Println("Error fetching from Django => user-skills:", err)
			return fiber.NewError(fiber.ErrBadGateway.Code, "Error fetching users")
		}
		return c.JSON(data)
	}
	fmt.Println("request profile ", err)
	return fiber.NewError(fiber.StatusUnauthorized, "Error : you need Authorization")
}

func ProfileUserRoutes(app *fiber.App) {
	api := app.Group("/profile/")
	api.Get("/info/:id", GetProfile)
	api.Get("/social-media", GetSocialMedia)
	api.Get("/work-histroy", GetWorkHistory)
	api.Get("/user-skills", GetUserSkills)
}
