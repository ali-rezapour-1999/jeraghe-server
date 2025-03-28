package utils

import (
	"context"
	"encoding/json"
	"fmt"
	"go-server/config"
	"io"
	"net/http"
	"time"
)

var cacheDuration = 30 * time.Minute

func FetchFromDjango(app string, endpoint string, token string, requiresAuth bool) (json.RawMessage, error) {
	cacheKey := "::" + app + endpoint + token

	val, err := config.RedisClient.Get(context.Background(), cacheKey).Result()
	if err == nil {
		return json.RawMessage(val), nil
	}

	req, err := http.NewRequest("GET", "http://localhost:8000/api/"+app+endpoint, nil)
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
	if resp.StatusCode == 200 {
		data, err := io.ReadAll(resp.Body)
		if err != nil {
			fmt.Println("Error reading response from Django:", err)
			return nil, err
		}

		err = config.RedisClient.Set(context.Background(), cacheKey, data, cacheDuration).Err()
		if err != nil {
			fmt.Println("Error caching data in Redis:", err)
		}
		return json.RawMessage(data), nil
	}
	return nil, err
}
