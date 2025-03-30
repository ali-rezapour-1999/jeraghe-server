package middleware

import (
	"context"
	"fmt"
	"go-server/config"
	"net/http"
	"strings"
	"time"

	"github.com/gofiber/fiber/v2"
)

const (
	tokenCacheDuration = 1 * time.Hour
	authServiceURL     = "http://django:8000/api/auth/token-verify/"
)

type AuthError struct {
	Message string
	Code    int
}

func (e *AuthError) Error() string {
	return e.Message
}

func IsAuthenticated(token string) (bool, error) {
	if token == "" {
		return false, &AuthError{Message: "Token is required", Code: http.StatusUnauthorized}
	}

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	redisClient := config.RedisClient
	if redisClient != nil {
		exists, err := redisClient.Exists(ctx, token).Result()
		if err == nil && exists == 1 {
			return true, nil
		}
	}

	req, err := http.NewRequestWithContext(ctx, "POST", authServiceURL, nil)
	if err != nil {
		return false, fmt.Errorf("failed to create auth request: %v", err)
	}
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{Timeout: 10 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		return false, fmt.Errorf("auth service error: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return false, &AuthError{Message: "Invalid token", Code: resp.StatusCode}
	}

	if redisClient != nil {
		if err := redisClient.Set(ctx, token, "valid", tokenCacheDuration).Err(); err != nil {
			fmt.Printf("Warning: failed to cache token: %v\n", err)
		}
	}

	return true, nil
}

func JWTMiddleware(c *fiber.Ctx) error {
	token := strings.TrimPrefix(c.Get("Authorization"), "Bearer ")
	token = strings.TrimSpace(token)

	authenticated, err := IsAuthenticated(token)
	if err != nil {
		if authErr, ok := err.(*AuthError); ok {
			return c.Status(authErr.Code).JSON(fiber.Map{
				"error": authErr.Message,
			})
		}
		return c.Status(http.StatusUnauthorized).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	if !authenticated {
		return c.Status(http.StatusUnauthorized).JSON(fiber.Map{
			"error": "Invalid token",
		})
	}

	return c.Next()
}

func SetupMiddleware(app *fiber.App) {
	app.Use(func(c *fiber.Ctx) error {
		privateRoutes := []string{
			"/api/private/auth/get/",
			"/api/private/profile/",
		}
		for _, route := range privateRoutes {
			if strings.HasPrefix(c.Path(), route) {
				return JWTMiddleware(c)
			}
		}
		if strings.HasPrefix(c.Path(), "/api") {
			return c.Next()
		}
		return c.Next()
	})
}
