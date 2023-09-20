import argparse
import json
import re
import urllib.parse
from serpapi import GoogleSearch
import logging
from typing import Optional, Dict, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReviewsScraper:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_reviews(self, data_id: str,
                      max_cnt: Optional[int] = None) -> None:
        cnt = 0
        params = {
            "engine": "google_maps_reviews",
            "data_id": data_id,
            "api_key": self.api_key,
        }

        results = self._make_search(params)

        self._save_reviews(data_id, cnt, results)
        self._save_info(data_id, results)  # こちらで_info.jsonを保存

        next_page_token = results.get(
            "serpapi_pagination", {}).get("next_page_token")

        while next_page_token and (max_cnt is None or cnt < max_cnt):
            cnt += 1
            params["next_page_token"] = next_page_token
            results = self._make_search(params)

            self._save_reviews(data_id, cnt, results)  # レビューの保存

            next_page_token = results.get("serpapi_pagination", {}).get(
                "next_page_token"
            )

    def _make_search(self, params: Dict[str, str]) -> Dict:
        search = GoogleSearch(params)
        return search.get_dict()

    def _save_reviews(self, data_id: str, cnt: int, results: Dict) -> None:
        with open(f"reviews_{data_id}_{cnt}.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False)

    def _save_info(self, data_id: str, results: Dict) -> None:
        with open(f"{data_id}_info.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False)

    def find_data_id(
        self, query: str, latitude: float, longitude: float
    ) -> Optional[str]:
        params = {
            "engine": "google_maps",
            "q": query,
            "ll": f"@{latitude},{longitude},12z",
            "api_key": self.api_key,
            "hl": "en",
        }

        results = self._make_search(params)
        place_results = results.get("place_results")
        if place_results and place_results.get("data_id"):
            return place_results.get("data_id")
        elif results.get("local_results"):
            return results.get("local_results")[0].get("data_id")


def extract_info_from_url(url: str) -> Tuple[str, float, float]:
    parsed = urllib.parse.urlparse(url)

    # print(parsed.path.split("/")[4])
    place_info_list = []
    match = re.search(r"data=(!.+)", parsed.path)
    if match:
        extracted_data = match.group(1)
        print(extracted_data)
        place_info_list.append(extracted_data)
    else:
        print("data= not found in URL.")

    if not place_info_list:
        raise ValueError(f"'data' parameter not found in URL: {url}")

    query = urllib.parse.unquote(parsed.path.split("/")[3])
    coordinates = parsed.path.split("/")[4].split("@")[1].split(",")[0:2]
    latitude = float(coordinates[0])
    longitude = float(coordinates[1])
    print(query, latitude, longitude)
    return query, latitude, longitude


def main():
    parser = argparse.ArgumentParser(
        description="Fetch Google Maps Reviews by Data ID."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", type=str, help="File containing the URLs.")
    group.add_argument("--query", type=str, help="Search query.")
    parser.add_argument("api_key", type=str, help="SerpAPI API Key.")
    parser.add_argument(
        "--cnt", type=int, default=None, help="Maximum number of pagination to fetch."
    )
    parser.add_argument(
        "--latitude", type=float, help="Latitude. Must be set if --query is set."
    )
    parser.add_argument(
        "--longitude", type=float, help="Longitude. Must be set if --query is set."
    )

    args = parser.parse_args()

    scraper = ReviewsScraper(args.api_key)

    if args.file:
        with open(args.file, "r") as f:
            for line in f:
                line = line.strip()
                query, latitude, longitude = extract_info_from_url(line)
                data_id = scraper.find_data_id(query, latitude, longitude)
                if data_id:
                    scraper.fetch_reviews(data_id, args.cnt)
                else:
                    logger.error(f"Data ID not found for {line}.")
    else:
        data_id = scraper.find_data_id(
            args.query, args.latitude, args.longitude)
        if data_id:
            scraper.fetch_reviews(data_id, args.cnt)
        else:
            logger.error("Data ID not found.")


if __name__ == "__main__":
    main()
