package main

import (
	"fmt"
	"go-server/config"
	"go-server/middleware"
	"go-server/routes"
	"log"
	"os"
)

func main() {
	app := config.SetupFiber()
	redisClient := config.ConnectRedis()
	if redisClient == nil {
		middleware.LogError(nil, fmt.Errorf("Cannot start server without Redis"), nil)
		log.Fatal("Cannot start server without Redis")
	}
	fmt.Println("✅ Redis is up and running!")

	db := config.ConnectPostgres()
	if db == nil {
		middleware.LogError(nil, fmt.Errorf("Cannot start server without PostgreSQL"), nil)
		log.Fatal("Cannot start server without PostgresSQL")
	}
	defer db.Close()
	fmt.Println("✅ PostgresSQL is up and running!")
	secret := config.SecretKeyLoader()
	if secret != "" {
		fmt.Println("✅ Env file loaded!")
	}
	routes.SetupRoutes(app, db)
	middleware.SetupErrorMiddleware(app, db)
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	fmt.Printf("🚀 Server is running on :%s\n", port)
	log.Fatal(app.Listen(":" + port))
}
