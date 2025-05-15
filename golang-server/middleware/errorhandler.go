package middleware

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"strings"
	"time"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

type ExceptionTrace struct {
	ID             uint      `gorm:"primaryKey"`
	Timestamp      time.Time `gorm:"type:timestamp with time zone;default:current_timestamp"`
	Path           string    `gorm:"type:varchar(255)"`
	Method         string    `gorm:"type:varchar(10)"`
	StatusCode     int       `gorm:"type:integer"`
	ErrorMessage   string    `gorm:"type:text"`
	StackTrace     string    `gorm:"type:text"`
	RequestHeaders string    `gorm:"type:jsonb;default:'{}'"`
	RequestBody    string    `gorm:"type:text"`
	UserID         string    `gorm:"type:varchar(100)"`
	IPAddress      string    `gorm:"type:varchar(45)"`
	IsFromGateway  bool      `gorm:"type:boolean;default:true"`
}

func SetupErrorMiddleware(app *fiber.App, db *gorm.DB) {
	app.Use(func(c *fiber.Ctx) error {
		start := time.Now()
		err := c.Next()
		latency := time.Since(start)
		statusCode := c.Response().StatusCode()

		db.Logger.Info(context.Background(), "Request: %s %s - Status: %d - Latency: %v",
			c.Method(), c.Path(), statusCode, latency)

		if statusCode >= 400 {
			trace := buildExceptionTrace(c, db, err, string(c.Response().Body()), statusCode)
			logTraceAsync(db, trace)
			return c.Status(statusCode).JSON(fiber.Map{
				"status":  "error",
				"message": string(c.Response().Body()),
				"details": err.Error(),
			})
		}

		return err
	})
}

func LogForwardedRequest(c *fiber.Ctx, db *gorm.DB, djangoResponseStatus int, djangoResponseBody string) {
	trace := buildExceptionTrace(c, db, nil, "Forwarded to Django", djangoResponseStatus)
	trace.ErrorMessage = fmt.Sprintf("Forwarded to Django - Response: %s", djangoResponseBody)
	logTraceAsync(db, trace)

	db.Logger.Info(context.Background(), "Forwarded to Django: %s %s - Status: %d",
		c.Method(), c.Path(), djangoResponseStatus)
}

func LogSystemError(db *gorm.DB, err error, message string) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	trace := ExceptionTrace{
		Timestamp:      time.Now().UTC(),
		Path:           "N/A",
		Method:         "N/A",
		StatusCode:     0,
		ErrorMessage:   fmt.Sprintf("%s: %v", message, err),
		StackTrace:     fmt.Sprintf("%+v", err),
		RequestHeaders: "{}",
		IsFromGateway:  false,
	}

	if err := db.WithContext(ctx).Create(&trace).Error; err != nil {
		db.Logger.Error(ctx, "Failed to log system error: %v", err)
	}

	db.Logger.Error(ctx, "%s: %v", message, err)
}

func buildExceptionTrace(c *fiber.Ctx, db *gorm.DB, err error, errorMessage string, statusCode int) ExceptionTrace {
	ctx := context.Background()

	trace := ExceptionTrace{
		Timestamp:      time.Now().UTC(),
		Path:           "N/A",
		Method:         "N/A",
		StatusCode:     statusCode,
		ErrorMessage:   errorMessage,
		StackTrace:     fmt.Sprintf("%+v", err),
		RequestHeaders: "{}",
		IPAddress:      "N/A",
		IsFromGateway:  true,
	}

	if c != nil {
		trace.Path = c.Path()
		trace.Method = c.Method()
		trace.IPAddress = c.IP()

		body := string(c.Body())
		if len(body) > 1024 {
			body = "Request body too large"
		}
		trace.RequestBody = body

		headers := make(map[string]string)
		for key, values := range c.GetReqHeaders() {
			if !strings.EqualFold(key, "Authorization") {
				headers[key] = strings.Join(values, ",")
			}
		}
		headersJSON, err := json.Marshal(headers)
		if err != nil {
			db.Logger.Warn(ctx, "Failed to marshal request headers: %v", err)
			trace.RequestHeaders = "{}" // Fallback to valid JSON
		} else {
			trace.RequestHeaders = string(headersJSON)
		}

		token := strings.TrimPrefix(c.Get("Authorization"), "Bearer ")
		if userID, parseErr := ParseUserIDFromToken(token); parseErr == nil {
			trace.UserID = userID
		} else if parseErr != nil {
			db.Logger.Warn(ctx, "Failed to parse user ID from token: %v", parseErr)
		}
	}

	return trace
}

func logTraceAsync(db *gorm.DB, trace ExceptionTrace) {
	go func() {
		ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
		defer cancel()

		if err := db.Exec("SELECT 1").Error; err != nil {
			db.Logger.Error(ctx, "Database connection lost: %v", err)
			return
		}

		if err := db.WithContext(ctx).Create(&trace).Error; err != nil {
			db.Logger.Error(ctx, "Failed to log exception trace: %v", err)
		}
	}()
}

func LogStartupInfo(db *gorm.DB, messages ...string) {
	ctx := context.Background()
	for _, msg := range messages {
		if db != nil {
			db.Logger.Info(ctx, "✅ %s", msg)
		} else {
			fmt.Printf("✅ %s\n", msg)
		}
	}
}

func LogStartupError(db *gorm.DB, err error, message string) {
	if db != nil {
		LogSystemError(db, err, message)
	} else {
		fmt.Printf("❌ %s: %v\n", message, err)
	}
	os.Exit(1)
}
