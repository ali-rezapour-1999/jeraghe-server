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

func CheckTokenCache(token string) (bool, error) {
	if token == "" {
		return false, fmt.Errorf("missing token")
	}
	exists, err := config.RedisClient.Exists(context.Background(), token).Result()
	if err != nil {
		return false, fmt.Errorf("error checking token in Redis: %v", err)
	}
	return exists > 0, nil
}

func StoreTokenCache(token string) error {
	if token == "" {
		return fmt.Errorf("cannot store empty token")
	}
	err := config.RedisClient.Set(context.Background(), token, true, tokenCacheDuration).Err()
	if err != nil {
		return err
	}
	return nil
}

func IsAuthontication(token string) (bool, error) {
	if token == "" {
		return false, fmt.Errorf("token required")
	}
	verify, err := CheckTokenCache(token)
	if verify && err == nil {
		return true, nil
	}
	newToken, err := VerifyToken(token)
	if newToken && err == nil {
		StoreTokenCache(token)
		return true, nil
	}
	return false, fmt.Errorf("unauthorized: Invalid Token")
}
