package middleware

import (
	"context"
	"fmt"
	"go-server/config"
	"net/http"
	"regexp"
	"slices"
	"strings"

	"github.com/gofiber/fiber/v2"
	"github.com/golang-jwt/jwt/v5"
	"gorm.io/gorm"
)

type ProtectionRule struct {
	PathPattern     *regexp.Regexp
	ExcludedMethods []string
	RequiresAuth    bool
}

func DBMiddleware(db *gorm.DB) fiber.Handler {
	return func(c *fiber.Ctx) error {
		c.Locals("db", db)
		return c.Next()
	}
}

func ConditionalAuth(rules []ProtectionRule) fiber.Handler {
	return func(c *fiber.Ctx) error {
		path := c.Path()
		method := c.Method()

		for _, rule := range rules {
			if rule.PathPattern.MatchString(path) {
				if slices.Contains(rule.ExcludedMethods, method) {
					return c.Next()
				}
				if rule.RequiresAuth {
					return JWTMiddleware(c)
				}
				break
			}
		}
		return c.Next()
	}
}

type AuthError struct {
	Message string
	Code    int
}

func (e *AuthError) Error() string {
	return e.Message
}

func IsAuthenticated(c *fiber.Ctx) (bool, string, error) {
	token := strings.TrimPrefix(c.Get("Authorization"), "Bearer ")
	token = strings.TrimSpace(token)
	if token == "" {
		return false, "", &AuthError{Message: "توکن مورد نیاز است", Code: http.StatusUnauthorized}
	}

	userID, err := ParseUserIDFromToken(token)
	if err != nil {
		return false, "", &AuthError{Message: err.Error(), Code: http.StatusUnauthorized}
	}
	if userID == "" {
		return false, "", &AuthError{Message: "توکن نامعتبر یا غیرمجاز است", Code: http.StatusUnauthorized}
	}
	return true, userID, nil
}

func ParseUserIDFromToken(tokenString string) (string, error) {
	if tokenString == "" {
		return "", fmt.Errorf("توکن خالی است")
	}
	secret := config.SecretKeyLoader()

	token, err := jwt.Parse(tokenString, func(token *jwt.Token) (any, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("روش امضای غیرمنتظره: %v", token.Header["alg"])
		}
		return []byte(secret), nil
	})
	if err != nil {
		return "", fmt.Errorf("خطا در تجزیه توکن: %v", err)
	}

	if !token.Valid {
		return "", fmt.Errorf("توکن نامعتبر است")
	}

	claims, ok := token.Claims.(jwt.MapClaims)
	if !ok {
		return "", fmt.Errorf("ادعاهای توکن نامعتبر است")
	}

	if userID, ok := claims["user_id"].(float64); ok {
		return fmt.Sprintf("%.0f", userID), nil
	}
	if sub, ok := claims["sub"].(string); ok {
		return sub, nil
	}

	return "", fmt.Errorf("شناسه کاربر در توکن یافت نشد")
}

func JWTMiddleware(c *fiber.Ctx) error {
	authenticated, id, err := IsAuthenticated(c)
	if err != nil {
		db, ok := c.Locals("db").(*gorm.DB)
		if ok && db != nil {
			LogSystemError(db, err, fmt.Sprintf("Authentication failed for %s %s", c.Method(), c.Path()))
		} else if !ok || db == nil {
			db.Logger.Error(context.Background(), "Database connection not available for logging authentication error: %v", err)
		}

		if authErr, ok := err.(*AuthError); ok {
			return c.Status(authErr.Code).JSON(fiber.Map{
				"status":  "error",
				"message": authErr.Message,
			})
		}
		return c.Status(http.StatusUnauthorized).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	if !authenticated || id == "" {
		return c.Status(http.StatusUnauthorized).JSON(fiber.Map{
			"status":  "error",
			"message": "توکن نامعتبر است",
		})
	}

	c.Locals("user_id", id)
	return c.Next()
}
