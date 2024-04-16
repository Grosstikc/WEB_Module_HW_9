from scrapy.crawler import CrawlerProcess
from quotes_scraper.spiders.quotes_spider import QuotesSpider

if __name__ == '__main__':
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': 'results.json'
    })
    process.crawl(QuotesSpider)
    process.start()
