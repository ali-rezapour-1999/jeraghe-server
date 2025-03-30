package config

import (
	"context"
	"fmt"
	"os"

	"github.com/redis/go-redis/v9"
)

var (
	RedisClient *redis.Client
	ctx         = context.Background()
)

func ConnectRedis() *redis.Client {
	RedisClient = redis.NewClient(&redis.Options{
		Addr:       os.Getenv("REDIS_URL"),
		MaxRetries: 10,
		DB:         0,
	})

	_, err := RedisClient.Ping(ctx).Result()
	if err != nil {
		fmt.Printf("Error connecting to Redis: %v", err)
		return nil
	}
	fmt.Println("Connected to Redis")
	return RedisClient
}
