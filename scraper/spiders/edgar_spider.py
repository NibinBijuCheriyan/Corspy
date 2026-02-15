import scrapy
from datetime import datetime
import xml.etree.ElementTree as ET

class EdgarSpider(scrapy.Spider):
    name = "edgar"
    custom_settings = {
        'USER_AGENT': 'CorporateSpyglass contact@example.com'
    }

    def start_requests(self):
        # Example CIKs: Apple (0000320193), Microsoft (0000789019), Tesla (0001318605)
        ciks = getattr(self, 'ciks', '0000320193,0000789019,0001318605').split(',')
        for cik in ciks:
            url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=&dateb=&owner=include&count=40&output=atom"
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # Helper to handle namespaces in Atom feed if necessary, or just use xpath
        # Atom namespace: http://www.w3.org/2005/Atom
        response.selector.register_namespace('atom', 'http://www.w3.org/2005/Atom')
        
        entries = response.xpath('//atom:entry')
        for entry in entries:
            title = entry.xpath('./atom:title/text()').get()
            link = entry.xpath('./atom:link/@href').get()
            updated = entry.xpath('./atom:updated/text()').get()
            summary = entry.xpath('./atom:summary/text()').get(default='')

            # Clean up logic
            if link and not link.startswith('http'):
                link = "https://www.sec.gov" + link

            # Date parsing (ISO 8601)
            try:
                dt = datetime.fromisoformat(updated.replace("Z", "+00:00"))
            except (ValueError, TypeError):
                dt = datetime.now()

            yield {
                'source': 'SEC',
                'title': title,
                'url': link,
                'date': dt,
                'content': title + "\n" + summary, # Using summary as content for now
                'pivot_score': 0.0 # Will be calculated in pipeline
            }
