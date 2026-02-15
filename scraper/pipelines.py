import sys
import os

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from database import SessionLocal, ScrapedItem, init_db
from nlp_processor import calculate_pivot_score

class SQLitePipeline:
    def open_spider(self, spider):
        self.db = SessionLocal()
        # Ensure table exists
        init_db()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        # Calculate pivot score if not present
        if 'pivot_score' not in item:
            item['pivot_score'] = calculate_pivot_score(item.get('content', ''))

        # Check for duplicates by URL
        existing = self.db.query(ScrapedItem).filter(ScrapedItem.url == item['url']).first()
        if existing:
            return item

        db_item = ScrapedItem(
            source=item.get('source'),
            title=item.get('title'),
            url=item.get('url'),
            date=item.get('date'),
            content=item.get('content'),
            pivot_score=item.get('pivot_score')
        )
        self.db.add(db_item)
        self.db.commit()
        return item
