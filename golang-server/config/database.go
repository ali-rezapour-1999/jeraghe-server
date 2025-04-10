package config

import (
	"database/sql"
	"fmt"
	"os"
	"time"

	_ "github.com/lib/pq"
)

var DB *sql.DB

func ConnectPostgres() *sql.DB {
	dsn := fmt.Sprintf("postgres://%s:%s@%s:%s/%s?sslmode=%s",
		getEnvOrDefault("DB_USER", "postgres"),
		getEnvOrDefault("DB_PASSWORD", "admin"),
		getEnvOrDefault("DB_HOST", "127.0.0.1"),
		getEnvOrDefault("DB_PORT", "5432"),
		getEnvOrDefault("DB_NAME", "jeraghe"),
		getEnvOrDefault("DB_SSLMODE", "disable"),
	)

	db, err := sql.Open("postgres", dsn)
	if err != nil {
		fmt.Printf("❌ Error opening database connection: %v\n", err)
		return nil
	}

	err = db.Ping()
	if err != nil {
		fmt.Printf("❌ Database is not accessible: %v\n", err)
		db.Close()
		return nil
	}

	db.SetMaxOpenConns(25)
	db.SetMaxIdleConns(25)
	db.SetConnMaxLifetime(5 * time.Minute)

	DB = db
	fmt.Println("✅ Secure connection to PostgreSQL established!")
	return db
}

func getEnvOrDefault(key, defaultValue string) string {
	value := os.Getenv(key)
	if value == "" {
		return defaultValue
	}
	return value
}
