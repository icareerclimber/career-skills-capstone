package controllers

import (
	_ "bytes"
	"github.com/revel/revel"
	"log"
)

const (
	_      = iota
	KB int = 1 << (10 * iota)
	MB
	GB
)

type FileInfo struct {
	ContentType string
	Filename    string
	RealFormat  string `json:",omitempty"`
	//	Resolution  string `json:",omitempty"`
	Size   int
	Status string `json:",omitempty"`
}

func (c ResumeAssistant) HandleUpload(resume []byte) revel.Result {
	// Validation rules.
	c.Validation.Required(resume)
	//c.Validation.MinSize(resume, 2*KB).
	//	Message("Minimum a file size of 2KB expected")
	c.Validation.MaxSize(resume, 2*MB).
		Message("File cannot be larger than 2MB")

		// Check format of the file.
		//conf, format, err := image.DecodeConfig(bytes.NewReader(resume))
		//c.Validation.Required(err == nil).Key("resume").
	//Message("Incorrect file format")
	//c.Validation.Required(format == "txt").Key("resume").
	//	Message("TXT file format is expected")

	// Handle errors.
	if c.Validation.HasErrors() {
		c.Validation.Keep()
		c.FlashParams()
		return c.Redirect((*ResumeAssistant).UploadResume)
	}

	//content := bytes.NewReader(resume)
	//contentLen := content.Len()
	log.Println(string(resume[:len(resume)]))
	return c.RenderJSON(FileInfo{
		ContentType: c.Params.Files["resume"][0].Header.Get("Content-Type"),
		Filename:    c.Params.Files["resume"][0].Filename,
		//RealFormat:  format,
		//Resolution:  fmt.Sprintf("%dx%d", conf.Width, conf.Height),
		Size:   len(resume),
		Status: "Successfully uploaded",
	})
}
