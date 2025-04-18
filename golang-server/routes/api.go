package routes

import (
	"go-server/config"
	"go-server/middleware"
	"go-server/proxys"

	"github.com/gofiber/fiber/v2"
)

type Route struct {
	Path         string
	Method       string
	Handler      fiber.Handler
	RequiresAuth bool
}

type ProtectionRule = middleware.ProtectionRule

func SetupRoutes(app *fiber.App, db *config.TrackedDB) {
	app.Use(middleware.DBMiddleware(db))

	protectionRules := getProtectionRules()

	Group := app.Group("/api/public")
	registerRoutes(Group, Router)

	app.All("/api/private/*", middleware.ConditionalAuth(protectionRules), proxys.ProxyToDjango(db))
}
