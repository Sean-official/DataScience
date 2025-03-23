# @Time   : 2025/3/23 17:12
# @Author : Sean
# @File   : spider.py

import json
import logging
from os.path import exists

import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
result_path = "jetbrains/result"
base_url = "https://plugins.jetbrains.com/api/plugins/"


def scrape_page(url) -> str | None:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            logging.error(f"got invalid code while scraping {url}: {response.status_code}")
            return None
    except Exception as e:
        logging.error(f"got exception while scraping {url}: {e}")


def get_general_data(raw_data: str) -> dict[str, str]:
    result: dict[str, str] = {}
    json_data = json.loads(raw_data)
    for key, value in json_data.items():
        if key == "name":
            result[key] = value
        if key == "preview":
            result[key] = value
        if key == "downloads":
            result[key] = value
        if key == "vendor":
            for _key, _value in value.items():
                if _key == "publicName":
                    result["vendor"] = _value
    return result


def get_rating_data(raw_data: str) -> dict[str, str]:
    result: dict[str, str] = {}
    json_data = json.loads(raw_data)
    # Bayesian Rating
    # bayesianRating = (sum(userRatings) + 2 * meanVote) / (count(userRatings) + 2)
    userRatings: int = 0
    sumRatings: int = 0
    meanVotes: int = 0
    for key, value in json_data.items():
        if key == "votes":
            result[key] = value
            for _key, _value in value.items():
                userRatings += _value
                sumRatings += _value * int(_key)
        if key == "meanVotes":
            result[key] = value
            meanVotes = value
        if key == "meanRatings":
            result[key] = value
    bayesianRating = (sumRatings + 2 * meanVotes) / (userRatings + 2)
    result["bayesianRating"] = bayesianRating
    return result


def get_plugin_data(_plugin_id: int) -> dict:
    result: dict = {}
    raw_data = scrape_page(base_url + str(_plugin_id))
    result["general_data"] = get_general_data(raw_data)
    raw_data = scrape_page(base_url + str(_plugin_id) + "/rating")
    result["rating_data"] = get_rating_data(raw_data)
    return result


def save_plugin_data(_plugin_id: int, res):
    if not exists(result_path):
        logging.error(f"{result_path} does not exist")
        exit(1)
    with open(f"{result_path}/{_plugin_id}.json", "w") as f:
        json.dump(res, f)


def scrape(plugin_id: int):
    logging.info(f"scraping plugin id: {plugin_id}")
    res = get_plugin_data(plugin_id)
    logging.info(f"scraped plugin id: {plugin_id}")
    logging.info(f"saving plugin data: {plugin_id}: {res['general_data']["name"]}")
    save_plugin_data(plugin_id, res)
    logging.info(f"saved plugin data: {plugin_id}: {res['general_data']['name']}")


if __name__ == '__main__':
    scrape(10650)
