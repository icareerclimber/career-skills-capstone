package controllers

import (
	"github.com/revel/revel"
)

type ResumeAssistant struct {
	*revel.Controller
}

func (c ResumeAssistant) Welcome() revel.Result {
	return c.Render()
}
