import sys
import os

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Import spiders
from scraper.spiders.edgar_spider import EdgarSpider
from scraper.spiders.news_spider import NewsSpider
from scraper.spiders.patents_spider import PatentsSpider
from scraper.spiders.linkedin_spider import LinkedInSpider

def run():
    # Load settings from scraper.settings
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'scraper.settings')
    settings = get_project_settings()
    
    process = CrawlerProcess(settings)
    process.crawl(EdgarSpider)
    process.crawl(NewsSpider)
    process.crawl(PatentsSpider)
    process.crawl(LinkedInSpider)
    process.start()

if __name__ == "__main__":
    run()
