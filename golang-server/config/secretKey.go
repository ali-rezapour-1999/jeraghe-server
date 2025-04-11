package config

import (
	"github.com/gofiber/fiber/v2/log"
	"github.com/joho/godotenv"
	"os"
)

func SecretKeyLoader() string {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("❌ Error loading .env file")
		return ""
	}
	secret := os.Getenv("JWT_SECRET")
	if secret == "" {
		log.Fatal("❌ JWT_SECRET is empty")
		return ""
	}
	return secret
}
