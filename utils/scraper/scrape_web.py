import asyncio

from utils.scraper.src.webscrape import WebScraper, ScraperConfig


async def run_scrapers():
    configs = [
        ScraperConfig(
            base_url="https://localhost/",
            output_dir="data/web",
            batch_size=5,
            delay_between_batches=1.0
        )
    ]

    scrapers = [WebScraper(config) for config in configs]

    await asyncio.gather(*(scraper.run() for scraper in scrapers))


def main():
    asyncio.run(run_scrapers())


if __name__ == "__main__":
    main()
