package routes

import (
	"go-server/service"
	"regexp"
)

var Router = []Route{
	{
		Path:         "/category/",
		Method:       "GET",
		Handler:      service.GetCategoryService,
		RequiresAuth: false,
	},
	{
		Path:         "/contact/",
		Method:       "GET",
		Handler:      service.GetContactUserService,
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
	{
		Path:         "/get-profile-skill/",
		Method:       "GET",
		Handler:      service.GetProfileSkill,
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
