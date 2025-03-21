package main

import (
	"fmt"
	"go-server/config"
	"go-server/middleware"
	"go-server/routes"
	"log"
	"os"
	"time"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
	"github.com/gofiber/fiber/v2/middleware/csrf"
	"github.com/gofiber/fiber/v2/middleware/limiter"
	"github.com/gofiber/fiber/v2/utils"
)

func main() {
	app := config.SetupFiber()
	redisClient := config.ConnectRedis()

	if redisClient == nil {
		log.Fatal("Cannot start server without Redis")
	}
	fmt.Println("Redis is up and running!")

	// router
	routes.ProfileUserRoutes(app)
	routes.PostRoutes(app)
	routes.BaseRoutes(app)

	app.Use(limiter.New())
	app.Use(limiter.New(limiter.Config{
		Max:        25,
		Expiration: 1 * time.Minute,
		KeyGenerator: func(c *fiber.Ctx) string {
			return c.IP()
		},
		LimitReached: func(c *fiber.Ctx) error {
			return c.SendStatus(fiber.StatusTooManyRequests)
		},
		SkipFailedRequests:     false,
		SkipSuccessfulRequests: true,
	}))

	app.Use(csrf.New(csrf.Config{
		KeyLookup:      "header:X-Csrf-Token",
		CookieName:     "csrf_",
		CookieSameSite: "Lax",
		Expiration:     1 * time.Hour,
		KeyGenerator:   utils.UUIDv4,
	}))

	allowOrigins := os.Getenv("CORS_ALLOW_ORIGINS")
	allowHeaders := os.Getenv("CORS_ALLOW_HEADERS")
	app.Use(cors.New(cors.Config{
		AllowOrigins: allowOrigins,
		AllowHeaders: allowHeaders,
	}))

	app.Use(middleware.ErrorHandler)

	port := ":8080"
	fmt.Println("Server is running on port", port)
	log.Fatal(app.Listen(port))
}
