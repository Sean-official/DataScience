import logging
import requests
from os import mkdir
from os.path import exists

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
result_path: str = "result"


def scrape_page(url: str) -> str | None:
    # TODO: implement scraper
    logging.info(f"Scraping {url}")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            logging.info(f"Successfully scraped: {url}")
            return response.text
        else:
            logging.error(f"got invalid code while scraping: {url}: {response.status_code}")
    except Exception as e:
        logging.error(f"Failed to scrape {url}: {e}")


if __name__ == "__main__":
    if not exists(result_path):
        logging.error(f"Result directory does not exist: {result_path}")
        exit(1)
    # detail_url: str = "https://plugins.jetbrains.com/search?excludeTags=internal&products=androidstudio&products=appcode&products=aqua&products=clion&products=dataspell&products=dbe&products=fleet&products=go&products=idea&products=idea_ce&products=mps&products=phpstorm&products=pycharm&products=pycharm_ce&products=rider&products=ruby&products=rust&products=webstorm&products=writerside&search=code%20gen"
    detail_url="https://plugins.jetbrains.com/plugin/10650-json-parser-and-code-generation"
    detail:str=scrape_page(detail_url)
    if detail is not None:
        with open(f"{result_path}/result.txt","w",encoding="utf-8") as f:
            f.write(detail)
        logging.info(f"Successfully saved {detail_url} to {result_path}/result.txt")
