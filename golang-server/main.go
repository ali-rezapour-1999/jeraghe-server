package main

import (
	"fmt"
	"go-server/config"
	"go-server/middleware"
	"go-server/routes"
	"os"
)

const AppVersion = "1.0.0"

func main() {
	app := config.SetupFiber()
	middleware.LogStartupInfo(nil, fmt.Sprintf("Starting application v%s in %s environment", AppVersion, config.GetEnvOrDefault("ENV", "development")))

	redisClient := config.ConnectRedis()
	if redisClient == nil {
		middleware.LogStartupError(nil, nil, "Cannot start server without Redis")
	}
	middleware.LogStartupInfo(nil, "Redis is up and running!")

	gormDB := config.ConnectGORM()
	if gormDB == nil {
		middleware.LogStartupError(nil, nil, "Cannot start server without PostgreSQL")
	}
	middleware.LogStartupInfo(gormDB, "PostgreSQL with GORM is up and running!")

	secret := config.SecretKeyLoader()
	if secret != "" {
		middleware.LogStartupInfo(gormDB, "Environment variables loaded!")
	}

	routes.SetupRoutes(app, gormDB)
	app.Use(middleware.DBMiddleware(gormDB))
	middleware.SetupErrorMiddleware(app, gormDB)

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	middleware.LogStartupInfo(gormDB, fmt.Sprintf("Server is running on :%s", port))

	if err := app.Listen(":" + port); err != nil {
		middleware.LogStartupError(gormDB, err, "Failed to start server")
	}
}
