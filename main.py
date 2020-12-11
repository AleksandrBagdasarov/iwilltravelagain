from models import Base
from fetcher import request
from loguru import logger
from sqlalchemy_worker import DataBase
import asyncio
from models import StartUrls, Activities
from config import HEADERS, DATA
import json
from parsel import Selector


START_URLS = [
    # тут должны быть параметры, начальных запросов
    # 'https://iwilltravelagain.com/usa/?page=1',
    # 'https://iwilltravelagain.com/europe/?page=1',
    # 'https://iwilltravelagain.com/latin-america-caribbean/?page=1',
    # 'https://iwilltravelagain.com/australia-new-zealand-asia/?page=1',
    'https://iwilltravelagain.com/edit/wp-admin/admin-ajax.php',
]

class IWillTravelAgain:

    def __init__(self):
        self.base = DataBase()

    async def start(self, urls):
        logger.info(f'START WITH {len(urls)} URLS')
        task = [self.base.save_row({'url': url}, StartUrls) for url in urls]
        await asyncio.wait(task)

        rows = self.base.get_all_rows(StartUrls)
        task = [self.get_category(row.id, row.url) for row in rows]
        await asyncio.wait(task)

    async def get_category(self, row_id, row_url):
        r = await request('POST', row_url, headers=HEADERS, data=DATA)
        json_response = json.load(r.text)

        task = [self.base.save_row(
            {
                'start_urls_id': row_id,
                'name': data.get('title'),
                'category': data.get('category'),
                'location': data.get('location'),
            },
            Activities
        )
            for data in json_response
        ]

    async def get_activity_web_site(self, activiti_id, url):
        r = await request('GET', 'example.com')
        tree = Selector(r.text)
        web_site = tree.xpath("some xpath").extract_first()
        row = self.base.update_row(
            {
                'web_site': web_site
            },
            Activities,
            activiti_id
        )
        task = [self.base.save_row({'web_site': web_site}, Activities)]



