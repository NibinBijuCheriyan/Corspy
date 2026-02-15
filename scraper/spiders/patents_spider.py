import scrapy
from datetime import datetime

class PatentsSpider(scrapy.Spider):
    name = "patents"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    def start_requests(self):
        companies = getattr(self, 'companies', 'Apple Inc,Microsoft Corp,Tesla Inc').split(',')
        for company in companies:
            # Monitoring patent news/filings via news search for now
            # A real implementation would use USPTO PEDS API or Google Patents scraping (complex)
            url = f"https://news.google.com/rss/search?q={company}+patent+application+when:30d&hl=en-US&gl=US&ceid=US:en"
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        response.selector.register_namespace('atom', 'http://www.w3.org/2005/Atom')
        items = response.xpath('//item')
        for item in items:
            title = item.xpath('title/text()').get()
            link = item.xpath('link/text()').get()
            pub_date = item.xpath('pubDate/text()').get()
            description = item.xpath('description/text()').get()

            try:
                dt = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %Z")
            except (ValueError, TypeError):
                dt = datetime.now()

            yield {
                'source': 'Patent',
                'title': title, # e.g. "Apple files patent for..."
                'url': link,
                'date': dt,
                'content': title + "\n" + (description or ""),
                # pivot_score calculated in pipeline
            }
