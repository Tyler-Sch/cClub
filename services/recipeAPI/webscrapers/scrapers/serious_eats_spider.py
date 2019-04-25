
import asyncio
from bs4 import BeautifulSoup
import aiofiles
import concurrent.futures
from spider import Spider
import aiohttp


class BasicSpider(Spider):

    """
        Demo of how to follow links in scraped pages. This script will follow
        and add links to queue, but doesnt download an info currently.
    """

    def __init__(self, start_url, boundry, num_workers, loop):
        super().__init__(start_url, boundry, num_workers, loop)

    async def populate_start_urls(self):
        """
            should call 'await self.populate_queue(links_to_add)'
            to add starting urls to the queue
            (This method is called by the scrape method to give the
            spider a list of urls to start on)
        """
        async with aiohttp.ClientSession() as session:
            start = await self.fetch_url(self.start_url, session)
            soup, links = await self.create_soup_obj(start)
            await self.populate_queue(links)


    async def parse(self, response):
        soup, links = await self.create_soup_obj(response)
        l = []
        for link in links:
            if link:
                if '/print/' not in link:
                    l.append(link)
        await self.add_to_queue(l)
        # parse bs4 soup object here


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    start_url = 'https://www.seriouseats.com/recipes'
    boundry = 'https://www.seriouseats.com/recipes/2018'
    num_workers = 8
    spider = BasicSpider(start_url, boundry, num_workers, loop)

    loop.run_until_complete(spider.scrape())
    loop.close()
