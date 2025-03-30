package routes

import (
	"database/sql"
	"go-server/controller"
	"go-server/proxys"

	"github.com/gofiber/fiber/v2"
)

func SetupRoutes(app *fiber.App, db *sql.DB) {
	public := app.Group("/api/public")

	public.Get("/category/", controller.GetCategroyController)

	app.All("/api/private/*", proxys.ProxyToDjango(db))
}
