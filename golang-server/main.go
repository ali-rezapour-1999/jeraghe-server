package main

import (
	"fmt"
	"go-server/config"
	"go-server/middleware"
	"go-server/routes"
	"log"

	"github.com/gofiber/fiber/v2/middleware/cors"
)

func main() {
	app := config.SetupFiber()
	redisClient := config.ConnectRedis()

	if redisClient == nil {
		log.Fatal("Cannot start server without Redis")
	}
	fmt.Println("Redis is up and running!")

	routes.ProfileUserRoutes(app)
	routes.PostRoutes(app)
	routes.BaseRoutes(app)

	app.Use(middleware.ErrorHandler)
	app.Use(cors.New())
	app.Use(cors.New(cors.Config{
		AllowOrigins: "http://localhost:8000, http://localhost:3000 , http://127.0.0.1:8000 , http://127.0.0.1:3000",
		AllowHeaders: "Authorization ,Origin, Content-Type, Accept",
	}))

	port := ":8080"
	fmt.Println("Server is running on port", port)
	log.Fatal(app.Listen(port))
}
