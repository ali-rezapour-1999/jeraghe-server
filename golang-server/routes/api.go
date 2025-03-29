package routes

import (
	"fmt"
	"go-server/controller"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/proxy"
)

func ProxyToDjango(c *fiber.Ctx) error {
	djangoAPI := "http://127.0.0.1:8000"
	url := fmt.Sprintf("%s%s", djangoAPI, c.OriginalURL())
	fmt.Println("Proxying to:", url)

	c.Request().Header.Set("Content-Type", "application/json")
	c.Request().Header.Set("User-Agent", "Fiber-Gateway")
	c.Request().Header.Set("Referer", "http://127.0.0.1:8080")

	if c.Method() == "POST" {
	}

	if err := proxy.Do(c, url); err != nil {
		fmt.Println("Proxy error:", err)
		return fiber.NewError(fiber.StatusBadGateway, "proxy error")
	}

	response := c.Response()
	fmt.Printf("Django response - Status: %d, Body: %s\n", response.StatusCode(), string(response.Body()))
	if response.StatusCode() >= 400 {
		errorMessage := string(response.Body())
		if errorMessage == "" {
			errorMessage = fmt.Sprintf("Django returned status code %d", response.StatusCode())
		}
		return fiber.NewError(response.StatusCode(), errorMessage)
	}

	return nil
}

func SetupRoutes(app *fiber.App) {
	public := app.Group("/api/public")
	// protected := app.Group("/api/protected") // Fixed typo

	public.Get("/category/", controller.GetCategroyController)
	app.All("/api/*", ProxyToDjango)
}
