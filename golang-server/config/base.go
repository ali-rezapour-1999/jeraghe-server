package config

import (
	"os"

	"github.com/gofiber/fiber/v2/log"
	"github.com/joho/godotenv"
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

func GetEnvOrDefault(key, defaultValue string) string {
	value := os.Getenv(key)
	if value == "" {
		return defaultValue
	}
	return value
}
