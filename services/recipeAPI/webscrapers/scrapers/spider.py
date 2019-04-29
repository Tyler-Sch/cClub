import aiohttp
import asyncio
import concurrent.futures
import datetime
import aiofiles
import logging
from bs4 import BeautifulSoup


logging.basicConfig(level=logging.DEBUG)
logging.getLogger("asyncio").setLevel(logging.WARNING)

class Spider:
    """                 #############################
                        #   Python 3.7 Web scraper  #
                        #############################
                        
        Web scraper class to be inherited when writing webscrapers.
        Scraper will not revisit previously visited urls and not visit urls
        outside of given url boundry.

        to use:
            create Class inheriting from Spider (Class BasicSpider(Spider))
            in __init__ call provide:
                -start_url,
                -boundry (a string with the
                    base url, scraper will not go to websites not starting with
                    boundry if following links),
                -num_workers (# of async tasks to be performed 4-8 seems ideal),
                -loop created with asyncio.get_event_loop()

                -super().__init__(start_url, boundry, num_workers, loop) to
                    initiate spider


            overwrite self.populate_start_urls with async function that uses
                self.populate_queue to add starting urls to queue

            ###################################################################
            #    example of self.populate_start_urls:                         #
            #                                                                 #
            #    async with aiohttp.ClientSession() as session:               #
            #        start = await self.fetch_url(self.start_url, session)    #
            #        soup, links = await self.create_soup_obj(start)          #
            #        await self.populate_queue(links)                         #
            ###################################################################

            overwrite self.parse(response) to parse html and do what you will
            and add new urls to queue (scraper will prevent you from visiting
            previously scraped urls)
                Note:
                    -create soup_obj and links from response with:
                        soup, links = await self.create_soup_obj(response)
                    -add new urls to queue with:
                        await self.add_to_queue([list of url strings to add])
    """

    def __init__(self, start_url, boundry, num_workers, loop):

        self.boundry_url = boundry
        self.num_workers = num_workers
        self.start_url = start_url
        self.visited_sites = set()
        self.in_q = set()
        self.q = asyncio.Queue()
        self.loop = loop
        self.pages_scraped = 0


    async def populate_queue(self, url_list):
        """
        input -> list of urls to scrape

        puts list of urls into asyncio queue after checking that url
        is within the url boundry, not already in the queue, and is not
        NoneType
        """
        for url in url_list:
            if url:
                if url.startswith(self.boundry_url) and url not in self.in_q:
                    self.q.put_nowait(url)
                    self.in_q.add(url)

    async def fetch_url(self, url, session):
        """
        input -> url to fetch
        output -> html response

        async coroutine fetching a url
        """
        async with session.get(url) as response:
            try:
                html_response = await response.text()
                return html_response
            except:
                logging.error(f'failed to get {url}')
                return '<h1>error</h1>'

    async def add_to_queue(self, items_to_add):
        """
        input -> list of urls

            takes list of urls, checks if it's within the boundry, if it's in
            the queue currently, and if it has been visited. If not, it adds
            to the queue
        """
        for item in items_to_add:
            if item:
                if item not in self.in_q and item not in self.visited_sites:
                    if item.startswith(self.boundry_url):
                        await self.q.put(item)
                        self.in_q.add(item)


    async def create_soup_obj(self, html):
        """
            input -> html string
            output -> soup_obj, list of links (not checked for validity) in
                that html

            uses threadpoolexecutor to turn html into soup object

            # NOTE: This is a convience method for an object inheriting from
            this class.
        """
        with concurrent.futures.ThreadPoolExecutor() as pool:
            soup_obj = await self.loop.run_in_executor(
                pool, BeautifulSoup, html, 'html.parser'
            )
            links = [link.get('href') for link in soup_obj.find_all('a')]

            return soup_obj, links

    async def handle_task(self, task_id):
        """
            worker task.
        """
        async with aiohttp.ClientSession() as session:

            while not self.q.empty():
                url = await self.q.get()
                print(f'worker {task_id} fetching {url}')
                response = await self.fetch_url(url, session)
                self.visited_sites.add(url)
                await self.parse(response)
                self.pages_scraped += 1
                if not self.pages_scraped % 50:
                    print(f'{self.pages_scraped} pages have been scraped')

    async def populate_start_urls(self):
        """
            overwrite this method with method which populates self.q
        """
        pass

    async def parse(self, response):
        """
        Overwrite this method with another method to parse your html_response

        """
        pass


    async def scrape(self):
        start = datetime.datetime.now()
        await self.populate_start_urls()
        tasks = [self.handle_task(i) for i in range(self.num_workers)]
        await asyncio.gather(*tasks)
        stop = datetime.datetime.now()
        time_past = stop - start
        minutes = (time_past.seconds % 3600) // 60
        seconds = time_past.seconds % 60
        print(
            f'visited {self.pages_scraped} websites in {minutes} minutes '
             f'and {seconds} seconds')
