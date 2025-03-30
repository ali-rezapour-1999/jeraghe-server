package proxys

import (
	"database/sql"
	"fmt"
	"go-server/middleware"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/proxy"
)

func ProxyToDjango(db *sql.DB) fiber.Handler {
	return func(c *fiber.Ctx) error {
		djangoAPI := "http://127.0.0.1:8000"
		url := fmt.Sprintf("%s%s", djangoAPI, c.OriginalURL())
		fmt.Println("Proxying to:", url)

		c.Request().Header.Set("Content-Type", "application/json")
		c.Request().Header.Set("User-Agent", "Fiber-Gateway")
		c.Request().Header.Set("Referer", "http://127.0.0.1:8080")

		if err := proxy.Do(c, url); err != nil {
			fmt.Println("Proxy error:", err)
			return fiber.NewError(fiber.StatusBadGateway, fmt.Sprintf("Proxy error: %v", err))
		}

		statusCode := c.Response().StatusCode()
		responseBody := string(c.Response().Body())

		if statusCode >= 400 {
			fmt.Printf("error Body: %s\n", responseBody)

			trace := middleware.ExceptionTrace{
				Timestamp:    middleware.GetTimestamp(),
				Path:         c.Path(),
				Method:       c.Method(),
				StatusCode:   statusCode,
				ErrorMessage: responseBody,
				IPAddress:    c.IP(),
			}

			token := c.Get("Authorization")
			if userID, err := middleware.ParseUserIDFromToken(token); err == nil {
				trace.UserID = userID
			}

			go middleware.LogExceptionTrace(db, trace)

			return fiber.NewError(statusCode, responseBody)
		}

		return nil
	}
}
