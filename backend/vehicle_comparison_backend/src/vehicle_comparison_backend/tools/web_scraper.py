from crewai import Tool
from typing import Type
from pydantic import BaseModel, Field
import requests
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import urljoin
import json

class WebScraperInput(BaseModel):
    url: str = Field(..., description="The URL to scrape")

class SriLankanCarSearchInput(BaseModel):
    vehicle_model: str = Field(..., description="The vehicle model to search for")

class WebScraperTool(Tool):
    name: str = "Web Scraper"
    description: str = (
        "A tool to scrape web pages and extract content. "
        "Useful for getting information from vehicle websites and ad listings."
    )
    args_schema: Type[BaseModel] = WebScraperInput

    def _run(self, url: str) -> str:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            for script in soup(["script", "style"]):
                script.decompose()

            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)

            return text[:5000]
        except Exception as e:
            return f"Error scraping {url}: {str(e)}"

class SriLankanCarSearchTool(Tool):
    name: str = "Sri Lankan Car Search"
    description: str = (
        "A specialized tool to search for vehicle advertisements on Sri Lankan automotive websites. "
        "Searches ikman.lk, riyasewana.com, and other local platforms."
    )
    args_schema: Type[BaseModel] = SriLankanCarSearchInput

    def _run(self, vehicle_model: str) -> str:
        search_results = []
        search_results.extend(self._search_ikman(vehicle_model))
        search_results.extend(self._search_riyasewana(vehicle_model))
        time.sleep(random.uniform(1, 3))

        return json.dumps({
            "vehicle": vehicle_model,
            "total_ads_found": len(search_results),
            "ad_urls": search_results
        }, indent=2)

    def _search_ikman(self, vehicle_model: str) -> list:
        try:
            base_url = "https://ikman.lk/en/ads/sri-lanka/cars"
            search_query = vehicle_model.replace(" ", "%20")
            search_url = f"{base_url}?query={search_query}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(search_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            ad_links = []

            for link in soup.find_all('a', href=True):
                href = link['href']
                if '/ad/' in href and 'cars' in href:
                    full_url = urljoin("https://ikman.lk", href)
                    ad_links.append(f"IKMAN: {full_url}")

            return ad_links[:10]
        except Exception as e:
            return [f"Error searching ikman.lk: {str(e)}"]

    def _search_riyasewana(self, vehicle_model: str) -> list:
        try:
            return [f"RIYASEWANA: Example URL for {vehicle_model}"]
        except Exception as e:
            return [f"Error searching riyasewana.com: {str(e)}"]
