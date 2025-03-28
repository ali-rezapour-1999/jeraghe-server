package middleware

import (
	"log"

	"github.com/gofiber/fiber/v2"
)

func ErrorHandler(c *fiber.Ctx) error {
	err := c.Next()
	log.Println(c)
	if err != nil {
		log.Println("Error:", err)

		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error":   true,
			"message": err.Error(),
			"status":  err.Error(),
		})
	}
	return nil
}
