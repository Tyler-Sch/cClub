import aiohttp
import asyncio
import gzip
from xml.etree.ElementTree import XMLPullParser
from spider import Spider
import aiofiles
import concurrent.futures
from bs4 import BeautifulSoup
import aiofiles
import json
import datetime

class NyTimesSpider(Spider):

    """
        An python 3.7 asyc webscraper for scraping recipes from cooking.nytimes.com

        script loads site map downloaded from cooking.nytimes.com, downloads
        referenced files, then scrapes recipes from html.

        Needs:
            nyTimesSiteMap/sitemap.xml.gz downloaded from
        http://spiderbites.nytimes.com/sitemaps/cooking.nytimes.com/sitemap.xml.gz


        Output:
            json files of scraped recipes:
                {
                    'recipe_url':
                    'name':
                    'inredients':
                    'yield':
                    'time':
                    'image':
                    'author':
                    'steps':
                }
            in nyTimesTest directory

    """

    def __init__(self, start_url, boundry, num_workers, loop):
        super().__init__(start_url, boundry, num_workers, loop)
        self.xml_queue = asyncio.Queue()

    async def load_xml_gz(self, file_path, session):
        # loads nytimes site map files from disk
        async with session.get(file_path) as resp:
            gzip_bin = await resp.read()
            decoded_gzip = gzip.decompress(gzip_bin)
            return decoded_gzip

    async def load_init_xml(self, file_path, loop):

        file = await loop.run_in_executor(None, gzip.open, file_path, 'rb')
        file_contents  = file.read()
        return file_contents

    async def handle_task(self, task_id, session):
        """
            async worker. Gets xml map file finds recipe urls, fetches html,
            and sends to parser
        """
        while not self.xml_queue.empty():
            xml_url = await self.xml_queue.get()
            print(f'worker {task_id}: fetching file {xml_url}')
            # get xml with recipes
            recipe_xml = await self.load_xml_gz(xml_url, session)
            recipe_xml_parser = XMLPullParser(['start', 'end'])
            recipe_xml_parser.feed(recipe_xml)
            for event, element in recipe_xml_parser.read_events():
                if 'loc' in element.tag and event == 'start':
                    url = element.text
                    if '/recipes/' in url:
                        html = await self.fetch_url(url, session)
                        await self.parse(html, url)
                        self.pages_scraped += 1
                        if not self.pages_scraped % 50:
                            print(f'{self.pages_scraped} pages scraped',
                                ' so far'
                            )

    async def parse(self, html, url):
        """
            uses BeautifulSoup to parse recipes.
        """
        with concurrent.futures.ThreadPoolExecutor() as pool:
            soup_obj = await self.loop.run_in_executor(
                pool,
                BeautifulSoup,
                html,
                'html.parser'
            )
            # Pull info from BeautifulSoup Object
            try:

                # print(url)
                recipe_dict = {}
                recipe_dict['recipe_url'] = url
                recipe = soup_obj.find('div', {'class': 'recipe'})
                recipe_dict['name'] = ' '.join(
                    recipe.find('h1', {'class': 'recipe-title'}).text.split()
                )
                ingredients = recipe.find('ul', {'class': 'recipe-ingredients'})
                recipe_dict['ingredients'] = [
                    ' '.join(i.text.split())
                    for i
                    in ingredients.find_all('li')
                ]

                time_and_yield = recipe.find_all(
                    'span',
                    {'class': 'recipe-yield-value'}
                )
                try:
                    recipe_dict['yield'] = time_and_yield[0].text
                    recipe_dict['time'] = time_and_yield[1].text

                except:
                    print(f'THERE WAS A PROBLEM WITH YIELD AND TIME FOR {url}')
                    recipe_dict['yield'] = None
                    recipe_dict['time'] = None

                try:
                    recipe_dict['image'] = (soup_obj.find(
                        'img',
                        {'itemprop': 'image'}
                        )['src']
                    )
                except TypeError:
                    recipe_dict['image'] = None

                recipe_dict['author'] = soup_obj.find('span', {'class': 'byline-name'}).text

                steps = (recipe.find(
                    'ol', {'class': 'recipe-steps'}
                    ).find_all('li')
                )
                recipe_dict['steps'] = [step.text for step in steps]

                # print(f'constructed food dict for {recipe_dict["name"]}')
                file_address = f'{recipe_dict["name"]}'.replace('/', '_')
                async with aiofiles.open(f'nyTimesTest/{file_address}.json',
                    mode='w') as f:

                    content = json.dumps(recipe_dict)
                    await f.write(content)

            except AttributeError:
                print(f'There was a problem parsing {url}')

    async def scrape(self):
        """
            loads initial xml map, puts elements in queue,
            assigns workers, and initializes the scrape
        """
        start = datetime.datetime.now()
        # load initial xml
        init_xml = await self.load_init_xml(
            'nyTimesSiteMap/sitemap.xml.gz',
            self.loop
        )
        # parse xml_file_tree
        parser = XMLPullParser(['start', 'end'])
        parser.feed(init_xml)
        for event, element in parser.read_events():
            if event == 'start' and 'sitemap' in element.text:
                self.xml_queue.put_nowait(element.text)

        async with aiohttp.ClientSession() as session:
            tasks = [self.handle_task(i, session) for i in range(self.num_workers)]
            await asyncio.gather(*tasks)

        stop = datetime.datetime.now()
        time_past = stop - start
        minutes = (time_past.seconds % 3600) // 60
        seconds = time_past.seconds % 60
        print(
            f'visited {self.pages_scraped} websites in {minutes} minutes '
             f'and {seconds} seconds')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    start_url = ''
    boundry = ''
    num_workers = 8
    spider = NyTimesSpider(start_url, boundry, num_workers, loop)

    loop.run_until_complete(spider.scrape())
    loop.close()
