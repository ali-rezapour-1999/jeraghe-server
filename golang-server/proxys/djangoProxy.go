package proxys

import (
	"bytes"
	"fmt"
	"go-server/config"
	"go-server/middleware"
	"io"
	"net/http"
	"path"
	"strings"
	"time"

	"github.com/gofiber/fiber/v2"
)

var djangoAPI = config.GetEnvOrDefault("DJANGO_API", "http://127.0.0.1:8000")

func ProxyToDjango(db *config.TrackedDB) fiber.Handler {
	return func(c *fiber.Ctx) error {
		isMediaRequest := c.Method() == fiber.MethodGet && strings.HasPrefix(c.Path(), "/media/")
		targetURL := fmt.Sprintf("%s%s", djangoAPI, c.OriginalURL())
		fmt.Println("Proxying to:", targetURL)

		body := c.Body()
		if len(body) == 0 && (c.Method() == fiber.MethodPost || c.Method() == fiber.MethodPut || c.Method() == fiber.MethodPatch) {
			body = []byte("{}")
		}

		httpReq, err := http.NewRequest(c.Method(), targetURL, bytes.NewReader(body))
		if err != nil {
			return fiber.NewError(fiber.StatusBadRequest, fmt.Sprintf("Failed to create proxy request: %v", err))
		}

		httpReq.Header.Set("User-Agent", "Fiber-Gateway")
		httpReq.Header.Set("Referer", djangoAPI)

		if !isMediaRequest {
			httpReq.Header.Set("Content-Type", c.Get("Content-Type", "application/json"))
		}

		if token := c.Get("Authorization"); token != "" {
			httpReq.Header.Set("Authorization", token)
		}

		client := &http.Client{}
		resp, err := client.Do(httpReq)
		if err != nil {
			return fiber.NewError(fiber.StatusBadGateway, fmt.Sprintf("Proxy request failed: %v", err))
		}
		defer resp.Body.Close()

		respBody, err := io.ReadAll(resp.Body)
		if err != nil {
			return fiber.NewError(fiber.StatusInternalServerError, "Failed to read response from Django")
		}

		if isMediaRequest {
			if strings.Contains(resp.Header.Get("Content-Type"), "application/json") {
				return fiber.NewError(fiber.StatusInternalServerError, "Invalid media response: JSON received instead of image")
			}

			ext := strings.ToLower(path.Ext(c.Path()))
			switch ext {
			case ".jpg", ".jpeg":
				c.Set("Content-Type", "image/jpeg")
				c.Set("Cache-Control", "public, max-age=31536000")
			case ".png":
				c.Set("Content-Type", "image/png")
				c.Set("Cache-Control", "public, max-age=31536000")
			case ".gif":
				c.Set("Content-Type", "image/gif")
				c.Set("Cache-Control", "public, max-age=31536000")
			case ".webp":
				c.Set("Content-Type", "image/webp")
				c.Set("Cache-Control", "public, max-age=31536000")
			default:
				c.Set("Content-Type", "application/octet-stream")
				c.Set("Cache-Control", "public, max-age=86400")
			}
		} else {
			for k, v := range resp.Header {
				for _, vv := range v {
					c.Set(k, vv)
				}
			}
		}

		c.Status(resp.StatusCode)
		c.Send(respBody)

		if resp.StatusCode >= 400 && !isMediaRequest {
			trace := middleware.ExceptionTrace{
				Timestamp:     time.Now().UTC(),
				Path:          c.Path(),
				Method:        c.Method(),
				StatusCode:    resp.StatusCode,
				ErrorMessage:  string(respBody),
				StackTrace:    "",
				RequestBody:   string(body),
				IPAddress:     c.IP(),
				IsFromGateway: true,
			}
			token := c.Get("Authorization")
			if userID, err := middleware.ParseUserIDFromToken(token); err == nil {
				trace.UserID = userID
			}
			go middleware.LogExceptionTrace(db, trace)
		}

		return nil
	}
}
