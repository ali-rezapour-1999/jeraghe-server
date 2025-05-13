package middleware

import (
	"context"
	"encoding/json"
	"fmt"
	"go-server/config"
	"strings"
	"time"

	"github.com/gofiber/fiber/v2"
)

type ExceptionTrace struct {
	Timestamp      time.Time
	Path           string
	Method         string
	StatusCode     int
	ErrorMessage   string
	StackTrace     string
	RequestHeaders map[string]string
	RequestBody    string
	UserID         string
	IPAddress      string
	IsFromGateway  bool
}

func SetupErrorMiddleware(app *fiber.App, db *config.TrackedDB) {
	err := createExceptionTable(db)
	if err != nil {
		fmt.Printf("Warning: Failed to create exception_traces table: %v\n", err)
	}

	app.Use(func(c *fiber.Ctx) error {
		start := time.Now()
		err := c.Next()
		latency := time.Since(start)

		fmt.Printf("Request: %s %s - Status: %d - Latency: %v\n",
			c.Method(), c.Path(), c.Response().StatusCode(), latency)

		headers := make(map[string]string)
		for key, values := range c.GetReqHeaders() {
			headers[key] = strings.Join(values, ",")
		}

		statusCode := c.Response().StatusCode()
		if statusCode >= 400 {
			trace := ExceptionTrace{
				Timestamp:      time.Now().UTC(),
				Path:           c.Path(),
				Method:         c.Method(),
				StackTrace:     fmt.Sprintf("%+v", err),
				StatusCode:     statusCode,
				ErrorMessage:   string(c.Response().Body()),
				RequestHeaders: headers,
				RequestBody:    string(c.Body()),
				IPAddress:      c.IP(),
				IsFromGateway:  true,
			}

			token := strings.TrimPrefix(c.Get("Authorization"), "Bearer ")
			if userID, parseErr := ParseUserIDFromToken(token); parseErr == nil {
				trace.UserID = userID
			} else {
				fmt.Printf("Warning: Failed to parse user ID from token: %v\n", parseErr)
			}

			go LogExceptionTrace(db, trace)
		}

		return err
	})
}

func createExceptionTable(db *config.TrackedDB) error {
	if db == nil {
		return fmt.Errorf("database connection is nil")
	}

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	query := `
		CREATE TABLE IF NOT EXISTS exception_traces (
			id SERIAL PRIMARY KEY,
			timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
			path VARCHAR(255) NOT NULL,
			method VARCHAR(10) NOT NULL,
			status_code INT NOT NULL,
			error_message TEXT NOT NULL,
			stack_trace TEXT,
			request_headers JSONB,
			request_body TEXT,
			user_id VARCHAR(100),
			ip_address VARCHAR(45),
			is_from_gateway BOOLEAN DEFAULT TRUE
		)`
	_, err := db.ExecContext(ctx, query)
	return err
}

func ErrorHandler(c *fiber.Ctx, err error) error {
	code := fiber.StatusInternalServerError
	message := "Internal Server Error"

	if e, ok := err.(*fiber.Error); ok {
		code = e.Code
		message = e.Message
	} else if authErr, ok := err.(*AuthError); ok {
		code = authErr.Code
		message = authErr.Message
	}

	db := c.Locals("db").(*config.TrackedDB)
	if db != nil {
		trace := ExceptionTrace{
			Timestamp:     time.Now().UTC(),
			Path:          c.Path(),
			Method:        c.Method(),
			StatusCode:    code,
			ErrorMessage:  message,
			StackTrace:    fmt.Sprintf("%+v", err),
			RequestBody:   string(c.Body()),
			IPAddress:     c.IP(),
			IsFromGateway: true,
		}

		headers := make(map[string]string)
		for key, values := range c.GetReqHeaders() {
			headers[key] = strings.Join(values, ",")
		}
		trace.RequestHeaders = headers

		token := strings.TrimPrefix(c.Get("Authorization"), "Bearer ")
		if userID, parseErr := ParseUserIDFromToken(token); parseErr == nil {
			trace.UserID = userID
		}

		go LogExceptionTrace(db, trace)
	}
	return c.Status(code).JSON(fiber.Map{
		"status":    "error",
		"message":   message,
		"timestamp": time.Now().UTC().Format(time.RFC3339),
	})
}

func LogExceptionTrace(db *config.TrackedDB, trace ExceptionTrace) {
	if db == nil {
		fmt.Println("Warning: Database connection not available for exception logging")
		return
	}

	headersJSON, _ := json.Marshal(trace.RequestHeaders)

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	query := `
		INSERT INTO exception_traces (
			timestamp, path, method, status_code, error_message, 
			stack_trace, request_headers, request_body, user_id, ip_address, is_from_gateway
		) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
	`
	_, err := db.ExecContext(ctx, query,
		trace.Timestamp, trace.Path, trace.Method, trace.StatusCode, trace.ErrorMessage,
		trace.StackTrace, headersJSON, trace.RequestBody, trace.UserID, trace.IPAddress, trace.IsFromGateway,
	)
	if err != nil {
		fmt.Printf("Failed to log exception trace: %v\n", err)
	}
}

func LogError(db *config.TrackedDB, err error, c *fiber.Ctx) {
	trace := ExceptionTrace{
		Timestamp:     time.Now().UTC(),
		ErrorMessage:  err.Error(),
		StackTrace:    fmt.Sprintf("%+v", err),
		IsFromGateway: true,
	}

	if c != nil {
		trace.Method = c.Method()
		trace.Path = c.Path()
		trace.StatusCode = c.Response().StatusCode()
		trace.RequestBody = string(c.Body())
		trace.IPAddress = c.IP()
	}

	if db == nil {
		fmt.Printf("❌ [Fallback] %s - %s\n", trace.ErrorMessage, trace.StackTrace)
		return
	}

	if err := createExceptionTable(db); err != nil {
		fmt.Printf("Warning: Failed to create exception_traces table: %v\n", err)
		return
	}

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	headersJSON, _ := json.Marshal(trace.RequestHeaders)

	query := `
		INSERT INTO exception_traces (
			timestamp, error_message, stack_trace, is_from_gateway, method, path, 
			status_code, request_body, request_headers, user_id, ip_address
		) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
	`
	_, err = db.ExecContext(ctx, query,
		trace.Timestamp, trace.ErrorMessage, trace.StackTrace, trace.IsFromGateway,
		trace.Method, trace.Path, trace.StatusCode, trace.RequestBody,
		headersJSON, trace.UserID, trace.IPAddress,
	)
	if err != nil {
		fmt.Printf("Failed to log error to database: %v\n", err)
	}
}
