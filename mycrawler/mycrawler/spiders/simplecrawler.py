import scrapy
from scrapy.crawler import CrawlerProcess

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    author_search = input("Enter the author Name: ")
    author_search = "+".join(author_search.split())
    total_number = int(input("Enter the number of page: "))
    page_number = 1
    start_urls = [
        f"https://dl.acm.org/action/doSearch?AllField={author_search}&pageSize=20&startPage=0"
    ]
    
    def parse(self, response):
        for paper in response.css("div.issue-item__content .issue-item__content-right"):
            title = paper.css(".hlFld-Title a::text").extract()
            author = paper.css(".truncate-list a span::text").extract()
            link = paper.css(".issue-item__doi::text").extract()
            yield {
                    'title': title,
                    "author": author,
                    "links": link,
                }
            
        next_page = f"https://dl.acm.org/action/doSearch?AllField={QuotesSpider.author_search}&pageSize=20&startPage=" + str(QuotesSpider.page_number)
        print("Crawling at page", QuotesSpider.page_number)
        if QuotesSpider.page_number <= QuotesSpider.total_number:
                QuotesSpider.page_number += 1
                yield response.follow(next_page, callback=self.parse)
                
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
})

process.crawl(QuotesSpider)
process.start() 