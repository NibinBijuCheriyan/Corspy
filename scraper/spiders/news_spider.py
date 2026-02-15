import scrapy
from datetime import datetime
import xml.etree.ElementTree as ET

class NewsSpider(scrapy.Spider):
    name = "news"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    def start_requests(self):
        # Queries to monitor
        queries = getattr(self, 'queries', 'Apple Inc,Microsoft Corp,Tesla Inc').split(',')
        for query in queries:
            url = f"https://news.google.com/rss/search?q={query}+when:7d&hl=en-US&gl=US&ceid=US:en"
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # Format is RSS (XML)
        response.selector.register_namespace('atom', 'http://www.w3.org/2005/Atom')
        
        items = response.xpath('//item')
        for item in items:
            title = item.xpath('title/text()').get()
            link = item.xpath('link/text()').get()
            pub_date = item.xpath('pubDate/text()').get()
            description = item.xpath('description/text()').get()

            # Date parsing (RFC 822)
            # e.g., "Mon, 05 Feb 2024 12:00:00 GMT"
            try:
                dt = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %Z")
            except (ValueError, TypeError):
                dt = datetime.now()

            yield {
                'source': 'News',
                'title': title,
                'url': link,
                'date': dt,
                'content': title + "\n" + (description or ""),
                # pivot_score calculated in pipeline
            }
