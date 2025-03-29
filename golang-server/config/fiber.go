package config

import (
	"time"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
	"github.com/gofiber/fiber/v2/middleware/limiter"
)

func SetupFiber() *fiber.App {
	app := fiber.New(fiber.Config{
		Prefork:       false,
		CaseSensitive: true,
		StrictRouting: true,
	})

	app.Use(limiter.New(limiter.Config{
		Max:        50,
		Expiration: 1 * time.Minute,
		KeyGenerator: func(c *fiber.Ctx) string {
			return c.IP()
		},
	}))

	app.Use(cors.New(cors.Config{
		AllowOrigins:     "http://localhost:8000,http://127.0.0.1:8000,http://django:8000",
		AllowHeaders:     "Authorization,Content-Type,X-Csrf-Token,x-csrftoken",
		AllowMethods:     "GET,POST,PUT,DELETE",
		AllowCredentials: true,
		ExposeHeaders:    "X-Csrf-Token,x-csrftoken",
	}))

	return app
}
