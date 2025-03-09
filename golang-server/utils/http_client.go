package utils

import (
	"context"
	"encoding/json"
	"fmt"
	"go-server/config"
	"go-server/middleware"
	"io"
	"net/http"
	"time"
)

var cacheDuration = 60 * time.Minute

var protectedEndpoints = map[string]bool{
	"profile": true,
}

func FetchFromDjango(app string, endpoint string, token string, id string) (json.RawMessage, error) {
	cacheKey := "::" + endpoint
	requiresAuth := protectedEndpoints[app]

	if requiresAuth {
		if token == "" {
			fmt.Println("Error token not founded")
		}
		valid, err := middleware.CheckTokenCache(token, id)
		if err != nil {
			fmt.Println("Error checking token in cache:", err)
		}
		if valid {
			val, err := config.RedisClient.Get(context.Background(), cacheKey).Result()
			if err == nil {
				fmt.Println("Data from Redis Cache")
				return json.RawMessage(val), nil
			}
		}
		if !valid {
			veryfy, err := middleware.VerifyToken(token)
			if err != nil {
				fmt.Println("Error verifying token with Django:", err)
				return nil, err
			}
			if !veryfy {
				return nil, fmt.Errorf("unauthorized: invalid token")
			}
			middleware.StoreTokenCache(token, id)
		}
	}

	val, err := config.RedisClient.Get(context.Background(), cacheKey).Result()
	if err == nil {
		fmt.Println("Data from Redis Cache")
		return json.RawMessage(val), nil
	}

	req, err := http.NewRequest("GET", "http://localhost:8000/api/"+app+"/"+endpoint, nil)
	if err != nil {
		fmt.Println("Error creating request:", err)
		return nil, err
	}

	if requiresAuth {
		req.Header.Set("Authorization", "Bearer "+token)
	}

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("Error connecting to Django:", err)
		return nil, err
	}
	defer resp.Body.Close()

	data, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("Error reading response from Django:", err)
		return nil, err
	}

	err = config.RedisClient.Set(context.Background(), cacheKey, data, cacheDuration).Err()
	if err != nil {
		fmt.Println("Error caching data in Redis:", err)
	}

	fmt.Println("Successfully fetched data from Django")
	return json.RawMessage(data), nil
}
