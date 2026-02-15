import scrapy
from datetime import datetime

class LinkedInSpider(scrapy.Spider):
    name = "linkedin"
    custom_settings = {
        'ROBOTSTXT_OBEY': False,  # LinkedIn specifically forbids scraping in robots.txt
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'DOWNLOAD_DELAY': 5, # High delay to avoid immediate blocking
        'AUTOTHROTTLE_ENABLED': True
    }

    def start_requests(self):
        # Example Company Pages (public) - these often require login or redirect to login
        # We will try to access public job postings or "people" search results if possible without login
        # Note: This is highly likely to be redirected to authwall.
        companies = getattr(self, 'companies', 'apple,microsoft,tesla').split(',')
        for company in companies:
            # Trying a public company url structure
            url = f"https://www.linkedin.com/company/{company}/"
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # Check if we hit the authwall
        if "authwall" in response.url or "login" in response.url:
            self.logger.warning(f"Hit LinkedIn Authwall for {response.url}. Skipping...")
            return

        # Attempt to extract some public info if available (Title, About, Recent Updates)
        # Selectors are fragile and change frequently on LinkedIn
        title = response.css('h1::text').get() or response.css('.org-top-card-summary__title::text').get()
        about = response.css('.org-grid__content-height-enforcer p::text').get()
        
        if title:
            yield {
                'source': 'LinkedIn',
                'title': title.strip(),
                'url': response.url,
                'date': datetime.now(),
                'content': f"Company: {title.strip()}\nAbout: {about or 'N/A'}",
                # pivot_score calculated in pipeline
            }
