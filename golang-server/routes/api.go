package routes

import (
	"go-server/middleware"
	"go-server/proxys"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

type Route struct {
	Path         string
	Method       string
	Handler      fiber.Handler
	RequiresAuth bool
}

type ProtectionRule = middleware.ProtectionRule

func SetupRoutes(app *fiber.App, db *gorm.DB) {
	app.Use(middleware.DBMiddleware(db))

	protectionRules := getProtectionRules()

	Group := app.Group("/api/public")
	registerRoutes(Group, Router)

	app.All("/api/private/*", middleware.ConditionalAuth(protectionRules), proxys.ProxyToDjango(db))
}
