package animego

import (
	"fmt"
	"log"

	"github.com/gocolly/colly"
)

type SearchType string

const (
	All   SearchType = "all"
	Anime SearchType = "anime"
	Manga SearchType = "manga"
)

const baseUrl = "https://animego.org/search/%s?q=%s"

func getSearchUrl(query string, searchType SearchType) string {
	return fmt.Sprintf(baseUrl, string(searchType), query)
}

type Item struct {
	Title    string `selector:"div > .animes-grid-item-body > .card-title > a"`
	Romaji   string `selector:".animes-grid-item-body > .small > div"`
	Url      string `selector:".animes-grid-item-body > .card-title > a" attr:"href"`
	ImageUrl string `selector:".animes-grid-item-picture > a > div" attr:"data-original"`
	Genre    string `selector:".animes-grid-item-body > .animes-grid-item-body-info > span:nth-child(1) > a"`
	Year     string `selector:".animes-grid-item-body > .animes-grid-item-body-info > .anime-year > a"`
}

func Search(query string, searchType SearchType) []*Item {
	url := getSearchUrl(query, searchType)
	return scrapContent(url)
}

func scrapContent(url string) []*Item {
	var items []*Item

	c := colly.NewCollector()

	c.OnHTML("div .animes-grid-item", func(e *colly.HTMLElement) {
		title := e.ChildText("div > .animes-grid-item-body > .card-title > a")
		romaji := e.ChildText(".animes-grid-item-body > .small > div")
		url := e.ChildAttr(".animes-grid-item-body > .card-title > a", "href")
		imageUrl := e.ChildAttr(".animes-grid-item-picture > a > div", "data-original")
		genre := e.ChildText(".animes-grid-item-body > .animes-grid-item-body-info > span:nth-child(1) > a")
		year := e.ChildText(".animes-grid-item-body > .animes-grid-item-body-info > .anime-year > a")

		item := &Item{
			Title:    title,
			Romaji:   romaji,
			Url:      url,
			ImageUrl: imageUrl,
			Genre:    genre,
			Year:     year,
		}

		items = append(items, item)
	})

	c.OnRequest(func(r *colly.Request) {
		log.Println("Visiting", r.URL.String())
	})

	c.Visit(url)

	log.Printf("Length: %v", len(items))
	return items
}
