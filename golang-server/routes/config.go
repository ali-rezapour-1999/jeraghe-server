package routes

import (
	"go-server/middleware"

	"github.com/gofiber/fiber/v2"
)

func registerRoutes(router fiber.Router, routes []Route) {
	for _, route := range routes {
		var handlers []fiber.Handler

		if route.RequiresAuth {
			handlers = append(handlers, middleware.JWTMiddleware)
		}

		handlers = append(handlers, route.Handler)

		switch route.Method {
		case "GET":
			router.Get(route.Path, handlers...)
		case "POST":
			router.Post(route.Path, handlers...)
		case "PUT":
			router.Put(route.Path, handlers...)
		case "DELETE":
			router.Delete(route.Path, handlers...)
		default:
			router.All(route.Path, handlers...)
		}
	}
}
