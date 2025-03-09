package config

import (
	"context"
	"fmt"

	"github.com/redis/go-redis/v9"
)

var RedisClient *redis.Client

func ConnectRedis() *redis.Client {
	RedisClient = redis.NewClient(&redis.Options{
		Addr:     "212.80.20.179:31752",
		Password: "Q2o8d6NxjC35R8fA",
		DB:       0,
	})

	_, err := RedisClient.Ping(context.Background()).Result()
	if err != nil {
		fmt.Printf("Error connecting to Redis: %v", err)
		return nil
	}
	fmt.Println("Connected to Redis")
	return RedisClient
}
