package middleware

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"os"
	"strings"
	"time"

	"github.com/gofiber/fiber/v2"
	"github.com/golang-jwt/jwt/v5"
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
}

func SetupErrorMiddleware(app *fiber.App, db *sql.DB) {
	err := createExceptionTable(db)
	if err != nil {
		fmt.Printf("Warning: Failed to create exception_traces table: %v\n", err)
	}

	app.Use(func(c *fiber.Ctx) error {
		err := c.Next()

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

func createExceptionTable(db *sql.DB) error {
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
			ip_address VARCHAR(45)
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

	return c.Status(code).JSON(fiber.Map{
		"error":     message,
		"timestamp": time.Now().UTC().Format(time.RFC3339),
	})
}

func ParseUserIDFromToken(tokenString string) (string, error) {
	if tokenString == "" {
		return "", nil
	}

	secretKey := os.Getenv("JWT_SECRET")
	if secretKey == "" {
		return "", fmt.Errorf("JWT secret key not configured")
	}

	token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
		}
		return []byte(secretKey), nil
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

	if userID, ok := claims["sub"].(string); ok && userID != "" {
		return userID, nil
	}
	if userID, ok := claims["user_id"].(string); ok && userID != "" {
		return userID, nil
	}

	return "", fmt.Errorf("user ID not found in token")
}

func LogExceptionTrace(db *sql.DB, trace ExceptionTrace) {
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
			stack_trace, request_headers, request_body, user_id, ip_address
		) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
	`
	_, err := db.ExecContext(ctx, query,
		trace.Timestamp, trace.Path, trace.Method, trace.StatusCode, trace.ErrorMessage,
		trace.StackTrace, headersJSON, trace.RequestBody, trace.UserID, trace.IPAddress,
	)
	if err != nil {
		fmt.Printf("Failed to log exception trace: %v\n", err)
	}
}

func LogError(db *sql.DB, err error) {
	trace := ExceptionTrace{
		Timestamp:    time.Now().UTC(),
		ErrorMessage: err.Error(),
		StackTrace:   fmt.Sprintf("%+v", err),
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

	query := `
		INSERT INTO exception_traces (
			timestamp, error_message, stack_trace
		) VALUES ($1, $2, $3)
	`
	_, err = db.ExecContext(ctx, query, trace.Timestamp, trace.ErrorMessage, trace.StackTrace)
	if err != nil {
		fmt.Printf("Failed to log error to database: %v\n", err)
	}
}

func GetTimestamp() time.Time {
	return time.Now().UTC()
}
