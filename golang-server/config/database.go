package config

import (
	"database/sql"
	"fmt"
	"log"
	"os"
	"runtime"
	"time"

	"github.com/joho/godotenv"
	_ "github.com/lib/pq"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

var (
	DB     *TrackedDB
	GormDB *gorm.DB
)

type TrackedDB struct {
	*sql.DB
}

func (t *TrackedDB) Close() error {
	pc, file, line, ok := runtime.Caller(1)
	caller := "unknown"
	if ok {
		caller = runtime.FuncForPC(pc).Name()
	}
	log.Printf("⚠️ WARNING: Attempt to close database connection detected! Called from %s (%s:%d)", caller, file, line)
	return t.DB.Close()
}

func (t *TrackedDB) CloseWithContext(component string) error {
	log.Printf("⚠️ WARNING: Attempt to close database connection detected by %s!", component)
	return t.DB.Close()
}

func ConnectPostgres() *TrackedDB {
	err := godotenv.Load(".env")
	if err != nil {
		fmt.Println("❌ Error loading .env file")
		os.Exit(1)
	}

	dsn := fmt.Sprintf("postgres://%s:%s@%s:%s/%s?sslmode=%s",
		GetEnvOrDefault("DB_USER", "postgres"),
		GetEnvOrDefault("DB_PASSWORD", "admin"),
		GetEnvOrDefault("DB_HOST", "127.0.0.1"),
		GetEnvOrDefault("DB_PORT", "5432"),
		GetEnvOrDefault("DB_NAME", "jeraghe"),
		GetEnvOrDefault("DB_SSLMODE", "disable"),
	)

	db, err := sql.Open("postgres", dsn)
	if err != nil {
		fmt.Printf("❌ Error opening database connection: %v\n", err)
		os.Exit(1)
	}

	if err := db.Ping(); err != nil {
		fmt.Printf("❌ Database is not accessible: %v\n", err)
		os.Exit(1)
	}

	db.SetMaxOpenConns(50)
	db.SetMaxIdleConns(20)
	db.SetConnMaxLifetime(3 * time.Minute)
	db.SetConnMaxIdleTime(2 * time.Minute)

	DB = &TrackedDB{DB: db}
	fmt.Println("✅ Secure connection to PostgreSQL established!")
	return DB
}

func ConnectGORM() *gorm.DB {
	sqlDB := ConnectPostgres()

	newLogger := logger.New(
		log.New(os.Stdout, "\r\n", log.LstdFlags),
		logger.Config{
			SlowThreshold: time.Second,
			LogLevel:      logger.Silent,
			Colorful:      true,
		},
	)

	gormDB, err := gorm.Open(postgres.New(postgres.Config{
		Conn: sqlDB.DB,
	}), &gorm.Config{
		Logger: newLogger,
	})
	if err != nil {
		log.Fatalf("❌ failed to initialize GORM: %v", err)
	}

	GormDB = gormDB
	fmt.Println("✅ Secure connection to PostgreSQL with GORM established!")
	return GormDB
}
