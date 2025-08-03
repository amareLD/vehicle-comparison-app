from crewai_tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import urljoin, urlparse
import json

class WebScraperInput(BaseModel):
    """Input schema for WebScraperTool."""
    url: str = Field(..., description="The URL to scrape")

class SriLankanCarSearchInput(BaseModel):
    """Input schema for SriLankanCarSearchTool."""
    vehicle_model: str = Field(..., description="The vehicle model to search for")

class WebScraperTool(BaseTool):
    name: str = "Web Scraper"
    description: str = (
        "A tool to scrape web pages and extract content. "
        "Useful for getting information from vehicle websites and ad listings."
    )
    args_schema: Type[BaseModel] = WebScraperInput

    def _run(self, url: str) -> str:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text[:5000]  # Limit to prevent token overflow
            
        except Exception as e:
            return f"Error scraping {url}: {str(e)}"

class SriLankanCarSearchTool(BaseTool):
    name: str = "Sri Lankan Car Search"
    description: str = (
        "A specialized tool to search for vehicle advertisements on Sri Lankan automotive websites. "
        "Searches ikman.lk, riyasewana.com, and other local platforms."
    )
    args_schema: Type[BaseModel] = SriLankanCarSearchInput

    def _run(self, vehicle_model: str) -> str:
        search_results = []
        
        # Search on ikman.lk
        ikman_results = self._search_ikman(vehicle_model)
        search_results.extend(ikman_results)
        
        # Search on riyasewana.com
        riyasewana_results = self._search_riyasewana(vehicle_model)
        search_results.extend(riyasewana_results)
        
        # Add delay to be respectful
        time.sleep(random.uniform(1, 3))
        
        return json.dumps({
            "vehicle": vehicle_model,
            "total_ads_found": len(search_results),
            "ad_urls": search_results
        }, indent=2)
    
    def _search_ikman(self, vehicle_model: str) -> list:
        try:
            # Construct search URL for ikman.lk
            base_url = "https://ikman.lk/en/ads/sri-lanka/cars"
            search_query = vehicle_model.replace(" ", "%20")
            search_url = f"{base_url}?query={search_query}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract ad links (you'll need to inspect ikman.lk structure)
            ad_links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                if '/ad/' in href and 'cars' in href:
                    full_url = urljoin("https://ikman.lk", href)
                    ad_links.append(f"IKMAN: {full_url}")
            
            return ad_links[:10]  # Limit to 10 results
            
        except Exception as e:
            return [f"Error searching ikman.lk: {str(e)}"]
    
    def _search_riyasewana(self, vehicle_model: str) -> list:
        try:
            # Similar implementation for riyasewana.com
            base_url = "https://riyasewana.com"
            # Implement search logic based on their website structure
            return [f"RIYASEWANA: Example URL for {vehicle_model}"]
            
        except Exception as e:
            return [f"Error searching riyasewana.com: {str(e)}"]