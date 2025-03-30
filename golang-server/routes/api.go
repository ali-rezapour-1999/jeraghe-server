package routes

import (
	"go-server/controller"
	"go-server/proxys"

	"github.com/gofiber/fiber/v2"
)

func SetupRoutes(app *fiber.App) {
	public := app.Group("/api/public")
	// protected := app.Group("/api/protected") // Fixed typo

	public.Get("/category/", controller.GetCategroyController)

	app.All("/api/*", proxys.ProxyToDjango)
}
