package middleware

import (
	"fmt"
	"github.com/gofiber/fiber/v2"
	"github.com/golang-jwt/jwt/v5"
	"go-server/config"
	"net/http"
	"strings"
)

const (
	authServiceURL = "http://localhost:8080/api/private/auth/token-verify/"
)

type AuthError struct {
	Message string
	Code    int
}

func (e *AuthError) Error() string {
	return e.Message
}

func ParseUserIDFromToken(tokenString string) (string, error) {
	if tokenString == "" {
		return "", nil
	}
	secret := config.SecretKeyLoader()

	token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
		}
		return []byte(secret), nil
	})
	if err != nil {
		return "", fmt.Errorf("failed to parse token: %v", err)
	}

	if !token.Valid {
		return "", fmt.Errorf("invalid token")
	}

	claims, ok := token.Claims.(jwt.MapClaims)
	if !ok {
		return "", fmt.Errorf("invalid token claims")
	}

	if userID, ok := claims["user_id"].(float64); ok {
		return fmt.Sprintf("%.0f", userID), nil
	}

	return "", fmt.Errorf("user ID not found in token")
}

func IsAuthenticated(c *fiber.Ctx) (bool, string, error) {
	token := strings.TrimPrefix(c.Get("Authorization"), "Bearer ")
	token = strings.TrimSpace(token)
	if token == "" {
		return false, "", &AuthError{Message: "Token is required", Code: http.StatusUnauthorized}
	}

	userID, err := ParseUserIDFromToken(token)
	if err != nil {
		return false, "", &AuthError{Message: err.Error(), Code: http.StatusUnauthorized}
	}
	if userID == "" {
		return false, "", &AuthError{Message: "Invalid or unauthorized token", Code: http.StatusUnauthorized}
	}

	return true, userID, nil
}

func JWTMiddleware(c *fiber.Ctx) error {
	authenticated, id, err := IsAuthenticated(c)
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

	if !authenticated || id == "" {
		return c.Status(http.StatusUnauthorized).JSON(fiber.Map{
			"error": "Invalid token",
		})
	}

	c.Locals("user_id", id)
	return c.Next()
}

func SetupMiddleware(app *fiber.App) {
	app.Use(func(c *fiber.Ctx) error {
		privateRoutes := []string{
			"/api/private/auth/get/",
			"/api/public/contact/",
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
