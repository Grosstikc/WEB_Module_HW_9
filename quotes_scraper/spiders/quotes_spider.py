import scrapy
import json

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/'
    ]

    def parse(self, response):
        quotes = response.css('div.quote')
        for quote in quotes:
            text = quote.css('span.text::text').get()
            author = quote.css('small.author::text').get()
            tags = quote.css('div.tags a.tag::text').getall()
            author_url = response.urljoin(quote.css('span a::attr(href)').get())
            
            yield response.follow(author_url, self.parse_author, meta={'quote': text, 'author': author, 'tags': tags})

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_author(self, response):
        author = response.meta['author']
        quote = response.meta['quote']
        tags = response.meta['tags']
        
        author_data = {
            'fullname': author,
            'born_date': response.css('span.author-born-date::text').get(),
            'born_location': response.css('span.author-born-location::text').get().strip(),
            'description': response.css('.author-description::text').get().strip()
        }

        yield {
            'tags': tags,
            'author': author,
            'quote': quote,
            'author_data': author_data
        }
