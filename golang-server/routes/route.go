package routes

import (
	"go-server/service"
	"regexp"
)

var Router = []Route{
	{
		Path:         "/category/",
		Method:       "GET",
		Handler:      service.GetCategroyService,
		RequiresAuth: false,
	},
	{
		Path:         "/contact/",
		Method:       "GET",
		Handler:      service.GetContactUserSerivce,
		RequiresAuth: true,
	},
	{
		Path:         "/get-idea-list/",
		Method:       "GET",
		Handler:      service.GetUserIdeaListService,
		RequiresAuth: true,
	},
	{
		Path:         "/get-idea/",
		Method:       "GET",
		Handler:      service.GetIdeaUserService,
		RequiresAuth: true,
	},

	{
		Path:         "/get-profile/",
		Method:       "GET",
		Handler:      service.GetProfileData,
		RequiresAuth: true,
	},
}

func getProtectionRules() []ProtectionRule {
	return []ProtectionRule{
		{
			PathPattern:  regexp.MustCompile(`^/api/private/auth/login/`),
			RequiresAuth: false,
		},
		{
			PathPattern:  regexp.MustCompile(`^/api/private/auth/register/`),
			RequiresAuth: false,
		},
		{
			PathPattern:  regexp.MustCompile(`^/api/private/auth/token-verify/`),
			RequiresAuth: false,
		},
		{
			PathPattern:  regexp.MustCompile(`^/api/private/auth/token-refresh/`),
			RequiresAuth: false,
		},
		{
			PathPattern:  regexp.MustCompile(`^/api/private/auth/.*`),
			RequiresAuth: true,
		},
		{
			PathPattern:  regexp.MustCompile(`^/api/private/profile/.*`),
			RequiresAuth: true,
		},
	}
}
