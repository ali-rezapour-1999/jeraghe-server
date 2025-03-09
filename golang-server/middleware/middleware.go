package middleware

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"go-server/config"
	"net/http"
	"time"
)

var tokenCacheDuration = 60 * time.Minute

func VerifyToken(token string) (bool, error) {
	if token == "" {
		return false, nil
	}

	djangoAuthURL := "http://localhost:8000/api/auth/token-verify/"

	payload := map[string]string{"token": token}
	jsonData, _ := json.Marshal(payload)

	req, err := http.NewRequest("POST", djangoAuthURL, bytes.NewBuffer(jsonData))
	if err != nil {
		return false, err
	}
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return false, err
	}
	defer resp.Body.Close()

	if resp.StatusCode == http.StatusOK {
		return true, nil
	}
	return false, nil
}

func CheckTokenCache(token string, keyId string) (bool, error) {
	if token == "" {
		return false, fmt.Errorf("missing token")
	}

	value, err := config.RedisClient.Get(context.Background(), keyId).Result()
	if err != nil {
		return false, err
	}
	if value != token {
		return false, nil
	}
	return true, nil
}

func StoreTokenCache(token string, id string) error {
	if token == "" {
		return fmt.Errorf("cannot store empty token")
	}

	err := config.RedisClient.Set(context.Background(), id, token, tokenCacheDuration).Err()
	if err != nil {
		return err
	}

	fmt.Println("Token cached successfully in Redis")
	return nil
}
