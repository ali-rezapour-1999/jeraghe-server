package config

import (
	"github.com/gofiber/fiber/v2"
)

func SetupFiber() *fiber.App {
	app := fiber.New(fiber.Config{
		Prefork:       false,
		CaseSensitive: true,
		StrictRouting: true,
	})
	return app
}
