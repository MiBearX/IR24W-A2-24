from threading import Thread
from inspect import getsource
from utils.download import download
from utils import get_logger
import scraper
import time
from scraper import webScraperStorage
class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        # basic check for requests in scraper
        assert {getsource(scraper).find(req) for req in {"from requests import", "import requests"}} == {-1}, "Do not use requests in scraper.py"
        assert {getsource(scraper).find(req) for req in {"from urllib.request import", "import urllib.request"}} == {-1}, "Do not use urllib.request in scraper.py"
        super().__init__(daemon=True)



    # def run(self):
    #     while True:
    #         tbd_url = self.frontier.get_tbd_url()
    #         if not tbd_url:
    #             self.logger.info("Frontier is empty. Stopping Crawler.")
    #             break
    #         resp = download(tbd_url, self.config, self.logger)
    #         self.logger.info(
    #             f"Downloaded {tbd_url}, status <{resp.status}>, "
    #             f"using cache {self.config.cache_server}.")
    #         scraped_urls = scraper.scraper(tbd_url, resp)
    #         for scraped_url in scraped_urls:
    #             self.frontier.add_url(scraped_url)
    #         self.frontier.mark_url_complete(tbd_url)
    #         time.sleep(self.config.time_delay)

    def run(self):
        while True:
            tbd_url = self.frontier.get_tbd_url()
            if not tbd_url:
                self.logger.info("Frontier is empty. Stopping Crawler.")
                print("50 MOST COMMON WORDS: ", sorted(webScraperStorage.wordFrequencyDict.items(), key=lambda freq : freq[1], reverse=True)[:50])
                print("TOTAL UNIQUE PAGES: ", webScraperStorage.totalURLCount)
                print("LONGEST PAGE: ", webScraperStorage.longestPage)
                print("LONGEST NUMBER OF WORDS: ", webScraperStorage.longestNumWords)
                sorted_token_info = sorted(webScraperStorage.ics_subdomain_freq.items(), key=lambda word_and_freq : word_and_freq[0])
                print("LIST OF SUBDOMAINS: ", sorted_token_info)
                break
            start = time.perf_counter()     #float value in seconds
            resp = download(tbd_url, self.config, self.logger)
            end = time.perf_counter()       
            self.logger.info(
                f"Downloaded {tbd_url}, status <{resp.status}>, "
                f"using cache {self.config.cache_server}.")
            scraped_urls = scraper.scraper(tbd_url, resp)
            for scraped_url in scraped_urls:
                self.frontier.add_url(scraped_url)
            self.frontier.mark_url_complete(tbd_url)
            time.sleep(self.config.time_delay)
            delay = (end - start) * 60  # convert to milliseconds
            time.sleep(delay)