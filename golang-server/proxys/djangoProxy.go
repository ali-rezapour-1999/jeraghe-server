package proxys

import (
	"bytes"
	"context"
	"go-server/config"
	"go-server/middleware"
	"io"
	"net/http"
	"path"
	"strings"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

var djangoAPI = config.GetEnvOrDefault("DJANGO_API", "http://127.0.0.1:8000")

func ProxyToDjango(db *gorm.DB) fiber.Handler {
	return func(c *fiber.Ctx) error {
		ctx := context.Background()
		isMediaRequest := c.Method() == fiber.MethodGet && strings.HasPrefix(c.Path(), "/media/")
		targetURL := djangoAPI + c.OriginalURL()
		db.Logger.Info(ctx, "Proxying to: %s", targetURL)

		body := c.Body()
		if len(body) == 0 && (c.Method() == fiber.MethodPost || c.Method() == fiber.MethodPut || c.Method() == fiber.MethodPatch) {
			body = []byte("{}")
		}

		httpReq, err := http.NewRequest(c.Method(), targetURL, bytes.NewReader(body))
		if err != nil {
			middleware.LogSystemError(db, err, "Failed to create proxy request")
			return fiber.NewError(fiber.StatusBadRequest, "Failed to create proxy request")
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
			middleware.LogSystemError(db, err, "Proxy request failed")
			return fiber.NewError(fiber.StatusBadGateway, "Proxy request failed")
		}
		defer resp.Body.Close()

		respBody, err := io.ReadAll(resp.Body)
		if err != nil {
			middleware.LogSystemError(db, err, "Failed to read response from Django")
			return fiber.NewError(fiber.StatusInternalServerError, "Failed to read response from Django")
		}

		middleware.LogForwardedRequest(c, db, resp.StatusCode, string(respBody))

		if isMediaRequest {
			if strings.Contains(resp.Header.Get("Content-Type"), "application/json") {
				middleware.LogSystemError(db, nil, "Invalid media response: JSON received instead of image")
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

		return c.Status(resp.StatusCode).Send(respBody)
	}
}
