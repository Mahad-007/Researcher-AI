from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import requests
import os

class FireCrawlScraperTool(BaseTool):
    name: str = "FireCrawlScraperTool"
    description: str = "Scrapes website content using FireCrawl API."

    class Args(BaseModel):
        url: str = Field(..., description="The URL of the website to scrape.")

    args_schema = Args

    def _run(self, url: str) -> str:
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            return "Missing FIRECRAWL_API_KEY in environment."

        try:
            response = requests.post(
                "https://api.firecrawl.dev/v1/scrape",
                headers={"Authorization": f"Bearer {api_key}"},
                json={"url": url}
            )
            response.raise_for_status()
            data = response.json()
            return data.get("text", "No text content found.")
        except Exception as e:
            return f"Error during scraping: {e}"
