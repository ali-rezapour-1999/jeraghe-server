package routes

import (
	"database/sql"
	"go-server/proxys"
	"go-server/service"

	"github.com/gofiber/fiber/v2"
)

func SetupRoutes(app *fiber.App, db *sql.DB) {
	public := app.Group("/api/public")

	// base service
	public.Get("/category/", service.GetCategroyService)
	public.Get("/contact/", service.GetContactUserSerivce)

	app.All("/api/private/*", proxys.ProxyToDjango(db))
}
